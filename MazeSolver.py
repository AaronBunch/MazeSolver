"""MazeSolver class."""

import sys
import random

__author__ = "Aaron Bunch"
__date__ = "Jan 9, 2018"

class MazeSolver:
    """Find the shortest path through a maze.

    Public method:
        solve_maze(n=50):   Solve the maze n times and return the shortest path 
                            marked on the original maze.
    Instance variables:
        original_maze:      The maze as it was loaded from its source file
                            (a list of strings).
        solution_lengths:   A list of the path-lengths of the real solutions
                            (spurious solutions omitted).
        solutions:          A list of solutions to the maze (spurious solutions
                            omitted).
        shortest_solution:  The solution with the shortest path.
    """

    def __init__(self, source_wall='0', source_path='1',
                 source_start='S', source_dest='D'):
        """Construct a MazeSolver object.

        Keyword Args:
            source_wall:    The wall character in the source file.
            source_path:    The path character in the source file.
            source_start:   The start character in the source file.
            source_dest:    The destination character in the source file.
        """
        self.wall = '\u2588'
        self.path = ' '
        self.start = 'S'
        self.dest = 'D'
        self.blaze = '\u00B7'
        self.source_wall = source_wall
        self.source_path = source_path
        self.source_start = source_start
        self.source_dest = source_dest

    def get_maze(self, filename, return_maze=False):
        """Load the maze and convert to internal wall and path characters.
        
        Args:
            filename:   name of source file
        
        Returns:
            maze:       a list of strings, source file characters converted
                        to internal wall and path characters,
                        if return_maze=True
        """
        
        with open(filename) as f:
            maze = f.readlines()
        maze = [row.rstrip() for row in maze]
        maze = [row.replace(self.source_wall, self.wall) for row in maze]
        maze = [row.replace(self.source_path, self.path) for row in maze]
        self.original_maze = maze
        if return_maze == True:
            return maze

    def verify_maze(self, return_maze=False):
        """Verify that the loaded maze is in the correct format.
        
        The maze must have exactly one start and one destination character; it
        must be rectangular (all rows of equal length); and if a border wall is
        missing, one is silently added. Prints a message and returns nothing if
        there is a problem.

        Returns:
            maze:   if return_maze==True
        """

        # get start and destination positions
        self.S_row, self.S_col = self.find_char(self.original_maze, 'S')
        self.D_row, self.D_col = self.find_char(self.original_maze, 'D')
        # check for multiple starts or destinations
        if (len(self.S_row) > 1) or (len(self.D_row) > 1):
            if not return_maze:
                print("""
                        The maze may contain only one start,
                        and one destination.
                      """)
            return
        # check for no start or no destination
        if (len(self.S_row) == 0) or (len(self.D_row) == 0):
            if not return_maze:
                print("""
                        Both a start and a destination
                        must be indicated on the maze.
                      """)
            return

        # find_char() returns a list; we want only the first element for S and D
        self.S_row = self.S_row[0]
        self.S_col = self.S_col[0]
        self.D_row = self.D_row[0]
        self.D_col = self.D_col[0]
        
        # check for rectangularity
        row_lengths = []
        for row in self.original_maze:
            row_lengths.append(len(row))
        if len(set(row_lengths)) > 1:
            if not return_maze:
                print("""
                        The maze must have rows of equal length.
                      """)
            return

        # check for border walls; insert them as necessary
        # check top wall
        if len(set(self.original_maze[0])) > 1:
            self.original_maze.insert(0,
                    self.wall*(len(self.original_maze[0])))
        # check bottom wall
        if len(set(self.original_maze[-1])) > 1:
            self.original_maze.append(
                    self.wall*(len(self.original_maze[-1])))
        # check left wall
        if len(set([row[0] for row in self.original_maze])) > 1:
            self.original_maze = [self.wall+row for row in self.original_maze]
        # check right wall
        if len(set([row[-1] for row in self.original_maze])) > 1:
            self.original_maze = [row+self.wall for row in self.original_maze]

        if return_maze == True:
            return self.original_maze

    def find_char(self, maze, char):
        """Find a given character in the maze.
      
        Args:
            maze:   a list of strings
            char:   the character to find

        Returns:
            char_row:   list of rows
            char_col:   list of columns
        """

        char_row = []
        char_col = []
        for row in range(0, len(maze)):
            for col in range(0, len(maze[row])):
                if maze[row][col] == char:
                    char_row.append(row)
                    char_col.append(col)
        return char_row, char_col
 
    def count_char(self, maze, char):
        """Count the number of a given character in the maze.
       
        Args:
            maze:   a list of strings
            char:   the character to count
                
        Returns:
            the count of the character
        """

        count = 0
        for row in range(0, len(maze)):
            for col in range(0, len(maze[row])):
                if maze[row][col] == char:
                    count += 1
        return count

    def num_branches(self, maze):
        """Count the number of path branches in the maze.

        Calls self.is_branch(). A branch is any path location with
        open paths on at least three sides.

        Args:
            maze:   a list of strings

        Returns:
            The number of branches in the maze.
        """

        count = 0
        for row in range(1, len(maze)-1):
            for col in range(1, len(maze[row])-1):
                if self.is_branch(maze, row, col):
                    count += 1
        return count

    def insert_char(self, maze, row, col, char):
        """Insert a character into a maze at a specified row and column.
       
        Args:
            maze:   a list of strings
            row:    the row in which to insert the character (int)
            col:    the column in which to insert the character (int)
            char:   character to insert

        Returns:
            The maze with the character inserted.
        """

        temp_list = list(maze[row])
        temp_list[col] = char
        maze[row] = ''.join(temp_list)
        return maze

    def get_paths(self, maze, row, col):
        """Find the open paths at a position in a maze.
      
        Paths that step off the border of the maze are not open.
        
        (The way this is implemented now, the maze can probably have a ragged
        right edge. But that still needs to be tested.)

        Args:
            maze:   a list of strings
            row:    the row number (int)
            col:    the column number (int)

        Returns:
            A tuple of booleans: path_north, path_south, path_east, path_west
            True means the path is open; False means no path in that direction.
        """

        path_north = False
        path_south = False
        path_east = False
        path_west = False

        try: 
            if maze[row+1][col] != self.wall:
                path_south = True
        except IndexError:
            pass
        try:
            if maze[row][col+1] != self.wall:
                path_east = True
        except IndexError:
            pass

        ######################################################################
        # We have to handle row[0] and col[0] differently, because row[-1] and
        # col[-1] will not raise an IndexError (they point to the end of the
        # list)
        ######################################################################

        try:
            if (row != 0) and (maze[row-1][col] != self.wall):
                path_north = True
        except IndexError:
            # trying to ferret out an IndexError I occasionally get here;
            # have not figured it out
            print(f'IndexError: {row}, {col}')
        try:
            if (col != 0) and (maze[row][col-1] != self.wall):
                path_west = True
        except IndexError:
            # trying to ferret out an IndexError I occasionally get here;
            # have not figured it out
            print(f'IndexError: {row}, {col}')

        return path_north, path_south, path_east, path_west

    def is_dead_end(self, maze, row, col):
        """Determine if a point in the maze is a dead-end.
       
        A dead-end is any path location with an open path in only one
        direction.

        Args:
            maze:   a list of strings
            row:    the row number (int)
            col:    the column number (int)
        
        Returns:
            Boolean
        """

        paths = self.get_paths(maze, row, col)
        num_paths = sum([1 for p in paths if p])
        if ((maze[row][col] in [self.path, self.start, self.dest]) and
            (num_paths == 1)):
            return True
        else:
            return False

    def is_walled_in(self, maze, row, col):
        """Determine if a maze location is surrounded entirely by walls.
        
        This is used to filter out spurious solutions, in which the
        start and destination are completely walled in.

        Args:
            maze:   a list of strings
            row:    the row number (int)
            col:    the column number (int)

        Returns:
            Boolean
        """

        paths = self.get_paths(maze, row, col)
        if any(paths):
            return False
        else:
            return True

    def is_branch(self, maze, row, col):
        """Determine if a maze location is branch in the path.
        
        A branch is any path location that has open paths on at least
        three sides.

        Args:
            maze:   a list of strings
            row:    the row number (int)
            col:    the column number (int)

        Returns:
            Boolean
        """

        paths = self.get_paths(maze, row, col)
        num_paths = sum([1 for path in paths if path])
        if ((maze[row][col] in [self.path, self.start, self.dest]) and
            (num_paths > 2)):
            return True
        else:
            return False

    def fill_in_dead_ends(self, maze):
        """Fill in all dead-ends with wall.
      
        Does not fill in start or destination tiles if these happen to
        lie at dead-ends.

        Args:
            maze:   a list of strings 

        Returns:
            The maze with no dead-ends.
        """

        dead_ends = True
        while dead_ends:
            dead_ends = False
            for row in range(0, len(maze)):
                for col in range(0, len(maze[row])):
                    if (maze[row][col] == self.path and
                        self.is_dead_end(maze, row, col)):
                        maze = self.insert_char(maze, row, col, self.wall)
                        dead_ends = True
        return maze

    def count_dead_ends(self, maze):
        """Counts the number of dead-ends in the maze. 

        Args:
            maze:   a list of strings

        Returns:
            count:  the number of dead-ends in the maze
        """

        count = 0
        for row in range(0, len(maze)):
            for col in range(0, len(maze[row])):
                if self.is_dead_end(maze, row, col):
                    count += 1
        return count

    @staticmethod
    def move_north(row, col):
        row -= 1
        return row, col

    @staticmethod
    def move_south(row, col):
        row += 1
        return row, col

    @staticmethod
    def move_east(row, col):
        col += 1
        return row, col

    @staticmethod
    def move_west(row, col):
        col -= 1
        return row, col

    def take_first_step(self, row, col, paths, turn):
        """Takes the first step in the maze.

        If we are starting at S, and there is more than one open path
        (S is a branch, for instance), then:
        1) If we are turning randomly right and left, then choose our
           starting direction randomly.
        2) If we are consistently turning right, then choose the first
           open path clockwise from north.
        3) If we are consistently turning left, then choose the first
           open path clockwise from south.

        Args:
            row:        current row (int)
            col:        current col (int)
            paths:      [path_north, path_south, path_east, past_west]
            turn:       the direction to turn at branches

        Returns:
            row:        the new row
            col:        the new column
        """

        path_north, path_south, path_east, path_west = paths

        if turn == 'random':
            no_path = True
            while no_path:
                # repeat until we randomly choose an open path
                direction = random.choice(['path_north', 'path_south',
                                           'path_east', 'path_west'])
                if (direction == 'path_north') and (path_north):
                    row, col = MazeSolver.move_north(row, col)
                    no_path = False
                elif (direction == 'path_south') and (path_south):
                    row, col = MazeSolver.move_south(row, col)
                    no_path = False
                elif (direction == 'path_east') and (path_east):
                    row, col = MazeSolver.move_east(row, col)
                    no_path = False
                elif (direction == 'path_west') and (path_west):
                    row, col = MazeSolver.move_west(row, col)
                    no_path = False
        elif turn == 'right':
            if path_north:
                row, col = MazeSolver.move_north(row, col)
            elif path_east:
                row, col = MazeSolver.move_east(row, col)
            elif path_south:
                row, col = MazeSolver.move_south(row, col)
            else:
                row, col = MazeSolver.move_west(row, col)
        else:
            # turn == 'left'
            if path_south:
                row, col = MazeSolver.move_south(row, col)
            elif path_west:
                row, col = MazeSolver.move_west(row, col)
            elif path_north:
                row, col = MazeSolver.move_north(row, col)
            else:
                row, col = MazeSolver.move_east(row, col)
        return row, col

    def take_step(self, row, col, prev_row, prev_col, paths, turn):
        """Takes a step in the maze.

        Args:
            row:        current row (int)
            col:        current col (int)
            prev_row:   the previous row (int)
            prev_col:   the previous column (int)
            paths:      [path_north, path_south, path_east, past_west]
            turn:       the direction to turn at branches

        Returns:
            row:        the new row (int)
            col:        the new column (int)
            prev_row:   the new previous row
            prev_col:   the new previous column
        """
        
        path_north, path_south, path_east, path_west = paths

        temp_row = row
        temp_col = col
        if (prev_row == row) and (col > prev_col):
            # coming from the west
            if turn == 'right':
                if path_south:
                    row, col = MazeSolver.move_south(row, col)
                elif path_east:
                    row, col = MazeSolver.move_east(row, col)
                else:
                    row, col = MazeSolver.move_north(row, col)
            else:
                # turn == 'left'
                if path_north:
                    row, col = MazeSolver.move_north(row, col)
                elif path_east:
                    row, col = MazeSolver.move_east(row, col)
                else:
                    row, col = MazeSolver.move_south(row, col)
        elif (prev_row == row) and (col < prev_col):
            # coming from the east
            if turn == 'right':
                if path_north:
                    row, col = MazeSolver.move_north(row, col)
                elif path_west:
                    row, col = MazeSolver.move_west(row, col)
                else:
                    row, col = MazeSolver.move_south(row, col)
            else:
                # turn == 'left'
                if path_south:
                    row, col = MazeSolver.move_south(row, col)
                elif path_west:
                    row, col = MazeSolver.move_west(row, col)
                else:
                    row, col = MazeSolver.move_north(row, col)
        elif (prev_col == col) and (row > prev_row):
            # coming from the north
            if turn == 'right':
                if path_west:
                    row, col = MazeSolver.move_west(row, col)
                elif path_south:
                    row, col = MazeSolver.move_south(row, col)
                else:
                    row, col = MazeSolver.move_east(row, col)
            else:
                # turn == 'left'
                if path_east:
                    row, col = MazeSolver.move_east(row, col)
                elif path_south:
                    row, col = MazeSolver.move_south(row, col)
                else:
                    row, col = MazeSolver.move_west(row, col)
        else:
            # coming from the south
            if turn == 'right':
                if path_east:
                    row, col = MazeSolver.move_east(row, col)
                elif path_north:
                    row, col = MazeSolver.move_north(row, col)
                else:
                    row, col = MazeSolver.move_west(row, col)
            else:
                # turn == 'left'
                if path_west:
                    row, col = MazeSolver.move_west(row, col)
                elif path_north:
                    row, col = MazeSolver.move_north(row, col)
                else:
                    row, col = MazeSolver.move_east(row, col)
        prev_row = temp_row
        prev_col = temp_col

        return row, col, prev_row, prev_col

    def break_loop(self, maze, turn='random'):
        """Find a loop in the maze, and break it by inserting a wall.
        
        The loop is recognized when the walker returns to a branch.
        The loop is broken by walling off the branch behind the walker.
          
        Args:
            maze:        a list of strings

        Keyword Args:
            turn:        determines whether the maze walker turns right,
                         left, or randomly at branches in the path

        Returns:
            False, if no loop is found.
            The maze with the loop broken, if a loop is found.
        """

        # start at S
        row, col = self.S_row, self.S_col
        path_north, path_south, path_east, path_west = self.get_paths(maze,
                row, col)
        paths = [path_north, path_south, path_east, path_west]
        prev_row, prev_col = None, None
        branches = []
        # when S and/or D are not dead-ends, use seen_S and seen_D to avoid
        # infinite loops
        seen_S = False
        seen_D = False 
        while True:
            if turn == 'random':
                this_turn = random.choice(['right', 'left'])
            else:
                this_turn = turn

            ################################################################
            # Check if the current location is the start, the destination, #
            # the base of a loop, or a branch not seen before.             #
            ################################################################

            # check if we are returning to the start
            if prev_row is not None: # do not check when first starting out
                if (row, col) == (self.S_row, self.S_col):
                    # if we have returned to S in a dead-end, return
                    if self.is_dead_end(maze, row, col):
                        return False
                    else:
                        # if we are returning to S for the second time,
                        # start over
                        if seen_S is True: 
                            maze = self.insert_char(maze, prev_row, prev_col,
                                                    self.wall)
                            return maze 
                        # if we are returning to S for the first time,
                        # keep going
                        else:
                            seen_S = True

            # check if we are at the destination
            if (row, col) == (self.D_row, self.D_col):
                if self.is_dead_end(maze, row, col):
                    return False
                else:
                    if seen_D is True:
                        maze = self.insert_char(maze, prev_row, prev_col,
                                                self.wall)
                        return maze 
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

            # if we are just starting out, there are special rules for how to
            # take the first step
            if (prev_row, prev_col) == (None, None):
                prev_row = row
                prev_col = col
                row, col = self.take_first_step(row, col, paths, this_turn)
            # otherwise take the first open path without back-tracking
            else:
                row, col, prev_row, prev_col = self.take_step(row, col,
                                               prev_row, prev_col, paths,
                                               this_turn)
            # get open paths at new position
            path_north, path_south, path_east, path_west = self.get_paths(maze,
                                                           row, col)
            paths = [path_north, path_south, path_east, path_west]

    def blaze_trail(self, solution):
        """Mark the solution on the original maze.
        
        Args:
            solution:   a maze completely filled in except for a single path
                        from start to finish
       
        Returns:
            The original maze with the solution marked on it.
        """

        blazed_trail = self.original_maze[:]
        for row in range(1, len(blazed_trail)-1):
            for col in range(1, len(blazed_trail[row])-1):
                if solution[row][col] == self.path:
                    blazed_trail = self.insert_char(blazed_trail,
                                                    row, col, self.blaze)
        return blazed_trail 

    def solve_maze(self, n=50):
        """Solve the maze n times, and return the shortest solution.
        
        Keyword Args:
            n:          number of times to solve the maze

        Returns:
            The shortest path from start to finish marked onto the original
            maze.
        """

        self.solutions = []
        self.solution_lengths = []
        for i in range(n):
            working_maze = self.original_maze[:] # refresh working maze 
            working_maze = self.fill_in_dead_ends(working_maze)
            # walk the maze turning randomly at branches until there are no more
            # loops
            num_branches = self.num_branches(working_maze)
            while num_branches > 0:
                broken_loop = self.break_loop(working_maze, turn='random')
                if broken_loop:
                    working_maze = broken_loop[:]
                    working_maze = self.fill_in_dead_ends(working_maze)
                num_branches = self.num_branches(working_maze)
            # filter out spurious solutions where S and/or D are completely walled
            # in (there is no path between S and D)
            if (not self.is_walled_in(working_maze, self.S_row, self.S_col) and
                not self.is_walled_in(working_maze, self.D_row, self.D_col)):
                self.solutions.append(working_maze)
                self.solution_lengths.append(self.count_char(working_maze,
                    self.path))
                print(self.solution_lengths[-1], end=' ', flush=True)
            else:
                print('*', end=' ', flush=True)
        # mark the solutions on the original maze
        for i, solution in enumerate(self.solutions):
            self.solutions[i] = self.blaze_trail(solution)
        # return the shortest solution
        # this is a monstrous way to find the shortest solution, but I don't
        # want to import numpy.argmin just for this one line
        self.shortest_solution = self.solutions[
            self.solution_lengths.index(min(self.solution_lengths))]
        print('\n')
        return self.shortest_solution




