from typing import List
from typing import Set


# Syntax characters
# fmt: off
SYNTAX_SEQ_START  = "\x1B["
SYNTAX_SEQ_END    = "m"
SYNTAX_HARD_RESET = f"{SYNTAX_SEQ_START}0{SYNTAX_SEQ_END}"
# fmt: on


# ANSI codes
# fmt: off
ANSI_CODE_STYLE_BASE_BOLD          =   1
ANSI_CODE_STYLE_BASE_ITALIC        =   3
ANSI_CODE_STYLE_BASE_UNDERLINE     =   4
ANSI_CODE_STYLE_BASE_STRIKETHROUGH =   9
ANSI_CODE_FG_BLACK                 =  30
ANSI_CODE_FG_RED                   =  31
ANSI_CODE_FG_GREEN                 =  32
ANSI_CODE_FG_YELLOW                =  33
ANSI_CODE_FG_BLUE                  =  34
ANSI_CODE_FG_PURPLE                =  35
ANSI_CODE_FG_CYAN                  =  36
ANSI_CODE_FG_WHITE                 =  37
ANSI_CODE_HI_BLACK                 =  90
ANSI_CODE_HI_RED                   =  91
ANSI_CODE_HI_GREEN                 =  92
ANSI_CODE_HI_YELLOW                =  93
ANSI_CODE_HI_BLUE                  =  94
ANSI_CODE_HI_PURPLE                =  95
ANSI_CODE_HI_CYAN                  =  96
ANSI_CODE_HI_WHITE                 =  97
ANSI_CODE_BG_BLACK                 =  40
ANSI_CODE_BG_RED                   =  41
ANSI_CODE_BG_GREEN                 =  42
ANSI_CODE_BG_YELLOW                =  43
ANSI_CODE_BG_BLUE                  =  44
ANSI_CODE_BG_PURPLE                =  45
ANSI_CODE_BG_CYAN                  =  46
ANSI_CODE_BG_WHITE                 =  47
ANSI_CODE_HI_BG_BLACK              = 100
ANSI_CODE_HI_BG_RED                = 101
ANSI_CODE_HI_BG_GREEN              = 102
ANSI_CODE_HI_BG_YELLOW             = 103
ANSI_CODE_HI_BG_BLUE               = 104
ANSI_CODE_HI_BG_PURPLE             = 105
ANSI_CODE_HI_BG_CYAN               = 106
ANSI_CODE_HI_BG_WHITE              = 107
# fmt: on


# TODO: Explore enums for codes? Makes sense


class ANSIStyle:
    # The codes that compose an ANSIStyle.
    # Note that base styles such as bold, italic, underline, strikethrough are
    # mutually inclusive.
    # Note that foreground and background codes are mutually exclusive.
    codes: Set[int]

    def __init__(self, codes: List[int]):
        self.codes = codes

    def format(self, s: str) -> str:
        parts: List[str] = []
        parts.append(SYNTAX_SEQ_START)  # "\x1B["
        for i, code in enumerate(self.codes): # "1;91;44"
            if i > 0:
                parts.append(";")
            parts.append(str(code))
        parts.append(SYNTAX_SEQ_END)  # "m"
        parts.append(s)  # "Hello, world!"
        parts.append(SYNTAX_HARD_RESET)  # "\x1B[0m"
        return "".join(parts)  # "\x1B[1;91;44mHello, world!\x1B[0m"


