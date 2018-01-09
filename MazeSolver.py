#!/usr/bin/env python
""" Written by Aaron Bunch
v.1 Jan 9, 2018
"""

import random

class MazeSolver:
    """docstring here"""

    def __init__(self, filename, source_wall='0', source_path='1',
                 source_start='S', source_dest='D'):
        """docstring here"""

        self.wall = '\u2588'
        self.path = ' '
        self.start = 'S'
        self.dest = 'D'
        self.blaze = '\u00B7'
        self.filename = filename
        self.source_wall = source_wall
        self.source_path = source_path
        self.source_start = source_start
        self.source_dest = source_dest
        self.get_original_maze()
        self.verify_maze()

    def get_original_maze(self):
        """docstring here"""

        with open(self.filename) as f:
            self.original_maze = f.readlines()
        self.original_maze = [row.rstrip() for row in self.original_maze]
        self.original_maze = [row.replace(self.source_wall, self.wall)
                              for row in self.original_maze]
        self.original_maze = [row.replace(self.source_path, self.path)
                              for row in self.original_maze]

    def verify_maze(self):
        """docstring here"""

        # check for start and destination
        self.S_row, self.S_col = self.find_char(self.original_maze, 'S')
        self.D_row, self.D_col = self.find_char(self.original_maze, 'D')
        if (self.S_row is None) or (self.D_row is None):
            print('\nThe maze must have both a\n')
            print('start and a destination.\n')
            quit()
        # check for rectangularity
        row_lengths = []
        for row in self.original_maze:
            row_lengths.append(len(row))
        if len(set(row_lengths)) > 1:
            print('\nThe maze must have rows\n')
            print('of equal length.\n')
            quit()
        # check for border wall; insert one if necessary
        if ((len(set(self.original_maze[0])) > 1) or
            (len(set(self.original_maze[-1])) > 1) or
            (len(set([row[0] for row in self.original_maze])) > 1) or
            (len(set([row[-1] for row in self.original_maze])) > 1)):
            self.original_maze.insert(0,
                    self.wall*(len(self.original_maze[0])))
            self.original_maze.insert(-1,
                    self.wall*(len(self.original_maze[-1])))
            self.original_maze = [self.wall+row for row in self.original_maze]
            self.original_maze = [row+self.wall for row in self.original_maze]

    def find_char(self, maze, char):
        """docstring here"""

        char_row = None
        char_col = None
        for row in range(1, len(maze)-1):
            for col in range(1, len(maze[row])-1):
                if maze[row][col] == char:
                    char_row = row
                    char_col = col
        return char_row, char_col

    def count_char(self, maze, char):
        """docstring here"""

        num = 0
        for row in range(1, len(maze)-1):
            for col in range(1, len(maze[row])-1):
                if maze[row][col] == char:
                    num += 1
        return num

    def num_branches(self, maze):
        """docstring here"""

        num = 0
        for row in range(1, len(maze)-1):
            for col in range(1, len(maze[row])-1):
                if self.is_branch(maze, row, col):
                    num += 1
        return num

    def insert_char(self, maze, row, col, char):
        """docstring"""

        temp_list = list(maze[row])
        temp_list[col] = char
        maze[row] = ''.join(temp_list)
        return maze

    def get_paths(self, maze, row, col):
        """docstring"""

        path_north = False
        path_south = False
        path_east = False
        path_west = False

        if maze[row-1][col] != self.wall:
            path_north = True
        if maze[row+1][col] != self.wall:
            path_south = True
        if maze[row][col+1] != self.wall:
            path_east = True
        if maze[row][col-1] != self.wall:
            path_west = True
        return path_north, path_south, path_east, path_west

    def is_dead_end(self, maze, row, col):
        """docstring"""

        paths = self.get_paths(maze, row, col)
        num_paths = sum([1 for p in paths if p])
        if ((maze[row][col] in [self.path, self.start, self.dest]) and
            (num_paths == 1)):
            return True
        else:
            return False

    def is_walled_in(self, maze, row, col):
        """docstring"""

        paths = self.get_paths(maze, row, col)
        if any(paths):
            return False
        else:
            return True

    def is_branch(self, maze, row, col):
        """docstring"""

        paths = self.get_paths(maze, row, col)
        num_paths = sum([1 for path in paths if path])
        if ((maze[row][col] in [self.path, self.start, self.dest]) and
            (num_paths > 2)):
            return True
        else:
            return False

    def fill_in_dead_ends(self, maze):
        """docstring"""

        dead_ends = True
        while dead_ends:
            dead_ends = False
            # working with indices, excluding the border of the maze
            for row in range(1, len(maze)-1):
                for col in range(1, len(maze[row])-1):
                    if (maze[row][col] == self.path and
                        self.is_dead_end(maze, row, col)):
                        maze = self.insert_char(maze, row, col, self.wall)
                        dead_ends = True
        return maze

    def move_north(row, col):
        row -= 1
        return row, col

    def move_south(row, col):
        row += 1
        return row, col

    def move_east(row, col):
        col += 1
        return row, col

    def move_west(row, col):
        col -= 1
        return row, col

    def break_loop(self, maze, turn='right'):
        """docstring"""

        # start at S
        row, col = self.S_row, self.S_col
        path_north, path_south, path_east, path_west = self.get_paths(maze, row, col)
        paths = [path_north, path_south, path_east, path_west]
        prev_row, prev_col = None, None
        branches = []
        # when D is not a dead-end, use seen_D to avoid an infinite loop
        seen_D = False 

        while True:

            if turn == 'random':
                this_turn = random.choice(['right', 'left'])
            else:
                this_turn = turn

            #####################################################
            # Check if the current location is the destination, #
            # the base of a loop, or a branch not seen before.  #
            #####################################################

            # check if we are at the destination
            if (row, col) == (self.D_row, self.D_col):
                if self.is_dead_end(maze, row, col):
                    return False
                else:
                    if seen_D is True:
                        return False
                    else:
                        seen_D = True

            # check if we are completing a loop
            if (self.is_branch(maze, row, col) and
                ((row, col) in branches) and
                (maze[prev_row][prev_col] not in [self.start, self.dest])):
                # put a wall at the previous position
                maze = self.insert_char(maze, prev_row, prev_col, self.wall)
                return maze 

            # check if we are at a branch for the first time
            if (self.is_branch(maze, row, col) and
                (row, col) not in branches):
                # record the location of the branch
                branches.append((row, col))

            ###############
            # Take a step #
            ###############

            # if we are starting at S, and there is more than one open path
            # (S is a branch, for instance), then:
            # 1) if we are turning randomly right and left, then choose our
            #    starting directly randomly
            # 2) if we are consistently turning right, then choose the first
            #    open path clockwise from north
            # 3) if we are consistently turning left, then choose the first
            #    open path clockwise from south

            if (prev_row, prev_col) == (None, None):
                prev_row = row
                prev_col = col

                if turn == 'random':
                    flag = True
                    while flag:
                        # repeat until we randomly choose an open path
                        direction = random.choice(['path_north', 'path_south',
                                                   'path_east', 'path_west'])
                        if (direction == 'path_north') and (path_north):
                            row, col = move_north(row, col)
                            flag = False
                        elif (direction == 'path_south') and (path_south):
                            row, col = move_south(row, col)
                            flag = False
                        elif (direction == 'path_east') and (path_east):
                            row, col = move_east(row, col)
                            flag = False
                        elif (direction == 'path_west') and (path_west):
                            row, col = move_west(row, col)
                            flag = False

                elif turn == 'right':
                    if path_north:
                        row, col = move_north(row, col)
                    elif path_east:
                        row, col = move_east(row, col)
                    elif path_south:
                        row, col = move_south(row, col)
                    else:
                        row, col = move_west(row, col)

                else:
                    # turn == 'left'
                    if path_south:
                        row, col = move_south(row, col)
                    elif path_west:
                        row, col = move_west(row, col)
                    elif path_north:
                        row, col = move_north(row, col)
                    else:
                        row, col = move_east(row, col)

            # otherwise take the first open path without back-tracking;
            # to avoid back-tracking, and to determine the walker's left
            # and right, we keep track of the walker's previous location
            # (the direction the walker has come from)

            else:
                temp_row = row
                temp_col = col
                if (prev_row == row) and (col > prev_col):
                    # coming from the west
                    if this_turn == 'right':
                        if path_south:
                            row, col = move_south(row, col)
                        elif path_east:
                            row, col = move_east(row, col)
                        else:
                            row, col = move_north(row, col)
                    else:
                        # turn == 'left'
                        if path_north:
                            row, col = move_north(row, col)
                        elif path_east:
                            row, col = move_east(row, col)
                        else:
                            row, col = move_south(row, col)
                elif (prev_row == row) and (col < prev_col):
                    # coming from the east
                    if this_turn == 'right':
                        if path_north:
                            row, col = move_north(row, col)
                        elif path_west:
                            row, col = move_west(row, col)
                        else:
                            row, col = move_south(row, col)
                    else:
                        # turn == 'left'
                        if path_south:
                            row, col = move_south(row, col)
                        elif path_west:
                            row, col = move_west(row, col)
                        else:
                            row, col = move_north(row, col)
                elif (prev_col == col) and (row > prev_row):
                    # coming from the north
                    if this_turn == 'right':
                        if path_west:
                            row, col = move_west(row, col)
                        elif path_south:
                            row, col = move_south(row, col)
                        else:
                            row, col = move_east(row, col)
                    else:
                        # turn == 'left'
                        if path_east:
                            row, col = move_east(row, col)
                        elif path_south:
                            row, col = move_south(row, col)
                        else:
                            row, col = move_west(row, col)
                else:
                    # coming from the south
                    if this_turn == 'right':
                        if path_east:
                            row, col = move_east(row, col)
                        elif path_north:
                            row, col = move_north(row, col)
                        else:
                            row, col = move_west(row, col)
                    else:
                        # turn == 'left'
                        if path_west:
                            row, col = move_west(row, col)
                        elif path_north:
                            row, col = move_north(row, col)
                        else:
                            row, col = move_east(row, col)
                prev_row = temp_row
                prev_col = temp_col

            # get open paths at new position
            path_north, path_south, path_east, path_west = self.get_paths(maze,
                    row, col)
            paths = [path_north, path_south, path_east, path_west]

    def solve_maze(self, n=20):
        """docstring"""

        self.solutions = []
        self.solution_lengths = []
        shortest = 10e9 # some arbitrarily large number
        for i in range(n):
            working_maze = self.original_maze[:] # refresh working maze 
            working_maze = self.fill_in_dead_ends(working_maze)
            # walk the maze turning randomly at branches until there are no more
            # loops
            num = self.num_branches(working_maze)
            while num > 0:
                broken_loop = self.break_loop(working_maze, turn='random')
                if broken_loop:
                    working_maze = broken_loop[:]
                    working_maze = self.fill_in_dead_ends(working_maze)
                num = self.num_branches(working_maze)

            # filter out spurious solutions where S and/or D are completely walled
            # in (there is no path between S and D)
            if (not self.is_walled_in(working_maze, self.S_row, self.S_col) and
                not self.is_walled_in(working_maze, self.D_row, self.D_col)):
                self.solutions.append(working_maze)
                self.solution_lengths.append(self.count_char(working_maze,
                    self.path))
                if self.solution_lengths[-1] < shortest:
                    shortest = self.solution_lengths[-1]
                    self.shortest_solution = working_maze

    def blaze_trail(self):
        """docstring"""

        working_maze = self.original_maze[:]
        for row in range(1, len(working_maze)-1):
            for col in range(1, len(working_maze[row])-1):
                if self.shortest_solution[row][col] == self.path:
                    working_maze = self.insert_char(working_maze,
                                                    row, col, self.blaze)
        self.blazed_trail = working_maze
