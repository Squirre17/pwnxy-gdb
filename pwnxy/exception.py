import gdb
import functools
import time
import sys
import traceback

from typing import (Callable, Any)
from pwnxy.utils.debugger import (err, dbg, note)
from pwnxy.proc import proc
from pwnxy.utils.color import Color
from pwnxy.config.parameters import Parameter


excp_debug = Parameter(
    argname = "exception-debugger", 
    default_val = False, 
    docdesc = "whether print full traceback when exception happen"
)

def handle(name = 'Error') -> None:
    '''
    refer pwndbg
    display exception to user ,optionally displaying a full traceback
    '''
    # TODO: add it to session or proc?
    if excp_debug :
        note("Exception debug mode : ")
        exception_msg = traceback.format_exc()
        print(exception_msg)

    else:
        exc_type, exc_value, exc_traceback = sys.exc_info()

        err('Exception occurred: {}: {} ({})'.format(name, exc_value, exc_type))
        note("To obtain more info : ")
        note('set exception-debugger on') 
    
