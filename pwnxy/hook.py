from enum import Enum
from typing import (Any, ByteString, Callable, Dict, Generator, Iterable,
                    Iterator, List, NoReturn, Optional, Sequence, Set, Tuple, Type,
                    Union, NewType)
from pwnxy.globals import __registered_cmds_cls__
import pwnxy.file
from pwnxy.cmds import (Cmd, register)
from pwnxy.utils.debugger import (unwrap, assert_eq, assert_ne, todo)
from pwnxy.utils.output import (xy_print, info, err, note, dbg)
from pwnxy.utils.color import Color
from pwnxy.utils.hightlight import highlight_src
import gdb
from pwnxy.arch import curarch
from pwnxy.ui import banner
from pwnxy.registers import AMD64_REG
from pwnxy.config.parameters import Parameter
from pwnxy.prompt import current_prompt
''' GDB API
GDB provides a general event facility so that Python code can be notified of various state changes, particularly changes that occur in the inferior.
In order to be notified of an event, you must register an event handler with an event registry. An event registry is an object in the gdb.events module which dispatches particular events. A registry provides methods to register and unregister event handlers:
'''
__all_registered_hook__ : Callable[[Callable[["gdb.StopEvent"], None]], None] = []
# TEMP: 
def register_hook(fn : Callable) -> None:
    def inner(*args, **kwargs):
        return fn(*args, **kwargs)

    __registered_cmds_cls__.add(fn)
    return inner

def hook_stop_handler(_ : gdb.StopEvent) -> None:
    """GDB event handler for stop cases."""
    gdb.execute("context")



def stop_event_hook(fn : Callable[["gdb.StopEvent"], None]) -> None:
    gdb.prompt_hook = current_prompt
    gdb.events.stop.connect(fn)

def register_all_hooks():
    stop_event_hook(hook_stop_handler)

