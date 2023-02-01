from enum import Enum
from typing import (Any, ByteString, Callable, Dict, Generator, Iterable,
                    Iterator, List, NoReturn, Optional, Sequence, Set, Tuple, Type,
                    Union, NewType)
import pwnxy.file
import pwnxy.memory
from pwnxy.cmds import (Cmd, register)
from pwnxy.utils.debugger import (unwrap, assert_eq, assert_ne, todo)
from pwnxy.utils.output import (info, err, note, dbg)
from pwnxy.utils.color import Color
from pwnxy.page import Page
import gdb
import pwnxy.vmmap
'''GDB API
Programs which are being run under GDB are called inferiors
Python scripts can access information about and manipulate inferiors controlled by GDB via objects of the gdb.Inferior class.
'''

@register
class Vmmap(Cmd):
    cmdname = "vmmap"
    
    def __init__(self) :
        super().__init__(self.cmdname)
    # TODO: what's args
    def do_invoke(self, args : List[str]) -> None:
        argc = len(args)
        # TODO:
        pwnxy.vmmap.show()
    # After registered to gdb, type 'cmd' will invoke this function
    def invoke(self, args : List[str], from_tty : bool = False) -> None :
        self.do_invoke(args)

    ...
    # TODO:
    
