# -*- coding: utf-8 -*-
import copy

class StopSolverException(BaseException):
    """This exception stops the solver pruning the search.
       This exception does not signal an error
    """
    pass

"""Do you want change BOX and SIZE? Go ahead.
   Change GRID also.
"""
BOX  = 2
SIZE = BOX * BOX
GRID = [[0, 3, 0, 0],
        [0, 0, 0, 1],
        [0, 0, 2, 0],
        [4, 0, 0, 0]]


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
        print 'End'


def generate_tree(grid, row = -1, col = SIZE - 1):
    """grid contains a partial solution
       row and col are the coordinates of the last updated cell
    """
    # We must search a new cell for updating, where grid[row][col] == 0
    col += 1
    if col == SIZE:
        col = 0
        row += 1
        if row == SIZE:
            show(grid)
            # Solution found, quitting search
            raise StopSolverException
    number = grid[row][col]
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


def read_board(filename):
    """Thanks, terror_macbeth
    """
    grid = []
    lines = open(filename, 'r').readlines()
    for line in lines[1:13]:
        row = []
        for c in line.split():
            try:
                row.append(int(c))
            except ValueError:
                if c == '.':
                    row.append(0)
        if row:
            grid.append(row)
    return grid

import sys
from time import clock
if __name__ == '__main__':
    if len(sys.argv) > 1:
        grid = read_board(sys.argv[1])
    else:
        grid = GRID
    t0 = clock()
    execute(grid)
    t1 = clock()
    print 'time %f' % (t1 - t0)    
 
