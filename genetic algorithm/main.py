import genome, evolution, sudoku
import numpy as np
from random import choice

init_vect = sum([list(range(1,10))] * 9, []) # A vector of 81 elements

"""

# To test a random genome in the start

puzzle = sudoku.PUZZLE
DIM = 9

def randomlyFillRows(sudoku):
    for row in range(0, DIM):
        for col in range(0, DIM):
            if(sudoku[row][col] == 0):
                randomNumber = choice([i for i in range(1,DIM+1) if i not in sudoku[row]])
                sudoku[row][col] = randomNumber
                #print(sudoku[row])
                #print("\n__________")

    return sudoku

init_vect = randomlyFillRows(puzzle)
init_vect = sum(init_vect, [])
"""

genome = genome.Genome(init_vect)

solver = evolution.Evolution(sudoku.ga_sudoku(sudoku.PUZZLE), genome)

solver.evolve(target_fitness = 0)
