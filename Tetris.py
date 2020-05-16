#################################################
# hw7.py: Tetris!
#
# Your name: Manish Nagireddy
# Your andrew id: mnagired
#
# Your partner's name: Roshan Ram
# Your partner's andrew id: rram
#################################################

import cs112_f19_week7_linter
import math, copy, random

from cmu_112_graphics import *
from tkinter import *

#################################################
# Helper functions
#################################################

def almostEqual(d1, d2, epsilon=10**-7):
    # note: use math.isclose() outside 15-112 with Python version 3.5 or later
    return (abs(d2 - d1) < epsilon)

import decimal
def roundHalfUp(d):
    # Round to nearest with ties going away from zero.
    rounding = decimal.ROUND_HALF_UP
    # See other rounding options here:
    # https://docs.python.org/3/library/decimal.html#rounding-modes
    return int(decimal.Decimal(d).to_integral_value(rounding=rounding))

#################################################
# Functions for you to write
#################################################

def appStarted(app):
    app.rows, app.cols, app.cellSize, app.margin = gameDimensions()
    app.emptyColor = 'blue'
    #list comprehension to create an 2D list with every cell being blue
    app.board = [([app.emptyColor] * app.cols) for row in range(app.rows)]
    app.tetrisPieces = tetrisPieces()
    app.tetrisPieceColors = ["red", "yellow", "magenta", "pink",
                       "cyan", "green", "orange"]
    newFallingPieceFunction(app)
    app.timerDelay = 500 #twice a second
    app.score = 0
    app.gameOver = False

def tetrisPieces():
    # Seven "standard" pieces (tetrominoes)
    iPiece = [[True, True, True, True]]
    jPiece = [[True, False, False],
            [True, True, True]]
    lPiece = [[False, False, True],
            [True, True, True]]
    oPiece = [[True, True],
            [True, True]]
    sPiece = [[False, True, True],
            [True, True, False]]
    tPiece = [[False, True, False],
             [True, True, True]]
    zPiece = [[True, True, False],
            [False, True, True]]
    return [iPiece, jPiece, lPiece, oPiece, sPiece, tPiece, zPiece]

def newFallingPieceFunction(app):
    randomIndex = random.randint(0, len(app.tetrisPieces) - 1)
    app.fallingPiece = app.tetrisPieces[randomIndex]
    app.fallingPieceRow = 0 #top of the board
    app.fallingPieceColor = app.tetrisPieceColors[randomIndex]
    app.numFallingPieceCols = len(app.fallingPiece[0])
    app.fallingPieceCol = app.cols//2 - app.numFallingPieceCols//2

def drawFallingPiece(app, canvas):
    color = app.fallingPieceColor
    for row in range(len(app.fallingPiece)):
        for col in range(len(app.fallingPiece[0])):
            if(app.fallingPiece[row][col] == True):
                drawCell(app, canvas, row+app.fallingPieceRow,
                         col+app.fallingPieceCol, color)

def redrawAll(app, canvas):
    canvas.create_rectangle(0,0,app.width,app.height, fill = 'orange')
    drawBoard(app, canvas)
    drawFallingPiece(app, canvas)
    drawScore(app, canvas)
    cx, cy = app.width/2, app.height/2
    if(app.gameOver):
        canvas.create_text(cx, cy, font="Arial 18 bold",
                           text="You lose! \nGet it together buddy!!",
                           fill="white")
        canvas.create_text(cx, cy + app.cellSize,font="Arial 14 bold",
                           text="\n(Hit 'r' to restart.)", fill="white")

def keyPressed(app, event):
    if(event.key == 'r'):
        appStarted(app)
    elif(not app.gameOver):
        if (event.key == 'Left'):
            moveFallingPieceFunction(app, 0, -1)
        elif (event.key == 'Right'):
            moveFallingPieceFunction(app, 0, +1)
        elif (event.key == 'Up'):
            rotateFallingPieceFunction(app)
        elif (event.key == 'Down'):
            moveFallingPieceFunction(app, +1, 0)
        elif (event.key == 'Space'):
            hardDrop(app)

def drawBoard(app, canvas):
    for row in range(app.rows):
        for col in range(app.cols):
            drawCell(app, canvas, row, col, '')

