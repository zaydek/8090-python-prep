# ansi.py — with IntEnum for clarity, no magic numbers
from enum import IntEnum
from typing import Dict, List


# TODO: Prefer longhand names over abbreviations?
class AnsiCodeEnum(IntEnum):
    # ANSI code for resetting all styles and colors
    RESET = 0

    # ANSI codes for styles
    BOLD = 1
    BOLD_OFF = 22
    DIM = 2
    DIM_OFF = 22  # ANSI is kind of retarded: DIM is the same as BOLD_OFF
    ITALIC = 3
    ITALIC_OFF = 23
    UNDERLINE = 4
    UNDERLINE_OFF = 24
    BLINK = 5
    BLINK_OFF = 25
    INVERT = 7
    INVERT_OFF = 27
    HIDDEN = 8
    HIDDEN_OFF = 28
    STRIKE = 9
    STRIKE_OFF = 29

    # ANSI codes for extended foreground and background colors
    EXTENDED_FOREGROUND = 38  # Start an extended foreground color e.g. 8-bit or 24-bit
    EXTENDED_BACKGROUND = 48  # Start an extended background color e.g. 8-bit or 24-bit
    COLOR_8_BIT = 5  # Start a 8-bit foreground color (256 colors)
    COLOR_24_BIT = 2  # Start a 24-bit foreground color (e.g. RGB)

    # ANSI codes for resetting foreground and background colors
    # Note that these are used for extended foreground and background colors
    # such as 8-bit and 24-bit colors
    FOREGROUND_RESET = 39
    BACKGROUND_RESET = 49

    # ANSI codes for standard foreground colors
    FOREGROUND_BLACK = 30
    FOREGROUND_RED = 31
    FOREGROUND_GREEN = 32
    FOREGROUND_YELLOW = 33
    FOREGROUND_BLUE = 34
    FOREGROUND_MAGENTA = 35
    FOREGROUND_CYAN = 36
    FOREGROUND_WHITE = 37

    # ANSI codes for high intensity foreground colors (bright colors)
    FOREGROUND_HIGH_INTENSITY_BLACK = 90
    FOREGROUND_HIGH_INTENSITY_RED = 91
    FOREGROUND_HIGH_INTENSITY_GREEN = 92
    FOREGROUND_HIGH_INTENSITY_YELLOW = 93
    FOREGROUND_HIGH_INTENSITY_BLUE = 94
    FOREGROUND_HIGH_INTENSITY_MAGENTA = 95
    FOREGROUND_HIGH_INTENSITY_CYAN = 96
    FOREGROUND_HIGH_INTENSITY_WHITE = 97

    # ANSI codes for standard background colors
    BACKGROUND_BLACK = 40
    BACKGROUND_RED = 41
    BACKGROUND_GREEN = 42
    BACKGROUND_YELLOW = 43
    BACKGROUND_BLUE = 44
    BACKGROUND_MAGENTA = 45
    BACKGROUND_CYAN = 46
    BACKGROUND_WHITE = 47

    # ANSI codes for high intensity background colors (bright colors)
    BACKGROUND_HIGH_INTENSITY_BLACK = 100
    BACKGROUND_HIGH_INTENSITY_RED = 101
    BACKGROUND_HIGH_INTENSITY_GREEN = 102
    BACKGROUND_HIGH_INTENSITY_YELLOW = 103
    BACKGROUND_HIGH_INTENSITY_BLUE = 104
    BACKGROUND_HIGH_INTENSITY_MAGENTA = 105
    BACKGROUND_HIGH_INTENSITY_CYAN = 106
    BACKGROUND_HIGH_INTENSITY_WHITE = 107
    # fmt: on


