#################################################
# hw6.py
#
# Your name: Kevin Kyi  
# Your andrew id: Kwkyi
#
# Your partner's name:
# Your partner's andrew id:
#################################################

import cs112_f21_week6_linter
import math, copy, random

from cmu_112_graphics import *



#################################################
# Tetris
#################################################

def appStarted(app):
    gamedimensions = gameDimensions()
    app.fallenPieces = 0
    app.rows = gamedimensions[0]
    app.cols = gamedimensions[1]
    app.cellSize = gamedimensions[2]
    app.margin = gamedimensions[3]
    app.isGameOver = False
    
    app.size = 0
    #creating the images of the board
    app.board = [ (['blue'] * app.cols) for row in range(app.rows) ]

    #from website tester colors
     
    #tetris Pieces 
    iPiece = [
        [  True,  True,  True,  True ]
    ]
    jPiece = [
        [  True, False, False ],
        [  True,  True,  True ]
    ]
    lPiece = [
        [ False, False,  True ],
        [  True,  True,  True ]
    ]
    oPiece = [
        [  True,  True ],
        [  True,  True ]
    ]
    sPiece = [
        [ False,  True,  True ],
        [  True,  True, False ]
    ]
    tPiece = [
        [ False,  True, False ],
        [  True,  True,  True ]
    ]
    zPiece = [
        [  True,  True, False ],
        [ False,  True,  True ]
    ]
    app.tetrisPieces = [ iPiece, jPiece, lPiece, oPiece, sPiece, tPiece, zPiece]
    app.tetrisPieceColors = [ "red", "yellow", "magenta", "pink",
    "cyan", "green", "orange" ]
    newFallingPiece(app)
    app.score = 0

def keyPressed(app, event):
    app.color = random.choice(['red', 'orange', 'yellow', 'green', 'blue'])
    if app.isGameOver and not event.key == 'r':
        return
    if event.key == 'Left':
        moveFallingPiece(app, 0, -1)
    elif event.key == 'Right':
        moveFallingPiece(app, 0, +1)
    elif event.key == 'Down':
        moveFallingPiece(app, +1, 0)
    elif event.key == 'Up':
        rotateFallingPiece(app)
    elif event.key == 'Space':
        test_fallen = app.fallenPieces
        while(test_fallen == app.fallenPieces):
            moveFallingPiece(app, +1, 0)
    elif event.key == 'r':
        app.isGameOver = False
        app.appStarted()


def timerFired(app):
    moveFallingPiece(app, +1, 0)
    app.size += 10

def drawCell(app, canvas, row, col, color):
    #for col in range(app.cols):
     #   for row in range(app.rows):
    x0, y0, x1, y1 = getCellBounds(app, row, col)
    if (x0 == 1 and y0 == 1 and x1 == 1 and y1 == 1):
        canvas.create_rectangle(x0, y0, x1, y1, fill = color, width = 3.5)
    else:
        canvas.create_rectangle(x0, y0, x1, y1, 
        fill = color, width = 3.5)

#creating the cells 10x15 on the canvas

def getCellBounds(app, row, col):
    # aka "modelToView"
    # returns (x0, y0, x1, y1) corners/bounding box of given cell in grid
    gridWidth  = app.width - 2*app.margin
    gridHeight = app.height - 2*app.margin
    cellWidth = gridWidth / app.cols
    cellHeight = gridHeight / app.rows
    x0 = app.margin + col * cellWidth
    x1 = app.margin + (col+1) * cellWidth
    y0 = app.margin + row * cellHeight
    y1 = app.margin + (row+1) * cellHeight
    return (x0, y0, x1, y1)


def drawBoard(app, canvas):
    canvas.create_rectangle(0, 0, app.width, app.height, fill = 'orange')
    for i in range(app.rows):
        for j in range(app.cols):
            drawCell(app, canvas, i, j, app.board[i][j])


def newFallingPiece(app):
    randomIndex = random.randint(0, len(app.tetrisPieces) - 1)
    app.fallingPiece = (app.tetrisPieces[randomIndex])
    app.fallingColor = (app.tetrisPieceColors[randomIndex])
    app.fallingPieceRows = 0
    app.numFallingPieceRows = len(app.fallingPiece[0])
    app.fallingPieceCols = app.cols // 2 - app.numFallingPieceRows // 2