## Citation: From getCellBounds in Lecture Notes Under Example 9: Grids
def drawCell(app, canvas, row, col, color):
    if (color == ''): color = app.board[row][col]
    gridWidth = app.width - 2 * app.margin
    gridHeight = app.height - 2 * app.margin
    columnWidth = gridWidth / app.cols
    rowHeight = gridHeight / app.rows
    x0 = app.margin + col * columnWidth
    x1 = app.margin + (col + 1) * columnWidth
    y0 = app.margin + row * rowHeight
    y1 = app.margin + (row + 1) * rowHeight
    canvas.create_rectangle(x0,y0,x1,y1,
                            fill = color, outline = 'black', width = 3)

def gameDimensions():
    defaultRows = 15
    defaultCols = 10
    defaultCellSize = 20
    defaultMargin = 25
    return defaultRows, defaultCols, defaultCellSize, defaultMargin

def moveFallingPieceFunction(app, drow, dcol):
    app.fallingPieceRow += drow
    app.fallingPieceCol += dcol
    hasMoved = True
    if(not fallingPieceIsLegal(app)):
        #can revert back to previous state by subtracting initial addition
        app.fallingPieceRow -= drow
        app.fallingPieceCol -= dcol
        hasMoved = False
    return hasMoved

def placeFallingPieceFunction(app):
    color = app.fallingPieceColor
    for row in range(len(app.fallingPiece)):
        for col in range(len(app.fallingPiece[0])):
            if (app.fallingPiece[row][col] == True):
                app.board[row+app.fallingPieceRow][col+app.fallingPieceCol] \
                    = color
    removeFullRows(app)

def fallingPieceIsLegal(app):
    for row in range(len(app.fallingPiece)):
        for col in range(len(app.fallingPiece[0])):
            if app.fallingPiece[row][col] == True:
                tempRow = app.fallingPieceRow+row
                tempCol = app.fallingPieceCol+col
                if (tempRow < 0 or tempRow >= app.rows or
                        tempCol < 0 or tempCol >= app.cols
                        or app.board[tempRow][tempCol] != app.emptyColor):
                    return False
    return True

def rotateFallingPieceFunction(app):
    oldPiece,oldRow,oldCol = app.fallingPiece,\
                               len(app.fallingPiece),len(app.fallingPiece[0])
    newPiece, newRow, newCol = [], oldCol, oldRow
    #initialize new list by transposing the old one
    newPiece += [[False] * newCol for row in range(newRow)]
    for row in range(newRow):
        for col in range(newCol):
            #use oldCol-1 to indicate new row is old columns - 1
            newPiece[oldCol - 1 - row][col] = app.fallingPiece[col][row]
    app.fallingPiece = newPiece
    #better rotation method by using center of piece
    oldCenterRow = app.fallingPieceRow+oldRow//2
    newRows = oldCenterRow - len(newPiece) // 2
    oldCenterCol = app.fallingPieceCol+oldCol//2
    newCols = oldCenterCol-len(newPiece[0])//2
    app.fallingPieceRow, app.fallingPieceCol = newRows, newCols
    if (not fallingPieceIsLegal(app)):
        app.fallingPiece = oldPiece
        app.fallingPieceRow, app.fallingPieceCol = oldRow, oldCol

def timerFired(app):
    if(not app.gameOver):
        if (not moveFallingPieceFunction(app, 1, 0)):
            placeFallingPieceFunction(app)
            newFallingPieceFunction(app)
        if (not fallingPieceIsLegal(app)):
            app.gameOver = True

def removeFullRows(app):
    nRow, score = app.rows-1, 0
    color = app.emptyColor
    #traverse from bottom of board to top
    for row in range(app.rows, 0, -1):
        row-=1 #make sure we don't crash on first iteration
        fullRow = True
        for col in range(app.cols):
            if (app.board[row][col] == color):
                fullRow = False
        if(fullRow == True):
            score += 1
        else:
            app.board[nRow] = copy.deepcopy(app.board[row])
            nRow -= 1 #check the next row above
    #loop to continuously add empty (blue) rows
    while (nRow >= 0):
        app.board[nRow] = [color] * app.cols
        nRow -= 1
    app.score += score**2 #calculate score based on rules

def drawScore(app, canvas):
    scoreHeight = 15
    canvas.create_text(app.width/2, scoreHeight,
                       text = f'User Score = {app.score}')

def hardDrop(app):
    for r in range(len(app.board)):
        if(fallingPieceIsLegal(app)):
            moveFallingPieceFunction(app, 1, 0)

def playTetris():
    rows,cols,cellSize,margin = gameDimensions()
    w = cols*cellSize + margin
    h = rows*cellSize + margin
    runApp(width=w, height=h)

#################################################
# main
#################################################

def main():
    cs112_f19_week7_linter.lint()
    playTetris()

if __name__ == '__main__':
    main()