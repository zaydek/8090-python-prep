from enum import Enum
from typing import List, Protocol


# https://gist.github.com/JBlond/2fea43a3049b38287e5e9cefc87b2124
# fmt: off
class AnsiCodeEnum(Enum):
    RESET_ALL = 0     # \x1b[0m

    # Styles
    STYLE_BOLD                = 1     # \x1b[1m
    # STYLE_BOLD_OFF            = 22    # \x1b[22m
    STYLE_DIM                 = 2     # \x1b[2m
    # STYLE_DIM_OFF             = 22    # \x1b[22m (same as BOLD_OFF)
    STYLE_ITALIC              = 3     # \x1b[3m
    # STYLE_ITALIC_OFF          = 23    # \x1b[23m
    STYLE_UNDERLINE           = 4     # \x1b[4m
    # STYLE_UNDERLINE_OFF       = 24    # \x1b[24m
    STYLE_BLINK_SLOW          = 5     # \x1b[5m
    STYLE_BLINK_FAST          = 6     # \x1b[6m
    # STYLE_BLINK_OFF           = 25    # \x1b[25m
    STYLE_INVERT              = 7     # \x1b[7m
    # STYLE_INVERT_OFF          = 27    # \x1b[27m
    STYLE_HIDDEN              = 8     # \x1b[8m
    # STYLE_HIDDEN_OFF          = 28    # \x1b[28m
    STYLE_STRIKETHROUGH       = 9     # \x1b[9m
    # STYLE_STRIKETHROUGH_OFF   = 29    # \x1b[29m

    # Foreground colors
    FOREGROUND_BLACK  = 30
    FOREGROUND_RED    = 31
    FOREGROUND_GREEN  = 32
    FOREGROUND_YELLOW = 33
    FOREGROUND_BLUE   = 34
    FOREGROUND_PURPLE = 35
    FOREGROUND_CYAN   = 36
    FOREGROUND_WHITE  = 37

    # High intensity foreground colors
    FOREGROUND_HIGH_INTENSITY_BLACK  = 90
    FOREGROUND_HIGH_INTENSITY_RED    = 91
    FOREGROUND_HIGH_INTENSITY_GREEN  = 92
    FOREGROUND_HIGH_INTENSITY_YELLOW = 93
    FOREGROUND_HIGH_INTENSITY_BLUE   = 94
    FOREGROUND_HIGH_INTENSITY_PURPLE = 95
    FOREGROUND_HIGH_INTENSITY_CYAN   = 96
    FOREGROUND_HIGH_INTENSITY_WHITE  = 97

    # Background colors
    BACKGROUND_BLACK  =  40
    BACKGROUND_RED    =  41
    BACKGROUND_GREEN  =  42
    BACKGROUND_YELLOW =  43
    BACKGROUND_BLUE   =  44
    BACKGROUND_PURPLE =  45
    BACKGROUND_CYAN   =  46
    BACKGROUND_WHITE  =  47

    # High intensity background colors
    BACKGROUND_HIGH_INTENSITY_BLACK  = 100
    BACKGROUND_HIGH_INTENSITY_RED    = 101
    BACKGROUND_HIGH_INTENSITY_GREEN  = 102
    BACKGROUND_HIGH_INTENSITY_YELLOW = 103
    BACKGROUND_HIGH_INTENSITY_BLUE   = 104
    BACKGROUND_HIGH_INTENSITY_PURPLE = 105
    BACKGROUND_HIGH_INTENSITY_CYAN   = 106
    BACKGROUND_HIGH_INTENSITY_WHITE  = 107
# fmt: on


class AnsiStyle:
    # The list of AnsiCodeEnum that compose an AnsiStyle.
    codes: List[AnsiCodeEnum]

    # Initialize the AnsiStyle with a variadic list of AnsiCodeEnum.
    def __init__(self, *codes: AnsiCodeEnum) -> None:
        self.codes = list(codes)
        return None

    # Format the AnsiStyle to an ANSI escape sequence string.
    #
    # "\x1B[1;91;44mHello, world!\x1B[0m"
    #  ^    ^ ^  ^  ^            ^
    #  |    | |  |  |            |
    #  |    | |  |  |            +-------- End of the escape sequence string
    #  |    | |  |  +--------------------- Input string
    #  |    | |  +------------------------ One or more ";"-delimited ANSI codes
    #  |    | +--------------------------- One or more ";"-delimited ANSI codes
    #  |    +----------------------------- One or more ";"-delimited ANSI codes
    #  +---------------------------------- Start of the escape sequence string
    #
    def format(self, s: str) -> str:
        # fmt: off
        ANSI_START_SEQUENCE = "\x1B["
        ANSI_END_SEQUENCE   = "m"
        ANSI_RESET          = "\x1B[0m"
        # fmt: on

        parts: List[str] = []
        parts.append(ANSI_START_SEQUENCE)
        for i, code in enumerate(self.codes):  # "1;91;44"
            if i > 0:
                parts.append(";")
            parts.append(str(code.value))  # Access the underlying value (int)
        parts.append(ANSI_END_SEQUENCE)
        parts.append(s)
        parts.append(ANSI_RESET)
        return "".join(parts)


