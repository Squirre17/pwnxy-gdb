from enum import Enum
from typing import (Any, ByteString, Callable, Dict, Generator, Iterable,
                    Iterator, List, NoReturn, Optional, Sequence, Set, Tuple, Type,
                    Union, NewType)
from pwnxy.cmds import (Cmd, register, AliasCmd)
from pwnxy.utils.debugger import (unwrap, assert_eq, assert_ne, todo)
from pwnxy.utils.output import (err_print_exc, info, err, note, dbg, warn)
from pwnxy.utils.color import Color
from pwnxy.utils.hightlight import highlight_src
from pwnxy.arch import curarch
from pwnxy.registers import AMD64_REG
from pwnxy.config.parameters import Parameter
from pwnxy.disasm import disassembler, Instruction
from pwnxy.utils.decorator import *
from pwnxy.breakpoint import BPs
from pwnxy.address import Address
from pwnxy.config import ICOV_SYMS
from pwnxy.outs import select_ops, OutStream, OutType
from pwnxy.monitor import memory_monitor
from pwnxy.types import typeset
from loguru import logger
from pwnxy.page import Page


import gdb
import pwnxy.file
import pwnxy.ui
import pwnxy.registers
import pwnxy.memory 
import pwnxy.vmmap
import pwnxy.symbol
import pwnxy.hignlight as hl
from pwnxy.disasm import disassembler
from pwnxy.symbol import Symbol

import pwnxy.themes.memory as M

# TODO: this parameter move to theme or other

arrow_left = Parameter(
    argname     = 'chain-arrow-left',
    default_val = Color.purpleify('←'), 
    docdesc     = 'left arrow of chain formatting'
)

arrow_right = Parameter(
    argname     = 'chain-arrow-right',
    default_val = Color.purpleify('→'), 
    docdesc     = 'right arrow of chain formatting'
)

recur_depth = Parameter(
    argname     = 'chain-recur-depth',
    default_val = 3, 
    docdesc     = 'left arrow of chain formatting'
)
# TEMP: formatter move to themes
def sym_addr(addr : Address):
    fmt = "{arrow} {addr:#x} {sym:s} "
    ...

def __last_entry(addr_or_data : int) -> str:
    '''
    if a address is last entry of chain, 
    use left arrow and data or disasm or string.
    With prefix.
    ◂— mov    edi, eax
    ◂— '/home/squ/prac/a.out'
    ◂— 0x100000000
    '''
    symbol : Symbol = pwnxy.symbol.get(addr_or_data) 
    page   : Page   = pwnxy.vmmap.find(addr_or_data)

    readable = True
    if page is None or not pwnxy.memory.can_access(addr_or_data):
        readable = False
    
    # if non-readable, `addr_or_data` is a only data
    if not readable:
        data = pwnxy.memory.read(addr_or_data)
        return str(arrow_left) + " %#x" %(data)
    
    else:
        addr = Address(addr_or_data)
        #  string 
        '''
        0x7fffffffd993 ◂— '/home/squ/prac/a.out'
              ↑
        '''
        string = pwnxy.memory.read_string(addr)
        assert string != ""
        if string is not None:
            return str(arrow_left) + " " + '\'' + Color.boldify(string) + '\''

        # instruction
        # like : 0x4012dc <main+0> ← endbr64
        if page.can_execute:
            inst : Instruction = disassembler.get(addr)
            if inst:
                logger.debug("%s %s" % (inst.mnem, inst.operand))
            else:
                raise NotImplementedError
            return str(arrow_left) + " " + hl.asm("%s %s" % (inst.mnem, inst.operand))
        
        # simply data
        data = pwnxy.memory.read(addr_or_data)
        return str(arrow_left) + " %#x" %(data)


# IDEA: latter can support multi addr pass in upstream 
'''
input 0x7fffffffd938 
0x7fffffffd938 → 0x7ffff7de2083 <__libc_start_main+243> ← mov edi,eax
'''
def generate(addr, depth = int(recur_depth)) -> str:
    '''
    generate a line of address chain, don't with prefix.
    '''
    '''
    0x7fffffffd578 —▸ 0x7ffff7de4083 (__libc_start_main+243) ◂— mov    edi, eax
    0x7fffffffd580 —▸ 0x7ffff7ffc620 (_rtld_global_ro) ◂— 0x50f5300000000
    0x7fffffffd588 —▸ 0x7fffffffd668 —▸ 0x7fffffffd993 ◂— '/home/squ/prac/a.out'
    0x7fffffffd590 ◂— 0x100000000
    '''
    addrs  : List[int] = __recur_deref(addr ,depth) # tuple is more proper??
    logger.debug(repr(addrs))
    result : List[str] = [M.dye("{:#x}".format(addr))]

    for addr in addrs:

        symbol : Symbol = pwnxy.symbol.get(addr)
        if symbol :
            res = "%s %s" %(addr, str(symbol))
            res = M.dyetext(res, addr)
        else:
            res = M.dye("{:#x}".format(addr))
        
        result.append(res)
        
        # TODO: colorify it
        
    result : str = (" " + str(arrow_right) + " ").join(result)
    logger.debug("%s" % (result))

    if len(addrs) == 0:
        padding = __last_entry(addr)
    else:
        padding = __last_entry(addrs[-1])

    logger.debug(result + " " + padding)
    return result + " " + padding

'''
input  : 0x7fffffffd938
return : [0x7ffff7de2083]

because : 0x7fffffffd938 → 0x7ffff7de2083
'''
def __recur_deref(addr : int, depth = int(recur_depth)) -> List[int]:
    '''
    recursively dereference a address, return a list of addresses.
    don't including head currently.
    '''

    result = []
    for i in range(depth):

        # cycle refer
        if result.count(addr) >= 2:
            break
        
        try :
            
            addr = int(pwnxy.memory.deref(addr, typeset.ppvoid))
            # TODO: if xor logic exist in hign version (tcache) ,handle it

            # cuz derefered result is either data or address, if it's data, handle it latter in __last_entry
            if not pwnxy.vmmap.find(Address(addr)):
                logger.debug("not pwnxy.vmmap.find(%#x)" %addr)
                break

            # TODO: addr &= pwnxy.arch.ptrmask
            mask = ((1 << (2 ** 6)) - 1)
            logger.debug(hex(mask))
            addr &= mask
            result.append(addr)

            ...
        except Exception as e:
            # TODO: gdb.MemeoryError
            logger.error(e)
            raise e
            break
    
    return result