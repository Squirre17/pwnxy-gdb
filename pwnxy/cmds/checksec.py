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
import os
from pwnxy.arch import curarch
from pwnxy.ui import banner
from pwnxy.registers import AMD64_REG
from pwnxy.config.parameters import Parameter
from pwnxy.disasm import disassembler, Instruction
from pwnxy.utils.decorator import (only_if_running, deprecated)
from pwnxy.elf import ELF
from pwnxy.proc import proc
@register
class Checksec(Cmd):
    '''
    checksec the security pretection of given executable
    - PIE
    - NX
    - RELRO
    - Canary
    format like:
    [*] '/home/squ/proj/pwnxy/pwnxy_gdb/tmp/a.out'
    Canary   : ✘ 
    NX       : ✓ 
    PIE      : ✘ 
    Fortify  : ✘ 
    RelRO    : ●
    '''
    cmdname  = "checksec"
    syntax   = "checksec /path/to/your/file"
    example  = "checksec /bin/ls"

    def __init__(self):
        super().__init__(self.cmdname)
    
    def invoke(self, args : List[str], from_tty : bool = False) -> None:
        argv = args.split()
        argc = len(argv)

        if argc == 0:
            filename = proc.path
        elif argc == 1:
            filename = os.path.realpath(os.path.expanduser(argv[0]))
            if not os.access(filename, os.R_OK):
                err(f"file {filename} don't have READ permission")
                return
        else :
            self.__usage__()
            return

        info(f"{self.cmdname} for {filename}")
        self.print_checksec(filename)
    
    def print_checksec(self, filename) -> None:
        sec : Dict[str, bool] = ELF(filename).checksec()

        result = []
        for k, flag in sec.items():
            fmt = "{sec:<20} : {icov}"
            # flag repr that protection whether exist
            select = lambda x ,flag : Color.greenify(x) if flag else Color.redify(x)
            colored = lambda sec, icov, flag : fmt.format(
                sec  = select(sec, flag),
                icov = select(icov, flag)
            )
            icov = "✓" if flag else "✘"
            icov = "TODO" if k == "FORTIFY" else icov # TODO:
            result.append(colored(k, icov, flag))

        print("\n".join(result))

    def __usage__(self) -> None:
        note("TODO impl me in checksec cmd")
        return  # TODO: