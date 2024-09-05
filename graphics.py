from settings import *


def load_image(s, size):
    return pygame.transform.scale(pygame.image.load("Images/" + s), (size, size))


def transparent_copy(block):
    new_block = block.copy()
    new_block.set_alpha(BLOCK_ALPHA)
    return new_block


class ViewController:
    def __init__(self, surface, size=TILE_SIZE):
        self.surface = surface
        self.size = size
        self.floor = load_image("floor.png", size)
        self.wall = load_image("wall.png", size)
        self.light_box = load_image("light_box.png", size)
        self.dark_box = load_image("dark_box.png", size)
        self.goal = pygame.image.load("Images/goal.svg")

    def draw_floor(self, x, y):
        self.surface.blit(self.floor, (x, y))

    def draw_wall(self, x, y):
        self.surface.blit(self.wall, (x, y))

    def draw_border(self, x, y, direction):
        start_pos = x + border_shift_x[direction][0], y + border_shift_y[direction][0]
        end_pos = x + border_shift_x[direction][1], y + border_shift_y[direction][1]
        pygame.draw.line(self.surface, (0, 0, 0), start_pos, end_pos, BORDER_WIDTH)


class BoardController(ViewController):
    def __init__(self, surface, level, size=TILE_SIZE, level_builder=None):
        super().__init__(surface, size)
        self.enable_borders = True
        self.background_color = BACKGROUND_COLOR
        self.size = size
        self.level_builder = level_builder
        self.goal = pygame.transform.scale(self.goal, (GOAL_HEIGHT, GOAL_WIDTH))

        self.hero_stay = (
            load_image("Hero/left/stay_handless.png", size),
            load_image("Hero/right/stay_handless.png", size),
            load_image("Hero/up/stay_handless.png", size),
            load_image("Hero/down/stay_handless.png", size)
        )

        if level is None:
            self.goals_map = None
            self.boxes = None
            self.hero = None
            self.height = 0
            self.width = 0
            self.pixel_x = None
            self.pixel_y = None
            return

        self.goals_map = level.goals_map
        self.boxes = level.boxes
        self.hero = level.hero
        self.hero_stay = (
            load_image("Hero/left/stay_handless.png", size),
            load_image("Hero/right/stay_handless.png", size),
            load_image("Hero/up/stay_handless.png", size),
            load_image("Hero/down/stay_handless.png", size)
        )

        self.hero_move = (
            (load_image("Hero/left/go_handless_1.png", size),
             load_image("Hero/left/go_handless_2.png", size)),
            (load_image("Hero/right/go_handless_1.png", size),
             load_image("Hero/right/go_handless_2.png", size)),
            (load_image("Hero/up/go_handless_1.png", size),
             load_image("Hero/up/go_handless_2.png", size)),
            (load_image("Hero/down/go_handless_1.png", size),
             load_image("Hero/down/go_handless_2.png", size))
        )

        self.hero_push = (
            (load_image("Hero/left/go_hands_1.png", size),
             load_image("Hero/left/go_hands_2.png", size)),
            (load_image("Hero/right/go_hands_1.png", size),
             load_image("Hero/right/go_hands_2.png", size)),
            (load_image("Hero/up/go_hands_1.png", size),
             load_image("Hero/up/go_hands_2.png", size)),
            (load_image("Hero/down/go_hands_1.png", size),
             load_image("Hero/down/go_hands_2.png", size))
        )

        self.transparent_hero = transparent_copy(self.hero_stay[DOWN])
        self.transparent_wall = transparent_copy(self.wall)
        self.transparent_light_box = transparent_copy(self.light_box)
        self.transparent_dark_box = transparent_copy(self.dark_box)
        self.transparent_goal = transparent_copy(self.goal)

        self.height = len(self.goals_map)
        self.width = len(self.goals_map[0])

        draw_methods_dict = {
            HERO_SYM: self.draw_transparent_hero,
            WALL_SYM: self.draw_transparent_wall,
            BOX_SYM: self.draw_transparent_box,
            GOAL_SYM: self.draw_transparent_goal
        }
        self.draw_transparent_methods = tuple(
            [draw_methods_dict[symbol] for symbol in PALETTE_OPTIONS if symbol != TRASH_SYM]
        )

        self.pixel_x = self.calc_pixel_x()
        self.pixel_y = self.calc_pixel_y()

    def calc_pixel_x(self):
        map_width = self.width * self.size
        offset_x = (self.surface.get_size()[0] - map_width) // 2
        return [i * self.size + offset_x for i in range(self.width)]

    def calc_pixel_y(self):
        map_height = self.height * self.size
        offset_y = (self.surface.get_size()[1] - map_height) // 2
        return [i * self.size + offset_y for i in range(self.height)]

    def draw_transparent_hero(self, i, j):
        if self.level_builder.is_floor_or_goal(i, j):
            x, y = self.pixel_x[j], self.pixel_y[i]
            self.surface.blit(self.transparent_hero, (x, y))

    def draw_transparent_wall(self, i, j):
        if self.level_builder.is_floor(i, j):
            x, y = self.pixel_x[j], self.pixel_y[i]
            self.surface.blit(self.transparent_wall, (x, y))

    def draw_transparent_box(self, i, j):
        x, y = self.pixel_x[j], self.pixel_y[i]
        if self.goals_map[i][j] == GOAL_SYM:
            self.surface.blit(self.transparent_dark_box, (x, y))
        elif self.level_builder.start_map[i][j] == FLOOR_SYM:
            self.surface.blit(self.transparent_light_box, (x, y))

    def draw_transparent_goal(self, i, j):
        if self.goals_map[i][j] == FLOOR_SYM:
            x, y = self.pixel_x[j], self.pixel_y[i]
            self.surface.blit(self.transparent_goal, (x + GOAL_MARGIN_X, y + GOAL_MARGIN_Y))

    def draw_goal(self, x, y):
        x1, y1 = self.goal.get_size()
        self.surface.blit(self.goal, (x + (self.size - x1 + 1) // 2, y + (self.size - y1) // 2))

    def to_indices(self, pos):
        pix_x, pix_y = pos
        map_width = self.width * TILE_SIZE
        map_height = self.height * TILE_SIZE
        offset_x = (self.surface.get_size()[0] - map_width) // 2
        offset_y = (self.surface.get_size()[1] - map_height) // 2
        return (pix_y - offset_y) // TILE_SIZE, (pix_x - offset_x) // TILE_SIZE,

    def valid_indices(self, i, j):
        return 0 <= i < self.height and 0 <= j < self.width

    def is_wall(self, i, j, direction):
        i += dy[direction]
        j += dx[direction]
        return self.valid_indices(i, j) and self.goals_map[i][j] == WALL_SYM

    def draw_wall_border(self, i, j):
        x, y = self.pixel_x[j], self.pixel_y[i]
        for k in range(4):
            if not self.is_wall(i, j, k):
                self.draw_border(x, y, k)

    def draw_map(self):
        for i, y in enumerate(self.pixel_y):
            for j, x in enumerate(self.pixel_x):
                if self.goals_map[i][j] == FLOOR_SYM:
                    self.draw_floor(x, y)
                elif self.goals_map[i][j] == WALL_SYM:
                    self.draw_wall(x, y)
                elif self.goals_map[i][j] == GOAL_SYM:
                    self.draw_floor(x, y)
                    self.draw_goal(x, y)

        if self.enable_borders:
            for i in range(len(self.pixel_y)):
                for j in range(len(self.pixel_x)):
                    if self.goals_map[i][j] == WALL_SYM:
                        self.draw_wall_border(i, j)

    def draw_hero(self):
        direction = self.hero.direction ^ self.hero.is_moving_back
        x, y = self.hero.get_coordinates()
        x, y = self.pixel_x[x], self.pixel_y[y]
        shift = self.hero.delay * TILE_SIZE // DELAY
        x -= shift * dx[direction]
        y -= shift * dy[direction]

        if self.hero.is_pushing:
            self.surface.blit(self.hero_push[self.hero.direction][self.hero.delay // 7 % 2], (x, y))
        elif self.hero.is_moving:
            self.surface.blit(self.hero_move[self.hero.direction][self.hero.delay // 7 % 2], (x, y))
        else:
            self.surface.blit(self.hero_stay[self.hero.direction], (x, y))

    def draw_box(self, box):
        direction = self.hero.direction ^ self.hero.is_moving_back
        x, y = self.pixel_x[box.x], self.pixel_y[box.y]

        if box is self.hero.box_to_push:
            shift = self.hero.delay * TILE_SIZE // DELAY
            x -= shift * dx[direction]
            y -= shift * dy[direction]

        box_image = self.dark_box if box.achieved_goal else self.light_box
        self.surface.blit(box_image, (x, y))

    @staticmethod
    def is_suitable_selected_option(ind):
        return ind != -1 and PALETTE_OPTIONS[ind] != TRASH_SYM

    def handle_mouse(self):
        ind = self.level_builder.selected_option
        if not pygame.mouse.get_pressed()[0] and self.is_suitable_selected_option(ind):
            i, j = self.to_indices(pygame.mouse.get_pos())
            if self.valid_indices(i, j):
                self.draw_transparent_methods[ind](i, j)

    def draw_board(self):
        self.surface.fill(self.background_color)
        self.draw_map()
        for box in self.boxes:
            self.draw_box(box)
        if self.hero.path[0][0] > 0:
            self.draw_hero()

        if self.level_builder is not None:
            self.handle_mouse()

    def draw_level_image(self, surface, level):
        self.surface = surface
        self.height = level.height
        self.width = level.width
        self.boxes = level.boxes
        self.goals_map = level.goals_map
        self.hero = level.hero
        self.pixel_x = self.calc_pixel_x()
        self.pixel_y = self.calc_pixel_y()
        self.draw_board()


class PaletteController(ViewController):
    def __init__(self, surface):
        super().__init__(surface)
        self.hero_stay = pygame.image.load("Images/Hero/down/stay_handless.png")
        self.goal = pygame.transform.scale(self.goal, (GOAL_HEIGHT_PALETTE, GOAL_WIDTH_PALETTE))
        self.trash = pygame.transform.scale(pygame.image.load("Images/trash.svg"), (TRASH_SIZE, TRASH_SIZE))
        drawing_order_dict = {
            HERO_SYM: self.draw_hero,
            WALL_SYM: self.draw_wall_with_border,
            BOX_SYM: self.draw_box,
            GOAL_SYM: self.draw_goal,
            TRASH_SYM: self.draw_trash
        }
        self.drawing_order = tuple([drawing_order_dict[symbol] for symbol in PALETTE_OPTIONS])

    @staticmethod
    def valid_option(x):
        return 0 <= x < len(PALETTE_OPTIONS)

    @staticmethod
    def get_option(pos):
        pix_x, pix_y = pos
        palette_width = len(PALETTE_OPTIONS) * PALETTE_TILE_SIZE
        offset_x = (WINDOW_WIDTH - palette_width) // 2
        offset_y = WINDOW_HEIGHT - PALETTE_TILE_SIZE - PALETTE_MARGIN
        x, y = (pix_x - offset_x) // PALETTE_TILE_SIZE, (pix_y - offset_y) // PALETTE_TILE_SIZE
        if y == 0 and PaletteController.valid_option(x):
            return x
        else:
            return -1

    def draw_goal(self, x, y):
        self.surface.blit(self.goal, (x + GOAL_MARGIN_PALETTE_X, y + GOAL_MARGIN_PALETTE_Y))

    def draw_box(self, x, y):
        self.surface.blit(self.light_box, (x, y))

    def draw_hero(self, x, y):
        self.surface.blit(self.hero_stay, (x, y))

    def draw_trash(self, x, y):
        self.surface.blit(self.trash, (x, y))

    def draw_wall_with_border(self, x, y):
        self.draw_wall(x, y)
        for k in range(4):
            self.draw_border(x, y, k)

    def draw_palette(self):
        palette_width = len(PALETTE_OPTIONS) * PALETTE_TILE_SIZE
        margin = (PALETTE_TILE_SIZE - TILE_SIZE) // 2
        x = (self.surface.get_size()[0] - palette_width) // 2 + margin
        y = self.surface.get_size()[1] - PALETTE_TILE_SIZE - PALETTE_MARGIN + margin
        for draw in self.drawing_order:
            draw(x, y)
            x += PALETTE_TILE_SIZE