################################################################################
# ThemeProtocol
################################################################################


# A theme is a object that can be used to style text.
class ThemeProtocol(Protocol):
    def bold_color(self, s: str) -> str: ...
    def bold(self, s: str) -> str: ...
    def color(self, s: str) -> str: ...
    def faint(self, s: str) -> str: ...
    def faint_color(self, s: str) -> str: ...


################################################################################
# Theme
################################################################################


class Theme(ThemeProtocol):
    # fmt: off
    _with_bold:  AnsiStyle
    _with_faint: AnsiStyle
    _default:    AnsiStyle
    _bold:       AnsiStyle
    _faint:      AnsiStyle
    # fmt: on

    def __init__(self, arg: AnsiCodeEnum) -> None:
        # fmt: off
        self._with_bold  = AnsiStyle(arg, AnsiCodeEnum.STYLE_BOLD)
        self._with_faint = AnsiStyle(arg, AnsiCodeEnum.STYLE_DIMMED)
        self._default    = AnsiStyle(arg)
        self._bold       = AnsiStyle(AnsiCodeEnum.STYLE_BOLD)
        self._faint      = AnsiStyle(AnsiCodeEnum.STYLE_DIMMED)
        # fmt: on

    def with_bold(self, s: str) -> str:
        return self._with_bold.format(s)

    def with_faint(self, s: str) -> str:
        return self._with_faint.format(s)

    def default(self, s: str) -> str:
        return self._default.format(s)

    def bold(self, s: str) -> str:
        return self._bold.format(s)

    def faint(self, s: str) -> str:
        return self._faint.format(s)


################################################################################
# PlainTheme
################################################################################


class PlainTheme(ThemeProtocol):
    def with_bold(self, s: str) -> str:
        return s

    def with_faint(self, s: str) -> str:
        return s

    def default(self, s: str) -> str:
        return s

    def bold(self, s: str) -> str:
        return s

    def faint(self, s: str) -> str:
        return s

    def color(self, s: str) -> str:
        return s

    def faint_color(self, s: str) -> str:
        return s


################################################################################
# Main
################################################################################


def main():
    # AnsiStyle
    s1 = AnsiStyle(
        AnsiCodeEnum.STYLE_BOLD,
        AnsiCodeEnum.FOREGROUND_HIGH_INTENSITY_RED,
        AnsiCodeEnum.BACKGROUND_BLUE,
    )
    s2 = AnsiStyle(
        AnsiCodeEnum.STYLE_ITALIC,
        AnsiCodeEnum.FOREGROUND_HIGH_INTENSITY_GREEN,
        AnsiCodeEnum.BACKGROUND_YELLOW,
    )
    s3 = AnsiStyle(*s1.codes, *s2.codes)
    print(s3.format("Hello, world!"))

    # Theme
    print("=" * 80)
    color_theme = Theme(AnsiCodeEnum.FOREGROUND_HIGH_INTENSITY_RED)
    print(color_theme.with_bold("with bold: Hello, world!"))
    # print(color_theme.with_faint("with faint: Hello, world!"))
    # print(color_theme.default("default: Hello, world!"))
    # print(color_theme.bold("bold: Hello, world!"))
    # print(color_theme.faint("faint: Hello, world!"))
#
    # # PlainTheme
    # print("=" * 80)
    # plain_theme = PlainTheme()
    # print(plain_theme.with_bold("with bold: Hello, world!"))
    # print(plain_theme.with_faint("with faint: Hello, world!"))
    # print(plain_theme.default("default: Hello, world!"))
    # print(plain_theme.bold("bold: Hello, world!"))
    # print(plain_theme.faint("faint: Hello, world!"))


if __name__ == "__main__":
    main()
