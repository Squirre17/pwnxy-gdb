'''
all decorators
'''
import gdb
import functools
import time

from typing import (Callable, Any)
from pwnxy.utils.debugger import (err, dbg, note)
from pwnxy.proc import proc
from pwnxy.utils.color import Color


def only_if_running(func : Callable) -> Callable:
    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        if proc.is_alive:
            return func(*args, **kwargs)
        else:
            note("This program in not running")
    return wrapper

def deprecated(func : Callable) -> Callable:
    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        print(Color.redify("WARNING : this function have been deprecated"))
        return func(*args, **kwargs)
    return wrapper

def timer(func : Callable) -> Callable:
    @functools.wraps(func)
    def wrapper(*args , **kwargs) -> Any:
        start = time.time()
        ret = func(*args, **kwargs)
        end   = time.time()
        note("function {} spend {:0.8f} ms".format(func.__name__, (end - start) * 1000))
        return ret
    return wrapper

def debug(func : Callable) -> Callable:
    @functools.wraps(func)
    def wrapper(*args , **kwargs) -> Any:
        dbg(f"function -> {func.__name__} : START")
        ret = func(*args, **kwargs)
        dbg(f"function -> {func.__name__} : END")
        return ret
    return wrapper