from enum import Enum
from typing import (Any, ByteString, Callable, Dict, Generator, Iterable,
                    Iterator, List, NoReturn, Optional, Sequence, Set, Tuple, Type,
                    Union, NewType)
from pwnxy.globals import __registered_cmds_cls__
import pwnxy.file
from pwnxy.cmds import (only_if_running,Cmd, register)
from pwnxy.utils.debugger import (deprecated ,unwrap, assert_eq, assert_ne, todo)
from pwnxy.utils.output import (xy_print, info, err, note, dbg)
from pwnxy.utils.color import Color
from pwnxy.utils.hightlight import highlight_src
import gdb
from pwnxy.arch import curarch
from pwnxy.ui import banner
from pwnxy.registers import AMD64_REG
from pwnxy.config.parameters import Parameter
from pwnxy.disasm import disassembler, Instruction
from pwnxy.utils.decorator import OnlyIfRunning
# TODO: only_if_running
# TODO: context + subcmd like `context bracktrace`
# def disasm_context() -> None: ...
# TODO: source code need syntax highlight

# TODO: add user context specify setting

@register
class Context(Cmd):
    cmdname = 'context'

    def __init__(self):
        super().__init__(self.cmdname)

    # TODO: add breakpoint display
    # TODO: colorify ,hightlight ,fade
    # TODO: arch name(option?)
    # TODO: encapulate pc
    def __context_disasm() -> str:

        disasm : List[Instruction] = disassembler.nearpc()
        try:
            pc = int(gdb.selected_frame().pc())
        except Exception as e:
            err(e)
        # TODO: add sym

        prefix = "→"
        fmtstr = "{prefix} {addr:<8s} {mnem:<6s} {operand:<10s}\n"
        fmt_list : List[str] = []
        # TODO: conditional jump, syscall
        for i in disasm :
            tmp = fmtstr.format(
                prefix = " ",
                addr = hex(i.addr), 
                mnem = i.mnem,
                operand = i.operand
            ) if i.addr != pc else Color.greenify(fmtstr.format(
                    prefix = prefix,
                    addr = hex(i.addr), 
                    mnem = i.mnem,
                    operand = i.operand
                ))

            fmt_list.append(tmp)
        
        return banner("DISASM") + "".join(fmt_list) # with ending '\n' 

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
        return banner("REGS") + "".join(result)
    

    def __context_code() -> str:
        dbg("entered __context_code")
        sal = gdb.selected_frame().find_sal()
        if sal is None:
            err("TODO: wait for deal with")
        try :
            fullname = sal.symtab.fullname()
        except AttributeError:
            # NOTE: external lib don't have fullname attr
            return ""
        
        src = pwnxy.file.get_text(fullname)

        if src is None:
            # can't get src code
            return ""
        
        pivot_line = sal.line # TODO: seems like current line
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

        return banner("src") + "\n".join(result) + "\n"
    # TODO: add "at file "
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
                err(e)
            
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

        return banner("bt") +"\n".join(lines) + "\n"

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
    # TODO: subcontext
    @deprecated
    def output_context(self):
        result = ""
        for title ,fn in self.context_sections.items():
            result += fn()
        print(result, end = "")

    # TODO; deal with subcmd
    @OnlyIfRunning()
    def invoke(self, args : List[str], from_tty : bool = False) -> None:
        dbg("context cmd invoked")
        self.do_invoke(args, from_tty)

    @OnlyIfRunning()
    def do_invoke(self, args : List[str], from_tty : bool = False) -> None:
        dbg("context cmd do_invoked")
        result = ""
        for title ,fn in self.context_sections.items():
            result += fn()
        print(result, end = "")


