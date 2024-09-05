import pygame
from settings import *
from box import *


class Hero:
    def __init__(self, x, y, level):
        self.path = [(x, y)]
        self.pushed_box = [False]
        self.direction = DOWN
        self.level = level

        self.is_moving = False
        self.is_moving_back = False
        self.is_pushing = False
        self.box_to_push = None
        self.delay = 0

    def get_coordinates(self):
        return self.path[-1]

    def push_box(self, x, y, direction):
        x1, y1 = x + dx[direction], y + dy[direction]
        self.box_to_push = self.level.boxes_map[y][x]
        self.box_to_push.move(direction)
        self.box_to_push.update(self.level.goals_map)
        self.level.boxes_map[y1][x1] = self.box_to_push
        self.level.boxes_map[y][x] = None
        self.is_pushing = True
        self.delay = DELAY

    def move(self, direction):
        self.direction = direction
        x, y = self.path[-1]
        x1 = x + dx[direction]
        y1 = y + dy[direction]
        x2 = x1 + dx[direction]
        y2 = y1 + dy[direction]

        if self.level.goals_map[y1][x1] != WALL_SYM:
            to_field = self.level.boxes_map[y1][x1]
            if to_field is None:
                self.path.append((x1, y1))
                self.pushed_box.append(False)
                self.is_moving = True
                self.delay = DELAY
            elif self.level.goals_map[y2][x2] != WALL_SYM and self.level.boxes_map[y2][x2] is None:
                self.push_box(x1, y1, direction)
                self.path.append((x1, y1))
                self.pushed_box.append(True)

    def step_back(self):
        if len(self.path) > 1:
            x, y = self.path[-1]
            x1, y1 = self.path[-2]
            self.direction = dxy.index((x - x1, y - y1))

            if self.pushed_box[-1]:
                self.push_box(x + (x - x1), y + (y - y1), self.direction ^ 1)
                self.is_moving_back = True
            else:
                self.is_moving = True
                self.is_moving_back = True
                self.delay = DELAY

            self.path.pop()
            self.pushed_box.pop()

    def update_push(self):
        self.delay -= 1
        if self.delay == 0:
            self.is_pushing = False
            self.is_moving_back = False
            self.box_to_push = None

    def update_move(self):
        self.delay -= 1
        if self.delay == 0:
            self.is_moving = False
            self.is_moving_back = False
