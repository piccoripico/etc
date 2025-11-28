import argparse
import random
from typing import List, Optional, Set, Tuple

Grid = List[List[int]]


class SudokuBoard:
    """Represents a single Sudoku puzzle and supports interactive play."""

    def __init__(self, puzzle: Grid, solution: Grid):
        self.puzzle = puzzle
        self.solution = solution
        self.current = [row[:] for row in puzzle]
        self.givens: Set[Tuple[int, int]] = {
            (r, c) for r, row in enumerate(puzzle) for c, value in enumerate(row) if value
        }

    def reset(self) -> None:
        self.current = [row[:] for row in self.puzzle]

    def is_complete(self) -> bool:
        return all(all(cell for cell in row) for row in self.current) and self.current == self.solution

    def display(self) -> None:
        line = "+-------+-------+-------+"
        print("    1 2 3   4 5 6   7 8 9")
        for r, row in enumerate(self.current):
            if r % 3 == 0:
                print(f"  {line}")
            row_cells = []
            for c, value in enumerate(row):
                prefix = "| " if c % 3 == 0 else ""
                cell = str(value) if value else "."
                row_cells.append(f"{prefix}{cell}")
            print(f"{r + 1} {' '.join(row_cells)} |")
        print(f"  {line}")

    def is_valid_move(self, row: int, col: int, value: int) -> bool:
        if (row, col) in self.givens:
            return False
        return self.solution[row][col] == value

    def set_value(self, row: int, col: int, value: int) -> bool:
        if value and not (1 <= value <= 9):
            return False
        if (row, col) in self.givens:
            return False
        if value == 0:
            self.current[row][col] = 0
            return True
        if self.is_valid_move(row, col, value):
            self.current[row][col] = value
            return True
        return False

    def reveal_one(self) -> Optional[Tuple[int, int, int]]:
        for r in range(9):
            for c in range(9):
                if self.current[r][c] == 0:
                    value = self.solution[r][c]
                    self.current[r][c] = value
                    return r, c, value
        return None


def generate_full_board() -> Grid:
    def backtrack(board: Grid, cell: int = 0) -> bool:
        if cell == 81:
            return True
        r, c = divmod(cell, 9)
        if board[r][c] != 0:
            return backtrack(board, cell + 1)
        numbers = list(range(1, 10))
        random.shuffle(numbers)
        for value in numbers:
            if is_safe(board, r, c, value):
                board[r][c] = value
                if backtrack(board, cell + 1):
                    return True
                board[r][c] = 0
        return False

    board = [[0] * 9 for _ in range(9)]
    backtrack(board)
    return board


def is_safe(board: Grid, row: int, col: int, value: int) -> bool:
    if any(board[row][c] == value for c in range(9)):
        return False
    if any(board[r][col] == value for r in range(9)):
        return False
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for r in range(start_row, start_row + 3):
        for c in range(start_col, start_col + 3):
            if board[r][c] == value:
                return False
    return True


def find_empty(board: Grid) -> Optional[Tuple[int, int]]:
    for r in range(9):
        for c in range(9):
            if board[r][c] == 0:
                return r, c
    return None


def count_solutions(board: Grid, limit: int = 2) -> int:
    empty = find_empty(board)
    if not empty:
        return 1
    r, c = empty
    solutions = 0
    for value in range(1, 10):
        if is_safe(board, r, c, value):
            board[r][c] = value
            solutions += count_solutions(board, limit)
            if solutions >= limit:
                board[r][c] = 0
                return solutions
            board[r][c] = 0
    board[r][c] = 0
    return solutions


def solve_board(board: Grid) -> Optional[Grid]:
    empty = find_empty(board)
    if not empty:
        return [row[:] for row in board]
    r, c = empty
    for value in range(1, 10):
        if is_safe(board, r, c, value):
            board[r][c] = value
            solved = solve_board(board)
            if solved:
                return solved
            board[r][c] = 0
    board[r][c] = 0
    return None


