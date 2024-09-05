import sys
import os
from settings import *
from game import start_game
from graphics import BoardController
from level import Level


def open_level(file):
    with open(file, 'r') as f:
        s = [line.strip() for line in f]
    start_map = s[:len(s) // 2]
    goals_map = s[len(s) // 2 + 1:]
    return start_map, goals_map


class LevelSelectorItem:
    def __init__(self, filename, pos, controller):
        self.pos = pos
        image_width = WINDOW_WIDTH // 5 + 20
        image_height = WINDOW_HEIGHT // 5 - 1
        text_height = 30
        self.surface = pygame.Surface((image_width, image_height + text_height))
        self.surface.fill(BACKGROUND_COLOR)
        image_surface = self.surface.subsurface(pygame.Rect(0, 0, image_width, image_height))

        self.maps = open_level(os.path.join("Levels", filename))
        self.level = Level(self.maps[0], self.maps[1])
        controller.draw_level_image(image_surface, self.level)

        border_rect = image_surface.get_rect().inflate(-10, -10)
        pygame.draw.rect(image_surface, (0, 0, 0), border_rect, width=4)

        font = pygame.font.SysFont(None, 40)
        level_name = os.path.splitext(filename)[0]
        self.level_name_text = font.render(level_name, True, (37, 50, 33))
        self.level_name_rect = self.level_name_text.get_rect(center=(image_width // 2, image_height + text_height // 2))
        self.surface.blit(self.level_name_text, self.level_name_rect)

    def handle_click(self, pos):
        rect = self.surface.get_rect()
        rect.update(self.pos, rect.size)
        return rect.collidepoint(pos)


class LevelPage:
    def __init__(self, files, controller):
        start_x = 50
        start_y = 140

        margin_x = 300
        margin_y = 250

        count = 4
        self.levels = []
        for i, file in enumerate(files):
            pos = (start_x + margin_x * (i % count), start_y + margin_y * (i // count))
            self.levels.append(LevelSelectorItem(file, pos, controller))

    def handle_click(self, surface, pos):
        for item in self.levels:
            if item.handle_click(pos):
                start_game(item.maps, surface)

    def draw(self, screen):
        for level in self.levels:
            screen.blit(level.surface, level.pos)


class PageSelectButton:
    def __init__(self, num, x, y, radius):
        self.is_selected = False
        self.page_number = num
        self.x = x
        self.y = y
        self.radius = radius

    def handle_click(self, pos):
        x1, y1 = pos
        if (self.x - x1) ** 2 + (self.y - y1) ** 2 <= self.radius ** 2:
            self.is_selected = True
            return True
        return False

    def draw(self, surface):
        color = 'dark gray' if self.is_selected else 'white'
        pos = (self.x, self.y)
        pygame.draw.circle(surface, color, pos, self.radius)
        pygame.draw.circle(surface, 'black', pos, self.radius, 2)

        font = pygame.font.SysFont(None, 20)
        text = font.render(str(self.page_number + 1), True, 'black')
        text_rect = text.get_rect(center=pos)
        surface.blit(text, text_rect)


class LevelPageNavigator:
    def __init__(self, count):
        radius = 20
        margin = 10
        width = (2 * radius + margin) * count - margin
        x = (WINDOW_WIDTH - width) // 2 + radius
        y = WINDOW_HEIGHT - 40
        self.buttons = []
        for i in range(count):
            self.buttons.append(PageSelectButton(i, x, y, radius))
            x += margin + 2 * radius
        self.buttons[0].is_selected = True

    def handle_click(self, pos):
        for button in self.buttons:
            if button.handle_click(pos):
                return button.page_number
        return -1

    def draw(self, surface):
        for button in self.buttons:
            button.draw(surface)


class SelectLevelPage:
    def __init__(self, screen):
        self.screen = screen
        self.controller = BoardController(None, None, PREVIEW_TILE_SIZE)
        self.controller.enable_borders = False
        self.controller.background_color = 'light gray'
        self.controller.goal = pygame.transform.scale(self.controller.goal, (6, 5))

        font = pygame.font.SysFont(None, 70)
        self.title_text = font.render("Select level", True, (0, 0, 0))
        self.title_rect = self.title_text.get_rect(center=(WINDOW_WIDTH // 2, 80))

        self.files = os.listdir("Levels")
        self.page_size = 12
        page_count = (len(self.files) + self.page_size - 1) // self.page_size
        self.pages = page_count * [None]
        self.selected_page = 0
        self.pages[self.selected_page] = LevelPage(self.files[:self.page_size], self.controller)
        self.page_navigator = LevelPageNavigator(page_count)

    def select_new_page(self, ind):
        if ind != -1 and ind != self.selected_page:
            self.page_navigator.buttons[self.selected_page].is_selected = False
            self.selected_page = ind
            if self.pages[ind] is None:
                page_files = self.files[ind * self.page_size: (ind + 1) * self.page_size]
                self.pages[ind] = LevelPage(page_files, self.controller)

    def draw(self):
        self.screen.fill(BACKGROUND_COLOR)
        self.screen.blit(self.title_text, self.title_rect)
        self.pages[self.selected_page].draw(self.screen)
        self.page_navigator.draw(self.screen)
        pygame.display.update()

    def run(self):
        clock = pygame.time.Clock()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    self.select_new_page(self.page_navigator.handle_click(pos))
                    self.pages[self.selected_page].handle_click(self.screen, pos)

            self.draw()
            clock.tick(FPS)
