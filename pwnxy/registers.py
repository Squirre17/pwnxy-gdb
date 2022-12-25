from typing import (Any, ByteString, Callable, Dict, Generator, Iterable,
                    Iterator, List, NoReturn, Optional, Sequence, Set, Tuple, Type,
                    Union, NewType)
import pwnxy.arch as arch
from pwnxy.arch import Arch

__all_registers__ : Set[Type["RegCollections"]] = set()
# TODO: add flags and seg reg
class RegCollections :
    pc       : str          = None
    stask    : str          = None # sp
    frame    : str          = None # bp
    gprs     : Tuple[str]   = None # General Purpose Registers
    fnrg     : Tuple[str]   = None # function register
    ret      : str          = None # return value register
    arch     : Type["Arch"] = None

    def __init__(self, 
        pc       : str,
        stask    : str,
        frame    : str,
        gprs     : Tuple[str],
        fnrg     : Tuple[str],
        ret      : str,
        arch     : Type["Arch"]
    ):
        self.pc    = pc
        self.stask = stask
        self.frame = frame
        self.gprs  = gprs
        self.fnrg  = fnrg
        self.ret   = ret
        self.arch  = arch

AMD64_REG = RegCollections(
    pc      = "rip",
    stask   = "rsp",
    frame   = "rbp",
    gprs    = ('rax','rbx','rcx','rdx','rdi','rsi',
                               'r8', 'r9', 'r10','r11','r12',
                               'r13','r14','r15'),
    fnrg    = ("rdi", "rsi", "rdx", "rcx", "r8", "r9"),
    ret     = "rax",
    arch    = arch.AMD64_ARCH
)
__all_registers__.add(AMD64_REG)




