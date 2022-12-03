import math, copy
import numpy as np

#solve sudoku board
def solve(board):
    legals = getLegals(board)
    row, col = leastLegals(legals)

    stack = list()
    stack.append([copy.deepcopy(board), row, col, legals[row][col]])

    while stack:
        board, row, col = stack[-1][:-1]
        move = stack[-1][-1].pop()
        if stack[-1][-1] == set(): stack.pop()
        board[row][col] = move

        if isSolved(board): return board #done if done

        #else keep lookin
        legals = getLegals(board)
        nextRow, nextCol = leastLegals(legals)
        if legals[nextRow][nextCol] != set():
            stack.append([copy.deepcopy(board), nextRow,
                          nextCol, legals[nextRow][nextCol]])

def leastLegals(legals):
    minRow, minCol = 0, 0
    for row in range(9):
        for col in range(9):
            if len(legals[row][col]) == 0: continue
            if (len(legals[minRow][minCol]) == 0 or
                len(legals[row][col]) < len(legals[minRow][minCol])):
                minRow, minCol = row, col
    return minRow, minCol


def isSolved(board):
    for row in range(9):
        for col in range(9):
            if board[row][col] == '0': return False
    return True

def getLegals(board):
    legals = [[set()] * 9 for _ in range(9)]
    for row in range(9):
        for col in range(9):
            if board[row][col] == '0':
                legals[row][col] = (set(['1', '2', '3', '4', '5', '6', '7', '8', '9'])
                                    - getRegion(board, row, col))
    return legals

#no longer used but in case future stuff
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

def indexToCoord(i):
    return 3 * (i // 3), 3 * (i % 3)

def rowCoords(row):
    return [(row, col) for col in range(9)]

def colCoords(col):
    return [(row, col) for row in range(9)]

def blockCoords(row, col):
    startRow, startCol = 3 * math.floor(row / 3), 3 * math.floor(col / 3)
    coords = list()
    for drow in range(3):
        for dcol in range(3):
            coords.append((startRow + drow, startCol + dcol))
    return coords

def allRegionCoords():
    regions = list()
    for i in range(9):
        regions.append(rowCoords(i))
        regions.append(colCoords(i))
        regions.append(blockCoords(*indexToCoord(i)))
    return regions