def drawFallingPiece(app, canvas):
    for i in range(len(app.fallingPiece)):
        for j in range(len(app.fallingPiece[i])):
            if app.fallingPiece[i][j]:
                drawCell(app, canvas, app.fallingPieceRows + i,
                app.fallingPieceCols + j, app.fallingColor)

def fallingPieceIsLegal(app):
    for i in range(len(app.fallingPiece)):
        for j in range(app.numFallingPieceRows):
            if app.fallingPiece[i][j]:#variable change row and col
                rowChange = app.fallingPieceRows + i
                colChange = app.fallingPieceCols + j
                
                #check boundaries 
                if (rowChange < 0 or colChange < 0 or rowChange > app.rows-1 or
                colChange > app.cols-1): return False
                if app.board[rowChange][colChange] != 'blue': return False
    return True


def moveFallingPiece(app, drow, dcol):
    app.fallingPieceCols += dcol
    app.fallingPieceRows += drow
    #check if legal if not reset move
    if not fallingPieceIsLegal(app):
        #reset fallingPieces
        oldCol = app.fallingPieceCols + len(app.fallingPiece)
        app.fallingPieceCols -= dcol
        app.fallingPieceRows -= drow
        if(oldCol >= len(app.fallingPiece) and
         oldCol < app.cols): placeFallingPiece(app)
        return False
    return True
        
def rotateFallingPiece(app):
    #storing relevant old pieces 
    restoreCol = copy.deepcopy(app.fallingPieceCols) 
    restoreRow = copy.deepcopy(app.fallingPieceRows)
    restorePiece = copy.deepcopy(app.fallingPiece)
    #print(restoreCol)
    #create new piece and list with NONE(make with new dimensions)
    rotatedPiece = [[restorePiece[j][len(restorePiece[0]) - i - 1] for j in 
        range(len(restorePiece))]
         for i in range(len(restorePiece[0]))]
    #iterate through all values and change their values 
    #checking if move is legal(if not move pieces back to their original)
    app.fallingPiece = rotatedPiece
    app.numFallingPieceRows = len(rotatedPiece[0])
    if(not fallingPieceIsLegal(app)):
        app.fallingPieceCols = restoreCol
        app.fallingPieceRows = restoreRow 
        app.numFallingPieceRows = len(app.fallingPiece[0])

def removeFullRows(app):
    for i in range(len(app.board)):
        test = True
        for j in range(len(app.board[0])):
            test = test and not (app.board[i][j] == 'blue')
        if test:
            for j in range(len(app.board[0])):
                app.board[i][j] = 'blue'
            oldBoard = copy.deepcopy(app.board)
            app.board[0] = ['blue' for i in range(len(app.board[0]))]
            for j in range(i):
                app.board[j + 1] = copy.copy(oldBoard[j])


def placeFallingPiece(app):
    for i in range(len(app.fallingPiece)):
        for j in range(len(app.fallingPiece[0])):
            row = i + app.fallingPieceRows
            col = j + app.fallingPieceCols
            if app.fallingPiece[i][j]:
                app.board[row][col] = app.fallingColor
    if not app.isGameOver: newFallingPiece(app)
    if(not fallingPieceIsLegal(app)):
        app.isGameOver = True
    removeFullRows(app)
    app.fallenPieces += 1

def drawScore(app, canvas):
    canvas.create_text(app.width//2,app.margin//2,
    text=f'Score:{app.score}',fill = 'blue',font = 'Arial 10 bold')

def drawGameOver(app,canvas):
    canvas.create_rectangle(0, app.height //6 -10, app.width,
    app.height //6 + 10, fill = 'black')
    canvas.create_text(app.width//2, app.height//6,text ="Game over :((((",
    fill = "magenta")

def redrawAll(app, canvas):
    drawBoard(app,canvas)
    drawFallingPiece(app, canvas)
    if app.isGameOver == True: drawGameOver(app, canvas)

def gameDimensions():
    rows = 15 
    cols = 10 
    cellSize = 20 
    margin = 25 
    return (rows, cols, cellSize, margin)

def playTetris():
    dimensions = gameDimensions()
    rows = dimensions[0]
    cols = dimensions[1]
    cellSize = dimensions[2]
    margin = dimensions[3]
    runApp(width = ((margin*2) + (cols * cellSize)), 
    height = ((margin*2) + (rows * cellSize)))
