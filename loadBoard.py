from cmu_graphics import *
from classes import *
from solver import *
from game import getCell, getCellMiddle, getCellSize, getCellLeftTop, radiusEndpoint
from start import readFile

def loadBoard_onScreenStart(app):
    app.selection = app.selectNum = None
    app.selecting = False
    app.solution = app.board
    app.legals = [[set([str(n) for n in range(1, 10)])
                   for _ in range(9)] for _ in range(9)]
    loadBoard_makeButtons(app)

def loadBoard_makeButtons(app):
    back = Button(__name__, 'Back', app.width * 3 / 27, 50, 120, 40)
    back.onClick, back.args = setActiveScreen, 'start'
    load = Button(__name__, 'Load Game', 840, 250, 200, 50)
    load.onClick, load.args = loadGame, app
    filepath = Button(__name__, 'Enter Board Path', 840, 370, 200, 50)
    filepath.onClick, filepath.args = getFilePath, app
    clear = Button(__name__, 'Clear', app.width * 3 / 27, 750, 120, 40)
    clear.onClick, clear.args = clearBoard, app

def clearBoard(app):
    app.board = [['0'] * app.cols for _ in range(app.rows)]

#loads file and starts game
def getFilePath(app):
    path = app.getTextInput('Enter path to txt board file')
    app.enterMode = 'normal'
    app.win = app.showLegals = False
    app.selection = app.selectNum = None
    app.selecting = False
    app.counter = 0
    app.states, app.stateIndex = list(), 0
    try:
        loadBoard(app, path)
        setActiveScreen('game')
    except FileNotFoundError:
        app.message = Message("Can't find file :(")
    except:
        app.message = Message('Something went wrong')

def loadBoard(app, path):
    boardText = readFile(path)
    i = 0
    for line in boardText.splitlines():
        j = 0
        for n in line.split():
            app.board[i][j] = n 
            j += 1
        i += 1
    app.solution = solve(app.board)
    app.legals = getLegals(app.board)
    app.states.append(State(app.board, app.legals))

def loadBoard_redrawAll(app):
    drawLabel('Load Board', 400, 50, size=52, bold=True,
              font=app.font, fill='dimGray')
    drawBoard(app)
    drawBoardBorder(app)
    drawSelecting(app)
    Button.drawButtons(app, __name__)
    drawLabel('OR', 840, 310, font=app.font, size=52)
    app.message.draw(app)

def drawBoard(app):
    for row in range(app.rows):
        for col in range(app.cols):
            drawCell(app, row, col)

def drawBoardBorder(app):
    # draw the block outlines
    for row in range(3):
        for col in range(3):
            drawRect(app.boardLeft + col * app.boardWidth / 3,
                     app.boardTop + row * app.boardWidth / 3,
                     app.boardWidth / 3, app.boardHeight / 3,
                     fill=None, border='dimGray',
                     borderWidth = 2 * app.cellBorderWidth)
    drawRect(app.boardLeft, app.boardTop,app.boardWidth, app.boardHeight,
             fill=None, border='dimGray',
             borderWidth = 4 * app.cellBorderWidth)

def drawCell(app, row, col):
    cellLeft, cellTop = getCellLeftTop(app, row, col)
    cellWidth, cellHeight = getCellSize(app)
    #highlight color
    if (row, col) == app.selection and app.board[row][col] == '0':
        color = 'lightBlue'
    else: color = None
    #draws numbers in board
    if app.board[row][col] != '0':
        x, y = getCellMiddle(app, row, col)
        drawLabel(app.board[row][col], x, y, font=app.font, 
                  size=22, fill='royalBlue', bold=True)
    #cell border
    drawRect(cellLeft, cellTop, cellWidth, cellHeight,
             fill=None, border='dimGray',
             borderWidth=app.cellBorderWidth)
    #highlight
    drawRect(cellLeft, cellTop, cellWidth, cellHeight,
            fill=color, opacity=40)

#modified from game
def drawSelecting(app):
    if app.selecting and app.selection != None:
        row, col = app.selection
        cx, cy = getCellMiddle(app, row, col)
        r = 80
        drawCircle(cx, cy, r + 20, opacity=45)
        for n in range(1, 10):
            theta = 90 - (n - 1) * 360 / 9 #kinda like 9 numbers on clock
            x, y = radiusEndpoint(cx, cy, r, theta)
            #if number isn't legal
            fill = 'lightCyan' if str(n) in app.legals[row][col] else 'lightSalmon'
            #hover over number
            if app.selectNum == n: drawCircle(x, y, 20, fill='cornflowerBlue')
            drawLabel(n, x, y, font=app.font, size=26,
                      fill=fill, bold=True)

#same as in game
def loadBoard_onMouseDrag(app, mouseX, mouseY):
    if app.selection != None and app.selecting:
        cx, cy = getCellMiddle(app, *app.selection)
        dx, dy = mouseX - cx, mouseY - cy
        r = (dx ** 2 + dy ** 2) ** 0.5
        theta = (90 + math.degrees(math.atan2(dy, dx))) % 360
        if 25 <= r <= 95:
            app.selectNum = 1 + (math.floor((theta + 20) / 40) % 9)
        elif r < 25:
            app.selectNum = 0

def loadBoard_onMouseMove(app, mouseX, mouseY):
    Button.checkHover(app, __name__, mouseX, mouseY)
    selectedCell = getCell(app, mouseX, mouseY)
    if selectedCell != None and not app.selecting:
        app.selection = selectedCell
    

def loadBoard_onMousePress(app, mouseX, mouseY):
    Button.checkClick(app, __name__, mouseX, mouseY)
    selectedCell = getCell(app, mouseX, mouseY)
    if selectedCell != None:
        app.selecting = True

#same as in game
def loadBoard_onMouseRelease(app, mouseX, mouseY):
    if app.selectNum != None: enterNum(app, *app.selection, app.selectNum)
    app.selection = app.selectNum = None
    app.selecting = False

#modified from game to not include states
def enterNum(app, row, col, number):
    app.board[row][col] = str(number)
    app.legals = getLegals(app.board)

def loadGame(app):
    app.enterMode = 'normal'
    app.win = False
    app.counter = 0
    app.states, app.stateIndex = list(), 0
    app.solution = solve(app.board)
    app.legals = getLegals(app.board)
    app.states.append(State(app.board, app.legals))
    app.showLegals = (app.difficulty != 'easy')
    setActiveScreen('game')