from level import Level
from hero import Hero
from box import *
from graphics import BoardController
from graphics import PaletteController
from game import start_game
from save_level_page import SaveLevelPage
from input_handler import InputHandler


def generate_map(height, width):
    s = (width + 2) * [WALL_SYM]
    t = [WALL_SYM] + width * [FLOOR_SYM] + [WALL_SYM]
    return [s] + [t[:] for _ in range(height)] + [s]


class LevelBuilder:
    def __init__(self, height, width, screen):
        self.clock = pygame.time.Clock()
        self.surface = screen
        self.height = height
        self.width = width
        
        self.start_map = generate_map(height, width)
        self.goals_map = generate_map(height, width)
        self.level = Level(self.start_map, self.goals_map)
        self.hero = Hero(0, 0, self.level)
        self.level.hero = self.hero

        self.goal_count = 0
        self.selected_option = -1
        self.building_methods = (
            self.set_hero_position,
            self.add_wall,
            self.add_box,
            self.add_goal,
            self.delete_block
        )

        self.input_handler = InputHandler(self)
        self.board_controller = BoardController(screen, self.level, TILE_SIZE, self)
        self.palette_controller = PaletteController(screen)

    def reset(self):
        self.start_map = generate_map(self.height, self.width)
        self.goals_map = generate_map(self.height, self.width)
        self.level = Level(self.start_map, self.goals_map)
        self.hero = Hero(0, 0, self.level)
        self.level.hero = self.hero

        self.selected_option = -1
        self.goal_count = 0

        self.board_controller = BoardController(self.board_controller.surface, self.level)

    def valid_indices(self, i, j):
        return 1 <= i <= self.height and 1 <= j <= self.width

    def is_floor(self, i, j):
        return self.valid_indices(i, j) and self.goals_map[i][j] == self.start_map[i][j] == FLOOR_SYM

    def is_floor_or_box(self, i, j):
        return self.valid_indices(i, j) and self.goals_map[i][j] == FLOOR_SYM

    def is_floor_or_goal(self, i, j):
        return self.valid_indices(i, j) and self.start_map[i][j] == FLOOR_SYM

    def add_wall(self, i, j):
        if self.is_floor(i, j):
            self.goals_map[i][j] = WALL_SYM
            self.start_map[i][j] = WALL_SYM

    def find_box(self, i, j):
        k = 0
        while self.level.boxes[k].get_coordinates() != (j, i):
            k += 1
        return self.level.boxes[k]

    def add_goal(self, i, j):
        if self.is_floor_or_box(i, j):
            self.goals_map[i][j] = GOAL_SYM
            self.goal_count += 1
            if self.start_map[i][j] == BOX_SYM:
                self.find_box(i, j).achieved_goal = True

    def add_box(self, i, j):
        if self.is_floor_or_goal(i, j):
            self.start_map[i][j] = BOX_SYM
            self.level.boxes.append(Box(self.goals_map[i][j] == GOAL_SYM, j, i))

    def hero_is_set(self):
        return self.hero.path[0][0] > 0

    def set_hero_position(self, i, j):
        if self.is_floor_or_goal(i, j):
            x, y = self.hero.path[0]
            if self.hero_is_set():
                self.start_map[y][x] = FLOOR_SYM
            self.start_map[i][j] = HERO_SYM
            self.hero.path[0] = (j, i)

    def erase_box(self, i, j):
        k = 0
        while self.level.boxes[k].get_coordinates() != (j, i):
            k += 1
        self.level.boxes.pop(k)

    def delete_block(self, i, j):
        if self.valid_indices(i, j):
            if self.start_map[i][j] == BOX_SYM:
                self.erase_box(i, j)
            self.goal_count -= self.goals_map[i][j] == GOAL_SYM
            if self.start_map[i][j] == HERO_SYM:
                self.hero.path[0] = (0, 0)
            self.start_map[i][j] = FLOOR_SYM
            self.goals_map[i][j] = FLOOR_SYM

    def can_build(self):
        return len(self.level.boxes) == self.goal_count > 0 and not self.level.is_complete() and self.hero_is_set()

    def run(self):
        while True:
            if not self.input_handler.handle_events():
                return

            self.board_controller.draw_board()
            self.palette_controller.draw_palette()
            pygame.display.update()
            self.clock.tick(FPS)

    def build(self):
        if not self.can_build():
            return False
        if start_game((self.start_map, self.goals_map), self.surface):
            SaveLevelPage(self.start_map, self.goals_map, self.surface).run()
            return True
        return False
