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
# TODO: only_if_running
# TODO: context + subcmd like `context bracktrace`
class Context():
    ...

    def disasm_context(self) -> str:
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
        
        print(banner("DISASM"))
        print("".join(fmt_list))
