from typing import (Any, ByteString, Callable, Dict, Generator, Iterable,
                    Iterator, List, NoReturn, Optional, Sequence, Set, Tuple, Type,
                    Union, NewType)
from pwnxy.utils.asserter import (assert_eq, assert_ne, todo)
from pwnxy.utils.output import (info, err, hint, dbg)

def get(path : str) -> Optional[ByteString] :
    '''
    get contents of the specified file on local
    TODO: considering remote ?
    '''
    try :
        with open(path, 'rb') as f:
            return f.read()
    except :
        return None