import sys
import os.path
from settings import *
from pygame_textinput import TextInputManager
from pygame_textinput import TextInputVisualizer


class SaveLevelPage:
    def __init__(self, start_map, goals_map, screen):
        self.start_map = start_map
        self.goals_map = goals_map
        self.screen = screen

        font = pygame.font.SysFont(None, 60)
        self.name_manager = TextInputManager(
            validator=level_name_validator,
            activated=True
        )
        self.name_input = TextInputVisualizer(manager=self.name_manager, font_object=font)

        self.title_text = font.render("Level Name: ", True, (0, 0, 0))
        self.title_rect = self.title_text.get_rect(center=(300, WINDOW_HEIGHT // 3))

    def save(self, file_name):
        with open(file_name, 'w') as file:
            for s in self.start_map:
                file.write(''.join(s) + '\n')
            file.write('\n')
            for s in self.goals_map:
                file.write(''.join(s) + '\n')

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                elif event.key == pygame.K_RETURN:
                    file_name = "Levels/" + self.name_input.value + ".txt"
                    if self.name_input.value != '' and not os.path.isfile(file_name):
                        self.save(file_name)
                        return False
        return True

    def draw(self):
        self.screen.fill(BACKGROUND_COLOR)
        self.screen.blit(self.title_text, self.title_rect)
        self.screen.blit(self.name_input.surface, (450, 300))
        pygame.display.update()

    def run(self):
        clock = pygame.time.Clock()
        while True:
            events = pygame.event.get()
            self.name_input.update(events)
            if not self.handle_events(events):
                return

            self.draw()
            clock.tick(FPS)
