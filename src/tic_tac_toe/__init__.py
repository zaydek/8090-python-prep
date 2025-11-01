import colorful as cf


def print_board() -> None:
    # --- Styles ---
    X = cf.bold
    O = cf.bold
    empty = cf.gray
    grid_line = cf.gray
    number = cf.gray

    # --- Static board ---
    board = [["X", " ", "O"], [" ", "X", " "], ["O", " ", "X"]]

    # --- Header ---
    print("\n" + cf.bold("   TIC TAC TOE   ") + "\n")

    # --- Rows ---
    for i, row in enumerate(board):
        cells = []
        for j, cell in enumerate(row):
            if cell == "X":
                cells.append(str(X(" X ")))
            elif cell == "O":
                cells.append(str(O(" O ")))
            else:
                pos = i * 3 + j + 1
                cells.append(str(number(f" {pos} ")))
        print(str(grid_line("│")).join(cells))

        if i < 2:
            print(str(grid_line("───┼───┼───")))

    # --- Footer ---
    print("\n" + cf.italic("Use numbers 1–9 to place your mark.") + "\n")


def main() -> None:
    """Main CLI program for Tic Tac Toe."""
    print_board()


if __name__ == "__main__":
    main()
