import pygame
import math

# max is player who want maximum point
MAX_MOVES = []
# min is computer who want to reduce max's point
MIN_MOVES = []

# variables
grid = [[None, None, None], [None, None, None], [None, None, None]]
screen_width = 400
screen_height = 400
line_width = 5
margin = 10
game_window_width = screen_width - margin * 2
game_window_height = screen_height - margin * 2
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)
xMark = 'X'
oMark = 'O'


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
                if value > previous_value:
                    previous_value = value
            else:
                if value < previous_value:
                    previous_value = value
    return previous_value


def best_move(maxMoves, minMoves):
    brd = Board(maxMoves, minMoves)
    blank_moves = brd.blank_moves
    pre_value = math.inf
    best = set()
    for bm in blank_moves:
        value = min_max(maxMoves.copy(), minMoves.copy(), bm, False)
        if value < pre_value:
            best = bm
            pre_value = value
    return best


def main_game(row, col):
    max_move = (row, col)
    MAX_MOVES.append(max_move)
    brd=Board(MAX_MOVES, MIN_MOVES)
    if not brd.is_max_win() and not brd.is_draw():
        min_move = best_move(MAX_MOVES.copy(), MIN_MOVES.copy())
        MIN_MOVES.append(min_move)
        grid[min_move[0]][min_move[1]] = oMark


def draw_line(screen):
    # horizontal line
    pygame.draw.line(screen, black, (margin, game_window_height // 3 + margin),
                     (screen_width - margin, game_window_height // 3 + margin), line_width)
    pygame.draw.line(screen, black, (margin, margin + game_window_height // 3 * 2),
                     (screen_width - margin, margin + game_window_height // 3 * 2), line_width)

    # vertical lines
    pygame.draw.line(screen, black, (game_window_width // 3 + margin, margin),
                     (game_window_width // 3 + margin, screen_height - margin), line_width)
    pygame.draw.line(screen, black, (game_window_width // 3 * 2 + margin, margin),
                     (game_window_width // 3 * 2 + margin, screen_height - margin), line_width)


def click_mapping(pos):
    # row calculation
    if pos[1] < game_window_height // 3:
        row = 0
    elif pos[1] > game_window_height // 3 and pos[1] < game_window_height // 3 * 2:
        row = 1
    elif pos[1] > game_window_height // 3 * 2:
        row = 2

    # column calculation
    if pos[0] < game_window_width // 3:
        col = 0
    elif pos[0] > game_window_width // 3 and pos[0] < game_window_width // 3 * 2:
        col = 1
    elif pos[0] > game_window_width // 3 * 2:
        col = 2

    return row, col


def text_printing_pos(row, col):
    return margin + game_window_width // 3 * col + 32, margin + game_window_height // 3 * row + 5


def game_loop():
    fps = 30
    running = True
    pygame.init()

    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption('tic-tac-toe')
    clock = pygame.time.Clock()

    font = pygame.font.SysFont('ubuntumono', 120, False, False)
    winFont=pygame.font.SysFont('ubuntumono', 80, False, False)
    xText = font.render(xMark, True, blue)
    oText = font.render(oMark, True, green)
    maxWin = winFont.render('max win', True, red)
    minWin = winFont.render('min win', True, red)
    drawText = winFont.render('  draw', True, red)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                brd = Board(MAX_MOVES, MIN_MOVES)
                if event.button == 1 and not brd.is_min_win() and not brd.is_max_win() and not brd.is_draw():
                    row, col = click_mapping(event.pos)
                    grid[row][col] = xMark
                    main_game(row, col)

        screen.fill(white)
        draw_line(screen)
        brd = Board(MAX_MOVES, MIN_MOVES)
        for row in range(len(grid)):
            for col in range(len(grid[0])):
                if grid[row][col] == xMark:
                    screen.blit(xText, (text_printing_pos(row, col)))
                elif grid[row][col] == oMark:
                    screen.blit(oText, (text_printing_pos(row, col)))

        if brd.is_min_win():
            screen.blit(minWin, (screen_width * .1, screen_height * .4))
        elif brd.is_max_win():
            screen.blit(maxWin, (screen_width * .1, screen_height * .4))
        elif brd.is_draw():
            screen.blit(drawText, (screen_width * .1, screen_height * .4))
        pygame.display.flip()
        clock.tick(fps)


game_loop()
pygame.quit()
