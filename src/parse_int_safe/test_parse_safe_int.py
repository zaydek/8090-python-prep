"""Tests for parse_int_safe functionality."""

from parse_int_safe import (
    parse_int_safe,
    Ok,
    Err,
    Bounds,
    ParseIntErrorKind,
)


# Test valid input without bounds
def test_parse_valid_positive_integer():
    """Test parsing a positive integer."""
    assert parse_int_safe("42") == Ok(42)


def test_parse_valid_zero():
    """Test parsing zero."""
    assert parse_int_safe("0") == Ok(0)


def test_parse_valid_negative_integer():
    """Test parsing a negative integer."""
    assert parse_int_safe("-10") == Ok(-10)


def test_parse_valid_integer_with_whitespace():
    """Test parsing an integer with surrounding whitespace."""
    assert parse_int_safe("  42  ") == Ok(42)


def test_parse_valid_negative_integer_with_whitespace():
    """Test parsing a negative integer with surrounding whitespace."""
    assert parse_int_safe("  -10  ") == Ok(-10)


################################################################################


# Test valid input with bounds
def test_parse_within_bounds_lower_bound():
    """Test parsing a value at the lower bound."""
    assert parse_int_safe("10", Bounds(min=10, max=20)) == Ok(10)


def test_parse_within_bounds_upper_bound():
    """Test parsing a value at the upper bound."""
    assert parse_int_safe("20", Bounds(min=10, max=20)) == Ok(20)


def test_parse_within_bounds_middle():
    """Test parsing a value in the middle of bounds."""
    assert parse_int_safe("15", Bounds(min=10, max=20)) == Ok(15)


def test_parse_within_bounds_zero_to_hundred():
    """Test parsing zero with bounds 0-100."""
    assert parse_int_safe("0", Bounds(min=0, max=100)) == Ok(0)


def test_parse_within_bounds_hundred():
    """Test parsing 100 with bounds 0-100."""
    assert parse_int_safe("100", Bounds(min=0, max=100)) == Ok(100)


################################################################################


# Test invalid input - not an integer
def test_parse_non_integer_alphabetic():
    """Test parsing alphabetic string returns error."""
    assert parse_int_safe("abc") == Err(ParseIntErrorKind.NOT_AN_INTEGER)


def test_parse_non_integer_decimal():
    """Test parsing decimal number returns error."""
    assert parse_int_safe("12.5") == Err(ParseIntErrorKind.NOT_AN_INTEGER)


def test_parse_empty_string():
    """Test parsing empty string returns error."""
    assert parse_int_safe("") == Err(ParseIntErrorKind.NOT_AN_INTEGER)


def test_parse_whitespace_only():
    """Test parsing whitespace-only string returns error."""
    assert parse_int_safe("   ") == Err(ParseIntErrorKind.NOT_AN_INTEGER)


def test_parse_non_integer_mixed():
    """Test parsing string with numbers and letters returns error."""
    assert parse_int_safe("42abc") == Err(ParseIntErrorKind.NOT_AN_INTEGER)


################################################################################


# Test invalid input - too low
def test_parse_too_low_below_min():
    """Test parsing value below minimum returns TOO_LOW error."""
    assert parse_int_safe("5", Bounds(min=10)) == Err(ParseIntErrorKind.TOO_LOW)


def test_parse_too_low_negative():
    """Test parsing negative value below minimum returns TOO_LOW error."""
    assert parse_int_safe("-5", Bounds(min=0)) == Err(ParseIntErrorKind.TOO_LOW)


def test_parse_too_low_zero():
    """Test parsing zero when minimum is 1 returns TOO_LOW error."""
    assert parse_int_safe("0", Bounds(min=1)) == Err(ParseIntErrorKind.TOO_LOW)


def test_parse_too_low_with_both_bounds():
    """Test parsing value below minimum with both bounds set."""
    assert parse_int_safe("9", Bounds(min=10, max=20)) == Err(ParseIntErrorKind.TOO_LOW)


################################################################################


# Test invalid input - too high
def test_parse_too_high_above_max():
    """Test parsing value above maximum returns TOO_HIGH error."""
    assert parse_int_safe("15", Bounds(max=10)) == Err(ParseIntErrorKind.TOO_HIGH)


def test_parse_too_high_one_hundred_one():
    """Test parsing 101 when max is 100 returns TOO_HIGH error."""
    assert parse_int_safe("101", Bounds(max=100)) == Err(ParseIntErrorKind.TOO_HIGH)


def test_parse_too_high_with_both_bounds():
    """Test parsing value above maximum with both bounds set."""
    assert parse_int_safe("21", Bounds(min=10, max=20)) == Err(
        ParseIntErrorKind.TOO_HIGH
    )


def test_parse_too_high_large_number():
    """Test parsing large number above maximum."""
    assert parse_int_safe("1000", Bounds(max=999)) == Err(ParseIntErrorKind.TOO_HIGH)
