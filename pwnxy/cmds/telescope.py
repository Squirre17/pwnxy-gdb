from enum import Enum
from typing import (Any, ByteString, Callable, Dict, Generator, Iterable,
                    Iterator, List, NoReturn, Optional, Sequence, Set, Tuple, Type,
                    Union, NewType)
import pwnxy.file
from pwnxy.cmds import (Cmd, register, AliasCmd)
from pwnxy.utils.debugger import (unwrap, assert_eq, assert_ne, todo)
from pwnxy.utils.output import (err_print_exc,info, err, note, dbg, warn)
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
from pwnxy.monitor import memory_monitor
import pwnxy.registers
import pwnxy.memory 
import pwnxy.chain
from pwnxy.types import typeset

import pwnxy.themes.chain as C
import pwnxy.themes.memory as M
import pwnxy.themes as theme

telescope_lines = Parameter(
    argname = "telescope-lines", 
    default_val = 8, 
    docdesc = "the count of lines which telescope display"
)

@register
class Telescope(Cmd):

    cmdname  = 'telescope'
    syntax   = 'telescope [addr]'
    examples = (
        "telescope",
        "telescope $rsp (ditto)",
        "tel 0xdeadbeef"
    )
    aliases  = []

    def __init__(self):
        super().__init__(self.cmdname)
        for alias in self.aliases:
            AliasCmd(alias, self.cmdname)

    def tel(self, addr = None, count = int(telescope_lines)) -> str:
        '''
        rsp 0x7fffffffd578 —▸ 0x7ffff7de4083 (__libc_start_main+243) ◂— mov    edi, eax
            0x7fffffffd580 —▸ 0x7ffff7ffc620 (_rtld_global_ro) ◂— 0x50f5300000000
            0x7fffffffd588 —▸ 0x7fffffffd668 —▸ 0x7fffffffd993 ◂— '/home/squ/prac/a.out'
            0x7fffffffd590 ◂— 0x100000000
            0x7fffffffd598 —▸ 0x401196 (main) ◂— endbr64 
            0x7fffffffd5a0 —▸ 0x401270 (__libc_csu_init) ◂— endbr64 
            0x7fffffffd5a8 ◂— 0x46b28e53cd54dd79
            0x7fffffffd5b0 —▸ 0x4010b0 (_start) ◂— endbr64 
        '''
        # TODO: best way : pwndbg.regs.sp & pwndbg.arch.ptrmask
        rsp = pwnxy.registers.get("rsp") # not considering 32-bit
        count = max(1, count)
        if addr is None:
            addr = rsp

        size   = 8 # arch
        start  = addr 
        end    = addr + (count + 1) * size # TODO: arch
        result = []
        prefix = lambda x : "rsp" if x == rsp else ""

        for i, addr in enumerate(range(start, end, size)):

            if not pwnxy.memory.can_access(addr):
                result.append("<Could not read memory at %#x>" % addr)
                break
                
            result.append(
                "{:<4s} ".format(prefix(addr)) + pwnxy.chain.generate(addr)
            )
        
        print("\n".join(result))



    @handle_exception
    @only_if_running
    def invoke(self, args : List[str], from_tty : bool = False) -> None:

        argv = args.split() 
        argn = len(argv)
        self.do_invoke(argv, argn, from_tty)

    def do_invoke(self, argv : List[str], argn : int, from_tty : bool = False) -> None:
        #TODO: bind out stream with specific context
        
        dbg(argv) #   TODO: use match
        if argn == 0:
            self.tel()
        if argn == 1:
            raise NotImplementedError
        if argn > 1:
            raise NotImplementedError