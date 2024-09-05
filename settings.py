import pygame


FPS = 60
DELAY = 20
TILE_SIZE = 56
PREVIEW_TILE_SIZE = 11
PALETTE_TILE_SIZE = 70
PALETTE_MARGIN = 20

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 960

BACKGROUND_COLOR = (255, 255, 255)

PALETTE_HERO_RADIUS = 2 * PALETTE_TILE_SIZE // 5

GOAL_HEIGHT = 26
GOAL_WIDTH = 24
GOAL_MARGIN_X = (TILE_SIZE - GOAL_WIDTH) // 2 - 1
GOAL_MARGIN_Y = (TILE_SIZE - GOAL_HEIGHT) // 2 + 1

GOAL_HEIGHT_PALETTE = 40
GOAL_WIDTH_PALETTE = 36
GOAL_MARGIN_PALETTE_X = (TILE_SIZE - GOAL_WIDTH_PALETTE) // 2 + 2
GOAL_MARGIN_PALETTE_Y = (TILE_SIZE - GOAL_HEIGHT_PALETTE) // 2

TRASH_SIZE = 50

HERO_SYM = 'H'
BOX_SYM = '*'
WALL_SYM = '#'
GOAL_SYM = 'X'
TRASH_SYM = '0'
FLOOR_SYM = ' '

PALETTE_OPTIONS = (HERO_SYM, WALL_SYM, BOX_SYM, GOAL_SYM, TRASH_SYM)

direction_key = (pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN)

LEFT = 0
RIGHT = 1
UP = 2
DOWN = 3

dx = (-1, 1, 0, 0)
dy = (0, 0, -1, 1)
dxy = ((-1, 0), (1, 0), (0, -1), (0, 1))


BLOCK_ALPHA = 128
BORDER_WIDTH = 2
border_shift_x = ((0, 0), (TILE_SIZE - BORDER_WIDTH, TILE_SIZE - BORDER_WIDTH),
                  (0, TILE_SIZE - 1), (0, TILE_SIZE - 1))
border_shift_y = ((0, TILE_SIZE), (0, TILE_SIZE),
                  (0, 0), (TILE_SIZE, TILE_SIZE))

HEIGHT_BOUNDARY = 11
WIDTH_BOUNDARY = 20
LEVEL_NAME_LEN = 12


def is_correct_sym(c):
    return ord('0') <= ord(c) <= ord('9') or ord('a') <= ord(c) <= ord('z') or ord('A') <= ord(c) <= ord('Z')


def level_name_validator(name):
    return len(name) <= LEVEL_NAME_LEN and all(is_correct_sym(c) for c in name)
