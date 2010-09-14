# -*- coding: utf-8 -*-
"""CrossWord Riddle Solver
   Assignments 2 and 3, lecture 5
   python cwr.py
"""

from time import clock
from random import sample
import sys

# We want to process words with these letters
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
        hi = 0
        top = len(list_of_words)
        # Search for subsequences of list_of_words 
        # where the words have the same k esim letter
        for each in letters:
	    lo = hi
            while hi < top and each == self.list_of_words[hi][k]:
                hi += 1
            self.index[each] = (lo, hi)

    def word_with_a_given_letter(self, letter):
        """Generator of the subsequence of list_of_words
           where the words have one given letter
        """
        lo, hi = self.index[letter]
        for word in self.list_of_words[lo:hi]:
	    yield word

    def word_with_two_given_letters(self, first, k, second):
        """Generator of the subsequence of list_of_words
           where the words have two given letters
        """
        lo, hi = self.index[first]
        for word in self.list_of_words[lo:hi]:
            if word[k] == second:
                yield word

class StopSolverException(BaseException):
    """This exception stops the solver pruning the search of solutions.
       This exception does not signal an error
    """
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
    """This objects counts solutions for a CWR
    """
    def __init__(self):
        self._counter = 0

    def add_solution(self, solution):
        self._counter += 1
        
    def counter(self):
	return self._counter

class CrossWordRiddleSolverFourWordsAnyLength(object):
    """This object searchs solutions for 4 words (any length) cross word riddles 
    """
    def __init__(self, index_array, callback):
        """Initializes searching
           index_array is an array of WordsIndex, may be with different words length
           callback for further solution processing
        """
        assert(len(index_array) == 4)
        self.index_array = index_array
        self.callback = callback

    def execute(self, word_0):
        first_letter_0 = word_0[0]
        last_letter_0 = word_0[-1]
        for word_1 in self.index_array[1].word_with_a_given_letter(first_letter_0):
	    last_letter_1 = word_1[-1]
	    for word_2 in self.index_array[2].word_with_a_given_letter(last_letter_1):
	        last_letter_2 = word_2[-1]
                for word_3 in self.index_array[3].word_with_two_given_letters(last_letter_2, 0, last_letter_0):
                    self.callback.add_solution([word_0, word_1, word_2, word_3])

class CrossWordRiddleSolverSixWords(object):
    """This object searchs solutions for 6 words cross word riddles 
    """
    def __init__(self, index_array, callback):
        """Initializes searching
           index_array is an array of WordsIndex, may be with different words length
           callback for further solution processing
        """
        assert(len(index_array) == 6)
        self.index_array = index_array
        self.callback = callback

    def execute(self, word_0):
        first_letter_0 = word_0[0]
        last_letter_0 = word_0[-1]
        for word_1 in self.index_array[1].word_with_a_given_letter(first_letter_0):
            last_letter_1 = word_1[-1]
            for word_2 in self.index_array[2].word_with_a_given_letter(last_letter_1):
                middle_letter_2 = word_2[1]
                last_letter_2 = word_2[-1]
                for word_3 in self.index_array[3].word_with_two_given_letters(last_letter_2, 0, last_letter_0):
                    for word_4 in self.index_array[4].word_with_a_given_letter(middle_letter_2):
                        last_letter_4 = word_4[-1]
                        for word_5 in self.index_array[5].word_with_a_given_letter(last_letter_4):
                            self.callback.add_solution([word_0, word_1, word_2, word_3, word_4, word_5])

def time_cwr_four_words_equal_length(
    title, 
    data,
    random_sample_size, 
    callback = StopCallback(SilentCallback())
    ):
    print title    
    
    list_of_words =  [w for w in open(data, 'r').read().split()]
    
    first_letter_index = WordsIndex(list_of_words, 0)
    last_letter_index = WordsIndex(list_of_words, -1)
    
    solver = CrossWordRiddleSolverFourWordsAnyLength(
      [first_letter_index, first_letter_index, first_letter_index, last_letter_index], 
      callback)
        
    max_time = 0.0
    t0 = clock()
    for word in sample(list_of_words, random_sample_size):
         ta = clock()	
         try:
             solver.execute(word)
         except StopSolverException:
            pass
         tb = clock()
         current = tb - ta
         if max_time < current:
             max_time = current
    t1 = clock()
    
    print 'Per solution time: max_time %2.16e' % max_time
    print '%d random initial words time, %d solutions: t1 - t0 %2.16e' % \
       (random_sample_size, solver.callback.counter(), t1 - t0)

