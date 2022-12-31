'''
TEMP:
'''
from pwnxy.utils.output import *
import gdb

def get(name : str) -> int :
    try :
        frame = gdb.newest_frame()
    except Exception as e :
        err_print_exc(e)
    return frame.read_register(name)

def get_ra() -> int : # tEMP:
    '''
    get return addr # note: must executed in ret
    '''
    p_long = gdb.lookup_type("uint64_t").pointer()

    rsp = get("rsp")
    ra = gdb.Value(int(rsp)).cast(p_long).dereference()
    ra.fetch_lazy()
    dbg(f" ra is {hex(ra)}")
    return int(ra)
