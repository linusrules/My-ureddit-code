# -*- coding: utf-8 -*-
import copy

SHEPHERD = "Shepherd"
CABBAGE  = "Cabbage"
WOLF     = "Wolf"
SHEEP    = "Sheep"
EMPTY    = ""

class StopSolverException(BaseException):
    """This exception stops the solver pruning the search of solutions.
       This exception does not signal an error
    """
    pass

class Solver(object):
    def __init__(self):
        self.visited = list()
        
    def is_a_solution(self, candidate):
        return candidate[0].count(EMPTY) == 4

    def execute(self):
        initial = [[SHEPHERD, CABBAGE, SHEEP, WOLF], [EMPTY, EMPTY, EMPTY, EMPTY]]
        self.visited.append(initial)
        try:
            self.generate_tree(initial)
        except StopSolverException:
            for move in self.visited:
                print '%-10s %-10s %-10s %-10s :----: %-10s %-10s %-10s %-10s' % \
                    (move[0][0], move[0][1], move[0][2], move[0][3], 
                     move[1][0], move[1][1], move[1][2], move[1][3])

    def generate_tree(self, partial_solution):
        if self.is_a_solution(partial_solution):
            raise StopSolverException()
        else:    
            for move in self.possible_moves(partial_solution):
                if move not in self.visited:
                    self.visited.append(move)
                    self.generate_tree(move)

    def possible_moves(self, partial_solution):
        moves = []
        if SHEPHERD in partial_solution[0]:
             side = 0
             other_side = 1
        else:
             side = 1
             other_side = 0
        for figure in range(1, 4):
             if partial_solution[side][figure] != EMPTY:
                 new_partial_solution = copy.deepcopy(partial_solution)
                 new_partial_solution[other_side][figure] = partial_solution[side][figure]
                 new_partial_solution[side][figure] = EMPTY
                 new_partial_solution[other_side][0] = SHEPHERD
                 new_partial_solution[side][0] = EMPTY
                 if self.check_riversides(new_partial_solution) and (new_partial_solution not in moves):
                     moves.append(new_partial_solution)
        new_partial_solution = copy.deepcopy(partial_solution)
        new_partial_solution[other_side][0] = SHEPHERD
        new_partial_solution[side][0] = EMPTY
        if self.check_riversides(new_partial_solution) and (new_partial_solution not in moves):
            moves.append(new_partial_solution)
        return moves

    def check_riversides(self, river):
        for side in river:
            if (SHEEP in side) and (SHEPHERD not in side):
                if ((WOLF in side) or (CABBAGE in side)):
                    return False
        return True
        
if __name__ == '__main__':
    solver = Solver()
    solver.execute()