'''
current only serve for registers
'''
from typing import (Any, ByteString, Callable, Dict, Generator, Iterable,
                    Iterator, List, NoReturn, Optional, Sequence, Set, Tuple, Type,
                    Union, NewType)
from pwnxy.cmds import only_if_running
import pwnxy.file
from pwnxy.cmds import (Cmd, register)
from pwnxy.utils.debugger import (unwrap, assert_eq, assert_ne, todo)
from pwnxy.utils.output import (xy_print, info, err, note, dbg)
from pwnxy.utils.color import Color
import gdb
from pwnxy.utils.decorator import OnlyIfRunning
'''GDB API
newest_frame will return cur thread's stack frame obj  
'''
@OnlyIfRunning()
def get_arch() :
    # IF RUNNING
    arch_name = gdb.newest_frame().architecture().name()
    dbg(arch_name) # i386:x86-64
    # TODO: ELSE proc.alive





class Arch :
    arch_type  : str       = None
    arch_size  : int       = None
    alias      : List[str] = None

    def __init__(self,
        arch_type  : str,
        arch_size  : int,
        alias      : List[str] = None
    ):
        self.arch_type = arch_type
        self.arch_size = arch_size
        self.alias = alias

AMD64_ARCH = Arch("amd64", 8)

# TEMP: 
curarch = AMD64_ARCH