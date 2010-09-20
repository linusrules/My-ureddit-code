# -*- coding: utf-8 -*-
import copy

class StopSolverException(BaseException):
    """This exception stops the solver pruning the search.
       This exception does not signal an error
    """
    pass

class Solver(object):
    def __init__(self):
        self.visited = list()
        
    def is_a_solution(self, candidate):
        return (candidate[0][0] + candidate[0][1] + candidate[0][2]) == 0

    def execute(self):
        initial = [[3, 3, 1], [0, 0, 0]]
        self.visited.append(initial)
        try:
            self.generate_tree(initial)
        except StopSolverException:
            for move in self.visited:
                print 'Missionaries %-2d Cannibals %-2d Boat %-2d:----: Missionaries %-2d Cannibals %-2d Boat %-2d' % \
                    (move[0][0], move[0][1], move[0][2],
                     move[1][0], move[1][1], move[1][2])

    def generate_tree(self, partial_solution):
        if self.is_a_solution(partial_solution):
            raise StopSolverException()
        else:
            for move in self.possible_moves(partial_solution):
                 self.visited.append(move)
                 self.generate_tree(move)
                 self.visited.pop()

    def possible_moves(self, partial_solution):
        moves = []
        if partial_solution[0][2] == 1:
            side = 0
            other_side = 1
        else:
            side = 1
            other_side = 0
        for cannibals in range(0, min(2, partial_solution[side][1]) + 1):
            for missionaries in range(0, min(2 - cannibals, partial_solution[side][0]) + 1):
                if cannibals + missionaries > 0:
                    new_partial_solution = copy.deepcopy(partial_solution)		
                    new_partial_solution[side][0] -= missionaries
                    new_partial_solution[side][1] -= cannibals
                    new_partial_solution[side][2] = 0
                    new_partial_solution[other_side][0] += missionaries
                    new_partial_solution[other_side][1] += cannibals
                    new_partial_solution[other_side][2] = 1
                    if self.check_riversides(new_partial_solution) and \
                       (new_partial_solution not in moves) and \
                       (new_partial_solution not in self.visited):
                        moves.append(new_partial_solution)
        return moves

    def check_riversides(self, candidate):
        for side in candidate:
            if (side[0] > 0) and (side[0] < side[1]):
                return False
        return True
        
if __name__ == '__main__':
    solver = Solver()
    solver.execute()