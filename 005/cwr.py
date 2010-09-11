# -*- coding: utf-8 -*-
"""CrossWord Riddle Solver
python cwr.py words.txt 500 scrabble.txt 500
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

class StopSolverException(BaseException):
      pass

class StopCallback(object):
    def __init__(self, callback):
	self.callback = callback

    def add_solution(self, solution):
	self.callback.add_solution(solution)
        raise StopSolverException()        

    def counter(self):
	return self.callback.counter()

class PrintCallback(object):
    """This objects prints solutions for a CWR
    """
    def __init__(self):
        self._counter = 0

    def add_solution(self, solution):
        print ', '.join(solution)
        self._counter += 1
        
    def counter(self):
	return self._counter

class SilentCallback(object):
    """This objects prints solutions for a CWR
    """
    def __init__(self):
        self._counter = 0

    def add_solution(self, solution):
        self._counter += 1
        
    def counter(self):
	return self._counter

class Callback_3x5(object):
    """This objects evaluates solutions for a 3x5 CWR
    """
    def __init__(self, first_letter_index, second_letter_index, callback = PrintCallback()):
        self.first_letter_index = first_letter_index
        self.second_letter_index = second_letter_index
        self.callback = callback

    def add_solution(self, solution):
        word = solution[-2]
        for w1 in self.first_letter_index.word_with_a_given_letter(word[1]):
            solution.append(w1)
            for w2 in self.second_letter_index.word_with_a_given_letter(w1[-1]):
                solution.append(w2)
                self.callback.add_solution(solution)
                solution.pop()
            solution.pop()

    def counter(self):
	return self.callback.counter()

class Callback_VLW(object):
    """This objects evaluates solutions for a VLW CWR
    """
    def __init__(self, first_letter_index, second_letter_index, callback = PrintCallback()):
        self.first_letter_index = first_letter_index
        self.second_letter_index = second_letter_index
        self.callback = callback

    def add_solution(self, solution):
        word = solution[-2]
        for w1 in self.first_letter_index.word_with_a_given_letter(word[1]):
            solution.append(w1)
            for w2 in self.second_letter_index.word_with_a_given_letter(w1[-1]):
                solution.append(w2)
                self.callback.add_solution(solution)
                solution.pop()
            solution.pop()

    def counter(self):
	return self.callback.counter()

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

def evaluate_solutions_3x3_and_3x5(data, random_sample_size):
    list_of_words =  [w for w in open(data, 'r').read().split()]

    first_letter_index = WordsIndex(list_of_words, 0)
    second_letter_index = WordsIndex(list_of_words, 1)
    
    solver_3x3 = CrossWordRiddleSolver(
        list_of_words, 
        first_letter_index, 
        StopCallback(SilentCallback()))

    max_3x3 = 0.0
    min_3x3 = 10.0
    tstart_3x3 = clock()
    for word in sample(list_of_words, random_sample_size):
         t0_3x3 = clock()	
         try:
             solver_3x3.execute([word], word[0])
         except StopSolverException:
            pass
         t1_3x3 = clock()
         current = (t1_3x3 - t0_3x3)
         if max_3x3 < current:
             max_3x3 = current
         if min_3x3 > current:
             min_3x3 = current
    tstop_3x3 = clock()
    
    solver_3x5 = CrossWordRiddleSolver(
       list_of_words, 
       first_letter_index, 
       StopCallback(
           Callback_3x5(
               first_letter_index, 
               second_letter_index, 
               SilentCallback())))

    max_3x5 = 0.0
    min_3x5 = 10.0
    tstart_3x5 = clock()
    for word in sample(list_of_words, random_sample_size):
         t0_3x5 = clock()	     	
	 try:
             solver_3x5.execute([word], word[0])
         except StopSolverException:
            pass
         t1_3x5 = clock()
         current = (t1_3x5 - t0_3x5)
         if max_3x5 < current:
             max_3x5 = current
         if min_3x5 > current:
             min_3x5 = current
    tstop_3x5 = clock()
    
    print '3x3 min %2.16e - max %2.16e' % (min_3x3, max_3x3)
    print '3x3 tstop - tstart %2.16e' % (tstop_3x3 - tstart_3x3)
    print '3x3 solutions %d' % solver_3x3.callback.counter()
    print '3x5 min %2.16e - max %2.16e' % (min_3x5, max_3x5)
    print '3x5 tstop - tstart %2.16e' % (tstop_3x5 - tstart_3x5)    
    print '3x5 solutions %d' % solver_3x5.callback.counter()    

def evaluate_solutions_4x4(data, random_sample_size):
    list_of_words =  [w for w in open(data, 'r').read().split()]

    first_letter_index = WordsIndex(list_of_words, 0)
    second_letter_index = WordsIndex(list_of_words, 1)
    
    solver_4x4 = CrossWordRiddleSolver(
        list_of_words, 
        first_letter_index, 
        StopCallback(PrintCallback()))

    max_4x4 = 0.0
    min_4x4 = 10.0
    tstart_4x4 = clock()
    for word in sample(list_of_words, random_sample_size):
         t0_4x4 = clock()	
         try:
             solver_4x4.execute([word], word[0])
         except StopSolverException:
            pass
         t1_4x4 = clock()
         current = (t1_4x4 - t0_4x4)
         if max_4x4 < current:
             max_4x4 = current
         if min_4x4 > current:
             min_4x4 = current
    tstop_4x4 = clock()
    
    print '4x4 min %2.16e - max %2.16e' % (min_4x4, max_4x4)
    print '4x4 tstop - tstart %2.16e' % (tstop_4x4 - tstart_4x4)
    print '4x4 solutions %d' % solver_4x4.callback.counter()

def evaluate_solutions_variable_length_words(list_of_words, random_sample_size):

    first_letter_index = WordsIndex(list_of_words, 0)
    second_letter_index = WordsIndex(list_of_words, 1)
    
    solver_vlw = CrossWordRiddleSolver(
       list_of_words, 
       first_letter_index, 
       StopCallback(
           Callback_VLW(
               first_letter_index, 
               second_letter_index, 
               StopCallback(PrintCallback()))))

    max_vlw = 0.0
    min_vlw = 10.0
    tstart_vlw = clock()
    for word in sample(list_of_words, random_sample_size):
         t0_vlw = clock()	
         try:
             solver_vlw.execute([word], word[0])
         except StopSolverException:
            pass
         t1_vlw = clock()
         current = (t1_vlw - t0_vlw)
         if max_vlw < current:
             max_vlw = current
         if min_vlw > current:
             min_vlw = current
    tstop_vlw = clock()
    
    print 'vlw min %2.16e - max %2.16e' % (min_vlw, max_vlw)
    print 'vlw tstop - tstart %2.16e' % (tstop_vlw - tstart_vlw)
    print 'vlw solutions %d' % solver_vlw.callback.counter()

import sys

if __name__ == '__main__':
    if len(sys.argv) != 5:
	print 'Error! I need four parameters: two pair of (a file with words and a random sample size)'
    else:
        data_3 = sys.argv[1]
        random_sample_size_3 = int(sys.argv[2])
	evaluate_solutions_3x3_and_3x5(data_3, random_sample_size_3)
        data_4 = sys.argv[3]
        random_sample_size_4 = int(sys.argv[4])
	evaluate_solutions_4x4(data_4, random_sample_size_4)
	
	vlw =  [w for w in open(data_3, 'r').read().split()]
	vlw.extend([w for w in open(data_4, 'r').read().split()])
	
	evaluate_solutions_variable_length_words(vlw, min(random_sample_size_3, random_sample_size_4))