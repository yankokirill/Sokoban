import pygame
import sys
from graphics import PaletteController


class InputHandler:
    def __init__(self, level_builder):
        self.level_builder = level_builder

    def set_new_option(self):
        option = PaletteController.get_option(pygame.mouse.get_pos())
        if option != -1:
            self.level_builder.selected_option = option

    def handle_mouse(self):
        if pygame.mouse.get_pressed()[0] and self.level_builder.selected_option != -1:
            i, j = self.level_builder.board_controller.to_indices(pygame.mouse.get_pos())
            self.level_builder.building_methods[self.level_builder.selected_option](i, j)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                elif event.key == pygame.K_RETURN and self.level_builder.build():
                    return False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.set_new_option()
        self.handle_mouse()
        return True
