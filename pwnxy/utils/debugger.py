from typing import (Any, ByteString, Callable, Dict, Generator, Iterable,
                    Iterator, List, NoReturn, Optional, Sequence, Set, Tuple, Type,
                    Union, NewType)
from pwnxy.utils.output import (info, err, note, dbg)
from pwnxy.utils.color import Color

def assert_eq(x : Any, y : Any):
    if x != y:
        err(f"{x} != {y}")
        assert(x == y)

def assert_ne(x : Any, y : Any):
    if x == y:
        err(f"{x} == {y}")
        assert(x != y)

def todo():
    err("Plz impl me")
    exit(1)

# ONLY for decorator
def debug(func):
    def inner(*args, **kwargs):
        print(Color.purpleify("------FOR-DBG-USE------"))
        func(*args, **kwargs)
    return inner

def unwrap(oa : Optional[Any], fn : Callable = lambda : ...) -> Any:
    if oa is None:
        return fn()
    else:
        oa_inner : Any = oa
        return oa_inner
# TODO: move to decarator.py
def deprecated(func):
    def inner(*args, **kwargs):
        print(Color.redify("WARNING : this function have been deprecated"))
        func(*args, **kwargs)
    return inner

NewType("TODO", Dict[int, Tuple[int, Sequence]])
    
if __name__ == "__main__":
    assert_eq(1, 2)

        
