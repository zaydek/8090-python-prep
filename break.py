# ansi.py — with IntEnum for clarity, no magic numbers
from enum import IntEnum
from typing import Dict, List


# TODO: Prefer longhand names over abbreviations?
# fmt: off
class AnsiCodeEnum(IntEnum):
    # ANSI code for resetting all styles and colors
    RESET = 0

    # ANSI codes for styles
    BOLD          =  1
    BOLD_OFF      = 22
    DIM           =  2
    DIM_OFF       = 22  # ANSI is kind of retarded: DIM is the same as BOLD_OFF
    ITALIC        =  3
    ITALIC_OFF    = 23
    UNDERLINE     =  4
    UNDERLINE_OFF = 24
    BLINK         =  5
    BLINK_OFF     = 25
    INVERT        =  7
    INVERT_OFF    = 27
    HIDDEN        =  8
    HIDDEN_OFF    = 28
    STRIKE        =  9
    STRIKE_OFF    = 29

    # ANSI codes for extended foreground and background colors
    EXTENDED_FOREGROUND = 38  # Start an extended foreground color e.g. 8-bit or 24-bit
    EXTENDED_BACKGROUND = 48  # Start an extended background color e.g. 8-bit or 24-bit
    COLOR_8_BIT         =  5  # Start a 8-bit foreground color (256 colors)
    COLOR_24_BIT        =  2  # Start a 24-bit foreground color (e.g. RGB)

    # ANSI codes for resetting foreground and background colors
    # Note that these are used for extended foreground and background colors
    # such as 8-bit and 24-bit colors
    FOREGROUND_RESET = 39
    BACKGROUND_RESET = 49

    # ANSI codes for standard foreground colors
    FOREGROUND_BLACK   = 30
    FOREGROUND_RED     = 31
    FOREGROUND_GREEN   = 32
    FOREGROUND_YELLOW  = 33
    FOREGROUND_BLUE    = 34
    FOREGROUND_MAGENTA = 35
    FOREGROUND_CYAN    = 36
    FOREGROUND_WHITE   = 37

    # ANSI codes for high intensity foreground colors (bright colors)
    FOREGROUND_HIGH_INTENSITY_BLACK   = 90
    FOREGROUND_HIGH_INTENSITY_RED     = 91
    FOREGROUND_HIGH_INTENSITY_GREEN   = 92
    FOREGROUND_HIGH_INTENSITY_YELLOW  = 93
    FOREGROUND_HIGH_INTENSITY_BLUE    = 94
    FOREGROUND_HIGH_INTENSITY_MAGENTA = 95
    FOREGROUND_HIGH_INTENSITY_CYAN    = 96
    FOREGROUND_HIGH_INTENSITY_WHITE   = 97

    # ANSI codes for standard background colors
    BACKGROUND_BLACK   = 40
    BACKGROUND_RED     = 41
    BACKGROUND_GREEN   = 42
    BACKGROUND_YELLOW  = 43
    BACKGROUND_BLUE    = 44
    BACKGROUND_MAGENTA = 45
    BACKGROUND_CYAN    = 46
    BACKGROUND_WHITE   = 47

    # ANSI codes for high intensity background colors (bright colors)
    BACKGROUND_HIGH_INTENSITY_BLACK   = 100
    BACKGROUND_HIGH_INTENSITY_RED     = 101
    BACKGROUND_HIGH_INTENSITY_GREEN   = 102
    BACKGROUND_HIGH_INTENSITY_YELLOW  = 103
    BACKGROUND_HIGH_INTENSITY_BLUE    = 104
    BACKGROUND_HIGH_INTENSITY_MAGENTA = 105
    BACKGROUND_HIGH_INTENSITY_CYAN    = 106
    BACKGROUND_HIGH_INTENSITY_WHITE   = 107
# fmt: on


