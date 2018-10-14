import numpy as np
from curses import *

class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = np.full((self.height, self.width), None)
        self.open_fields = self.width * self.height

    def add(self, col, player):
        for y in range(self.height):
            inv = self.height - 1 - y
            if self.grid[inv][col] == None:
                self.grid[inv][col] = player
                self.open_fields -= 1
                return True
        return False

    def is_full(self):
        if self.open_fields == 0:
            return True
        return False

    def player_won(self, player):
        seq = np.full((4), player)

        for row in self.grid:
            if contains_seq(row, seq):
                return True

        for row in self.grid.T:
            if contains_seq(row, seq):
                return True

        for row in range(1 - self.height, self.width):
            if contains_seq(self.grid.diagonal(row), seq):
                return True

        for row in range(- self.height, self.width - 1):
            if contains_seq(np.rot90(self.grid).diagonal(row), seq):
                return True

        return False

class Game:
    def __init__(self, width, height):
        self.board = Board(width, height)
        self.player = 0
        self.winner = None

    def start(self):
        cursor = 0
        while not self.board.is_full():
            stdscr.clear()
            self.show_board()
            stdscr.addstr(self.board.height, cursor * 2 + 1, "^")
            key = stdscr.getch()
            if key == KEY_RIGHT:
                cursor += 1
            if key == KEY_LEFT:
                cursor -= 1
            if key == 10:
                if self.board.add(cursor, self.player):
                    if self.board.player_won(self.player):
                        self.winner = self.player
                        break
                    self.switch_players()
            cursor %= self.board.width

        stdscr.clear()
        self.show_board()

        messages = {
            None: "It's a tie.",
            0: "Player 1 won!",
            1: "Player 2 won!"
        }

        stdscr.addstr(self.board.height, 0, messages[self.winner])
        stdscr.addstr(self.board.height + 1, 0, "Press ESC to leave . . .")

        while True:
            if stdscr.getch() == 27:
                break

    def switch_players(self):
        if self.player == 0:
            self.player = 1
        else:
            self.player = 0

    def show_board(self):
        for row in range(self.board.height):
            for col in range(self.board.width + 1):
                stdscr.addstr(row, col * 2, "|")

        for row_num, row in enumerate(self.board.grid):
            for col_num, char in enumerate(row):
                if char == 0:
                    stdscr.addstr(row_num, col_num * 2 + 1, "X", color_pair(1))
                elif char == 1:
                    stdscr.addstr(row_num, col_num * 2 + 1, "O", color_pair(2))

def contains_seq(a, b):
    for offset in range(len(a)):
        if np.array_equal(a[offset:offset + len(b)], b):
            return True
    return False

if __name__ == "__main__":
    stdscr = initscr()
    noecho()
    cbreak()
    stdscr.keypad(True)
    curs_set(0)

    start_color()
    init_pair(1, COLOR_RED, COLOR_BLACK)
    init_pair(2, COLOR_GREEN, COLOR_BLACK)

    my_game = Game(7, 6)

    my_game.start()