# Returns True if the code is a foreground color
def is_foreground_color(code: AnsiCodeEnum) -> bool:
    return (
        AnsiCodeEnum.FOREGROUND_BLACK <= code <= AnsiCodeEnum.FOREGROUND_WHITE
        or AnsiCodeEnum.FOREGROUND_HIGH_INTENSITY_BLACK <= code <= AnsiCodeEnum.FOREGROUND_HIGH_INTENSITY_WHITE
    )


# Returns True if the code is a background color
def is_background_color(code: AnsiCodeEnum) -> bool:
    return (
        AnsiCodeEnum.BACKGROUND_BLACK <= code <= AnsiCodeEnum.BACKGROUND_WHITE
        or AnsiCodeEnum.BACKGROUND_HIGH_INTENSITY_BLACK <= code <= AnsiCodeEnum.BACKGROUND_HIGH_INTENSITY_WHITE
    )


class AnsiStyle:
    # Escape a list of ANSI codes into an ANSI escape sequence string.
    # For example: [AnsiCodeEnum.BOLD, AnsiCodeEnum.FOREGROUND_RED] -> "\x1b[1;31m"
    @staticmethod
    def _escape(*codes: AnsiCodeEnum) -> str:
        codes_str = ";".join(map(str, codes))
        return f"\x1b[{codes_str}m"

    @staticmethod
    def dynamic(codes: List[AnsiCodeEnum], text: str) -> str:
        # Maps on codes to off codes
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

        # If there are no on codes, return the text as is
        # TODO: I'm not 100% sure not works correctly here; I don't know
        # Python's quirks well enough to be sure.
        if not codes:
            return text

        # Escape the start sequence
        start_sequence = AnsiStyle._escape(*codes)

        # Escape the end sequence
        off_codes: List[AnsiCodeEnum] = []
        reversed_codes = reversed(codes)
        for code in reversed_codes:
            # Check if the code is a foreground or background color
            if is_foreground_color(code):
                off_codes.append(AnsiCodeEnum.FOREGROUND_RESET)
            # Check if the code is a background color
            elif is_background_color(code):
                off_codes.append(AnsiCodeEnum.BACKGROUND_RESET)
            # Check if the code has an off code
            elif code in OFF_MAP:
                off_codes.append(OFF_MAP[code])
            elif code == AnsiCodeEnum.EXTENDED_FOREGROUND:
                # TODO: This part seems highly repetitive; can we refactor?
                off_codes.append(AnsiCodeEnum.FOREGROUND_RESET)
            elif code == AnsiCodeEnum.EXTENDED_BACKGROUND:
                # TODO: This part seems highly repetitive; can we refactor?
                off_codes.append(AnsiCodeEnum.BACKGROUND_RESET)
        end_sequence = AnsiStyle._escape(*off_codes) if off_codes else ""

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


# Create a banner for the given text
def banner(text: str) -> str:
    parts: List[str] = []
    parts.append("#" * 80)
    parts.append(f"## {text} ##")
    parts.append("#" * 80)
    return "\n".join(parts)


