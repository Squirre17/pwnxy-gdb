'''globals.py
for store all global variables
DEPRE: not use
'''
from typing import (Any, ByteString, Callable, Dict, Generator, Iterable,
                    Iterator, List, NoReturn, Optional, Sequence, Set, Tuple, Type,
                    Union, NewType)
from pwnxy.cmds import Cmd
from pwnxy.registers import RegCollections
# from pwnxy.registers import () TODO: arch
# TODO: upperify it
# ------ GLOBAL REGION ------ 
# DEPRE: move to cmds dir
__registered_cmds_cls__ : Set[Type["Cmd"]] = set()

# ---------  END  -----------


