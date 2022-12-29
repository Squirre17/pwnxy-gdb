'''
runtime properties
'''
from typing import (Optional, Callable, Any)
import gdb
import pathlib
from pwnxy.utils.debugger import (dbg)

import functools
# TEMP: avoid circular import 
def debug(func : Callable) -> Callable:
    @functools.wraps(func)
    def wrapper(*args , **kwargs) -> Any:
        dbg(f"function -> {func.__name__} : START")
        ret = func(*args, **kwargs)
        dbg(f"function -> {func.__name__} : END")
        return ret
    return wrapper

class Process:
    def __init__(self):
        self.__path = None
    
    @property
    def pid(self) -> Optional[int]:
        inferior = gdb.selected_inferior()
        if inferior is not None :
            return inferior.pid
        return None

    @property
    def is_alive(self) -> bool:
        return gdb.selected_thread() is not None
    
    @property
    def is_disable_color(self) -> bool:
        '''
        TODO: sometimes need
        '''
    @property
    def path(self) -> pathlib.Path:
        '''
        get current file absolute path
        '''
        if self.__path is None:
            self.get_filepath()
        return self.__path

    def get_filepath(self) -> None:
        fpath : str = gdb.current_progspace().filename
        self.__path = pathlib.Path(fpath).expanduser()
        assert self.__path is not None


proc = Process()