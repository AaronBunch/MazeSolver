# MazeSolver
A python maze solver class

## Really Two Maze Solvers

### My First Idea
My first idea was that it would be easier to find the dead-ends in a maze than
the path through it. So the first solver scans through the maze, filling in all
the dead-ends, and what is left is the path from start to finish.

This first solver became a little more complicated, because if there are loops
in the maze, those loops will be left over when all the dead-ends are filled in.
So a walker, turning randomly at branches, discovers and 'breaks' all the loops
by inserting a wall at the branch where the loop comes together. After breaking
a loop, new dead-ends are created that can be filled in. After all of the loops
are broken, and the new dead-ends filled in, there is a single path from start
to finish.

As you can imagine, the randomly turning walker does not always find the
shortest path through the loops. And sometimes the walker breaks the loops in
such a way that there is no path from start to finish. So, we solve the maze
fifty times (by default) and pick the shortest solution.

This method works beautifully for all mazes with single-width paths. It has
trouble with big open spaces and double- or triple width paths.

### Then I Discovered Network Analysis
If you convert the maze to a networkx graph, finding the shortest path between
any two points in the graph is trivial. It takes very little code, and it solves
every kind of maze you can imagine. 

## Use

### Maze Walker
```python
from MazeSolver import MazeSolver
ms = MazeSolver()
ms.get_maze(filename)
ms.verify_maze()
ms.solve_maze()
```

### Network Analysis
```python
from MazeSolver import MazeSolver
ms = MazeSolver()
ms.get_maze(filename)
ms.verify_maze()
ms.to_graph()
ms.solve_graph()
```

## Methods
1. \_\_init\_\_(source_wall='0', source_path='1',
            source_start='S', source_dest='D'):
    Creates a MazeSolver object. Sets the local and source file maze
    characters. Source file characteres can be set with keyword
    arguments.

2. get_maze(filename): Loads the maze from filename and converts the source file
   characters to local characters. The source file should be a text file with
   lines of equal length.

3. verify_maze(): Optional. Verifies that the loaded maze has the correct form.
   The maze should have rows of equal length, have exactly one start and one
   destination character, and be completely bordered by wall characters. If a
   border wall is missing, one is silently added. See test mazes,
   'test_maze_10\*.txt', in this repository.

4. solve_maze(n=50): Solves the maze n times and returns the shortest solution
   marked on the original maze. As a progress indicator, it prints to the screen
   the path length of each solution as it finds it, or an asterisk indicating a
   failed attempt (the maze walker has cut off all paths from start to
   destination). 

5. get_forays(n, return_forays=False, print_forays=True):
   For a particular solution with index, n, prints or returns a list of all the
   forays into the maze that break the loops. n indexes all attempted solutions,
   even ones that fail (as indicated by \* in the progress indicator). Whereas
   the solutions and solution_lengths attributes contain only the successful
   attempts. So use the progress indicator to choose n for this method.

6. to_graph(return_graph=False): Converts the maze to a networkx graph.

7. solve_graph(print_solution=True, return_solution=False): Use with
   to_graph(). Returns the shortest path from start to destination marked on
   the original maze.

## Attributes
1. original_maze:  This is available as soon as a maze is loaded with
   get_maze(filename).

2. shortest_solution:  The shortest path from start to finish marked on the
   original maze. 

3. solutions:  A list of all solutions found by the walker (there may be fewer
   than n, because failed attempts are omitted).
                      
4. solution_lengths:  A list of the lengths of all solutions found by the walker
   (excluding failed attempts).

5. steps:  Nested lists of every step taken in the maze for each solution
   (including failed attempts). It has the structure:
   [ [ solution index, [ foray index, [ (row, col), ...]]]]

6. breaks:  Nested lists of every broken loop with new dead-ends filled in for
   each solution (including failed attempts). It as the structure:
   [ [ solution index, [ broken loop, broken loop, ...]]]

7. G:  The original maze represented as a networkx graph.

## Known Issues
1. Bafflingly, every so often, after successfully solving the maze many times,
   the maze walker takes off seemingly at random, walks through walls, across
   paths, until it runs off the edge of the maze and raises an IndexError. I
   have not figured out what causes this behavior. Re-running the solver
   navigates the maze without incident.
