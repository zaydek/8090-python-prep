from typing import Protocol


class Theme(Protocol):
    """Theme defines the interface for styling CLI output.

    >>> theme = PlainTheme()
    >>> theme.bold("Hi")  # No styling
    'Hi'
    """

    def get_color(self) -> str:
        """Returns the color as a string (ANSI code or hex).

        Examples:
        - ANSI: "10"
        - Hex: "#00FF00"
        - Plain: ""
        """
        ...

    def bold_color(self, s: str) -> str:
        """Returns bold version of colored string."""
        ...

    def bold(self, s: str) -> str:
        """Returns string in bold."""
        ...

    def color(self, s: str) -> str:
        """Returns colored string."""
        ...

    def faint(self, s: str) -> str:
        """Returns faint (dimmed) string."""
        ...

    def faint_color(self, s: str) -> str:
        """Returns faint colored string."""
        ...
