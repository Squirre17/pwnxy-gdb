class Color:
    """Used to colorify terminal output."""
    colors = {
        "reset"          : "\033[0m",
        "gray"           : "\033[1;38;5;240m",
        "light_gray"     : "\033[0;37m",
        "red"            : "\033[31m",
        "green"          : "\033[32m",
        "yellow"         : "\033[33m",
        "blue"           : "\033[34m",
        "pink"           : "\033[35m",
        # "cyan"           : "\033[36m",
        # "bold"           : "\033[1m",
        # "underline"      : "\033[4m",
        # "underline_off"  : "\033[24m",
        # "highlight"      : "\033[3m",
        # "highlight_off"  : "\033[23m",
        # "blink"          : "\033[5m",
        # "blink_off"      : "\033[25m",
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
    def pinkify(msg: str) -> str:       return Color.colorify(msg, "pink")

    @staticmethod
    def colorify(msg : str , color_key : str) -> str:
        return Color.colors[color_key] + msg + Color.colors["reset"]
    

def color_test():
    print(Color.colorify("color", "blue"))
    print("111")


if __name__ == "__main__":
    color_test()
