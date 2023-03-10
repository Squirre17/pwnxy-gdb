'''
all decorators
'''
import gdb
import functools
import time

from typing import (Callable, Any)
from pwnxy.utils.output import (err, dbg, note, warn)
from pwnxy.proc import proc
from pwnxy.utils.color import Color


def only_if_running(func : Callable) -> Callable:
    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        if proc.is_alive:
            return func(*args, **kwargs)
        else:
            warn("This program in not running")
    return wrapper

def deprecated(func : Callable) -> Callable:
    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        print(Color.redify(f"WARNING : this function `{func}` have been deprecated"))
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

def debug_wrapper(func : Callable) -> Callable:
    @functools.wraps(func)
    def wrapper(*args , **kwargs) -> Any:
        dbg(f"function -> {func.__name__} : START")
        ret = func(*args, **kwargs)
        dbg(f"function -> {func.__name__} : END")
        return ret
    return wrapper

import traceback
def handle_exception(func : Callable) -> Callable:
    @functools.wraps(func)
    def wrapper(*args , **kwargs) -> Any:
        try :
            return func(*args, **kwargs)
        except Exception as e :
            err("Exception occur!")
            print(traceback.format_exc())
    return wrapper