# ANSI styles
#
# Note:
# - Base styles (e.g. bold, italic, underline, strikethrough) are mutually inclusive.
# - Foreground and background styles are mutually exclusive.
#
# fmt: off
ANSI_STYLE_BASE_BOLD          = ANSIStyle(ANSI_CODE_STYLE_BASE_BOLD)
ANSI_STYLE_BASE_ITALIC        = ANSIStyle(ANSI_CODE_STYLE_BASE_ITALIC)
ANSI_STYLE_BASE_UNDERLINE     = ANSIStyle(ANSI_CODE_STYLE_BASE_UNDERLINE)
ANSI_STYLE_BASE_STRIKETHROUGH = ANSIStyle(ANSI_CODE_STYLE_BASE_STRIKETHROUGH)
ANSI_STYLE_FG_BLACK           = ANSIStyle(ANSI_CODE_FG_BLACK)
ANSI_STYLE_FG_RED             = ANSIStyle(ANSI_CODE_FG_RED)
ANSI_STYLE_FG_GREEN           = ANSIStyle(ANSI_CODE_FG_GREEN)
ANSI_STYLE_FG_YELLOW          = ANSIStyle(ANSI_CODE_FG_YELLOW)
ANSI_STYLE_FG_BLUE            = ANSIStyle(ANSI_CODE_FG_BLUE)
ANSI_STYLE_FG_PURPLE          = ANSIStyle(ANSI_CODE_FG_PURPLE)
ANSI_STYLE_FG_CYAN            = ANSIStyle(ANSI_CODE_FG_CYAN)
ANSI_STYLE_FG_WHITE           = ANSIStyle(ANSI_CODE_FG_WHITE)
ANSI_STYLE_HI_BLACK           = ANSIStyle(ANSI_CODE_HI_BLACK)
ANSI_STYLE_HI_RED             = ANSIStyle(ANSI_CODE_HI_RED)
ANSI_STYLE_HI_GREEN           = ANSIStyle(ANSI_CODE_HI_GREEN)
ANSI_STYLE_HI_YELLOW          = ANSIStyle(ANSI_CODE_HI_YELLOW)
ANSI_STYLE_HI_BLUE            = ANSIStyle(ANSI_CODE_HI_BLUE)
ANSI_STYLE_HI_PURPLE          = ANSIStyle(ANSI_CODE_HI_PURPLE)
ANSI_STYLE_HI_CYAN            = ANSIStyle(ANSI_CODE_HI_CYAN)
ANSI_STYLE_HI_WHITE           = ANSIStyle(ANSI_CODE_HI_WHITE)
ANSI_STYLE_BG_BLACK           = ANSIStyle(ANSI_CODE_BG_BLACK)
ANSI_STYLE_BG_RED             = ANSIStyle(ANSI_CODE_BG_RED)
ANSI_STYLE_BG_GREEN           = ANSIStyle(ANSI_CODE_BG_GREEN)
ANSI_STYLE_BG_YELLOW          = ANSIStyle(ANSI_CODE_BG_YELLOW)
ANSI_STYLE_BG_BLUE            = ANSIStyle(ANSI_CODE_BG_BLUE)
ANSI_STYLE_BG_PURPLE          = ANSIStyle(ANSI_CODE_BG_PURPLE)
ANSI_STYLE_BG_CYAN            = ANSIStyle(ANSI_CODE_BG_CYAN)
ANSI_STYLE_BG_WHITE           = ANSIStyle(ANSI_CODE_BG_WHITE)
ANSI_STYLE_HI_BG_BLACK        = ANSIStyle(ANSI_CODE_HI_BG_BLACK)
ANSI_STYLE_HI_BG_RED          = ANSIStyle(ANSI_CODE_HI_BG_RED)
ANSI_STYLE_HI_BG_GREEN        = ANSIStyle(ANSI_CODE_HI_BG_GREEN)
ANSI_STYLE_HI_BG_YELLOW       = ANSIStyle(ANSI_CODE_HI_BG_YELLOW)
ANSI_STYLE_HI_BG_BLUE         = ANSIStyle(ANSI_CODE_HI_BG_BLUE)
ANSI_STYLE_HI_BG_PURPLE       = ANSIStyle(ANSI_CODE_HI_BG_PURPLE)
ANSI_STYLE_HI_BG_CYAN         = ANSIStyle(ANSI_CODE_HI_BG_CYAN)
ANSI_STYLE_HI_BG_WHITE        = ANSIStyle(ANSI_CODE_HI_BG_WHITE)
# fmt: on


# bold_hi_red_on_blue = ANSI_STYLE_BOLD + ANSI_STYLE_HI_RED + ANSI_STYLE_BG_BLUE
# print(bold_hi_red_on_blue)  # \x1B[1;91;44mAlert\x1B[0m


def main():
    ansi_style = ANSIStyle(
        [ANSI_CODE_STYLE_BASE_BOLD, ANSI_CODE_HI_RED, ANSI_CODE_BG_BLUE]
    )
    formatted = ansi_style.format("Hello, world!")
    print(formatted)


if __name__ == "__main__":
    main()
