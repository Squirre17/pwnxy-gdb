from pwnxy.themes.lexer import PwntoolsLexer
import pygments
import pygments.formatters
import pygments.lexers

lexer_cache = {}

# TODO: parameterize it
formatter = pygments.formatters.Terminal256Formatter(style=str("monokai"))

def asm(code : str, filename='.asm'):
    # No syntax highlight if pygment is not installed
    # if not pygments or disable_colors:
    #     return code

    # TODO: cache it(by name)
    lexer = PwntoolsLexer()

    if lexer:
        lexer_cache[filename] = lexer

        code = pygments.highlight(code, lexer, formatter).rstrip()

    return code
