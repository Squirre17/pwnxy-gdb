import os 
import sys

class fake_gdb:
    def execute(self, cmd, from_tty = False, to_string = False):     
        hint(f"executed {cmd}")
        if to_string:
            return """
                    1 test cmd 
                    2 test cmd 
                    3 test cmd 
            """
# NOTE: remember specify PYTHONPATH
from pwnxy.utils.output import (info, err, hint, dbg)
from pwnxy.utils.debugger import (assert_eq, assert_ne)

try:
    import gdb
except ModuleNotFoundError:
    hint("import gdb can't be standalon")
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
    info(f"gdb executed `{cmd}`")

# TODO: maybe sometime can't disasm to intel format ?
try:
    gdb.execute("set disassembly-flavor intel")
except gdb.error:
    pass

# ------ test region ------
def from_addr(cls, p):
        ptr = gdb.Value(p)
        ptr = ptr.cast(cls.gdb_type())
        return cls(ptr)

lines_tmp = gdb.execute("show commands", from_tty = False, to_string = True)
if lines_tmp is not None:
    lines = lines_tmp.splitlines()

for ln in lines:
    dbg(ln)

dbg("--------------DBG-TEST-----------------")
gdb.execute("start")
dbg("prefix with `0x` => %#x" % 123)
dbg(gdb.parse_and_eval("1+1"))

assert_ne(b'', None)

from pwnxy.cmds.aslr import aslr
aslr()
assert_eq(b"a\n".strip(), b"a")
dbg(int(b"1"))

from pwnxy.cmds.vmmap import vmmap
vmmap()

from pwnxy.cmds import show_registered_cmds
show_registered_cmds()
# ------ ---------- ------