def main() -> None:
    # Test styles
    print(banner("## Styles ##"))
    print(AnsiStyle.dynamic([AnsiCodeEnum.DIM], "Dim"))
    print(AnsiStyle.dynamic([AnsiCodeEnum.ITALIC], "Italic"))
    print(AnsiStyle.dynamic([AnsiCodeEnum.UNDERLINE], "Underline"))
    print(AnsiStyle.dynamic([AnsiCodeEnum.BLINK], "Blink (may not work in all terminals)"))
    print(AnsiStyle.dynamic([AnsiCodeEnum.INVERT], "Invert"))
    print(AnsiStyle.dynamic([AnsiCodeEnum.HIDDEN], "Hidden (should be invisible)"))
    print(AnsiStyle.dynamic([AnsiCodeEnum.STRIKE], "Strike"))

    # Test combinations
    print(banner("## Combinations ##"))
    print(AnsiStyle.dynamic([AnsiCodeEnum.BOLD, AnsiCodeEnum.ITALIC], "Bold + Italic"))
    print(AnsiStyle.dynamic([AnsiCodeEnum.UNDERLINE, AnsiCodeEnum.STRIKE], "Underline + Strike"))
    print(
        AnsiStyle.dynamic(
            [AnsiCodeEnum.BOLD, AnsiCodeEnum.UNDERLINE, AnsiCodeEnum.ITALIC],
            "Bold + Underline + Italic",
        )
    )

    # Test standard colors
    print(banner("## Standard FG Colors ##"))
    print(AnsiStyle.dynamic([AnsiCodeEnum.FOREGROUND_BLACK], "Black"))
    print(AnsiStyle.dynamic([AnsiCodeEnum.FOREGROUND_RED], "Red"))
    print(AnsiStyle.dynamic([AnsiCodeEnum.FOREGROUND_GREEN], "Green"))
    print(AnsiStyle.dynamic([AnsiCodeEnum.FOREGROUND_YELLOW], "Yellow"))
    print(AnsiStyle.dynamic([AnsiCodeEnum.FOREGROUND_BLUE], "Blue"))
    print(AnsiStyle.dynamic([AnsiCodeEnum.FOREGROUND_MAGENTA], "Magenta"))
    print(AnsiStyle.dynamic([AnsiCodeEnum.FOREGROUND_CYAN], "Cyan"))
    print(AnsiStyle.dynamic([AnsiCodeEnum.FOREGROUND_WHITE], "White"))

    # Test bright foreground colors
    print(banner("## Bright FG Colors ##"))
    print(AnsiStyle.dynamic([AnsiCodeEnum.FOREGROUND_HIGH_INTENSITY_BLACK], "Bright Black"))
    print(AnsiStyle.dynamic([AnsiCodeEnum.FOREGROUND_HIGH_INTENSITY_RED], "Bright Red"))
    print(AnsiStyle.dynamic([AnsiCodeEnum.FOREGROUND_HIGH_INTENSITY_GREEN], "Bright Green"))
    print(AnsiStyle.dynamic([AnsiCodeEnum.FOREGROUND_HIGH_INTENSITY_YELLOW], "Bright Yellow"))
    print(AnsiStyle.dynamic([AnsiCodeEnum.FOREGROUND_HIGH_INTENSITY_BLUE], "Bright Blue"))
    print(AnsiStyle.dynamic([AnsiCodeEnum.FOREGROUND_HIGH_INTENSITY_MAGENTA], "Bright Magenta"))
    print(AnsiStyle.dynamic([AnsiCodeEnum.FOREGROUND_HIGH_INTENSITY_CYAN], "Bright Cyan"))
    print(AnsiStyle.dynamic([AnsiCodeEnum.FOREGROUND_HIGH_INTENSITY_WHITE], "Bright White"))

    # Test standard background colors
    print(banner("## Standard BG Colors ##"))
    print(AnsiStyle.dynamic([AnsiCodeEnum.BACKGROUND_BLACK], "Black BG"))
    print(AnsiStyle.dynamic([AnsiCodeEnum.BACKGROUND_RED], "Red BG"))
    print(AnsiStyle.dynamic([AnsiCodeEnum.BACKGROUND_GREEN], "Green BG"))
    print(AnsiStyle.dynamic([AnsiCodeEnum.BACKGROUND_YELLOW], "Yellow BG"))
    print(AnsiStyle.dynamic([AnsiCodeEnum.BACKGROUND_BLUE], "Blue BG"))
    print(AnsiStyle.dynamic([AnsiCodeEnum.BACKGROUND_MAGENTA], "Magenta BG"))
    print(AnsiStyle.dynamic([AnsiCodeEnum.BACKGROUND_CYAN], "Cyan BG"))
    print(AnsiStyle.dynamic([AnsiCodeEnum.BACKGROUND_WHITE], "White BG"))

    # Test bright background colors
    print(banner("## Bright BG Colors ##"))
    print(AnsiStyle.dynamic([AnsiCodeEnum.BACKGROUND_HIGH_INTENSITY_BLACK], "Bright Black BG"))
    print(AnsiStyle.dynamic([AnsiCodeEnum.BACKGROUND_HIGH_INTENSITY_RED], "Bright Red BG"))
    print(AnsiStyle.dynamic([AnsiCodeEnum.BACKGROUND_HIGH_INTENSITY_GREEN], "Bright Green BG"))
    print(AnsiStyle.dynamic([AnsiCodeEnum.BACKGROUND_HIGH_INTENSITY_YELLOW], "Bright Yellow BG"))
    print(AnsiStyle.dynamic([AnsiCodeEnum.BACKGROUND_HIGH_INTENSITY_BLUE], "Bright Blue BG"))
    print(AnsiStyle.dynamic([AnsiCodeEnum.BACKGROUND_HIGH_INTENSITY_MAGENTA], "Bright Magenta BG"))
    print(AnsiStyle.dynamic([AnsiCodeEnum.BACKGROUND_HIGH_INTENSITY_CYAN], "Bright Cyan BG"))
    print(AnsiStyle.dynamic([AnsiCodeEnum.BACKGROUND_HIGH_INTENSITY_WHITE], "Bright White BG"))

    # Test 8-bit colors
    print(banner("## 8-bit Colors ##"))
    print(AnsiStyle.dynamic(AnsiStyle.foreground_8_bit(208), "Orange FG (code 208)"))
    print(AnsiStyle.dynamic(AnsiStyle.background_8_bit(235), "Dark Gray BG (code 235)"))
    print(
        AnsiStyle.dynamic([*AnsiStyle.foreground_8_bit(46), *AnsiStyle.background_8_bit(232)], "Green FG on Black BG")
    )

    # Test 24-bit colors
    print(banner("## 24-bit Colors ##"))
    print(AnsiStyle.dynamic(AnsiStyle.foreground_24_bit(255, 100, 100), "Light Red FG"))
    print(AnsiStyle.dynamic(AnsiStyle.background_24_bit(40, 40, 60), "Dark Blue-Gray BG"))
    print(
        AnsiStyle.dynamic(
            [*AnsiStyle.foreground_24_bit(0, 255, 0), *AnsiStyle.background_24_bit(50, 50, 50)], "Green FG on Gray BG"
        )
    )

    #### # Test mixed style + color
    #### print("\n=== Mixed Style + Color ===")
    #### print(Ansi.dynamic([AnsiCode.BOLD, AnsiCode.ITALIC, AnsiCode.FOREGROUND_RED], "Bold Italic Red"))
    #### print(Ansi.dynamic([AnsiCode.UNDERLINE, *Ansi.bg8(220)], "Underline on Yellowish BG"))
    #### print(
    ####     Ansi.dynamic(
    ####         [AnsiCode.STRIKE, *Ansi.fg24(128, 0, 128), AnsiCode.INVERT],
    ####         "Strike Purple Invert",
    ####     )
    #### )
    ####
    #### # Test nesting/composition
    #### print("\n=== Nesting/Composition ===")
    #### print(
    ####     Ansi.dynamic(
    ####         [AnsiCode.BOLD],
    ####         "Bold start " + Ansi.dynamic([AnsiCode.ITALIC], "nested italic") + " bold end",
    ####     )
    #### )
    #### print(
    ####     Ansi.dynamic(
    ####         [AnsiCode.FOREGROUND_GREEN],
    ####         "Green " + Ansi.dynamic([AnsiCode.BACKGROUND_RED], "on red BG") + " green continues? No, off resets properly.",
    ####     )
    #### )

    # Final reset
    # TODO: Why the fuck are we calling this?
    #### print(Ansi._esc(AnsiCode.RESET))

    print("Hello, world!")


if __name__ == "__main__":
    main()
