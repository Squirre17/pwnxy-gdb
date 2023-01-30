# cli call stack

enter `cli set regs regs on`, it will be parsed by Cli(cmd class) , then trigger `set` action.
context(cmd class) will reserve a interface and expose it to cli, use gcm(GdbCmdManager) to obtain registered context object and call it.
```python
    @enable_decorater
    def set(self, argv : List[str]) -> None:

        from pwnxy.cmds import gcm
        argn = len(argv)

        # argv = r regs on
        if argn != 3:
            warn("cli set arguments not correct")
            return
        
        cliname, sec, op = (argv[i] for i in range(argn))
        # TODO cliname not used
        ctxobj : Type["Context"] = gcm.getobj("context")
        ctxobj.ctx_cli_set(sec, op, cliname)
```
I use a `outs.py` module to abstract all out stream (FILE STDOUT and CLIENT) with a abs class `OutStream` which have a abs method `printout`. Use this method to output all context sections.

```python
class OutStream(ABC):

    @abstractmethod
    def printout(self, data): pass
```
I build a subclass inside `Context` to mapping section's literal string to a object which have context generator function and `OutStream` obj.

```python
    # NOTE: ordered 
    context_sections : Dict[str, ctx_os] = {
        "regs"   : ctx_os(__context_regs,        select_ops()),
        "disasm" : ctx_os(__context_disasm,      select_ops()),
        "code"   : ctx_os(__context_code,        select_ops()),
        "bt"     : ctx_os(__context_backtrace,   select_ops()),
        "ghidra" : ctx_os(__context_ghidra,      select_ops()),
        "ws"     : ctx_os(__context_watchstruct, select_ops()),
    }
```
もちろん, it will be reconstructed to ordered dict latter.

so The abovementioned interface it's effect is that do some necessary check and modify `ctx_os` object's `OutStream` object. all sections will output by this `OutStream` object in `do_invoke`.

```python
    def do_invoke(self, argv : List[str], argn : int, from_tty : bool = False) -> None:
        #TODO: bind out stream with specific context
        
        dbg(argv) #   TODO: use match

        assert argn <= 3, print(f"len(argv) is {len(argv)}")

        for _ , ctxos in self.context_sections.items():
            (fn, target) = ctxos.tuple
            target.printout(fn())   <<- trigger point
```
Cliout class implement printout method like following:
```python
class Cliout(OutStream):
    '''
    Out to external client, context manager wrapper
    '''
    def __init__(self, name) -> None:
        self.name = name


    def printout(self, data : str):
        cliobj = gcm.getobj("cli")
        cliobj.send(self.name ,data)
```

all structure is clear now:
```
Cli      ->        set ctx_op        -> Context
                                           ↓
Cli.send <-   ctx_op call printout   <- Context
```
