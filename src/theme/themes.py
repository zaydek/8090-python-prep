import colorful as cf
from colorful import ansi
from colorful.core import Colorful

cf.use_true_colors()  # Enable true colors for hex/RGB

# RGB for 16 ANSI codes
ANSI_16_RGB = [
    (0, 0, 0),
    (128, 0, 0),
    (0, 128, 0),
    (128, 128, 0),
    (0, 0, 128),
    (128, 0, 128),
    (0, 128, 128),
    (192, 192, 192),
    (128, 128, 128),
    (255, 0, 0),
    (0, 255, 0),
    (255, 255, 0),
    (0, 0, 255),
    (255, 0, 255),
    (0, 255, 255),
    (255, 255, 255),
]

# ANSI codes
ANSI_CODE_BLACK = 0
ANSI_CODE_DARK_RED = 1
ANSI_CODE_DARK_GREEN = 2
ANSI_CODE_DARK_YELLOW = 3
ANSI_CODE_DARK_BLUE = 4
ANSI_CODE_DARK_MAGENTA = 5
ANSI_CODE_DARK_CYAN = 6
ANSI_CODE_LIGHT_GRAY = 7
ANSI_CODE_MEDIUM_GRAY = 8
ANSI_CODE_BRIGHT_RED = 9
ANSI_CODE_BRIGHT_GREEN = 10
ANSI_CODE_BRIGHT_YELLOW = 11
ANSI_CODE_BRIGHT_BLUE = 12
ANSI_CODE_BRIGHT_MAGENTA = 13
ANSI_CODE_BRIGHT_CYAN = 14
ANSI_CODE_WHITE = 15


def _create_rgb_color_style(r: int, g: int, b: int):
    """Create a ColorfulStyle for RGB color using true colors."""
    # Create ANSI escape code for true color foreground
    start_code = ansi.ANSI_ESCAPE_CODE.format(
        code=f"{8 + ansi.FOREGROUND_COLOR_OFFSET};2;{r};{g};{b}"
    )
    end_code = ansi.ANSI_ESCAPE_CODE.format(
        code=ansi.FOREGROUND_COLOR_OFFSET + ansi.COLOR_CLOSE_OFFSET
    )
    # Create ColorfulStyle with the style tuple
    style_tuple = (start_code, end_code)
    return Colorful.ColorfulStyle(style_tuple, Colorful.TRUE_COLORS, cf.colorful)


def new_theme_from_ansi_code(code: int) -> "CustomTheme":
    """Create a CustomTheme from an ANSI code (0-15)."""
    return CustomTheme(str(code))


def new_theme_from_hex_color(hex_color: str) -> "CustomTheme":
    """Create a CustomTheme from a hex color string (e.g., "#00FF00")."""
    return CustomTheme(hex_color)


class CustomTheme:
    """Implements Theme with ANSI or hex.

    >>> theme = new_theme_from_hex_color("#00FF00")
    >>> theme.color("Test")  # Colored output
    """

    def __init__(self, color_value: str):
        self.color_value = color_value
        self._color_styler = self._get_color_styler()

    def _get_color_styler(self):
        if self.color_value.isdigit():
            code = int(self.color_value)
            if 0 <= code <= 15:
                r, g, b = ANSI_16_RGB[code]
                return _create_rgb_color_style(r, g, b)
            raise ValueError("Unsupported ANSI code")
        elif self.color_value.startswith("#"):
            r = int(self.color_value[1:3], 16)
            g = int(self.color_value[3:5], 16)
            b = int(self.color_value[5:7], 16)
            return _create_rgb_color_style(r, g, b)
        raise ValueError("Invalid color value")

    def get_color(self) -> str:
        return self.color_value

    def bold_color(self, s: str) -> str:
        return (cf.bold & self._color_styler)(s)

    def bold(self, s: str) -> str:
        return cf.bold(s)

    def color(self, s: str) -> str:
        return self._color_styler(s)

    def faint(self, s: str) -> str:
        return cf.dimmed(s)

    def faint_color(self, s: str) -> str:
        return (cf.dimmed & self._color_styler)(s)


class PlainTheme:
    """Implements Theme without colors.

    >>> theme = PlainTheme()
    >>> theme.faint_color("Dim")  # No effect
    'Dim'
    """

    def get_color(self) -> str:
        return ""

    def bold_color(self, s: str) -> str:
        return s

    def bold(self, s: str) -> str:
        return s

    def color(self, s: str) -> str:
        return s

    def faint(self, s: str) -> str:
        return s

    def faint_color(self, s: str) -> str:
        return s


# Predefined themes
ANSI_CODE_BLACK_THEME = new_theme_from_ansi_code(ANSI_CODE_BLACK)
ANSI_CODE_DARK_RED_THEME = new_theme_from_ansi_code(ANSI_CODE_DARK_RED)
ANSI_CODE_DARK_GREEN_THEME = new_theme_from_ansi_code(ANSI_CODE_DARK_GREEN)
ANSI_CODE_DARK_YELLOW_THEME = new_theme_from_ansi_code(ANSI_CODE_DARK_YELLOW)
ANSI_CODE_DARK_BLUE_THEME = new_theme_from_ansi_code(ANSI_CODE_DARK_BLUE)
ANSI_CODE_DARK_MAGENTA_THEME = new_theme_from_ansi_code(ANSI_CODE_DARK_MAGENTA)
ANSI_CODE_DARK_CYAN_THEME = new_theme_from_ansi_code(ANSI_CODE_DARK_CYAN)
ANSI_CODE_LIGHT_GRAY_THEME = new_theme_from_ansi_code(ANSI_CODE_LIGHT_GRAY)
ANSI_CODE_MEDIUM_GRAY_THEME = new_theme_from_ansi_code(ANSI_CODE_MEDIUM_GRAY)
ANSI_CODE_BRIGHT_RED_THEME = new_theme_from_ansi_code(ANSI_CODE_BRIGHT_RED)
ANSI_CODE_BRIGHT_GREEN_THEME = new_theme_from_ansi_code(ANSI_CODE_BRIGHT_GREEN)
ANSI_CODE_BRIGHT_YELLOW_THEME = new_theme_from_ansi_code(ANSI_CODE_BRIGHT_YELLOW)
ANSI_CODE_BRIGHT_BLUE_THEME = new_theme_from_ansi_code(ANSI_CODE_BRIGHT_BLUE)
ANSI_CODE_BRIGHT_MAGENTA_THEME = new_theme_from_ansi_code(ANSI_CODE_BRIGHT_MAGENTA)
ANSI_CODE_BRIGHT_CYAN_THEME = new_theme_from_ansi_code(ANSI_CODE_BRIGHT_CYAN)
ANSI_CODE_WHITE_THEME = new_theme_from_ansi_code(ANSI_CODE_WHITE)