def generate_puzzle(clues: int = 32) -> Tuple[Grid, Grid]:
    if not 17 <= clues <= 81:
        raise ValueError("Clues must be between 17 and 81.")

    solution = generate_full_board()
    puzzle = [row[:] for row in solution]
    cells = [(r, c) for r in range(9) for c in range(9)]
    random.shuffle(cells)

    removed = 0
    for r, c in cells:
        if 81 - removed <= clues:
            break
        backup = puzzle[r][c]
        puzzle[r][c] = 0
        if count_solutions([row[:] for row in puzzle]) != 1:
            puzzle[r][c] = backup
        else:
            removed += 1
    return puzzle, solution


def parse_puzzle(text: str) -> Grid:
    digits = [int(ch) if ch.isdigit() else 0 for ch in text if not ch.isspace()]
    if len(digits) != 81:
        raise ValueError("Puzzle text must describe exactly 81 cells.")
    grid = [digits[i : i + 9] for i in range(0, 81, 9)]
    return grid


def start_interactive(board: SudokuBoard) -> None:
    commands = """
Available commands:
  set r c v     - Set value v (1-9) at row r, column c
  clear r c     - Clear the value at row r, column c
  hint          - Reveal one correct value
  reset         - Reset the board to the initial state
  solve         - Show the full solution and exit
  quit          - Exit the game
"""
    print("新しい数独を開始します。行と列は1から9までです。")
    print(commands)
    board.display()

    while True:
        if board.is_complete():
            print("おめでとうございます！すべて正解です。")
            break
        raw = input("move> ").strip()
        if not raw:
            continue
        parts = raw.split()
        cmd = parts[0].lower()

        try:
            if cmd == "set" and len(parts) == 4:
                r = int(parts[1]) - 1
                c = int(parts[2]) - 1
                v = int(parts[3])
                if board.set_value(r, c, v):
                    print("OK")
                else:
                    print("その場所にはその数字を置けません。")
            elif cmd == "clear" and len(parts) == 3:
                r = int(parts[1]) - 1
                c = int(parts[2]) - 1
                if board.set_value(r, c, 0):
                    print("消去しました。")
                else:
                    print("元の問題の数字は消せません。")
            elif cmd == "hint":
                revealed = board.reveal_one()
                if revealed:
                    r, c, value = revealed
                    print(f"({r + 1}, {c + 1}) に {value} を入力しました。")
                else:
                    print("ヒントを出せるマスがありません。")
            elif cmd == "reset":
                board.reset()
                print("リセットしました。")
            elif cmd == "solve":
                board.current = [row[:] for row in board.solution]
                board.display()
                print("解答を表示しました。")
                break
            elif cmd == "quit":
                print("終了します。")
                break
            elif cmd == "help":
                print(commands)
            else:
                print("コマンドが正しくありません。help で一覧を表示できます。")
        except (ValueError, IndexError):
            print("入力が正しくありません。例: set 1 1 5")
            continue

        board.display()


def main() -> None:
    parser = argparse.ArgumentParser(description="Command line Sudoku generator and solver.")
    parser.add_argument("--clues", type=int, default=32, help="Number of clues to keep in the generated puzzle (17-81).")
    parser.add_argument("--seed", type=int, default=None, help="Random seed for reproducible puzzles.")
    parser.add_argument("--puzzle", type=str, default=None, help="81-character puzzle string to solve (0 or . for empty).")
    parser.add_argument("--solve-only", action="store_true", help="Solve the supplied puzzle and print the solution without starting a game.")
    args = parser.parse_args()

    if args.seed is not None:
        random.seed(args.seed)

    if args.puzzle:
        puzzle = parse_puzzle(args.puzzle)
        solution = solve_board([row[:] for row in puzzle])
        if solution is None:
            raise ValueError("このパズルには解がありません。")
        board = SudokuBoard(puzzle, solution)
        if args.solve_only:
            for row in solution:
                print(" ".join(str(v) for v in row))
            return
    else:
        puzzle, solution = generate_puzzle(args.clues)
        board = SudokuBoard(puzzle, solution)

    start_interactive(board)


if __name__ == "__main__":
    main()
