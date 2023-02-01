from typing import Set, Type, Any, List, Dict ,Tuple
import functools
from loguru import logger
class IPManager():

    def __init__(self):
        # name -> (value , docstring)
        self.ipns : Dict[str, Tuple[Any, str]] = dict() # ip' name set 

    def add(self, n, dv, doc) -> bool :
        try :
            _dv, _doc = self.ipns[n]
            logger.warning("repeat")

        except KeyError:
            self.ipns[n] = (dv, doc)
    
    # @staticmethod
    # def ip_register(f) -> Any:

    #     @functools.wraps(f)
    #     def wrapper(*args) -> Any:

    #         (name, _, _) = args

    #         return f(*args)

    #     return wrapper

ipmanager = IPManager()

# @ipmanager.ip_register
def InnerParameter(argname, default_val, docdesc) -> Any:

    ipmanager.add(argname, default_val, docdesc)

    return default_val
        

