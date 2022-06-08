import random
import numpy as np
import math
from random import choice
import statistics
import time

import sudokuprint

# The dimension of the puzzle
#DIM = 9
#BOX_SIZE = 3

DIM = 9
BOX_SIZE = 3

BIGPUZZLE = [0, 15, 2, 10, 7, 0,0,0,0,0,0,8,13,0,16,3,0,3,5,0,8,0,0,0,12,0,7,0,2,0,0,0,0,0,0,0,0,0,0,0,0,4,0,13,0,0,10,0,0,0,0,0,3,0,0,4,0,0,2,0,0,6,12,9,11,0,0,0,0,0,0,2,4,7,3,0,0,10,0,1,6,0,0,5,4,0,0,11,0,0,0,0,0,0,0,0,0,13,0,2,0,0,0,5,0,0,0,0,15,12,0,0,0,0,3,16,0,0,8,0,9,13,0,6,0,0,5,0,0,0,10,3,0,15,7,6,0,0,12,0,16,0,0,0,0,0,9,0,5,11,14,0,0,0,0,0,12,4,13,0,12,0,0,0,0,0,0,0,0,15,10,4,3,11,2,0,0,11,0,14,0,0,0,0,7,0,0,0,10,5,0,0,0,0,0,0,0,7,0,3,8,5,0,0,0,13,0,6,2,0,0,4,0,0,0,0,15,12,0,3,0,0,0,0,0,5,14,15,0,0,4,0,13,0,0,0,0,0,0,0,0,0,7,0,9,0,12,0,0,6,0,11,0,2,8,0]

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

FLATPUZZLE = """004800017
                670900000
                508030004
                300740100
                069000780
                001069005
                100080306
                000006091
                240001500"""

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

def splitup(sudoku):
    """Take a flat vector and make it 2D
    
    @param solution: A flat vector with DIM * DIM elements
    
    @return: A 2D vector with DIM rows and DIM elements for each row.
    """

    return [sudoku[i * DIM:(i+1) * DIM] for i in range(DIM)]

def flatten(sudoku):
    """Take a 2D vector and make it flat
    
    @param solution: A 2D vector with DIM rows and DIM elements for each row. DIM * DIM elements
    
    @return: A flat vector with DIM * DIM elements
    """
    # z = 0
    flatpuzzle = []
    for i in range(0,DIM):
        for j in range(0,DIM):
            flatpuzzle.append(sudoku[i][j])
            # z += 1
    return flatpuzzle

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


def print_sudoku2(board):
    print("-"*math.trunc(DIM*37/9))
    for i, row in enumerate(board):
        print(("|" + " {}   {}   {} |"* math.trunc(DIM/BOX_SIZE) ).format(*[x if x != 0 else " " for x in row]))
        if i == DIM - 1:
            print("-"*math.trunc(DIM*37/9))
        elif i % 3 == 2:
            print("|" + "---+"*(DIM -1) + "---|")
        else:
            print("|" + "   +"* (DIM -1) + "   |")

def FixSudokuValues(fixed_sudoku):
    for i in range (0,DIM):
        for j in range (0,DIM):
            if fixed_sudoku[i][j] != 0:
                fixed_sudoku[i][j] = 1
    
    return(fixed_sudoku)


def consistent(sudoku):
    """Check how many different elements there are in each row.
    
    Ideally there should be DIM different elements, if there are no duplicates.
    
    @param solution: A DIM x DIM 2D vector with a puzzle
    
    @return: The sum of duplicates in each row
    """
    return sum(DIM - len(set(row)) for row in sudoku) # A set can never have duplicates -> set(row) is row without duplicates, if it has duplicates, len(set(row)) is inferior than DIM and it gets added
     
def boxes(sudoku):
    """Divide a flat vector into vectors with 9 elements, representing 3 x 3
    Boxes in the corresponding 9 x 9 2D vector. These are the standard sudoku boxes.
    
    @param sudoku: A 9 x 9 2D vector, containing a sudoku solution
    
    @return: A vector of vectors with 9 elements, representing sudoku boxes.
    """
    boxes = []
    for i in range(0, DIM):
        box = []
        for j in range(0,BOX_SIZE):
            for k in range(0,BOX_SIZE):
                box.append(sudoku[j+BOX_SIZE*((i)%BOX_SIZE)][k + BOX_SIZE*math.trunc((i)/BOX_SIZE)])
        boxes.append(box)
    return boxes


# Cost function
def numberOfErrors(sudoku):
    """Calculates the number of errors inside the sudoku
    
    @param sudoku: A flat vector, containing a sudoku solution
    
    @return: The number of errors
    """

    flatsolution = flatten(sudoku)
    
    numberOfErrors = 0
    # The rows are automatically checked at the moment of creation
    numberOfErrors = consistent(sudoku) 
    numberOfErrors += consistent(zip(*sudoku)) # zip(*solution) unpacks 2d solution vector and zips it -> inverts rows and columns and zips it, in order to check columns as if they were rows with the consistent() function
    numberOfErrors += consistent(boxes(sudoku))

    return numberOfErrors

