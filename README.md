# MazeSolver
A python maze solver class

## The Idea
This maze solver started with the idea that it would be
easier to find the dead-ends in a maze than the path through
it. So the solver scans through the maze, filling in all
the dead-ends, and what is left is the path from start to
finish.

Almost. If there are loops in the maze, those loops will be
left over when all the dead-ends have been filled in. So, a
walker, turning randomly at branches, discovers and 'breaks'
all the loops by inserting a wall at the branch where the
loop comes together. Loops can be broken in this way without
losing access to any part of the loop. After breaking a
loop, new dead-ends are created that can be filled in. After
all of the loops are broken, and the new dead-ends filled in,
there is a single path from start to finish.

Almost. The randomly turning walker does not always find the
shortest path through the loops. And sometimes the walker
breaks the loops in such a way that there is no path from
start to finish. So, we solve the maze fifty times (by
default) and pick the shortest real solution.

## Use
```python
from MazeSolver import MazeSolver
maze = MazeSolver()
maze.get_maze(filename)
maze.verify_maze()
maze.solve_maze()
```
The maze file should be a text file with lines of equal length, and exactly one
start and one destination character.  By default '0' -> wall, '1' -> path, 'S'
-> start, and 'D' -> destination. These defaults can be changed with keyword
arguments when the MazeSolver object is instantiated. The maze should be
completely bordered by wall. If a border wall is missing, one is silently added.
See test mazes, 'test_maze_10\*.txt', in this repository. 

The solve_maze() method returns the original maze marked with the shortest path
from start to finish. As a progress indicator, it prints to the screen the path
length of each solution as it finds it, or an asterisk indicating a failed
attempt (the maze walker has cut off all paths from start to destination). 

After solve_maze() is called, the MazeSolver object has the following attributes:

1. original_maze:  This is available as soon as the object is initialized.

2. shortest_solution:  The shortest path from start to finish marked on the
   original maze. 

3. solutions:  A list of all solutions found by the walker (there may be fewer
   than n, because failed attempts are omitted).
                      
4. solution_lengths:  A list of the lengths of all solutions found by the walker
   (excluding failed attempts).

5. steps:  A nested list of every step taken in the maze for each solution
   (failed attempts are included).

6. breaks:  A nested list of every broken loop with new dead-ends filled in for
   each solution (failed attempts are included).

## Diagnostics

There is a diagnostic method, get_forays(n, return_forays=False,
print_forays=True), which, for a particular solution with index, n, prints or
returns a list of all the forays into the maze that break the loops. n indexes
all attempted solutions, even ones that fail (as indicated by \* in the progress
indicator). Whereas the solutions and solution_lengths attributes contain only the
successful attempts. So use the progress indicator to choose n for get_forays().

