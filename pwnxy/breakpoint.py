from typing import (Any, ByteString, Callable, Dict, Generator, Iterable,
                    Iterator, List, NoReturn, Optional, Sequence, Set, Tuple, Type,
                    Union, NewType)

import pwnxy.file
from pwnxy.cmds import (Cmd, register)
from pwnxy.utils.debugger import *
from pwnxy.utils.output import *
from pwnxy.utils.decorator import *

from pwnxy.utils.color import Color
from pwnxy.utils.hightlight import highlight_src
import gdb
from pwnxy.arch import curarch
import pwnxy.ui
from pwnxy.config.parameters import Parameter
from pwnxy.disasm import disassembler, Instruction
'''GDB API
bp.location simply return a str like:
final
*0x12345
*12345
'''

class Breakpoint:
    def __init__(self) -> None:
        self.__bps : List[gdb.Breakpoint] = []

    def __get(self):
        '''
        every time need to call to update bps
        '''
        try :
            self.__bps = gdb.breakpoints()
        except Exception as e :
            err_print_exc(e)
            
    def addr_has_bp(self, addr : int) -> bool :
        # TODO: if break at a symbol, cvt to addr
        '''
        Whether has a breakpoint in given addr
        addr is int repr (TEMP: -> to addr class repr)
        '''
        self.__get()
        # filter bps
        # NOTE: gdb also allow break a point at a decimal address but I think no one will do so,
        #     : so I assume that all bps at hexdecimal address i.e. start with "*0x"
        bps_addr : List[int] = [int(bp.location[1:].strip(), 16) for bp in self.__bps if bp.location.startswith("*0x")]
        return any(addr == bp_addr for bp_addr in bps_addr)







BPs = Breakpoint()

# TEMP:
def print_location():
    for bps in gdb.breakpoints():
        dbg(f"location is {bps.location}")