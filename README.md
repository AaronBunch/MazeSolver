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
from MazeSolver import MazeSolver as ms
maze1 = ms('test_maze_1.txt')
maze1.solve_maze()
```
The maze file should be a text file with lines of equal length.
By default 0 -> wall, 1 -> path, 'S' -> start, and 'D' ->
destination. If there is no border wall around the maze, one
is added. See the test mazes in this repository. A small maze
template is also provided.

The solve_maze() method returns the original maze marked with the
shortest path from start to finish. After solve_maze() is called,
the MazeSolver object has the following attributes:

1. MazeSolver.original_maze:  This is available as soon as the object
is initialized.

2. MazeSolver.shortest_solution:  The shortest path from start to
finish marked on the original maze.

3. MazeSolver.solutions:  A list of all solutions found by the
walker (there may be fewer than n, because spurious solutions are
omitted). Each solution is marked on the original maze.
                      
5. MazeSolver.solution_lengths:  A list of the lengths of all solutions
found by the walker (excluding the spurious solutions).


