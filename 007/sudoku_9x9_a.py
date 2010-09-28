# -*- coding: utf-8 -*-
from time import clock

class StopSolverException(BaseException):
    """This exception stops the solver pruning the search.
       This exception does not signal an error
    """
    pass

"""Do you want change BOX and SIZE? Go ahead.
   Change GRID also.
"""
BOX  = 3
SIZE = BOX * BOX
GRID_1 = [[0, 3, 0, 9, 0, 0, 0, 0, 8],
          [0, 0, 0, 5, 0, 0, 0, 3, 7],
          [6, 8, 0, 1, 0, 0, 0, 0, 0],
          [0, 1, 0, 7, 8, 0, 6, 0, 2],
          [0, 0, 0, 0, 0, 0, 0, 0, 0],
          [5, 0, 9, 0, 4, 3, 0, 7, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0]]

GRID_2 = [[5, 3, 4, 0, 0, 0, 9, 0, 2],
          [0, 7, 2, 1, 0, 0, 5, 0, 8],
          [0, 9, 0, 5, 4, 2, 0, 6, 0],
          [8, 5, 9, 0, 0, 0, 4, 2, 3],
          [4, 2, 6, 8, 5, 3, 7, 0, 1],
          [7, 0, 3, 0, 2, 1, 8, 5, 6],
          [9, 6, 0, 0, 3, 5, 2, 0, 0],
          [2, 0, 0, 4, 1, 0, 6, 0, 5],
          [3, 0, 5, 0, 0, 0, 1, 7, 0]]

def show(grid):
        for r in range(SIZE):
            print repr(grid[r])


def execute(grid):
    print 'Start'
    try:
        show(grid)
        print ''
        generate_tree(grid)
    except StopSolverException:
        print '  Solution found!'
    finally:
        print 'End'


def generate_tree(grid, row = -1, col = SIZE - 1):
    """grid contains a partial solution
       row and col are the coordinates of the last updated cell
    """
    # We must search a new cell for updating, where grid[row][col] == 0
    number = 1
    while number != 0:
        col += 1
        if col == SIZE:
            col = 0
            row += 1
            if row == SIZE:
                show(grid)
                # Solution found, quitting search
                raise StopSolverException
        number = grid[row][col]
    # Now, we need to find values in the box, the row, and the column            
    values = set()
    box = ((p, q) 
                for p in xrange(BOX * (row / BOX), BOX * (row / BOX) + BOX) 
                for q in xrange(BOX * (col / BOX), BOX * (col / BOX) + BOX))
    for (p, q) in box:                
        values.add(grid[p][q])
    for p in grid[row]:
        values.add(p)
        for q in [grid[rr][col] for rr in xrange(SIZE)]:
            values.add(q)
    for number in xrange(1, SIZE + 1):
        # Solutions contain numbers not in values      
        if number not in values:
               grid[row][col] = number
               generate_tree(grid, row, col)
               grid[row][col] = 0


LENGTH = 80


if __name__ == '__main__':
    print '=' * LENGTH
    grid = GRID_1
    t0 = clock()
    execute(grid)
    t1 = clock()
    print 'time %f' % (t1 - t0)    
    print '=' * LENGTH
    grid = GRID_2
    t0 = clock()
    execute(grid)
    t1 = clock()
    print 'time %f' % (t1 - t0)    
    
