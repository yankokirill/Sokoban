import sys
from settings import *
from select_level_page import SelectLevelPage
from level_builder_page import LevelBuilderPage
from button import Button


class MainMenu:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Sokoban")
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        font = pygame.font.SysFont(None, 70)
        self.title_text = font.render("Sokoban", True, (0, 0, 0))
        self.title_rect = self.title_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 3))
        self.play_button = Button(self.screen, "Play", WINDOW_WIDTH // 2, WINDOW_HEIGHT // 3 + 110)
        self.build_button = Button(self.screen, "Build", WINDOW_WIDTH // 2, WINDOW_HEIGHT // 3 + 220)

    def handle_events(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
        if self.play_button.pressed(events):
            SelectLevelPage(self.screen).run()
        elif self.build_button.pressed(events):
            LevelBuilderPage(self.screen).run()

    def draw_menu(self):
        self.screen.fill(BACKGROUND_COLOR)
        self.screen.blit(self.title_text, self.title_rect)
        self.play_button.draw()
        self.build_button.draw()

    def run(self):
        clock = pygame.time.Clock()
        while True:
            self.handle_events()
            self.draw_menu()
            pygame.display.update()
            clock.tick(FPS)


if __name__ == '__main__':
    menu = MainMenu()
    menu.run()
