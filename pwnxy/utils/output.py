from pwnxy.utils.color import Color
import traceback
def info(msg):
    prompt = Color.colorify("[+]" ,"green")
    body   = " INFO : "
    print(prompt + body, end = "")
    print(msg)


def dbg(msg):
    prompt = Color.colorify("[#]" ,"yellow")
    body   = " DBG  : "
    print(prompt + body, end = "")
    print(msg)

def err(msg):
    prompt = Color.colorify("[!]" ,"red")
    body   = " ERR  : "
    print(prompt + body, end = "")
    print(msg)


def note(msg):
    prompt = Color.colorify("[*]" ,"blue")
    body   = " NOTE : "
    print(prompt + body, end = "")
    print(msg)


def xy_print(*args):
    print("[XYPRINT] : ", end = "")
    print(*args)

def err_print_exc(msg):
    err(msg)
    traceback.print_exc()

if __name__ == "__main__":
    s = "123"
    info(s)
    dbg(s)
    err(s)
    note(s)