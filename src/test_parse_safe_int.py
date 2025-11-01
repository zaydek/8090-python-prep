import pytest
import parse_int_safe as mod


@pytest.mark.parametrize(
    "input_str, expected",
    [
        ("42", mod.Ok(42)),
        ("0", mod.Ok(0)),
        ("-10", mod.Ok(-10)),
        ("100", mod.Ok(100)),
        ("  42  ", mod.Ok(42)),
        ("  -10  ", mod.Ok(-10)),
    ],
)
def test_valid_without_bounds(input_str, expected):
    """Test that valid integer strings are parsed correctly without bounds."""
    assert mod.parse_int_safe(input_str) == expected


################################################################################
################################################################################


@pytest.mark.parametrize(
    "input_str, bounds, expected",
    [
        ("10", mod.Bounds(min=10, max=20), mod.Ok(10)),
        ("20", mod.Bounds(min=10, max=20), mod.Ok(20)),
        ("15", mod.Bounds(min=10, max=20), mod.Ok(15)),
        ("0", mod.Bounds(min=0, max=100), mod.Ok(0)),
        ("100", mod.Bounds(min=0, max=100), mod.Ok(100)),
    ],
)
def test_valid_with_bounds(input_str, bounds, expected):
    """Test that valid integer strings within bounds are parsed correctly."""
    assert mod.parse_int_safe(input_str, bounds) == expected


################################################################################
################################################################################


@pytest.mark.parametrize(
    "input_str, bounds, expected",
    [
        # Not an integer
        ("abc", mod.Bounds(), mod.Err(mod.ParseIntErrorKind.NOT_AN_INTEGER)),
        ("12.5", mod.Bounds(), mod.Err(mod.ParseIntErrorKind.NOT_AN_INTEGER)),
        ("", mod.Bounds(), mod.Err(mod.ParseIntErrorKind.NOT_AN_INTEGER)),
        ("   ", mod.Bounds(), mod.Err(mod.ParseIntErrorKind.NOT_AN_INTEGER)),
        ("hello", mod.Bounds(), mod.Err(mod.ParseIntErrorKind.NOT_AN_INTEGER)),
        ("42abc", mod.Bounds(), mod.Err(mod.ParseIntErrorKind.NOT_AN_INTEGER)),
        # Too low
        ("5", mod.Bounds(min=10), mod.Err(mod.ParseIntErrorKind.TOO_LOW)),
        ("-5", mod.Bounds(min=0), mod.Err(mod.ParseIntErrorKind.TOO_LOW)),
        ("0", mod.Bounds(min=1), mod.Err(mod.ParseIntErrorKind.TOO_LOW)),
        ("9", mod.Bounds(min=10, max=20), mod.Err(mod.ParseIntErrorKind.TOO_LOW)),
        # Too high
        ("15", mod.Bounds(max=10), mod.Err(mod.ParseIntErrorKind.TOO_HIGH)),
        ("101", mod.Bounds(max=100), mod.Err(mod.ParseIntErrorKind.TOO_HIGH)),
        ("21", mod.Bounds(min=10, max=20), mod.Err(mod.ParseIntErrorKind.TOO_HIGH)),
        ("1000", mod.Bounds(max=999), mod.Err(mod.ParseIntErrorKind.TOO_HIGH)),
    ],
)
def test_invalid(input_str, bounds, expected):
    """Test that invalid inputs return appropriate error results.

    This includes:
    - Non-integer strings (alphabetical, decimal, empty, etc.)
    - Values below the minimum bound
    - Values above the maximum bound
    """
    assert mod.parse_int_safe(input_str, bounds) == expected
