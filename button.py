import pygame


class Button:
    def __init__(self, surface, text, x_pos, y_pos, height=70, width=250, font_size=50):
        self.surface = surface
        self.text = text
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.height = height
        self.width = width
        self.font = pygame.font.SysFont(None, font_size)
        coordinates = (x_pos - width // 2, y_pos - height // 2)
        self.button_rect = pygame.rect.Rect(coordinates, (self.width, self.height))
        self.is_pressed = False

    def draw(self):
        button_text = self.font.render(self.text, True, 'black')
        button_text_rect = button_text.get_rect(center=(self.x_pos, self.y_pos))
        color = 'dark gray' if self.is_pressed else 'light gray'
        pygame.draw.rect(self.surface, color, self.button_rect, 0, 5)
        pygame.draw.rect(self.surface, 'black', self.button_rect, 2, 5)
        self.surface.blit(button_text, button_text_rect)

    def pressed(self, events):
        mouse_pos = pygame.mouse.get_pos()
        if self.button_rect.collidepoint(mouse_pos):
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.is_pressed = True
                elif self.is_pressed and event.type == pygame.MOUSEBUTTONUP:
                    self.is_pressed = False
                    return True
        else:
            self.is_pressed = False
        return False
