from pwnxy.utils.color import Color

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


def hint(msg):
    prompt = Color.colorify("[*]" ,"blue")
    body   = " HINT : "
    print(prompt + body, end = "")
    print(msg)


def xy_print(*args):
    print("[XYPRINT] : ", end = "")
    print(*args)

if __name__ == "__main__":
    s = "123"
    info(s)
    dbg(s)
    err(s)
    hint(s)