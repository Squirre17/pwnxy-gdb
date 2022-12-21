from xypwn.utils.color import Color

def info(msg : str):
    prompt = Color.colorify("[+]" ,"green")
    body   = " INFO : "
    print(prompt + body + msg)

def dbg(msg : str):
    prompt = Color.colorify("[#]" ,"yellow")
    body   = " DBG  : "
    print(prompt + body + msg)

def err(msg : str):
    prompt = Color.colorify("[!]" ,"red")
    body   = " ERR  : "
    print(prompt + body + msg)

def hint(msg : str):
    prompt = Color.colorify("[*]" ,"blue")
    body   = " HINT : "
    print(prompt + body + msg)

if __name__ == "__main__":
    s = "123"
    info(s)
    dbg(s)
    err(s)
    hint(s)