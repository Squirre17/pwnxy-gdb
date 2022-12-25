import gdb

gdb.execute("set confirm off")
gdb.execute("set verbose off")
gdb.execute("set print pretty on")
gdb.execute("set pagination off")

gdb.execute("b swap")
gdb.execute("r")
frame = gdb.newest_frame()

print(frame.name()) # main => prompt?
# print( gdb.frame_stop_reason_string())

print(gdb.frame_stop_reason_string(frame.unwind_stop_reason())) 
# no reason 

# Returns the frame’s resume address.
print(hex(frame.pc())) # 0x401196

print(frame.function()) # main

# print(frame.order())
print(frame.newer()) # None

# Return the frame’s symtab and line object. See Symbol Tables In Python.
print(frame.find_sal()) # symbol and line for c.c, line 15

print(frame.read_register("rax")) # 4294956864

# NOTE: The variable argument must be a string or a gdb.Symbol object;
print(frame.read_var("b")) # 4199101