# Returns the off code for the given code, or None if no off code is found.
def _get_off_code(code: AnsiCodeEnum) -> AnsiCodeEnum | None:
    def get_foreground_off_code(code: AnsiCodeEnum) -> AnsiCodeEnum | None:
        if (
            AnsiCodeEnum.FOREGROUND_BLACK <= code <= AnsiCodeEnum.FOREGROUND_WHITE
            or AnsiCodeEnum.FOREGROUND_HIGH_INTENSITY_BLACK <= code <= AnsiCodeEnum.FOREGROUND_HIGH_INTENSITY_WHITE
            or code == AnsiCodeEnum.EXTENDED_FOREGROUND
        ):
            return AnsiCodeEnum.FOREGROUND_RESET
        return None

    def get_background_off_code(code: AnsiCodeEnum) -> AnsiCodeEnum | None:
        if (
            AnsiCodeEnum.BACKGROUND_BLACK <= code <= AnsiCodeEnum.BACKGROUND_WHITE
            or AnsiCodeEnum.BACKGROUND_HIGH_INTENSITY_BLACK <= code <= AnsiCodeEnum.BACKGROUND_HIGH_INTENSITY_WHITE
            or code == AnsiCodeEnum.EXTENDED_BACKGROUND
        ):
            return AnsiCodeEnum.BACKGROUND_RESET
        return None

    def get_other_off_code(code: AnsiCodeEnum) -> AnsiCodeEnum | None:
        # fmt: off
        OFF_MAP: Dict[AnsiCodeEnum, AnsiCodeEnum] = {
            AnsiCodeEnum.BOLD:      AnsiCodeEnum.BOLD_OFF,
            AnsiCodeEnum.DIM:       AnsiCodeEnum.DIM_OFF,
            AnsiCodeEnum.ITALIC:    AnsiCodeEnum.ITALIC_OFF,
            AnsiCodeEnum.UNDERLINE: AnsiCodeEnum.UNDERLINE_OFF,
            AnsiCodeEnum.BLINK:     AnsiCodeEnum.BLINK_OFF,
            AnsiCodeEnum.INVERT:    AnsiCodeEnum.INVERT_OFF,
            AnsiCodeEnum.HIDDEN:    AnsiCodeEnum.HIDDEN_OFF,
            AnsiCodeEnum.STRIKE:    AnsiCodeEnum.STRIKE_OFF,
        }
        # fmt: on
        return OFF_MAP.get(code)

    return get_foreground_off_code(code) or get_background_off_code(code) or get_other_off_code(code)


def remove_consecutive_duplicates(input: List[int]) -> List[int]:
    """
    Remove consecutive duplicates from a list, preserving order.

    >>> remove_consecutive_duplicates([1, 1, 2, 3, 2, 4, 5])
    [1, 2, 3, 2, 4, 5]

    >>> remove_consecutive_duplicates([1, 2, 2, 2, 3])
    [1, 2, 3]
    """
    if not input:
        return []
    output = [input[0]]
    for item in input[1:]:
        last_item = output[-1]
        if item != last_item:
            output.append(item)
    return output


class AnsiStyle:
    # Escape a list of ANSI codes into an ANSI escape sequence string.
    # For example: [AnsiCodeEnum.BOLD, AnsiCodeEnum.FOREGROUND_RED] -> "\x1b[1;31m"
    @staticmethod
    def _escape_codes(*codes: AnsiCodeEnum) -> str:
        codes_str = ";".join(map(str, codes))
        return f"\x1b[{codes_str}m"

    # Format a list of ANSI codes into an ANSI escape sequence string.
    # For example: [AnsiCodeEnum.BOLD, AnsiCodeEnum.FOREGROUND_RED] -> "\x1b[1;31m"
    # TODO: Rename this to compose or format?
    @staticmethod
    def dynamic(codes: List[AnsiCodeEnum], text: str) -> str:
        if not codes:
            return text

        # Get the off codes
        off_codes: List[AnsiCodeEnum] = []
        reversed_codes = reversed(codes)
        for code in reversed_codes:
            if off_code := _get_off_code(code):
                off_codes.append(off_code)

        # Escape the start sequence
        start_sequence = AnsiStyle._escape_codes(*codes)

        # Escape the end sequence
        # Dedupe off codes because of extended foreground and background codes
        deduped_off_codes = remove_consecutive_duplicates(off_codes)
        end_sequence = AnsiStyle._escape_codes(*deduped_off_codes)

        # Return the combined start and end sequences
        return f"{start_sequence}{text}{end_sequence}"

    # ANSI codes for 8-bit foreground colors
    # TODO: This is kind of awkward: Ideally this is a side effect of how we
    # we render colors
    @staticmethod
    def foreground_8_bit(code: int) -> List[AnsiCodeEnum]:
        return [AnsiCodeEnum.EXTENDED_FOREGROUND, AnsiCodeEnum.COLOR_8_BIT, code]

    # ANSI codes for 8-bit background colors
    # TODO: This is kind of awkward: Ideally this is a side effect of how we
    # we render colors
    @staticmethod
    def background_8_bit(code: int) -> List[AnsiCodeEnum]:
        return [AnsiCodeEnum.EXTENDED_BACKGROUND, AnsiCodeEnum.COLOR_8_BIT, code]

    # ANSI codes for 24-bit foreground colors
    # TODO: This is kind of awkward: Ideally this is a side effect of how we
    # we render colors
    @staticmethod
    def foreground_24_bit(r: int, g: int, b: int) -> List[AnsiCodeEnum]:
        return [AnsiCodeEnum.EXTENDED_FOREGROUND, AnsiCodeEnum.COLOR_24_BIT, r, g, b]

    # ANSI codes for 24-bit background colors
    # TODO: This is kind of awkward: Ideally this is a side effect of how we
    # we render colors
    @staticmethod
    def background_24_bit(r: int, g: int, b: int) -> List[AnsiCodeEnum]:
        return [AnsiCodeEnum.EXTENDED_BACKGROUND, AnsiCodeEnum.COLOR_24_BIT, r, g, b]


