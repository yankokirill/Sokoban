from settings import *


class Box:
    def __init__(self, success, x, y):
        self.achieved_goal = success
        self.x = x
        self.y = y

    def get_coordinates(self):
        return self.x, self.y

    def move(self, direction):
        self.x += dx[direction]
        self.y += dy[direction]

    def update(self, goals_map):
        self.achieved_goal = goals_map[self.y][self.x] == GOAL_SYM
