# import gdb
# gdb.execute("start")
# gdb.execute("set pagination off")
# gdb.execute("set confirm off")
# gdb.execute("b final")
# gdb.execute("r")

# Python program to demonstrate
# default_factory argument of
# defaultdict
# class Decorator:
#     def __init__(self) -> None:
#         ...
#     def __call__(self, f):
#         print(f"invoked decorator with {f}")
#         def wrapper(*args, **kwargs) :
#             print("wrapper")
#             return f(*args, **kwargs)
#         return wrapper

# class Test(object):
#     @Decorator()
#     def bar(self) :
#         print("normal call")

# test = Test()

# # @Decorator()
# # def aaa():
# #     print("aaa")

# test.bar()
# test.bar()
# test.bar()
# test.bar()
# test.bar()


# aaa()
# aaa()
# aaa()
# aaa()

import gdb
print(gdb.selected_thread())