# import gdb
# gdb.execute("start")
# gdb.execute("set pagination off")
# gdb.execute("set confirm off")
# gdb.execute("b final")
# gdb.execute("r")

# Python program to demonstrate
# default_factory argument of
# defaultdict

import gdb
import traceback
from pwnxy.utils.output import err_print_exc
try :
    arch_name = gdb.newest_frame().architecture().name()
except Exception as e :
    err_print_exc(e)