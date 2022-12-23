from enum import Enum
from typing import (Any, ByteString, Callable, Dict, Generator, Iterable,
                    Iterator, List, NoReturn, Optional, Sequence, Set, Tuple, Type,
                    Union, NewType)
from pwnxy.globals import __registered_cmds__
import pwnxy.file
from pwnxy.cmds import (Cmd, register)
from pwnxy.utils.debugger import (unwrap, assert_eq, assert_ne, todo)
from pwnxy.utils.output import (xy_print, info, err, hint, dbg)
from pwnxy.utils.color import Color
# from pwnxy.file import (get)

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

    dbg(b"aslr content is " + ctnt)
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
class ASLRCmd(Cmd):
    cmdname = "aslr"
    
    # TODO: what's args
    def do_invoke(self, args : List[str]) -> None:
        argc = len(args)

    ...
    # TODO: