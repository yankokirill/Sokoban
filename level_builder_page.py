import sys
from settings import *
from pygame_textinput import TextInputManager
from pygame_textinput import TextInputVisualizer
from level_builder import LevelBuilder


class LevelBuilderPage:
    def __init__(self,  screen):
        font = pygame.font.SysFont(None, 60)

        self.screen = screen

        self.height_manager = TextInputManager(
            validator=lambda size: size == '' or size.isdigit() and 0 < int(size) <= HEIGHT_BOUNDARY,
            activated=True
        )
        self.width_manager = TextInputManager(
            validator=lambda size: size == '' or size.isdigit() and 0 < int(size) <= WIDTH_BOUNDARY,
            activated=False
        )

        self.height_input = TextInputVisualizer(manager=self.height_manager, font_object=font)
        self.width_input = TextInputVisualizer(manager=self.width_manager, font_object=font)

        self.height_text = font.render("Height: ", True, (0, 0, 0))
        self.width_text = font.render("Width: ", True, (0, 0, 0))

        self.height_rect = self.height_text.get_rect(center=(300, WINDOW_HEIGHT // 3))
        self.width_rect = self.width_text.get_rect(center=(300, WINDOW_HEIGHT // 3 * 2))

    def draw_page(self):
        self.screen.fill(BACKGROUND_COLOR)
        self.screen.blit(self.height_text, self.height_rect)
        self.screen.blit(self.width_text, self.width_rect)

        self.screen.blit(self.height_input.surface, (450, 300))
        self.screen.blit(self.width_input.surface, (440, 620))

        pygame.display.update()

    def get_height(self):
        return 0 if len(self.height_manager.value) == 0 else int(self.height_manager.value)

    def get_width(self):
        return 0 if len(self.width_manager.value) == 0 else int(self.width_manager.value)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                if event.key == pygame.K_TAB:
                    self.height_manager.activated ^= True
                    self.width_manager.activated ^= True
                elif event.key == pygame.K_RETURN:
                    if self.get_height() >= 1 and self.get_width() >= 1:
                        LevelBuilder(self.get_height(), self.get_width(), self.screen).run()
                        return False
        return True

    def run(self):
        clock = pygame.time.Clock()
        while True:
            events = pygame.event.get()
            self.width_input.update(events)
            self.height_input.update(events)
            if not self.handle_events(events):
                return

            self.draw_page()
            clock.tick(FPS)
