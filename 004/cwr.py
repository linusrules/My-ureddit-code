# -*- coding: utf-8 -*-
"""Module docstring.

--data filename
"""


# Wa want to process words with these letters
letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

class LegalWords(object):
    """
       This object keeps a sorted list of words and 
       a dictionary for fast searching words 
          by the initial letter
          by the initial and final letters
    """
    def __init__(self, list_of_words):
        self.list_of_words = sorted(list_of_words)
        self.initials = {}
        # lo and hi are indexes for list_of_words
        lo = 0
        hi = lo
        top = len(list_of_words)
        # Search for each subsequence of list_of_words 
        # where the words have the same initial letter
        for l in letters:
            while hi < top and l == list_of_words[hi][0]:
                hi += 1
            self.initials[l] = (lo, hi)
            lo = hi

    def by_initial_letter(self, initial):
        """Generator of the subsequence of list_of_words
           where the words have the same initial letter
        """
        lo, hi = self.initials[initial]
        for i in xrange(lo, hi):
            yield self.list_of_words[i]

    def by_initial_and_final_letter(self, initial, final):
        """Generator of the subsequence of list_of_words
           where the words have the same initial
           and final letters
        """
        lo, hi = self.initials[initial]
        for i in xrange(lo, hi):
            word = self.list_of_words[i]
            if word[-1] == final:
                yield word

class ForestCallbackSolver(object):
    """This objects stores solutions in a tree of dictionaries
    """
    def __init__(self):
        self.forest = dict()
        self.counter = 0

    def __add_solution(self, solution, level):
        if len(solution) > 1:
           word = solution[0]
           if word not in level.keys():
               level[word] = dict()
           self.__add_solution(solution[1:], level[word])
        elif len(solution) == 1:
           word = solution[0]
           if word not in level.keys():
               level[word] = None


    def add_solution(self, solution):
        self.counter += 1
        self.__add_solution(solution, self.forest)


class PrintCallbackSolver(object):
    def __init__(self):
        self.counter = 0

    def add_solution(self, solution):
	self.counter += 1
        print ', '.join(solution)
        
    def print_stats(self):
	print '%d solutions!' % self.counter
        
class CrossWordRiddleSolver(object):
    """This object solves the riddle searching solutions.
       It can be used to get all possible solutions.
       It uses callback for further processing
    """
    def __init__(self, list_of_words, search_max_depth, callback):
        """Initializes searching
           list_of_words may be a non sorted list of any length words
           search_max_depth specifies the length of the solution, also
        """
        self.legal_words = LegalWords(list_of_words)
        self.search_max_depth = search_max_depth
        self.callback = callback

    def execute(self, partial_solution, letter):
	"""Recursive search
	   len(partial_solution) <= self.search_max_depth
	"""
        if len(partial_solution) < self.search_max_depth:
            for word in self.legal_words.by_initial_letter(letter):
                new_partial_solution = list(partial_solution)
                new_partial_solution.append(word)
                self.execute(new_partial_solution, word[-1])
        elif len(partial_solution) == self.search_max_depth:
            for word in self.legal_words.by_initial_and_final_letter(partial_solution[0][-1], letter):
                solution = list(partial_solution)
                solution.append(word)
                self.callback.add_solution(solution)
                print ', '.join(solution)
        else:
            raise ValueError('partial solution longer than expected.')
        
def evaluate_solutions(data, search_max_depth = 3, callback = PrintCallbackSolver()):
    # The following line is shameless copied from http://github.com/llimllib work
    # at http://github.com/llimllib/personal_code/blob/master/python/reddit_ai_101/lecture_4/betterxword.py#L1
    # Thanks llimllib
    list_of_words =  [w for w in open(data, 'r').read().split()]
    
    solver = CrossWordRiddleSolver(list_of_words, search_max_depth, callback)
    
    # Generating all possible solutions
    for word in list_of_words:
        solver.execute([word], word[0])
        
    callback.print_stats()
        
import sys

if __name__ == '__main__':
    if len(sys.argv) != 2:
	print 'We need some file with words'
	print 'For example'
	print '    python cwr.py words.txt'
    else:
	evaluate_solutions(sys.argv[1])