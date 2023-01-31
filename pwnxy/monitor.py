'''
monitor specified memory ,register ,watched struct modification 
maybe can cooperate with Context and Cli
'''
from enum import Enum
from typing import (Any, ByteString, Callable, Dict, Generator, Iterable,
                    Iterator, List, NoReturn, Optional, Sequence, Set, Tuple, Type,
                    Union, NewType)
import pwnxy.file
from pwnxy.cmds import (Cmd, register, AliasCmd)
from pwnxy.utils.debugger import (unwrap, assert_eq, assert_ne, todo)
from pwnxy.utils.output import (err_print_exc, xy_print, info, err, note, dbg, warn)
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
import pwnxy.memory


class Monitor:
    ...

class MemoryMonitor(Monitor):
    class MemUnit:
        __address : Address
        __wordlen : int
        __count   : int
        __hash    : int
        __mems    : List[Tuple[int, bool]] # bool indicate whether modified

        def __init__(self, address : Address, wordlen = 8, count = 8):

            assert wordlen in (1, 2, 4, 8)

            self.__address = address
            self.__wordlen = wordlen
            self.__count   = count
            # TODO: more complex hash
            self.__hash    = hash(str(address) + str(wordlen) + str(count)) 

            self.__mems    = [
                (pwnxy.memory.read(address + i * wordlen, wordlen), False) 
                for i in range(count)
            ]
            dbg(f"hash is {self.__hash}")

        @property
        def address(self): return self.__address

        @property
        def wordlen(self): return self.__wordlen
        
        @property
        def count(self): return self.__count

        @property
        def hash(self): return self.__hash

        @property
        def mems(self): return self.__mems

        def update(self) -> List[Tuple[int, bool]]:
            '''
            update all memory unit and return the tuples, and set all flag to False
            return flaged mems
            '''

            result : List[Tuple[int, bool]] = []
            
            for i in range(self.count):

                mem_value = pwnxy.memory.read(self.address + i * self.wordlen, self.wordlen)

                result.append((mem_value, mem_value != self.mems[i][0]))

                self.mems[i] = (mem_value, False)
            
            return result

    mems : Dict[int, MemUnit] = {}

    def __init__(self):
        ...
    
    @only_if_running
    def add(self, addr : Address, wordlen : int = 8, count : int = 8) -> int:
        '''
        add a monitor memory to monitor pool
        return a hash number for corresponding MemUnit
        '''
        mu = self.MemUnit(addr, wordlen, count)
        self.mems[mu.hash] = mu
        return mu.hash
    
    @only_if_running
    def drop(self, hashval : int) -> None:

        # assert access successfully, cuz this not from user input
        self.mems.pop(hashval)
    
    @only_if_running
    def read(self, hashval : int) -> List[Tuple[int, bool]] :
        '''
        This function expose to external.
        get memory unit(by int repr) by hash value, 
        Don't deal with KeyError.
        '''
        
        return self.mems[hashval].update()

memory_monitor = MemoryMonitor()