"""Safe integer parsing with optional bounds validation."""

from enum import Enum, auto
from typing import Generic, TypeVar, NamedTuple, Optional
import sys

T = TypeVar("T")
E = TypeVar("E")


class Ok(NamedTuple, Generic[T]):
    value: T


class Err(NamedTuple, Generic[E]):
    error: E


type Result[T, E] = Ok[T] | Err[E]


class ParseIntErrorKind(Enum):
    NOT_AN_INTEGER = auto()
    TOO_LOW = auto()
    TOO_HIGH = auto()


class Bounds(NamedTuple):
    min: Optional[int] = None
    max: Optional[int] = None


def parse_int_safe(s: str, bounds: Bounds = Bounds()) -> Result[int, ParseIntErrorKind]:
    """Safely parse string to int with optional bounds."""
    try:
        val = int(s.strip())
        if bounds.min is not None and val < bounds.min:
            return Err(ParseIntErrorKind.TOO_LOW)
        if bounds.max is not None and val > bounds.max:
            return Err(ParseIntErrorKind.TOO_HIGH)
        return Ok(val)
    except ValueError:
        return Err(ParseIntErrorKind.NOT_AN_INTEGER)


def main(
    input_fn=input,
    output_fn=print,
    exit_fn=sys.exit,
    max_tries: int = 3,
) -> None:
    """Main CLI program with dependency injection for testing.

    Args:
        input_fn: Function to get user input (default: builtin input)
        output_fn: Function to output messages (default: builtin print)
        exit_fn: Function to exit the program (default: sys.exit)
        max_tries: Maximum number of invalid attempts allowed
    """
    # Prompt the user for their name
    name = input_fn("What is your name? ").strip()
    output_fn(f"Hello, {name}!")

    tries = 0

    # Prompt the user for their age
    while tries < max_tries:
        age = input_fn("What is your age? ").strip()
        result = parse_int_safe(age, Bounds(min=0, max=100))

        # Check if the age is valid
        match result:
            case Ok(value):
                output_fn(f"You are {value} years old.")
                return
            case Err(error):
                # Print the error message
                match error:
                    case ParseIntErrorKind.NOT_AN_INTEGER:
                        output_fn("Error: Not a valid integer. Try again.")
                    case ParseIntErrorKind.TOO_LOW:
                        output_fn("Error: Age too low (must be >=0). Try again.")
                    case ParseIntErrorKind.TOO_HIGH:
                        output_fn("Error: Age too high (must be <=100). Try again.")
                tries += 1

    output_fn("Error: Too many invalid attempts. Exiting.")
    exit_fn(1)


if __name__ == "__main__":
    main()
