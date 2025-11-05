import colorful as cf
from enum import Enum
from typing import Protocol


# fmt: off
class ThemeProtocol(Protocol):
  def  bold_color(self, s: str) -> str: ...
  def        bold(self, s: str) -> str: ...
  def       color(self, s: str) -> str: ...
  def       faint(self, s: str) -> str: ...
  def faint_color(self, s: str) -> str: ...
# fmt: on


class Theme(ThemeProtocol):
    code: int

    def __init__(self, color: int) -> None:
        self.color = color

    def bold_color(self, s: str) -> str:
        return cf.bold(s)

    def bold(self, s: str) -> str:
        return cf.bold(s)

    def color(self, s: str) -> str:
        return cf.color(s)

    def faint(self, s: str) -> str:
        return cf.faint(s)

    def faint_color(self, s: str) -> str:
        return cf.faint_color(s)


def main() -> None:
    # # create a colored string using clever method translation
    # print(cf.bold_white('Hello World'))
    # # create a colored string using `str.format()`
    # print('{c.bold}{c.lightCoral_on_white}Hello World{c.reset}'.format(c=cf))
    #
    # # nest colors
    # print(cf.red('red {0} red'.format(cf.white('white'))))
    # print(cf.red('red' + cf.white(' white ', nested=True) + 'red'))
    #
    # # combine styles with strings
    # print(cf.bold & cf.red | 'Hello World')
    #
    # # use true colors
    # cf.use_true_colors()
    #
    # # extend default color palette
    # cf.update_palette({'mint': '#c5e8c8'})
    # print(cf.mint_on_snow('Wow, this is actually mint'))
    #
    # # choose a predefined style
    # cf.use_style('solarized')
    # # print the official solarized colors
    # print(cf.yellow('yellow'), cf.orange('orange'),
    #     cf.red('red'), cf.magenta('magenta'),
    #     cf.violet('violet'), cf.blue('blue'),
    #     cf.cyan('cyan'), cf.green('green'))
    #
    # # directly print with colors
    # cf.print('{c.bold_blue}Hello World{c.reset}')
    #
    # # choose specific color mode for one block
    # with cf.with_8_ansi_colors() as c:
    #     print(c.bold_green('colorful is awesome!'))
    #
    # # create and choose your own color palette
    # MY_COMPANY_PALETTE = {
    #     'companyOrange': '#f4b942',
    #     'companyBaige': '#e8dcc5'
    # }
    # with cf.with_palette(MY_COMPANY_PALETTE) as c:
    #     print(c.companyOrange_on_companyBaige('Thanks for choosing our product!'))
    #
    # # use f-string (only Python >= 3.6)
    # print(f'{cf.bold}Hello World')
    #
    # # support for chinese
    # print(cf.red('你好'))

    s1 = cf.red
    s2 = cf.bold
    print((s1 & s2)("Hello, world!"))


if __name__ == "__main__":
    main()

#### class AnsiCodeEnum(Enum):
####   BLACK          = 0
####   DARK_RED       = 1
####   DARK_GREEN     = 2
####   DARK_YELLOW    = 3
####   DARK_BLUE      = 4
####   DARK_MAGENTA   = 5
####   DARK_CYAN      = 6
####   LIGHT_GRAY     = 7
####   MEDIUM_GRAY    = 8
####   BRIGHT_RED     = 9
####   BRIGHT_GREEN   = 10
####   BRIGHT_YELLOW  = 11
####   BRIGHT_BLUE    = 12
####   BRIGHT_MAGENTA = 13
####   BRIGHT_CYAN    = 14
####   WHITE          = 15
####
#### # fmt: off
#### class ThemeProtocol(Protocol):
####   def  bold_color(self, s: str) -> str: ...
####   def        bold(self, s: str) -> str: ...
####   def       color(self, s: str) -> str: ...
####   def       faint(self, s: str) -> str: ...
####   def faint_color(self, s: str) -> str: ...
#### # fmt: on
