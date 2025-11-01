import colorful as cf


def print_board() -> None:
    # --- Styles ---
    X = cf.bold & cf.red
    O = cf.bold & cf.blue
    empty = cf.dim_grey
    grid_line = cf.cyan
    number = cf.yellow

    # --- Static board ---
    board = [["X", " ", "O"], [" ", "X", " "], ["O", " ", "X"]]

    # --- Header ---
    print("\n" + cf.bold("   TIC TAC TOE   ").background_lightgrey.on_darkgrey + "\n")

    # --- Rows ---
    for i, row in enumerate(board):
        cells = []
        for j, cell in enumerate(row):
            if cell == "X":
                cells.append(X(" X "))
            elif cell == "O":
                cells.append(O(" O "))
            else:
                pos = i * 3 + j + 1
                cells.append(number(f" {pos} "))
        print(grid_line("│").join(cells))

        if i < 2:
            print(grid_line("───┼───┼───"))

    # --- Footer ---
    print("\n" + cf.italic("Use numbers 1–9 to place your mark.") + "\n")


def main() -> None:
    """Main CLI program for Tic Tac Toe."""
    print_board()


if __name__ == "__main__":
    main()
