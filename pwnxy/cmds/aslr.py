from enum import Enum
from typing import (Any, ByteString, Callable, Dict, Generator, Iterable,
                    Iterator, List, NoReturn, Optional, Sequence, Set, Tuple, Type,
                    Union, NewType)
from pwnxy.globals import __registered_cmds_cls__
import pwnxy.file
from pwnxy.cmds import (Cmd, register)
from pwnxy.utils.debugger import (unwrap, assert_eq, assert_ne, todo)
from pwnxy.utils.output import (xy_print, info, err, hint, dbg)
from pwnxy.utils.color import Color

try:
    import gdb
except ModuleNotFoundError:
    hint("import gdb can't be standalon")



def check_aslr() -> Tuple[str ,str]:
    aslr_path = "/proc/sys/kernel/randomize_va_space"
    ctnt : bytes = unwrap(
        pwnxy.file.get(aslr_path),
        lambda : err("check aslr failed")
    )
    ctnt = ctnt.strip() # striped trailing \n

    if ctnt == b'0' :
        retstr = "randomize_va_space == 0"
        status = Color.redify("OFF")
    else :
        retstr = f"randomize_va_space == {int(ctnt)}" 
        status = Color.redify("ON")
    
    return (retstr, status)
    
def aslr():
    retstr, status = check_aslr()
    xy_print(f"ASLR is ({status}), {retstr}")

@register
class AslrCmd(Cmd):
    cmdname = "aslr"
    
    def __init__(self) :
        super().__init__(self.cmdname)
        ...

    # def __new__(cls: Type["AslrCmd"]) -> Type["AslrCmd"]:
    #     return super().__new__()

    # TODO: what's args
    def do_invoke(self, args : List[str]) -> None:
        argc = len(args)
        aslr()
    # TODO: 
    def invoke(self, args : List[str], from_tty : bool = False) -> None:
        self.do_invoke(args)

    # TODO:
    def __usage__(self) -> None:
        return super().__usage__()
    
    # TODO:
    ...