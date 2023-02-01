from typing import (Any, ByteString, Callable, Dict, Generator, Iterable,
                    Iterator, List, NoReturn, Optional, Sequence, Set, Tuple, Type,
                    Union, NewType)
import pwnxy.arch as arch
from pwnxy.arch import Arch
import gdb
# from pwnxy.utils.decorator import *
from pwnxy.utils.output import err_print_exc
# TODO : only server for Arch and only called by arch !!!
__all_registers__ : Set[Type["RegCollections"]] = set()
# TODO: add flags and seg reg
class RegCollections :
    pc       : str          = None
    stack    : str          = None # sp
    frame    : str          = None # bp
    gprs     : Tuple[str]   = None # General Purpose Registers
    fnrg     : Tuple[str]   = None # function register
    ret      : str          = None # return value register
    arch     : Type["Arch"] = None
    all_regs : Tuple[str]   = None 

    def __init__(self, 
        pc       : str,
        stack    : str,
        frame    : str,
        gprs     : Tuple[str],
        fnrg     : Tuple[str],
        ret      : str,
        arch     : Type["Arch"]
    ):
        self.pc       = pc
        self.stack    = stack
        self.frame    = frame
        self.gprs     = gprs
        self.fnrg     = fnrg
        self.ret      = ret
        self.arch     = arch
        self.all_regs = [pc ,stack ,frame]
        for r in gprs:
            self.all_regs.append(r)



AMD64_REG = RegCollections(
    pc      = "rip",
    stack   = "rsp",
    frame   = "rbp",
    gprs    = ('rax','rbx','rcx','rdx','rdi','rsi',
                               'r8', 'r9', 'r10','r11','r12',
                               'r13','r14','r15'),
    fnrg    = ("rdi", "rsi", "rdx", "rcx", "r8", "r9"),
    ret     = "rax",
    arch    = arch.AMD64_ARCH
)
__all_registers__.add(AMD64_REG)

def get(reg : str) -> int :
    '''
    obtain a value from given register name.
    '''
    return int(gdb.parse_and_eval("$" + reg))
