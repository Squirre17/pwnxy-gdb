from typing import Optional
class Color:
    """Used to colorify terminal output."""
    colors = {
        "normal"         : "",
        "reset"          : "\033[0m",
        "gray"           : "\033[1;38;5;240m",
        "light_gray"     : "\033[0;37m",
        "red"            : "\033[31m",
        "green"          : "\033[32m",
        "yellow"         : "\033[33m",
        "blue"           : "\033[34m",
        "purple"         : "\033[35m",
        "cyan"           : "\033[36m",
        "bold"           : "\033[1m",
        "underline"      : "\033[4m",
        "underline_off"  : "\033[24m",
        "highlight"      : "\033[3m",
        "highlight_off"  : "\033[23m",
        "blink"          : "\033[5m",
        "blink_off"      : "\033[25m",
    }
    @staticmethod
    def redify(msg: str) -> str:        return Color.colorify(msg, "red")
    @staticmethod
    def greenify(msg: str) -> str:      return Color.colorify(msg, "green")
    @staticmethod
    def blueify(msg: str) -> str:       return Color.colorify(msg, "blue")
    @staticmethod
    def yellowify(msg: str) -> str:     return Color.colorify(msg, "yellow")
    @staticmethod
    def grayify(msg: str) -> str:       return Color.colorify(msg, "gray")
    @staticmethod
    def light_grayify(msg: str) -> str: return Color.colorify(msg, "light_gray")
    @staticmethod
    def purpleify(msg: str) -> str:     return Color.colorify(msg, "purple")
    @staticmethod
    def cyanify(msg: str) -> str:       return Color.colorify(msg, "cyan")
    @staticmethod
    def boldify(msg: str) -> str:       return Color.colorify(msg, "bold")
    @staticmethod
    def underlineify(msg: str) -> str: return Color.colorify(msg, "underline")
    @staticmethod
    def highlightify(msg: str) -> str: return Color.colorify(msg, "highlight")
    @staticmethod
    def blinkify(msg: str) -> str :    return Color.colorify(msg, "blink")



    @staticmethod
    def colorify(msg : str , color_key : str = "reset") -> str:
        if color_key == '' or color_key == None:
            color_key = "reset"
        return Color.colors[color_key] + msg + Color.colors["reset"]
    

def color_test():
    print(Color.colorify("color", "blue"))
    print(Color.boldify("color"))
    print(Color.underlineify("color"))
    print(Color.blinkify("color"))
    print(Color.redify(Color.boldify("color")))

if __name__ == "__main__":
    color_test()
