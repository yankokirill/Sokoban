from hero import Hero
from box import Box
from settings import *


class Level:
    def __init__(self, start_map, goals_map):
        self.goals_map = goals_map
        self.height = len(goals_map)
        self.width = len(goals_map[0])

        self.boxes = []
        self.boxes_map = [[None for _ in range(self.width)] for _ in range(self.height)]
        self.hero = None

        for i in range(self.height):
            for j in range(self.width):
                if start_map[i][j] == BOX_SYM:
                    self.boxes.append(Box(self.goals_map[i][j] == GOAL_SYM, j, i))
                    self.boxes_map[i][j] = self.boxes[-1]
                elif start_map[i][j] == HERO_SYM:
                    self.hero = Hero(j, i, self)

    def is_complete(self):
        for box in self.boxes:
            if not box.achieved_goal:
                return False
        return True
