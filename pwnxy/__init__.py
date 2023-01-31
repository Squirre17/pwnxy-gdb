import os 
import sys

# NOTE: remember specify PYTHONPATH
from pwnxy.utils.output import (err_print_exc,info, err, note, dbg)
from pwnxy.utils.debugger import (assert_eq, assert_ne)

import gdb

# ---- decorator function ----- 


# ------ gdb execute cmds in advance ------

pre_exec_cmds = """
    set confirm off
    set verbose off
    set print pretty on
    set pagination off
    set follow-fork-mode child
""" # TODO: considering width????

# TODO: not yet 
'''
    set backtrace past-main on
    set step-mode on

    set height 0
    set history expansion on
    set history save on

    handle SIGALRM nostop print nopass
    handle SIGBUS  stop   print nopass
    handle SIGPIPE nostop print nopass
    handle SIGSEGV stop   print nopass
'''

for cmd in pre_exec_cmds.strip().splitlines():
    gdb.execute(cmd)


# TODO: maybe sometime can't disasm to intel format ?
try:
    gdb.execute("set disassembly-flavor intel")
except gdb.error:
    pass

# ------ test region ------
def from_addr(cls, p):
    try :
        ptr = gdb.Value(p)
        ptr = ptr.cast(cls.gdb_type())
    except Exception as e:
        err_print_exc(e)

    return cls(ptr)

lines_tmp = gdb.execute("show commands", from_tty = False, to_string = True)
if lines_tmp is not None:
    lines = lines_tmp.splitlines()

for ln in lines:
    dbg(ln)

dbg("--------------DBG-TEST-----------------")


# ------- all cmd load by import ------
# TODO: move to cmd __init__ and import cmd
import pwnxy.cmds.aslr
import pwnxy.cmds.vmmap
import pwnxy.cmds.x
import pwnxy.cmds.context
import pwnxy.cmds.checksec
import pwnxy.cmds.cli
import pwnxy.cmds.mm
# -------------------------------------


from pwnxy.cmds import gcm

gcm.load()
gcm.show_registered_cmds()
# gdb.execute("b final")
# gdb.execute("c")


from pwnxy.config.parameters import Parameter
# Parameter(argname = "squ", default_val = 1, setdesc = "123",docdesc = "456") # TEMP:
from pwnxy.hook import register_all_hooks
register_all_hooks()

import pwnxy.exception
# gdb.execute("set exception-debugger on")
try :
    raise NotImplementedError
except :
    pwnxy.exception.handle()

from pwnxy.monitor import memory_monitor
gdb.execute("start")
hs = memory_monitor.add(0x7fffffffd908)
print(memory_monitor.read(hs))
gdb.execute("mm add 0x7fffffffd908")
gdb.execute("mm show")
# cli = gcm.getobj("cli")
# ------ ---------- ------

# WARN: asdasdasd

# TODO: asdasdasd

# FIXME: asdasdasd

# REF:

# HACK:

# TEMP:

# NOTE: 

# DEPRE: 

# PUZZ: 

# IDEA:
