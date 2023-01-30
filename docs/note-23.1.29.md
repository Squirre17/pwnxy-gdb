# Cmd specification
the following code is must to be repeated (template)
```python
@register
class Cli(Cmd):
    cmdname  = 'cli'
    syntax   = 'cli [cli op] [cli name] [section] (on|off)'
    examples = (
        "cli set r regs on",
        "cli set b bt off",
        "cli show all",
    )

    aliases = []
    def __init__(self):
        super().__init__(self.cmdname)
        for alias in self.aliases:
            AliasCmd(alias, self.cmdname)
    
    @handle_exception
    @only_if_running
    def invoke(self, args : List[str], from_tty : bool = False) -> None:

        argv = args.split() 
        argn = len(argv)
        self.do_invoke(argv, argn, from_tty)

    def do_invoke(self, argv : List[str], argn : int, from_tty : bool = False) -> None:
        ...
```