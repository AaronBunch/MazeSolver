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
start to finish. So, we solve the maze twenty times (by
default) and pick the shortest real solution.

## Use
```python
from MazeSolver import MazeSolver as ms
maze1 = ms('test_maze_1.txt')
ms.solve_maze()
ms.blaze_trail()
```
The solve_maze() method generates filled-in mazes (all black)
except for a single path from start to finish. The blaze_trail()
method marks the shortest path on the original maze. Once the
maze has been solved and the trail blazed, the maze solver
object has the following attributes:

  *ms.blazed_trail        the original maze marked with the shortest
                          path from start to finish

  *ms.solutions           a list of all n solutions found by the
                          walker; each solution is a maze completely
                          filled in except for one path from start
                          to finish; spurious solutions are omitted
                      
  *ms.shortest_solution   the original maze, completely filled in,
                          except for the shortest path from start
                          to finish

  *ms.solution_lengths    a list of the lengths of all n solutions
                          found by the walker (excluding the spurious
                          solutions)