def time_cwr_six_words_equal_length(
    title, 
    data, 
    random_sample_size, 
    callback = StopCallback(SilentCallback())
    ):
    print title    
    
    list_of_words =  [w for w in open(data, 'r').read().split()]
    
    first_letter_index = WordsIndex(list_of_words, 0)
    last_letter_index = WordsIndex(list_of_words, -1)
    middle_letter_index = WordsIndex(list_of_words, 1)
    
    solver = CrossWordRiddleSolverSixWords(
      [first_letter_index, first_letter_index, first_letter_index, 
       last_letter_index, first_letter_index, middle_letter_index], 
      callback)
        
    max_time = 0.0
    t0 = clock()
    for word in sample(list_of_words, random_sample_size):
         ta = clock()	
         try:
             solver.execute(word)
         except StopSolverException:
            pass
         tb = clock()
         current = tb - ta
         if max_time < current:
             max_time = current
    t1 = clock()
    
    print 'Per solution time: max_time %2.16e' % max_time
    print '%d random initial words time, %d solutions: t1 - t0 %2.16e' % \
       (random_sample_size, solver.callback.counter(), t1 - t0)

def time_cwr_six_words_different_length(
    title, 
    data_1, 
    data_2, 
    random_sample_size, 
    callback = StopCallback(SilentCallback())
    ):
    print title    
    
    first_list_of_words =  [w for w in open(data_1, 'r').read().split()]
    second_list_of_words =  [w for w in open(data_2, 'r').read().split()]    
    
    index_1 = WordsIndex(first_list_of_words, 0)
    index_2 = WordsIndex(second_list_of_words, 0)
    index_3 = WordsIndex(second_list_of_words, -1)
    index_4 = WordsIndex(first_list_of_words, 1)
    
    solver = CrossWordRiddleSolverSixWords(
      [index_1, index_2, index_1, index_3, index_1, index_4], 
      callback)
        
    max_time = 0.0
    t0 = clock()
    for word in sample(first_list_of_words, random_sample_size):
         ta = clock()	
         try:
             solver.execute(word)
         except StopSolverException:
            pass
         tb = clock()
         current = tb - ta
         if max_time < current:
             max_time = current
    t1 = clock()
    
    print 'Per solution time: max_time %2.16e' % max_time
    print '%d random initial words time, %d solutions: t1 - t0 %2.16e' % \
       (random_sample_size, solver.callback.counter(), t1 - t0)

RANDOM_SAMPLE_SIZE = 500

if __name__ == '__main__':
    time_cwr_four_words_equal_length(
        title = '3 x 3 CrossWord Riddle Solver', 
        data = 'words_3.txt', 
        random_sample_size = RANDOM_SAMPLE_SIZE,
        callback = StopCallback(SilentCallback())
    )  
    time_cwr_four_words_equal_length(
        title = '4 x 4 CrossWord Riddle Solver', 
        data = 'words_4.txt', 
        random_sample_size = RANDOM_SAMPLE_SIZE, 
        callback = StopCallback(SilentCallback())
    )  
    time_cwr_six_words_equal_length(
        title = '3 x 5 CrossWord Riddle Solver', 
        data = 'words_3.txt', 
        random_sample_size = RANDOM_SAMPLE_SIZE, 
        # you may change the following line to callback = StopCallback(PrintCallback())        
        callback = StopCallback(SilentCallback())
    )  
    time_cwr_six_words_different_length(
    title = '3 x 5 CrossWord Riddle Solver',  
    data_1 = 'words_3.txt',
    data_2 = 'words_4.txt',
    random_sample_size = RANDOM_SAMPLE_SIZE, 
    callback = StopCallback(SilentCallback())
    )
