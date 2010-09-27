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
    
class Node(object):
    def __init__(self, node = None, grid = None):
        self.grid = [[0, 0, 0], [0, 0, 0], [0, 0, 0]] if grid == None else grid	
        if node == None:
            self.parent = None
            self.depth = 0
        else:
            self.parent = node
            self.depth = node.depth + 1

    def show(self):
        for r in range(3):
            print repr(self.grid[r])

class Solver(object):
    def __init__(self, callback = SolverCallback()):
        self.visited = list()
        self.callback = callback
        
    def is_a_solution(self, candidate):
        return candidate.depth == 9

    def execute(self, grid):
        initial = Node()
        try:
            self.generate_tree(initial)
        except StopSolverException:
            pass

    def free_cell(self, grid):
        for r in range(3):
            for c in range(3):
                if 0 == grid[r][c]:
                    yield (r, c)

    def generate_tree(self, node):
        if self.is_a_solution(node):
            self.callback.execute(node)
        else:
            for update in self.possible_updates(node):
                 self.generate_tree(Node(node, update))

    def possible_updates(self, node):
        for cell in self.free_cell(node.grid):
            for number in range(1, 4):
                if self.verify(number, cell, node.grid):
                    new_grid = copy.deepcopy(node.grid)
                    new_grid[cell[0]][cell[1]] = number
                    yield new_grid

    def verify(self, number, cell, grid):
        for i in range(3):
            if (number == grid[cell[0]][i]) or (number == grid[i][cell[1]]):
                return False
        return True        


if __name__ == '__main__':
    solver = Solver(StopCallback(SolverCallback()))
    root = Node()
    root.grid[1][0] = 1
    root.grid[0][2] = 3
    solver.execute(root)
