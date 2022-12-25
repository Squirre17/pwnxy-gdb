from enum import Enum
from typing import (Any, ByteString, Callable, Dict, Generator, Iterable,
                    Iterator, List, NoReturn, Optional, Sequence, Set, Tuple, Type,
                    Union, NewType)
from pwnxy.globals import __registered_cmds_cls__
import pwnxy.file
from pwnxy.cmds import (Cmd, register)
from pwnxy.utils.debugger import (unwrap, assert_eq, assert_ne, todo)
from pwnxy.utils.output import (xy_print, info, err, hint, dbg)
from pwnxy.utils.color import Color
import gdb
from pwnxy.arch import curarch
from pwnxy.ui import banner
from pwnxy.registers import AMD64_REG
# TODO: only_if_running
# TODO: context + subcmd like `context bracktrace`
# def disasm_context() -> None: ...


# TODO: add user context specify setting
class Context:
    ...
    def __context_disasm() -> str:
        gdb_frame = gdb.newest_frame()
        gdb_arch = gdb.selected_inferior().architecture()
        pc = int(gdb_frame.pc())
        disasm = gdb_arch.disassemble(start_pc = pc, count = 10)
        '''
        [
            {'addr': 4198742, 'asm': 'endbr64 ', 'length': 4},
            {'addr': 4198746, 'asm': 'push   %rbp', 'length': 1},
            {'addr': 4198747, 'asm': 'mov    %rsp,%rbp', 'length': 3}, 
            {'addr': 4198750, 'asm': 'mov    $0x8,%edx', 'length': 5}
        ]
        '''
        fmtstr   = "  {:<8s} {:<16s}\n"
        fmtstr_1 = "→ {:<8s} {:<16s}\n"
        fmt_list : List[str] = []
        flag = True
        for d in disasm :
            tmp = fmtstr.format(hex(d['addr']), d['asm'])
            if flag:
                tmp = tmp = Color.greenify(Color.boldify(
                    fmtstr_1.format(hex(d['addr']), d['asm']
                )))
                flag = False
            fmt_list.append(tmp)
        
        return banner("DISASM") + "".join(fmt_list) # with ending '\n' 

    def __context_regs() -> str:
        result : List[str] = []
        frame = gdb.newest_frame()
        for r in AMD64_REG.all_regs:
            val = int(frame.read_register(r))
            dbg(f"{r} is {val}")
            result.append(
                "{:<4s} ".format(r).upper() + "{:#x}".format(val) + '\n'
            )
        return banner("REGS") + "".join(result)

    def __context_code() -> str:
        ...
        return ""

    def __context_backtrace() -> str:
        ...
        return ""

    def __context_ghidra() -> str:
        # TODO:
        ...
        return ""

    def __context_watchstruct() -> str:
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
    def output_context(self):
        result = ""
        for title ,fn in self.context_sections.items():
            result += fn()
        print(result, end = "")

