import sys
from settings import *
from level import Level
from graphics import BoardController


class Game:
    def __init__(self, level, screen):
        self.level = level
        self.hero = level.hero
        self.board_controller = BoardController(screen, level)
        self.clock = pygame.time.Clock()

    def run(self):
        while True:
            if not self.hero.is_pushing and self.level.is_complete():
                return True
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return True
                    elif event.key == pygame.K_SPACE:
                        return False

            keys = pygame.key.get_pressed()
            if self.hero.is_pushing:
                self.hero.update_push()
            elif self.hero.is_moving:
                self.hero.update_move()
            elif keys[pygame.K_BACKSPACE]:
                self.hero.step_back()
            else:
                for i, key in enumerate(direction_key):
                    if keys[key]:
                        self.hero.move(i)
                        break

            self.board_controller.draw_board()
            pygame.display.update()
            self.clock.tick(FPS)

    def restart(self, level):
        self.level = level
        self.hero = level.hero
        self.board_controller = BoardController(self.board_controller.surface, level)


def start_game(maps, screen):
    start_map, goals_map = maps
    game = Game(Level(start_map, goals_map), screen)

    while not game.run():
        game.restart(Level(start_map, goals_map))

    return game.level.is_complete()
