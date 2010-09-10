# -*- coding: utf-8 -*-
"""CrossWord Riddle Solver
--data filename
"""


# Wa want to process words with these letters
letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

class WordsIndex(object):
    """
       This object keeps a sorted list of words and 
       a dictionary for fast searching words by a fixed letter
    """
    def __init__(self, list_of_words, k = 0):
        self.list_of_words = sorted(list_of_words, cmp = lambda x, y: cmp(x[k], y[k]))
        self.index = {}
        # lo and hi are indexes for list_of_words
        lo = 0
        hi = lo
        top = len(list_of_words)
        # Search for each subsequence of list_of_words 
        # where the words have the same k esim letter
        for l in letters:
            while hi < top and l == self.list_of_words[hi][k]:
                hi += 1
            self.index[l] = (lo, hi)
            lo = hi

    def word_with_a_given_letter(self, letter):
        """Generator of the subsequence of list_of_words
           where the words have one given letter
        """
        lo, hi = self.index[letter]
        for i in xrange(lo, hi):
            yield self.list_of_words[i]

    def word_with_two_given_letters(self, first, k, second):
        """Generator of the subsequence of list_of_words
           where the words have two given letters
        """
        lo, hi = self.index[first]
        for i in xrange(lo, hi):
            word = self.list_of_words[i]
            if word[k] == second:
                yield word

import pdb

class Callback_3x3(object):
    """This objects stores solutions in a tree of dictionaries
    """
    def __init__(self):
        self.counter = 0

    def add_solution(self, solution):
        print ', '.join(solution)
        self.counter += 1

class Callback_3x5(object):
    """This objects stores solutions in a tree of dictionaries
    """
    def __init__(self, first_letter_index, second_letter_index):
        self.counter = 0
        self.first_letter_index = first_letter_index
        self.second_letter_index = second_letter_index        

    def add_solution(self, solution):
	# pdb.set_trace()
	# print '* %s' % ', '.join(solution)
	word = solution[-2]
        for w1 in self.first_letter_index.word_with_a_given_letter(word[1]):
	    solution.append(w1)
            for w2 in self.second_letter_index.word_with_a_given_letter(w1[-1]):
                solution.append(w2)
                print ', '.join(solution)
                self.counter += 1
                solution.pop()
            solution.pop()

class CrossWordRiddleSolver(object):
    """This object solves the riddle searching solutions.
       It can be used to get all possible solutions.
       It uses callback for further processing
    """
    def __init__(self, list_of_words, index, callback):
        """Initializes searching
           list_of_words may be a non sorted list of any length words
           search_max_depth specifies the length of the solution, also
        """
        self.index = index
        self.callback = callback
        self.search_max_depth = 3
        

    def execute(self, solution, letter):
	"""Recursive search
	   len(solution) <= self.search_max_depth
	"""
        if len(solution) < self.search_max_depth:
            for word in self.index.word_with_a_given_letter(letter):
                new_solution = list(solution)
                new_solution.append(word)
                self.execute(new_solution, word[-1])
        elif len(solution) == self.search_max_depth:
            for word in self.index.word_with_two_given_letters(solution[0][-1], -1, letter):
                solution.append(word)
                self.callback.add_solution(solution)
                solution.pop()
        else:
            raise ValueError('partial solution longer than expected.')

from time import clock
from random import sample

def evaluate_solutions(data, random_sample_size):
    # The following line is shameless copied from http://github.com/llimllib work
    # at http://github.com/llimllib/personal_code/blob/master/python/reddit_ai_101/lecture_4/betterxword.py#L1
    # Thanks llimllib
    list_of_words =  [w for w in open(data, 'r').read().split()]

    first_letter_index = WordsIndex(list_of_words, 0)
    second_letter_index = WordsIndex(list_of_words, 1)
    
    solver_3x3 = CrossWordRiddleSolver(list_of_words, first_letter_index, Callback_3x3())

    t0_3x3 = clock()
    # Generating all possible solutions
    for word in sample(list_of_words, random_sample_size):
         solver_3x3.execute([word], word[0])
    t1_3x3 = clock()
    
    solver_3x5 = CrossWordRiddleSolver(
       list_of_words, 
       first_letter_index, 
       Callback_3x5(first_letter_index, second_letter_index))


    t0_3x5 = clock()
    # Generating all possible solutions
    for word in sample(list_of_words, random_sample_size):
        solver_3x5.execute([word], word[0])
    t1_3x5 = clock()
    
    print '3x3 counter %d' % solver_3x3.callback.counter
    print '3x3 timer %d' % t1_3x3 - t0_3x3
    
    print '3x5 %d' % solver_3x5.callback.counter
    print '3x5 timer %d' % t1_3x5 - t0_3x5    
    
import sys

# 
# <insert code to time>
# runtime = clock() - t1

if __name__ == '__main__':
    if len(sys.argv) != 2:
	print 'Error!'
    else:
        data = sys.argv[1]
	evaluate_solutions(data, 1)