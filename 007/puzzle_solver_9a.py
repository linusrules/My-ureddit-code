# -*- coding: utf-8 -*-
import copy

class StopSolverException(BaseException):
    """This exception stops the solver pruning the search.
       This exception does not signal an error
    """
    pass

class StopCallback(object):
    def __init__(self, callback):
        self.callback = callback

    def execute(self, solution):
        self.callback.execute(solution)
        raise StopSolverException
    
class SolverCallback(object):
    def __init__(self):
        pass

    def execute(self, solution):
        solution.show()

SIZE = 9
BOX  = 3

class Node(object):
    def __init__(self, info, row = -1, col = SIZE - 1, number = 0):
        self.row = row
        self.col = col
        if number == 0:
            self.parent = None
            self.depth = 0
            self.grid = info
        else:
            self.parent = info
            self.depth = info.depth + 1
            self.grid = copy.deepcopy(info.grid)
            self.grid[row][col] = number
            

    def show(self):
        for r in range(SIZE):
            print repr(self.grid[r])

class Solver(object):
    def __init__(self, callback = SolverCallback()):
        self.callback = callback
        self.boxes = [None] * SIZE
        for row in xrange(SIZE):
	    self.boxes[row] = [0] * SIZE
	    for col in xrange(SIZE):
                self.boxes[row][col] = ((p, q) 
                      for p in xrange(BOX * (row // BOX), BOX * (row // BOX) + BOX)
                      for q in xrange(BOX * (col // BOX), BOX * (col // BOX) + BOX))

    def execute(self, grid):
        print 'Start'
        try:
	    initial = Node(grid)
	    initial.show()
	    print ''
            self.generate_tree(initial)
        except StopSolverException:
            print 'End'


    def generate_tree(self, node):
        col = node.col + 1
        if col == SIZE:
            col = 0
            row = node.row + 1
            if row == SIZE:
                self.callback.execute(node)		    
                return
        else:
            row = node.row
        number = node.grid[row][col]
        while number != 0:
            col += 1
            if col == SIZE:
                col = 0
                row += 1
                if row == SIZE:
                    self.callback.execute(node)		    
                    return
            number = node.grid[row][col]
        values = set(v for v in xrange(1, SIZE + 1))
        for p, q in self.boxes[row][col]:
            v = node.grid[p][q]
            if v in values:
               values.remove(v)
        for p in node.grid[row]:
            if p in values: values.remove(p)
            for q in [node.grid[rr][col] for rr in xrange(SIZE)]:
                if q in values: values.remove(q)
        for number in values:
            self.generate_tree(Node(node, row, col, number))


def read_board(filename):
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
    return position

import sys
from time import clock
if __name__ == '__main__':
    if len(sys.argv) > 1:
        grid = read_board(sys.argv[1])
    else:
        grid = [[0, 3, 0, 9, 0, 0, 0, 0, 8],
                [0, 0, 0, 5, 0, 0, 0, 3, 7],
                [6, 8, 0, 1, 0, 0, 0, 0, 0],
                [0, 1, 0, 7, 8, 0, 6, 0, 2],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [5, 0, 9, 0, 4, 3, 0, 7, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0]]
    solver = Solver(StopCallback(SolverCallback()))
    t0 = clock()
    solver.execute(grid)
    t1 = clock()
    print 'time %f' % (t1 - t0)    
    
    
