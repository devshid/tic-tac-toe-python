import math

# max is player who want maximum point
MAX_MOVES = []
# min is computer who want to reduce max's point
MIN_MOVES = []


class Board:

    def __init__(self, max_moves, min_moves):
        self.max_moves = max_moves
        self.min_moves = min_moves
        self.blank_moves = self.get_blank_moves()
        self.game_over = self.is_game_over()

    def get_blank_moves(self):
        blank_moves = list()
        for row in range(3):
            for col in range(3):
                if (row, col) not in self.min_moves and (row, col) not in self.max_moves:
                    blank_moves.append((row, col))
        return blank_moves

    def row_match(self, moves):
        row = {}
        for move in moves:
            if str(move[0]) in row.keys():
                row[str(move[0])] += 1
            else:
                row[str(move[0])] = 1
        for r in row.values():
            if r >= 3:
                return True
        return False

    def col_match(self, moves):
        col = {}
        for move in moves:
            if str(move[1]) in col.keys():
                col[str(move[1])] += 1
            else:
                col[str(move[1])] = 1
        for r in col.values():
            if r >= 3:
                return True
        return False

    def make_number(self, set):
        return set[0] * 10 + set[1]

    def dia_match(self, moves):
        times = 0
        if (0, 0) in moves and (1, 1) in moves and (2, 2) in moves:
            return True
        if (0, 2) in moves and (1, 1) in moves and (2, 0) in moves:
            return True
        return False

    def total_moves(self):
        return len(self.max_moves) + len(self.min_moves)

    def is_draw(self):
        if len(self.blank_moves) == 0 and not self.is_min_win() and not self.is_max_win():
            return True
        else:
            return False

    def is_min_win(self):
        if self.row_match(self.min_moves) or self.col_match(self.min_moves) or self.dia_match(self.min_moves):
            return True
        else:
            return False

    def is_max_win(self):
        if self.row_match(self.max_moves) or self.col_match(self.max_moves) or self.dia_match(self.max_moves):
            return True
        else:
            return False

    def is_game_over(self):
        if self.is_min_win() or self.is_max_win() or self.is_draw():
            return True
        else:
            return False


def min_max(max, min, new_move, isMax):
    if isMax:
        max.append(new_move)
        isMax = False
    else:
        isMax = True
        min.append(new_move)
    brd = Board(max, min)
    if brd.is_max_win():
        return 1
    elif brd.is_min_win():
        return -1
    elif brd.is_draw():
        return 0
    else:
        blank_moves = brd.blank_moves
        if isMax:
            previous_value = -math.inf
        else:
            previous_value = math.inf
        for bm in blank_moves:
            value = min_max(max.copy(), min.copy(), bm, isMax)
            if isMax:
                if value == 1:
                    return value
                elif value > previous_value:
                    previous_value = value
            else:
                if value == -1:
                    return value
                elif value < previous_value:
                    previous_value = value
    return previous_value


def best_move(maxMoves, minMoves):
    brd = Board(maxMoves, minMoves)
    blank_moves = brd.blank_moves
    pre_value = math.inf
    best = set()
    for bm in blank_moves:
        value = min_max(maxMoves.copy(), minMoves.copy(), bm, False)
        if value == -1:
            return bm
        elif value < pre_value:
            best = bm
            pre_value = value
    return best


def main_game():
    running = True
    while running:
        print('max move --- ')
        row = int(input('enter row : '))
        col = int(input('enter col : '))
        max_move = (row, col)
        MAX_MOVES.append(max_move)
        if Board(MAX_MOVES, MIN_MOVES).is_max_win():
            print('max win')
            running = False
        else:
            min_move = best_move(MAX_MOVES.copy(), MIN_MOVES.copy())
            print('min move :', min_move)
            MIN_MOVES.append(min_move)
            if Board(MAX_MOVES, MIN_MOVES).is_min_win():
                print('min win')
                running = False
        if Board(MAX_MOVES, MIN_MOVES).is_draw():
            print('match draw')
            running = False


if __name__ == '__main__':
    main_game()
