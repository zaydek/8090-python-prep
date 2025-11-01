"""Tests for the main CLI program."""

from parse_int_safe import main


def test_main_successful_input():
    """Test main with valid name and age on first try."""
    inputs = ["Alice", "25"]
    input_iter = iter(inputs)
    outputs = []

    def mock_input(prompt):
        return next(input_iter)

    def mock_print(*args):
        outputs.append(" ".join(map(str, args)))

    def mock_exit(code):
        outputs.append(f"EXIT({code})")

    main(input_fn=mock_input, output_fn=mock_print, exit_fn=mock_exit)

    assert "Hello, Alice!" in outputs
    assert "You are 25 years old." in outputs
    assert "EXIT" not in " ".join(outputs)


def test_main_max_tries_exceeded():
    """Test main exits after max tries."""
    inputs = ["David", "abc", "xyz", "hello"]
    input_iter = iter(inputs)
    outputs = []

    def mock_input(prompt):
        return next(input_iter)

    def mock_print(*args):
        outputs.append(" ".join(map(str, args)))

    def mock_exit(code):
        outputs.append(f"EXIT({code})")

    main(input_fn=mock_input, output_fn=mock_print, exit_fn=mock_exit, max_tries=3)

    assert "Hello, David!" in outputs
    assert outputs.count("Error: Not a valid integer. Try again.") == 3
    assert "Error: Too many invalid attempts. Exiting." in outputs
    assert "EXIT(1)" in outputs


def test_main_too_low_then_valid():
    """Test main with age too low, then valid."""
    inputs = ["Charlie", "-5", "50"]
    input_iter = iter(inputs)
    outputs = []

    def mock_input(prompt):
        return next(input_iter)

    def mock_print(*args):
        outputs.append(" ".join(map(str, args)))

    def mock_exit(code):
        outputs.append(f"EXIT({code})")

    main(input_fn=mock_input, output_fn=mock_print, exit_fn=mock_exit)

    assert "Hello, Charlie!" in outputs
    assert "Error: Age too low (must be >=0). Try again." in outputs
    assert "You are 50 years old." in outputs
