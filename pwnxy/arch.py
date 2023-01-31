'''
current only serve for registers
'''
from typing import (Any, ByteString, Callable, Dict, Generator, Iterable,
                    Iterator, List, NoReturn, Optional, Sequence, Set, Tuple, Type,
                    Union, NewType)
import pwnxy.file
from pwnxy.cmds import (Cmd, register)
from pwnxy.utils.debugger import (unwrap, assert_eq, assert_ne, todo)
from pwnxy.utils.output import (xy_print, info, err, note, dbg)
from pwnxy.utils.color import Color
import gdb
import traceback
from pwnxy.utils.decorator import only_if_running
from pwnxy.instruction import Instruction
import enum
'''GDB API
newest_frame will return cur thread's stack frame obj  
'''
@only_if_running
def get_arch() :
    # IF RUNNING
    try :
        arch_name = gdb.newest_frame().architecture().name()
    except Exception as e:
        traceback.print_exc()
    dbg(arch_name) # i386:x86-64
    # TODO: ELSE proc.alive

# abstract all arch instuction
class insttype(enum.Enum): # TEMP:
    COND_BRA = 1 # conditional branch
    DIRE_BRA = 2 # directly branch
    RET      = 2
    CALL     = 3
    OTHER    = 4

class Endianness:
    LIT = 1
    BIG = 2

class Arch :

    endiness   : Endianness = None
    arch_type  : str        = None
    arch_size  : int        = None
    alias      : List[str]  = None

    def __init__(self,
        arch_type  : str,
        arch_size  : int,
        alias      : List[str] = None
    ):
        self.arch_type = arch_type
        self.arch_size = arch_size
        self.alias = alias

    # TEMP: dispatch all task to each arch handler
    def get_type(self, inst : Instruction) -> insttype:
        if inst.mnem.startswith("j"):
            if inst.mnem.startswith("jmp"):
                return insttype.DIRE_BRA
            return insttype.COND_BRA
        elif inst.mnem == "ret":
            return insttype.RET
        elif inst.mnem == "call":
            return insttype.CALL
        else:
            return insttype.OTHER
            
        

class AMD64(Arch):

    def __init__(
        self,
        arch_type  : str,
        arch_size  : int,
        alias      : List[str] = None
    ):
        super().__init__(arch_type, arch_size, alias)
        self.__endiness = Endianness.LIT
    
    @property
    def endiness(self): return self.__endiness


AMD64_ARCH = AMD64("amd64", 8)

# TEMP: 
curarch = AMD64_ARCH