def randomlyFillRows(sudoku):
    for row in range(0, DIM):
        for col in range(0, DIM):
            if(sudoku[row][col] == 0):
                randomNumber = choice([i for i in range(1,DIM+1) if i not in sudoku[row]])
                sudoku[row][col] = randomNumber
                print(sudoku[row])
                print("\n__________")

    return sudoku

def flipRandomBoxes(sudoku, fixedSudoku):
    valid = False
    proposedSudoku = np.copy(sudoku)
    randomRow = choice([i for i in range(0,DIM)])
    fixedNumbers = 0
    for col in range(0, DIM) :
        fixedNumbers += fixedSudoku[randomRow][col]
    # If the fixed numbers are 7 or more it doesn't make sense to swap and returns the base sudoku
    if fixedNumbers > DIM-2:
        return (sudoku, [0,0], [0,0]) # the boxes swapped are the same box to leave it as the beginning sudoku

    firstBox = choice([i for i in range(0,DIM) if fixedSudoku[randomRow][i] != 1])
    secondBox = choice([i for i in range(0,DIM) if i != firstBox and fixedSudoku[randomRow][i] != 1])
        
    tmp = proposedSudoku[randomRow, firstBox]
    proposedSudoku[randomRow, firstBox] = proposedSudoku[randomRow, secondBox]
    proposedSudoku[randomRow, secondBox] = tmp

    return (proposedSudoku, [randomRow, firstBox], [randomRow, secondBox])

def calculateInitialSigma(sudoku, fixedSudoku):
    listOfDifferences = []
    tmpSudoku = np.copy(sudoku)
    print_sudoku(tmpSudoku)
    for i in range(0,DIM):
        tmpSudoku = flipRandomBoxes(tmpSudoku, fixedSudoku)[0]
        listOfDifferences.append(numberOfErrors(tmpSudoku))
    # The sigma is calculated as the standard deviation of the errors of n randomly generated states where n is the sudoku dimension
    return (statistics.pstdev(listOfDifferences))

def chooseNewState(currentSudoku, fixedSudoku, sigma):
    proposal = flipRandomBoxes(currentSudoku, fixedSudoku)
    newSudoku = proposal[0]
    firstCoordinate = [proposal[1][0], proposal[1][1]]
    secondCoordinate = [proposal[2][0], proposal[2][1]]
    currentCost = numberOfErrors(currentSudoku)
    newCost = numberOfErrors(newSudoku)
    costDifference = newCost - currentCost
    rho = math.exp(-costDifference/sigma)
    if(np.random.uniform(1,0,1) < rho):
        return ([newSudoku, costDifference])
    return ([currentSudoku, 0])
    
def chooseNumberOfIterations(fixedSudoku):
    numberOfIterations = 0
    for i in range(0, DIM):
        for j in range (0, DIM):
            if fixedSudoku[i][j] != 0:
                numberOfIterations += 1
    return numberOfIterations

sudoku = []
"""
for i in range(0,DIM):
    for j in range(0,DIM):
        sudoku[i][j] = BIGPUZZLE[i+(j%16)]
"""
#sudoku = splitup(BIGPUZZLE)
sudoku = np.copy(PUZZLE)

# sudoku = np.array([[int(i) for i in line] for line in FLATPUZZLE.split()])

print_sudoku(sudoku)

f = open("results.txt", "a")
f2 = open("results_time.txt", "a")
start = time.time()
solutionFound = False
decreaseFactor = 0.99
stuckCount = 0
fixedSudoku = np.copy(sudoku)
fixedSudoku = FixSudokuValues(fixedSudoku)
sudoku = randomlyFillRows(sudoku)
sigma = calculateInitialSigma(sudoku, fixedSudoku)
score = numberOfErrors(sudoku)
iterations = chooseNumberOfIterations(sudoku)
if score <= 0:
    solutionFound = True

while solutionFound == False:
    previousScore = score
    for i in range(0, iterations):
        newState = chooseNewState(sudoku, fixedSudoku, sigma)
        sudoku = newState[0]
        scoreDiff = newState[1]
        score += scoreDiff 
        print(score)
        f.write(str(score) + '\n')
        f2.write(str(score) + ' ' + str(time.time() - start ) + '\n')
        if score <= 0:
            solutionFound = True
            break
        
    sigma *= decreaseFactor
    if score >= previousScore:
        stuckCount += 1
    else:
        stuckCount = 0
    
    if stuckCount > 80:
        sigma += 1
    
    if(numberOfErrors(sudoku) == 0):
        print("***A solution has been found!***")
        print_sudoku(sudoku)
        break

print(numberOfErrors(sudoku))

f.close


        







"""
print_sudoku(PUZZLE)

sudoku2 = FixSudokuValues(PUZZLE)

print_sudoku(sudoku2)
"""