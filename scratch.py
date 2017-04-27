#!python3
# -*- coding:utf-8 -*-

import random
import pprint

game_pane_x_size, game_pane_y_size = 8, 8
game_pane_size = game_pane_x_size * game_pane_y_size
gem_types = ['A', 'B', 'C', 'D', 'E', 'F']
blank = 0


class game_pane:

    def __init__(self, gem_types, blank, game_pane_x_size, game_pane_y_size):
        self.gem_types = gem_types
        self.blank = blank
        self.game_pane_x_size = game_pane_x_size
        self.game_pane_y_size = game_pane_y_size
        self.pane = self.__new_game_pane()

    def __new_game_pane(self):
        # randomly generate a game pane
        return [[random.choice(self.gem_types) for i in range(self.game_pane_y_size)] for j in range(self.game_pane_x_size)]

    # The Game Pane is designed like this
    # [[2, 4, 1, 1, 1, 3, 3, 1],
    #  [3, 3, 4, 4, 1, 1, 4, 3],
    #  [4, 4, 1, 2, 3, 4, 2, 3],
    #  [4, 3, 2, 2, 4, 1, 1, 1],
    #  [2, 3, 4, 4, 2, 3, 4, 4],
    #  [4, 4, 4, 3, 2, 2, 2, 4],
    #  [2, 1, 4, 4, 4, 3, 4, 3],
    #  [2, 3, 4, 3, 4, 4, 3, 3]]

    def print_current_pane(self):
        pprint.pprint(self.pane)
        return 0

    def __check_stage(self, pane=None):
        # Check the current game pane to see if there are any gems that should be cleared.
        # Returns a set, which contains tuples of coordinates of gems that should be cleared.
        # If no gem needs to be cleared, returns an empty set.
        if not pane:
            pane = self.pane
        gems_to_clear = set()
        # Check column (y) direction
        for x in range(0, self.game_pane_x_size):
            for y in range(0, self.game_pane_y_size - 2):
                if pane[x][y] == pane[x][y + 1] == pane[x][y + 2]:
                    gems_to_clear = gems_to_clear.union(
                        {(x, y), (x, y + 1), (x, y + 2)})
        # Check line (x) direction
        for x in range(0, self.game_pane_x_size - 2):
            for y in range(0, self.game_pane_y_size):
                if pane[x][y] == pane[x + 1][y] == pane[x + 2][y]:
                    gems_to_clear = gems_to_clear.union(
                        {(x, y), (x + 1, y), (x + 2, y)})
        return gems_to_clear

    def __gem_fall_algo(self, gem_column):
        # Make gems in gem_column to fall
        new_column = [self.blank for _ in range(len(gem_column))]
        y = 0
        for gem in gem_column:
            if gem != self.blank:
                new_column[y] = gem
                y += 1
            else:
                pass
        return new_column

    def __gem_fill_column_algo(self, gem_column):
        # Fills all blanks in gem_column with randomly chosen gems.
        for y in range(len(gem_column)):
            if gem_column[y] == self.blank:
                gem_column[y] = random.choice(gem_types)
            else:
                pass
        return gem_column

    def __gem_fall_and_fill_pane(self):
        # Construct new pane after the stage is cleared
        for x in range(0, self.game_pane_x_size):
            self.pane[x] = self.__gem_fill_column_algo(self.__gem_fall_algo(self.pane[x]))
        return 0

    def clear_stage(self):
        # Recursively reconstruct current pane after one move
        gems_to_clear = self.__check_stage()
        if gems_to_clear:
            print(gems_to_clear)
            for gem_x, gem_y in gems_to_clear:
                self.pane[gem_x][gem_y] = self.blank
            self.__gem_fall_and_fill_pane()
            self.clear_stage()
        else:
            pass
        return 0

    def __exchange(self, gem1, gem2, pane=None):
        if not pane:
            pane = self.pane
        pane[gem2[0]][gem2[1]], pane[gem1[0]][gem1[1]] = pane[gem1[0]][gem1[1]], pane[gem2[0]][gem2[1]]
        return 0

    def exchange(self, gem1, gem2):
        if (abs(gem1[0] - gem2[0]) == 1 and gem1[1] == gem2[1]) or (abs(gem1[1] - gem2[1]) == 1 and gem1[0] == gem2[0]):
            new_pane = self.pane[:]
            self.__exchange(gem1, gem2, new_pane)
            if self.__check_stage(new_pane):
                self.pane = new_pane
                return 0
            else:
                return 1
        else:
            return 1


my_game_pane = game_pane(gem_types, blank, game_pane_x_size, game_pane_y_size)
my_game_pane.print_current_pane()
my_game_pane.clear_stage()
my_game_pane.print_current_pane()

while True:
    if my_game_pane.exchange(list(map(int, input().split())),list(map(int, input().split()))):
        print('Failure')
    else:
        my_game_pane.clear_stage()
        my_game_pane.print_current_pane()

# my_game_pane = game_pane(gem_types, blank, game_pane_x_size, game_pane_y_size)
# my_game_pane.pane = [[0 for i in range(game_pane_y_size)] for j in range(game_pane_x_size)]
# my_game_pane.print_current_pane()
#
# my_game_pane.pane[2][4] = 1
# my_game_pane.print_current_pane()