################################################################################
# Main
################################################################################


# Renders a banner for the given text
def render_banner(text: str) -> str:
    parts: List[str] = []
    parts.append("#" * 80)
    parts.append(f"## {text} ##")
    parts.append("#" * 80)
    parts_str = "\n".join(parts)
    return parts_str


def main() -> None:
    # Test styles
    print(render_banner("## Styles ##"))
    print(AnsiStyle.dynamic([AnsiCodeEnum.DIM], "Dim"))
    print(AnsiStyle.dynamic([AnsiCodeEnum.ITALIC], "Italic"))
    print(AnsiStyle.dynamic([AnsiCodeEnum.UNDERLINE], "Underline"))
    print(AnsiStyle.dynamic([AnsiCodeEnum.BLINK], "Blink (may not work in all terminals)"))
    print(AnsiStyle.dynamic([AnsiCodeEnum.INVERT], "Invert"))
    print(AnsiStyle.dynamic([AnsiCodeEnum.HIDDEN], "Hidden (should be invisible)"))
    print(AnsiStyle.dynamic([AnsiCodeEnum.STRIKE], "Strike"))

    # Test combinations
    print(render_banner("## Combinations ##"))
    print(AnsiStyle.dynamic([AnsiCodeEnum.BOLD, AnsiCodeEnum.ITALIC], "Bold + Italic"))
    print(AnsiStyle.dynamic([AnsiCodeEnum.UNDERLINE, AnsiCodeEnum.STRIKE], "Underline + Strike"))
    print(
        AnsiStyle.dynamic(
            [AnsiCodeEnum.BOLD, AnsiCodeEnum.UNDERLINE, AnsiCodeEnum.ITALIC],
            "Bold + Underline + Italic",
        )
    )

    # Test standard colors
    print(render_banner("## Standard FG Colors ##"))
    print(AnsiStyle.dynamic([AnsiCodeEnum.FOREGROUND_BLACK], "Black"))
    print(AnsiStyle.dynamic([AnsiCodeEnum.FOREGROUND_RED], "Red"))
    print(AnsiStyle.dynamic([AnsiCodeEnum.FOREGROUND_GREEN], "Green"))
    print(AnsiStyle.dynamic([AnsiCodeEnum.FOREGROUND_YELLOW], "Yellow"))
    print(AnsiStyle.dynamic([AnsiCodeEnum.FOREGROUND_BLUE], "Blue"))
    print(AnsiStyle.dynamic([AnsiCodeEnum.FOREGROUND_MAGENTA], "Magenta"))
    print(AnsiStyle.dynamic([AnsiCodeEnum.FOREGROUND_CYAN], "Cyan"))
    print(AnsiStyle.dynamic([AnsiCodeEnum.FOREGROUND_WHITE], "White"))

    # Test bright foreground colors
    print(render_banner("## Bright FG Colors ##"))
    print(AnsiStyle.dynamic([AnsiCodeEnum.FOREGROUND_HIGH_INTENSITY_BLACK], "Bright Black"))
    print(AnsiStyle.dynamic([AnsiCodeEnum.FOREGROUND_HIGH_INTENSITY_RED], "Bright Red"))
    print(AnsiStyle.dynamic([AnsiCodeEnum.FOREGROUND_HIGH_INTENSITY_GREEN], "Bright Green"))
    print(AnsiStyle.dynamic([AnsiCodeEnum.FOREGROUND_HIGH_INTENSITY_YELLOW], "Bright Yellow"))
    print(AnsiStyle.dynamic([AnsiCodeEnum.FOREGROUND_HIGH_INTENSITY_BLUE], "Bright Blue"))
    print(AnsiStyle.dynamic([AnsiCodeEnum.FOREGROUND_HIGH_INTENSITY_MAGENTA], "Bright Magenta"))
    print(AnsiStyle.dynamic([AnsiCodeEnum.FOREGROUND_HIGH_INTENSITY_CYAN], "Bright Cyan"))
    print(AnsiStyle.dynamic([AnsiCodeEnum.FOREGROUND_HIGH_INTENSITY_WHITE], "Bright White"))

    # Test standard background colors
    print(render_banner("## Standard BG Colors ##"))
    print(AnsiStyle.dynamic([AnsiCodeEnum.BACKGROUND_BLACK], "Black BG"))
    print(AnsiStyle.dynamic([AnsiCodeEnum.BACKGROUND_RED], "Red BG"))
    print(AnsiStyle.dynamic([AnsiCodeEnum.BACKGROUND_GREEN], "Green BG"))
    print(AnsiStyle.dynamic([AnsiCodeEnum.BACKGROUND_YELLOW], "Yellow BG"))
    print(AnsiStyle.dynamic([AnsiCodeEnum.BACKGROUND_BLUE], "Blue BG"))
    print(AnsiStyle.dynamic([AnsiCodeEnum.BACKGROUND_MAGENTA], "Magenta BG"))
    print(AnsiStyle.dynamic([AnsiCodeEnum.BACKGROUND_CYAN], "Cyan BG"))
    print(AnsiStyle.dynamic([AnsiCodeEnum.BACKGROUND_WHITE], "White BG"))

    # Test bright background colors
    print(render_banner("## Bright BG Colors ##"))
    print(AnsiStyle.dynamic([AnsiCodeEnum.BACKGROUND_HIGH_INTENSITY_BLACK], "Bright Black BG"))
    print(AnsiStyle.dynamic([AnsiCodeEnum.BACKGROUND_HIGH_INTENSITY_RED], "Bright Red BG"))
    print(AnsiStyle.dynamic([AnsiCodeEnum.BACKGROUND_HIGH_INTENSITY_GREEN], "Bright Green BG"))
    print(AnsiStyle.dynamic([AnsiCodeEnum.BACKGROUND_HIGH_INTENSITY_YELLOW], "Bright Yellow BG"))
    print(AnsiStyle.dynamic([AnsiCodeEnum.BACKGROUND_HIGH_INTENSITY_BLUE], "Bright Blue BG"))
    print(AnsiStyle.dynamic([AnsiCodeEnum.BACKGROUND_HIGH_INTENSITY_MAGENTA], "Bright Magenta BG"))
    print(AnsiStyle.dynamic([AnsiCodeEnum.BACKGROUND_HIGH_INTENSITY_CYAN], "Bright Cyan BG"))
    print(AnsiStyle.dynamic([AnsiCodeEnum.BACKGROUND_HIGH_INTENSITY_WHITE], "Bright White BG"))

    # Test 8-bit colors
    print(render_banner("## 8-bit Colors ##"))
    print(AnsiStyle.dynamic(AnsiStyle.foreground_8_bit(208), "Orange FG (code 208)"))
    print(AnsiStyle.dynamic(AnsiStyle.background_8_bit(235), "Dark Gray BG (code 235)"))
    print(
        AnsiStyle.dynamic([*AnsiStyle.foreground_8_bit(46), *AnsiStyle.background_8_bit(232)], "Green FG on Black BG")
    )

    # Test 24-bit colors
    print(render_banner("## 24-bit Colors ##"))
    print(AnsiStyle.dynamic(AnsiStyle.foreground_24_bit(r=255, g=100, b=100), "Light Red FG"))
    print(AnsiStyle.dynamic(AnsiStyle.background_24_bit(r=40, g=40, b=60), "Dark Blue-Gray BG"))
    print(
        AnsiStyle.dynamic(
            [*AnsiStyle.foreground_24_bit(r=0, g=255, b=0), *AnsiStyle.background_24_bit(r=50, g=50, b=50)],
            "Green FG on Gray BG",
        )
    )

    print("Hello, world!")


if __name__ == "__main__":
    main()
