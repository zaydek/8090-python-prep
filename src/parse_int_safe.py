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


def main() -> None:
    # Prompt the user for their name
    name = input("What is your name? ").strip()
    print(f"Hello, {name}!")

    MAX_TRIES = 3
    tries = 0

    # Prompt the user for their age
    while tries < MAX_TRIES:
        age = input("What is your age? ").strip()
        result = parse_int_safe(age, Bounds(min=0, max=100))

        # Check if the age is valid
        match result:
            case Ok(value):
                print(f"You are {value} years old.")
                break
            case Err(error):
                # Print the error message
                match error:
                    case ParseIntErrorKind.NOT_AN_INTEGER:
                        print("Error: Not a valid integer. Try again.")
                    case ParseIntErrorKind.TOO_LOW:
                        print("Error: Age too low (must be >=0). Try again.")
                    case ParseIntErrorKind.TOO_HIGH:
                        print("Error: Age too high (must be <=100). Try again.")
                tries += 1

    if tries == MAX_TRIES:
        print("Error: Too many invalid attempts. Exiting.")
        sys.exit(1)


if __name__ == "__main__":
    main()
