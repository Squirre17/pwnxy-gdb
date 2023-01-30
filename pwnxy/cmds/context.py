from enum import Enum
from typing import (Any, ByteString, Callable, Dict, Generator, Iterable,
                    Iterator, List, NoReturn, Optional, Sequence, Set, Tuple, Type,
                    Union, NewType)
import pwnxy.file
from pwnxy.cmds import (Cmd, register, AliasCmd)
from pwnxy.utils.debugger import (unwrap, assert_eq, assert_ne, todo)
from pwnxy.utils.output import (err_print_exc, xy_print, info, err, note, dbg, warn)
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
from pwnxy.address import Address
from pwnxy.config import ICOV_SYMS
from pwnxy.outs import select_ops, OutStream, OutType

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
    aliases  = ['ctx']

    def __init__(self):
        super().__init__(self.cmdname)
        for alias in self.aliases:
            AliasCmd(alias, self.cmdname)
        
        # WARN: don't use following init assignment, otherwise context will lose
        # self.context_sections = {} # TODO: orderdict? 

    # TODO: add breakpoint display
    # TODO: colorify ,hightlight ,fade
    # TODO: arch name(option?)
    # TODO: encapulate pc

    def __context_disasm() -> str:

        disasm : List[Instruction] = disassembler.nearpc()
        try:
            pc = int(gdb.selected_frame().pc())
        except Exception as e:
            err_print_exc(e)
            err("impossible for __context_disasm")

        pc_icov = Color.greenify(ICOV_SYMS["right-arrow"]) # TEMP:
        bp_icov = Color.redify(ICOV_SYMS["breakpoint"])
        fmtstr = "{addr:<8s} {sym:<12s} {mnem:<6s} {operand:<10s}\n"
        fmt_list : List[str] = []
        # TODO: conditional jump, syscall
        pivot_flag = True
        call_prefix = ""
        trun_right_arrow : str = " " + ICOV_SYMS["trun-right-arrow"]
        for i in disasm :
            ''' CALL EXAMPLE:
               0x4011c3 <main+45>    mov    eax, 0
            ●→ 0x4011c8 <main+50>    call   __isoc99_scanf@plt                      <__isoc99_scanf@plt>
                    format: 0x402008 < 0x809ce60064256425 /* '%d%d' */
                    vararg: 0x7fffffffd670 > 0x7fffffffd770 < 0x1
            
               ╰→ 0x4010a4  <__isoc99_scanf@plt+4> ✔ bnd jmp qword ptr [rip + 0x2f85]     <0x401060>
                  0x401060                          endbr64 
                  0x401064                          push   3
                  0x401069                          bnd jmp 0x401020                      <0x401020>

            bp pc addr sym mnem oprand
            '''
            """ branch example
            ●→ 0x7ffff7ddcdf6 <__cxa_atexit+22>    je     __cxa_atexit+238                <__cxa_atexit+238>
                ↓
               0x7ffff7ddcdfc <__cxa_atexit+28>    mov    rbx, rdi
               0x7ffff7ddcdff <__cxa_atexit+31>    mov    eax, dword ptr fs:[0x18]
               0x7ffff7ddce07 <__cxa_atexit+39>    lea    rbp, [rip + 0x1aa4da]         <0x7ffff7f872e8>
               0x7ffff7ddce0e <__cxa_atexit+46>    test   eax, eax
            """

            destination = None # for predict branch destination
            bp_prefix   = bp_icov if BPs.addr_has_bp(i.addr) else " "
            pc_prefix   = pc_icov if pc == i.addr else " "

            prefix_fmt = "{bp_prefix:s}{pc_prefix:s}{call_prefix:s} "
            
            if i.addr < pc and pivot_flag:    # passed instruction ,fade it 
                prefix = prefix_fmt.format(
                    call_prefix = call_prefix,
                    bp_prefix = bp_prefix,
                    pc_prefix = pc_prefix
                )
                line = prefix + Color.grayify(fmtstr.format(
                    addr = hex(i.addr), 
                    sym = i.symbol,
                    mnem = i.mnem,
                    operand = i.operand,
                ))
            elif i.addr == pc: # hit pc ,green it
                '''
                IDEA: maybe nearpc can flag instruction as a predicted inst?
                '''
                prefix = prefix_fmt.format(
                    call_prefix = call_prefix,
                    bp_prefix = bp_prefix,
                    pc_prefix = pc_prefix
                )
                line = prefix + Color.greenify(fmtstr.format(
                    addr = hex(i.addr), 
                    sym = i.symbol,
                    mnem = i.mnem,
                    operand = i.operand,
                ))
                if (i.is_call or i.is_ret) and i.dest is not None:
                    call_prefix = trun_right_arrow
                '''
                in some call cases , called address will below the pc, and will faded
                use pivot_flag to avoid that
                '''
                pivot_flag = False 
            else :             # normal
                prefix = prefix_fmt.format(
                    call_prefix = call_prefix,
                    bp_prefix = bp_prefix,
                    pc_prefix = pc_prefix
                )
                if call_prefix == trun_right_arrow:
                    call_prefix = "   "
                line = prefix + fmtstr.format(
                    addr = hex(i.addr), 
                    sym = i.symbol,
                    mnem = i.mnem,
                    operand = i.operand,
                ) 

            fmt_list.append(line)
        
        return pwnxy.ui.banner("DISASM") + "".join(fmt_list) # with ending '\n' 
        
    def __context_regs() -> str:
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
    def __context_backtrace() -> str:
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
        # TODO:
        ...
        return ""
    # FRATURE: 
    def __context_watchstruct() -> str:
        ...
        return ""

    class ctx_os:
        def __init__(self, fn : Callable, os : OutStream):
            self.__fn = fn
            self.__os = os
        
        @property
        def os(self): return self.__os

        @property
        def fn(self): return self.__fn

        @fn.setter
        def fn(self, fn): self.__fn = fn

        @os.setter
        def os(self, newos : OutStream): self.__os = newos
        
        @property
        def tuple(self): return (self.__fn, self.__os)

    # NOTE: ordered 
    context_sections : Dict[str, ctx_os] = {
        "regs"   : ctx_os(__context_regs,        select_ops()),
        "disasm" : ctx_os(__context_disasm,      select_ops()),
        "code"   : ctx_os(__context_code,        select_ops()),
        "bt"     : ctx_os(__context_backtrace,   select_ops()),
        "ghidra" : ctx_os(__context_ghidra,      select_ops()),
        "ws"     : ctx_os(__context_watchstruct, select_ops()),
    }
    # expose a interface to cli
    def ctx_cli_set(self, sec : str, op : str, name : str) -> None:
        '''
        account for validity check
        '''
        try :
            ctxos = self.context_sections[sec]
        except KeyError:
            keys = [k for k, _ in self.context_sections.items()]
            keys = ", ".join(keys)
            warn(f"key must select from ({keys})")
            return

        if op not in ("on", "off"):
            warn(f"operation must select from (on, off)")
            return

        if op == "on":
            ctxos.os = select_ops(OutType.CLI, name)
            info(f"{sec} client on")
        elif op == "off":
            ctxos.os = select_ops()
            info(f"{sec} client off")
        
        self.context_sections[sec] = ctxos


    # TODO; deal with subcmd
    @handle_exception
    @only_if_running
    def invoke(self, args : List[str], from_tty : bool = False) -> None:
        '''
        subcmd :
            context regs
            context bt
            context code
        subcmd on/off
            `context regs off/on/om(only modified)` or `context regs out`

        TODO: help context ,alias ctx
        '''
        argv = args.split() 
        argn = len(argv)
        self.do_invoke(argv, argn, from_tty)

    def do_invoke(self, argv : List[str], argn : int, from_tty : bool = False) -> None:
        #TODO: bind out stream with specific context
        
        dbg(argv) #   TODO: use match

        assert argn <= 3, print(f"len(argv) is {len(argv)}")

        for _ , ctxos in self.context_sections.items():
            (fn, target) = ctxos.tuple
            target.printout(fn())
            
        # print(result, end = "")
        print(pwnxy.ui.banner("END")) 


