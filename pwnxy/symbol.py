from typing import (Any, ByteString, Callable, Dict, Generator, Iterable,
                    Iterator, List, NoReturn, Optional, Sequence, Set, Tuple, Type,
                    Union, NewType)
import pwnxy.file
from pwnxy.cmds import (Cmd, register)
from pwnxy.utils.debugger import (unwrap, assert_eq, assert_ne, todo)
from pwnxy.utils.output import (err_print_exc ,xy_print, info, err, note, dbg)
from pwnxy.utils.color import Color
from pwnxy.utils.hightlight import highlight_src
from pwnxy.utils.decorator import (deprecated, )
import gdb
from pwnxy.ui import banner
from pwnxy.config.parameters import Parameter
from collections import defaultdict
import re

class Symbol:
    def __init__(self, sym : str, offset : int):
        self.__sym    : str = sym
        self.__offset : int = offset

    def __str__(self): # TODO: if offset is 0 return `<sym>` rather than `<sym+0>`
        return "<" + self.__sym + "+" + str(self.__offset) + ">"

    @property
    def sym(self) :
        return self.__sym
    @property
    def offset(self) :
        return self.__offset
    
    ...

def get(obj : Union[str, int]) -> Optional[Union[Type["Symbol"], int]]:
    '''TEMP:
    if obj is a address(int repr), then return a Symbol class
    if obj is a symbol(str repr), then return a addr(TEMP int repr)
    '''
    if type(obj) is str:
        symbol = obj
        try :
            ''' lookup_symbol :
            The result is a tuple of two elements. The first element is a gdb.Symbol object or None if the symbol is not found. If the symbol is found, the second element is True if the symbol is a field of a method’s object 
            '''
            symbolobj, _ = gdb.lookup_symbol(symbol)
            if symbolobj is not None :
                return int(symbolobj.value().address)
        except Exception:
            pass
        try :
            '''
            (gdb) info address f1
            Symbol "f1" is a function at address 0x40115a.
            (gdb) info address f
            No symbol "f" in current context.
            '''
            result = gdb.execute("info address %s" % symbol, to_string = True)
            if "No symbol" not in result:
                addr = int(re.search(r"0x[0-9a-fA-F]+", result).group(), 16)
            else:
                return None
        except Exception as e:
            err_print_exc(e)
            # TODO: return None 

    elif type(obj) is int:
        assert obj <= ((1 << 64) - 1) # TEMP integrate to other module
        addr = obj
        try :
            '''
            NOTE: the offset is decimal

            # pwnxy @ main > info symbol 0x4011d1
            main + 4 in section .text of /home/squ/proj/pwnxy/pwnxy_gdb/tmp/a.out

            # pwnxy @ main > info symbol 0x123456
            No symbol matches 0x123456.

            # pwnxy @ main > info symbol 0x4011cd
            main in section .text of /home/squ/proj/pwnxy/pwnxy_gdb/tmp/a.out
            '''
            result = gdb.execute("info symbol %#x" % addr, to_string = True)
            if "No symbol" not in result:
                expr = r"(.*)\s\+\s([0-9]+)\sin"
                match = re.search(expr, result)
                if match:
                    # like main , 4
                    name   = match.group(1)
                    offset = int(match.group(2))
                    symbol = Symbol(name, offset)
                    return symbol
                else :# TODO: cuz not familiar with re ,so use this remedy
                    expr = r"(.*)\sin"
                    match = re.search(expr, result)
                    if match:
                        # like main , 4
                        name   = match.group(1)
                        offset =  0
                        symbol = Symbol(name, offset)
                        return symbol
                        # fatal error
                    err_print_exc("unreachable")
            else:
                return None
        except Exception as e:
            err_print_exc(e)
            ...
    else:
        err("symbol.get : TypeError")

def get_debug_dir() -> Optional[str]:
    result = gdb.execute("show debug-file-directory", from_tty = False, to_string = True)
    expr = r'The directory where separate debug symbols are searched for is "(.*)".'

    match = re.search(expr, result)

    return match.group(1) if match else None

def set_debug_dir(dir : str) -> None:
    gdb.execute("set debug-file-directory %s" % dir)

def add_debug_dir(dir : str) -> None:
    cur = get_debug_dir()
    if cur :
        set_debug_dir("%s:%s" % (dir, cur))
    else:
        set_debug_dir(dir)






