"""This module contains a fitness function for sudoku puzzles.
It is specialized for 9x9 puzzles, but could be extended to 4x4, 16x16, 25x25,
etc, by making DIM a parameter and fixing one_box and boxes.

To use this module, you want to call either sudoku_fitness or ga_sudoku.

An example puzzle and solution is provided in PUZZLE and SOLUTION.
"""

import math
from os import system, name

# The dimension of the puzzle
DIM = 9
BOX_SIZE = int(math.sqrt(DIM))

# A sudoku puzzle for test
PUZZLE = [[0, 0, 4, 8, 0, 0, 0, 1, 7],
          [6, 7, 0, 9, 0, 0, 0, 0, 0],
          [5, 0, 8, 0, 3, 0, 0, 0, 4],
          [3, 0, 0, 7, 4, 0, 1, 0, 0],
          [0, 6, 9, 0, 0, 0, 7, 8, 0],
          [0, 0, 1, 0, 6, 9, 0, 0, 5],
          [1, 0, 0, 0, 8, 0, 3, 0, 6],
          [0, 0, 0, 0, 0, 6, 0, 9, 1],
          [2, 4, 0, 0, 0, 1, 5, 0, 0]]


# The solution of the puzzle
SOLUTION = [[9, 3, 4, 8, 2, 5, 6, 1, 7],
            [6, 7, 2, 9, 1, 4, 8, 5, 3],
            [5, 1, 8, 6, 3, 7, 9, 2, 4],
            [3, 2, 5, 7, 4, 8, 1, 6, 9],
            [4, 6, 9, 1, 5, 3, 7, 8, 2],
            [7, 8, 1, 2, 6, 9, 4, 3, 5],
            [1, 9, 7, 5, 8, 2, 3, 4, 6],
            [8, 5, 3, 4, 7, 6, 2, 9, 1],
            [2, 4, 6, 3, 9, 1, 5, 7, 8]]

def one_box(solution, i):
    tempbox = [] 
    box = []
    for j in range(BOX_SIZE):
        tempbox.append(solution[i + j*DIM : i + j*DIM + BOX_SIZE])
    for i in range(BOX_SIZE):
        for j in range(BOX_SIZE):
            box.append(tempbox[i][j])
    return box

def boxes(solution):
    # boxes = [[0 for x in range(DIM)] for y in range(DIM)] # initialize array
    boxesarray = []
    k = 0
    z = 0
    for i in range(DIM):
        boxesarray.append(one_box(solution, k))
        k += BOX_SIZE
        z += 1
        if z == BOX_SIZE:  
            k += DIM
            k += DIM
            z = 0
    return boxesarray

def splitup(solution):
    """return a 2d vector with dim rows and dim elements each row"""
    return [solution[i * DIM:(i+1) * DIM] for i in range(DIM)]

def consistent(solution):
    """How many different elements in each row"""

    return sum(DIM - len(set(row)) for row in solution) # A set can never have duplicates -> set(row) is row without duplicates, if it has duplicates, len(set(row)) is inferior than DIM and it gets added

def compare(xs1, xs2):
    """Compare two flat vectors and return how much they differ. 
    Zeroes are not compared for xs1 (to check the difference from the "blocked" values of the sudoku)"""

    return sum(1 if x1 and x1 != 0 and x1 != x2 else 0 for x1, x2 in zip(xs1, xs2))

def sudoku_fitness(flatsolution, puzzle, flatpuzzle=None):
    """Evaluate fitness of a flatsolution
    
    @param puzzle: the starting puzzle, 0 is unknown
    """

    if not flatpuzzle: 
        flatpuzzle = sum(puzzle, []) # Better if precalculated


    solution = splitup(flatsolution)
    fitness = consistent(solution)
    fitness += consistent(zip(*solution)) # zip(*solution) unpacks 2d solution vector and zips it -> inverts rows and columns and zips it, in order to check columns as if they were rows with the consistent() function
    fitness += consistent(boxes(flatsolution))
    fitness += compare(flatpuzzle, flatsolution) * 10 # Multiply by factor 10 the differences from the starting empty puzzle
    
    return fitness

def print_sudoku(board):

    print("-" * int(DIM * 3.5))

    for i, row in enumerate(board):
        if i%BOX_SIZE == 0 and i != 0:
            print("|", end="")
            print(("-"*(3*BOX_SIZE) + "|")*BOX_SIZE)
        
        print("|", end="")
        for j in range(BOX_SIZE):
            print((" {} "*BOX_SIZE).format(*[x if x != 0 else " " for x in row[j*BOX_SIZE : j*BOX_SIZE+BOX_SIZE]]), end="")
            print("|", end="")
        print()
    print("-" * int(DIM * 3.5))   

def clear():
    # for windows
    if name == 'nt':
        _ = system('cls')
    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')

def ga_sudoku(puzzle):
    """fitness function wrapper that extracts genes from an individual and sends it to sudoku_fitness."""

    flatpuzzle = sum(puzzle, []) # precalculation for performance
    def fit(guy):
        """GA wrapper for sudoku_fitness"""
        return sudoku_fitness(guy.genes, puzzle, flatpuzzle)

    return fit
    



