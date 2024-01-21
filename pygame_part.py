import pygame
import threading
import pygame
from checkers.game import Game
from minimax.algorithm import minimax
from checkers import board_parameters
from checkers.constants import *

# Using getter functions
WIDTH = board_parameters.get_width()
HEIGHT = board_parameters.get_height()
ROWS, COLS = board_parameters.get_rows(), board_parameters.get_cols()
SQUARE_SIZE = board_parameters.get_square_size()



FPS = 60

def get_row_col_from_mouse(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col

def run_pygame():
    WIN = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Checkers')
    run = True
    clock = pygame.time.Clock()
    game = Game(WIN)

    while run:
        clock.tick(FPS)

        if game.turn == WHITE:
            value, new_board = minimax(game.get_board(), 4, True, game, -100, 100)
            game.ai_move(new_board)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = get_row_col_from_mouse(pos)
                game.select(row, col)

        game.update()

    pygame.quit()

# This function will start the Pygame loop in a new thread
def start_pygame_thread(mode = None, color=None, difficulty=None, board_size=None):
    print(mode, color, difficulty, board_size)
    if mode == "player_vs_computer":
        print(1, 1)
        if board_size == "8x8":
            board_parameters.set_rows_cols(8, 8)
        elif board_size == "10x10":
            board_parameters.set_rows_cols(10, 10)
        else:
            board_parameters.set_rows_cols(12, 12)

    if mode == "player_vs_player":
        if board_size == "8x8":
            board_parameters.set_rows_cols(8, 8)
        elif board_size == "10x10":
            board_parameters.set_rows_cols(10, 10)
        else:
            board_parameters.set_rows_cols(12, 12)
    pygame_thread = threading.Thread(target=run_pygame)
    pygame_thread.daemon = True
    pygame_thread.start()