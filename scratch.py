#!python3
# -*- coding:utf-8 -*-

import random
import pprint

game_pane_x_size, game_pane_y_size = 8, 8
game_pane_size = game_pane_x_size * game_pane_y_size
gem_types = [1, 2, 3, 4]
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

    # The Game Pane is designed and printed like
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

    def __check_stage(self):
        # Check the current game pane to see if there are any gems that should be cleared.
        # Returns a set, which contains tuples of coordinates of gems that should be cleared.
        # If no gem needs to be cleared, returns an empty set.
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
        # Returns a falled column of gems
        blank = self.blank
        old_column = gem_column
        new_column = [blank for _ in range(len(old_column))]
        y = 0
        for gem in old_column:
            if gem != blank:
                new_column[y] = gem
                y += 1
            else:
                pass
        return new_column

    def __gem_fill_column_algo(self, gem_column):
        # Fills all blanks with randomly chosen gems.
        blank = self.blank
        old_column = gem_column
        new_column = gem_column
        for y in range(len(old_column)):
            if old_column[y] == blank:
                new_column[y] = random.choice(gem_types)
            else:
                pass
        return new_column

    def __construct_gem_falled_and_filled_pane(self):
        # Construct new pane after the stage is cleared
        old_pane = self.pane
        new_pane = self.pane
        for x in range(0, self.game_pane_x_size):
            new_pane[x] = self.__gem_fill_column_algo(
                self.__gem_fall_algo(old_pane[x]))
        self.pane = new_pane

    def clear_stage(self):
        # Recursively reconstruct current pane after one move
        gems_to_clear = self.__check_stage()
        if gems_to_clear:
            print(gems_to_clear)
            for gem_x, gem_y in gems_to_clear:
                self.pane[gem_x][gem_y] = self.blank
            self.__construct_gem_falled_and_filled_pane()
            self.clear_stage()
        else:
            pass


my_game_pane = game_pane(gem_types, blank, game_pane_x_size, game_pane_y_size)
my_game_pane.print_current_pane()
my_game_pane.clear_stage()
my_game_pane.print_current_pane()
