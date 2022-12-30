from enum import Enum
from typing import (Any, ByteString, Callable, Dict, Generator, Iterable,
                    Iterator, List, NoReturn, Optional, Sequence, Set, Tuple, Type,
                    Union, NewType)
from pwnxy.globals import __registered_cmds_cls__
import pwnxy.file
from pwnxy.cmds import (Cmd, register)
from pwnxy.utils.debugger import (unwrap, assert_eq, assert_ne, todo)
from pwnxy.utils.output import (err_print_exc, xy_print, info, err, note, dbg)
from pwnxy.utils.color import Color
from pwnxy.utils.hightlight import highlight_src
import gdb
from pwnxy.arch import curarch
import pwnxy.ui
from pwnxy.registers import AMD64_REG
from pwnxy.config.parameters import Parameter
from pwnxy.disasm import disassembler, Instruction
from pwnxy.utils.decorator import *
from pwnxy.breakpoint import BPs

# TODO: context + subcmd like `context bracktrace`
# def disasm_context() -> None: ...
# TODO: source code need syntax highlight

# TODO: add user context specify setting
# TODO: 
@register
class Context(Cmd):
    cmdname  = 'context'
    syntax   = 'context [subcmd]'
    examples = (
        "context",
        "context regs/disasm/code/bt/ghidra/ws", # NOTE : This need to manual maintain...
        "context regs/disasm/code/bt/ghidra/ws out" # TODO: current not
    )

    def __init__(self):
        super().__init__(self.cmdname)
        # WARN: don't use following init assignment, otherwise context will lose
        # self.context_sections = {} # TODO: orderdict? 

    # TODO: add breakpoint display
    # TODO: colorify ,hightlight ,fade
    # TODO: arch name(option?)
    # TODO: encapulate pc
    @debug
    def __context_disasm() -> str:

        disasm : List[Instruction] = disassembler.nearpc()
        try:
            pc = int(gdb.selected_frame().pc())
        except Exception as e:
            err_print_exc(e)
            err("impossible for __context_disasm")

        pc_icov = Color.greenify("→") # TEMP:
        bp_icov = Color.redify("●")
        fmtstr = "{addr:<8s} {sym:<12s} {mnem:<6s} {operand:<10s}\n"
        fmt_list : List[str] = []
        # TODO: conditional jump, syscall
        for i in disasm :
            '''
            0x4011cb <f5+19>          pop    rbp
            0x4011cc <f5+20>          ret    
            0x4011cd <main+0>         endbr64 
        ●→  0x4011d1 <main+4>         push   rbp
            0x4011d2 <main+5>         mov    rbp, rsp
            0x4011d5 <main+8>         mov    eax, 0x0

        bp pc addr sym mnem oprand
            '''
            bp_prefix = bp_icov if BPs.addr_has_bp(i.addr) else " "
            pc_prefix = pc_icov if pc == i.addr else " "
            prefix = f"{bp_prefix}{pc_prefix} "

            if i.addr < pc:    # passed instruction ,fade it 
                line = prefix + Color.grayify(fmtstr.format(
                    addr = hex(i.addr), 
                    sym = i.symbol,
                    mnem = i.mnem,
                    operand = i.operand,
                ))
            elif i.addr == pc: # hit pc ,green it
                line = prefix + Color.greenify(fmtstr.format(
                    addr = hex(i.addr), 
                    sym = i.symbol,
                    mnem = i.mnem,
                    operand = i.operand,
                ))
            else :             # normal
                line = prefix + fmtstr.format(
                    addr = hex(i.addr), 
                    sym = i.symbol,
                    mnem = i.mnem,
                    operand = i.operand,
                ) 

            fmt_list.append(line)
        
        return pwnxy.ui.banner("DISASM") + "".join(fmt_list) # with ending '\n' 

    def __context_regs() -> str:
        dbg("entered __context_regs")
        # TODO: ljust regs and upper
        # TODO： modified flag
        result : List[str] = []
        frame = gdb.newest_frame()
        for r in AMD64_REG.all_regs:
            # add recording for modified compare
            val = int(frame.read_register(r))
            result.append(
                "{:<4s} ".format(r).upper() + "{:#x}".format(val) + '\n'
            )
        return pwnxy.ui.banner("REGS") + "".join(result)
    
    def __context_code() -> str:
        '''
        get source code context
        '''
        sal = gdb.selected_frame().find_sal()
        if sal is None:
            err_print_exc("impossible in __context_code")
        try :
            fullname = sal.symtab.fullname()
        except AttributeError:
            # NOTE: external lib don't have fullname attr
            return ""
        
        src = pwnxy.file.get_text(fullname)

        if src is None: # repr that can't get src code
            return ""
        
        pivot_line = sal.line # PUZZ: seems like current line
        src : List[str] = highlight_src(src.split("\n"))

        start_line    = max(pivot_line - 3, 0) # TODO: complexify
        end_line      = min(pivot_line + 7, len(src)) # TODO: complexify
        ln_width      = len(str(end_line))
        prefix_symbol = "→"         # TODO: mv to config
        prefix_width  = len(prefix_symbol)

        src = src[start_line : end_line]
        fmt = '{prefix:{prefix_width}} {line_number:>{ln_width}} {code}'
        result : List[str] = []
        for ln_num, code in enumerate(src, start = start_line + 1) :
            if ln_num == pivot_line:
                prefix = prefix_symbol
                ... # TODO:
            else :
                prefix = " "

            result.append(fmt.format(
                prefix       = prefix,
                prefix_width = prefix_width,
                line_number  = ln_num,
                ln_width     = ln_width,
                code         = code
            ))

        return pwnxy.ui.banner("src") + "\n".join(result) + "\n"
    # TODO: add "at file "
    @debug
    def __context_backtrace() -> str:
        dbg("entered __context_backtrace")
        # TODO: ref config setting with gdb
        from collections import deque
        default_bt_cnt = 8
        cur_frame = gdb.newest_frame()
        new_frame = cur_frame
        old_frame = cur_frame
        assert cur_frame is not None

        deq : deque[gdb.Frame] = deque() # TODO: not use 
        # TODO: more trick here
        for _ in range(default_bt_cnt):
            candidate = old_frame.older()
            if not candidate:
                break
            deq.append(candidate)
            old_frame = candidate
        
        for _ in range(default_bt_cnt):
            candidate = new_frame.newer()
            if not candidate:
                break
            deq.appendleft(candidate)
            new_frame = candidate
        
        ''' format REF: gef
        [#0] 0x40121c → swap(a=0x0, b=0x4012bd)
        [#1] 0x4011dc → main()
        [#{idx}] addr sym fun(arg ...)
        '''
        # TODO: if hit current frame ,colorify it's prefix

        fmt = "[{idx:<{width}}] {addr:#x} {sym} {fun}({args})"
        idx = 0
        lines : List[str] = []
        # TODO: addr highlight
        
        while cur_frame:
            try :
                cur_args = gdb.FrameDecorator.FrameDecorator(cur_frame).frame_args()
            except Exception as e:
                err_print_exc(e)
            
            # assert cur_args is not None
            # TODO: cur_args maybe be None
            if cur_args is None:
                break

            line = fmt.format(
                idx    = Color.blueify("#" + str(idx)) if cur_frame == new_frame else Color.purpleify("#" + str(idx)) ,
                width  = len(str(default_bt_cnt)), # TEMP: this
                addr   = cur_frame.pc(),
                sym    = "→",  # TEMP: this
                fun    = Color.greenify(cur_frame.name()),
                args   = ", ".join([
                    "{}={!s}".format( # TODO: !s
                        Color.yellowify(str(s.sym)), s.sym.value(cur_frame) 
                    ) for s in cur_args
                ])
            )
            idx += 1
            lines.append(line)
            cur_frame = cur_frame.older()

        return pwnxy.ui.banner("bt") +"\n".join(lines) + "\n"

    def __context_ghidra() -> str:
        dbg("entered __context_ghidra")
        # TODO:
        ...
        return ""
    # FRATURE: 
    def __context_watchstruct() -> str:
        dbg("entered __context_watchstruct")
        ...
        return ""
    # NOTE: ordered 
    context_sections : Dict[str, Callable] = {
        "regs"   : __context_regs,
        "disasm" : __context_disasm,
        "code"   : __context_code,
        "bt"     : __context_backtrace,
        "ghidra" : __context_ghidra,
        "ws"     : __context_watchstruct,
    }

    # TODO; deal with subcmd
    @only_if_running
    def invoke(self, args : List[str], from_tty : bool = False) -> None:
        '''
        subcmd :
            context regs
            context bt
            context code
        subcmd on/off
            `context regs off/on/om(only modified)` or `context regs out`

        TODO: help context 
        '''
        assert len(args) <= 3
        result = ""
        for title ,fn in self.context_sections.items():
            result += fn()
        print(result, end = "")
        print(pwnxy.ui.banner("END")) 


