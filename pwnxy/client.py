'''
relay message to client to implement the multi terminal feature

'''
from typing import (Any, ByteString, Callable, Dict, Generator, Iterable,
                    Iterator, List, NoReturn, Optional, Sequence, Set, Tuple, Type,
                    Union, NewType)
import pwnxy.file
from pwnxy.cmds import (Cmd, register)
from pwnxy.utils.debugger import (unwrap, assert_eq, assert_ne, todo)
from pwnxy.utils.output import (err_print_exc ,xy_print, info, err, note, dbg)
from pwnxy.utils.color import Color
from pwnxy.utils.hightlight import highlight_src
from pwnxy.utils.decorator import (deprecated, )
import gdb
from pwnxy.ui import banner
from pwnxy.config.parameters import Parameter
from collections import defaultdict
import re
import os
import socket 
import requests
import base64

port = NewType("port", int) 
# TEMP: reconstruct it
class Client:

    successful = False

    def __init__(self) -> None:
        self.cps : List[port] = []   # client ports
        self.sd               = None # socket descriptor

        port = os.getenv("PWNXY_CLIENT_PORT")
        if not port:
            # self.successful = False
            err("port get failed")
            return
        
        self.successful = True
        self.cps.append(port)


    def send(self, msg: str) -> bool:
        # TODO:
        msg = base64.b64encode(msg.encode())
        try :
            r = requests.post(url = "http://127.0.0.1:8080/echo", data = msg)
        except requests.exceptions.ConnectionError:
            err("connection error, can't use client")
            return 

        dbg(f"{r.text}")
        return 
    
    def is_connected(self):
        try:
            host = "127.0.0.1"
            # TODO:
            s = socket.create_connection((host, 8080), 2)
            s.close()
            return True
        except Exception:
            pass # we ignore any errors, returning False
        return False

    def __TODO__(self):
        self.sd.close()

pwnxy_cli = Client()









