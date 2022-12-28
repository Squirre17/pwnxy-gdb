import gdb
from typing import Callable
from pwnxy.utils.debugger import (err, dbg, note)
# TODO: move to other
def is_alive() -> bool:
    """Check if GDB is running."""
    print("""Check if GDB is running.""")
    try:
        return gdb.selected_inferior().pid > 0
    except Exception:
        return False

# DECORATOR
# DEPRE: 
def only_if_running(func : Callable):
    import functools
    dbg("DEPRECATED:")
    @functools.wraps(func)
    def inner(*args, **kwargs):
        if is_alive():
            return func(*args, **kwargs)
        else:
            note("This program in not running")
    return inner

class OnlyIfRunning:
    def __init__(self) -> None:
        ...
    def __call__(self, f):
        import functools
        

        @functools.wraps(f)
        def wrapper(*args, **kwargs) :
            print(f"invoked decorator with {f}")
            if is_alive():
                return f(*args, **kwargs)
            else:
                note("This program in not running")
        return wrapper