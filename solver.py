import copy, math
import numpy as np

#solve sudoku board
def solve(board):
    if isSolved(board): return board
    board = copy.deepcopy(board) #don't mutate
    legals = getLegals(board)
    row, col = leastLegals(legals)
    for num in legals[row][col]:
        board[row][col] = num
        result = solve(board)
        if result != None: return result
    return None

def leastLegals(legals):
    rows, cols = len(legals), len(legals[0])
    minRow, minCol = 0, 0
    for row in range(rows):
        for col in range(cols):
            if len(legals[row][col]) == 0: continue
            if (len(legals[minRow][minCol]) == 0 or
                len(legals[row][col]) < len(legals[minRow][minCol])):
                minRow, minCol = row, col
    return minRow, minCol


def isSolved(board):
    rows, cols = len(board), len(board[0])
    for row in range(rows):
        for col in range(cols):
            if board[row][col] == '0': return False
    return True

def getLegals(board):
    rows, cols = len(board), len(board[0])
    legals = [[set()] * cols for _ in range(rows)]
    for row in range(rows):
        for col in range(cols):
            if board[row][col] == '0':
                legals[row][col] = (set(['1', '2', '3', '4', '5', '6', '7', '8', '9'])
                                    - getRegion(board, row, col))
    return legals

def isLegalMove(board, row, col):
    rows, cols = len(board), len(board[0])
    #check nonzero values in rows for duplicates
    notZero = [v for v in getRow(board, row) if v != '0']
    if len(notZero) != len(set(notZero)): return False
    #check nonzero values in cols for duplicates
    notZero = [v for v in getCol(board, col) if v != '0']
    if len(notZero) != len(set(notZero)): return False
    #check blocks
    block = [v for v in getBlock(board, row, col) if v != '0']
    if len(block) != len(set(block)): return False
    return True

def getRow(board, row):
    return board[row]

def getCol(board, col):
    return [board[row][col] for row in range(len(board))]

def getBlock(board, row, col, flatten=True):
    startRow, startCol = 3 * math.floor(row / 3), 3 * math.floor(col / 3)
    block = [[None] * 3 for _ in range(3)]
    for drow in range(3):
        for dcol in range(3):
            block[drow][dcol] = board[startRow + drow][startCol + dcol]
    if flatten: return block[0] + block[1] + block[2]
    else: return block

def getRegion(board, row, col):
    region = set(getRow(board, row)) | set(getCol(board, col)) | set(getBlock(board, row, col))
    return set(region)