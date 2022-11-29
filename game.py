from cmu_graphics import *
from classes import *
import math
from solver import *

def radiusEndpoint(x, y, r, theta):
    theta = math.radians(theta)
    return int(x + r * math.cos(theta)), int(y - r * math.sin(theta))

def game_onScreenStart(app):
    app.rows = app.cols = 9
    app.boardLeft = app.boardTop = 100
    app.boardWidth = app.boardHeight = 600
    app.cellBorderWidth = 1
    app.board = [['0'] * app.cols for _ in range(app.rows)]
    app.controls = 0 # 0: standard, 1: kb, 2: mouse
    game_makeButtons(app)
    app.message = Message('Hello!')

def game_makeButtons(app):
    quit = Button(__name__, 'Quit', app.width * 3 / 27, 50, 120, 40)
    quit.onClick, quit.args = setActiveScreen, 'start'
    help = Button(__name__, 'Help', 860, 500, 120, 40)
    help.onClick, help.args = setActiveScreen, 'help'
    undoButton = Button(__name__, 'Undo', 70, 750, 70, 30)
    undoButton.onClick, undoButton.args = undo, app
    redoButton = Button(__name__, 'Redo', 170, 750, 70, 30)
    redoButton.onClick, redoButton.args = redo, app
    enableLegals = Button(__name__, 'x', 800, 750, 20, 20, fill=None,
                          border='black', labelFill='black', borderWidth = 2)
    enableLegals.onClick, enableLegals.args = toggleLegals, app
    singletons = Button(__name__, 'Singleton', 350, 750, 120, 30, size=14)
    singletons.onClick, singletons.args = singleton, app
    allSingletons = Button(__name__, 'All Singletons', 500, 750, 120, 30, size=14)
    allSingletons.onClick, allSingletons.args = singleton, (app, True)
    toggleMode = Button(__name__, 'Enter Mode: Normal',
                       860, 650, 210, 40)
    toggleMode.onClick, toggleMode.args = toggleEnterMode, app
    controls = Button(__name__, 'Controls: Standard',
                      860, 570, 210, 40)
    controls.onClick, controls.args = changeControls, app

def game_redrawAll(app):
    drawLabel('Sudoku!', 400, 50, size=52, bold=True,
              font=app.font, fill='dimGray')
    drawBoard(app)
    drawBoardBorder(app)
    drawSelecting(app)
    Button.drawButtons(app, __name__)
    drawButtonExtras(app)
    app.message.draw(app)
    drawTimer(app)
    if app.win: drawWin(app)

def drawTimer(app):
    seconds = app.counter // app.stepsPerSecond
    minutes = seconds // 60
    drawLabel(f"{int(minutes)}:{str(seconds % 60).zfill(2)}", 860, 150,
              size=54, font=app.font)

def drawButtonExtras(app):
    drawLabel("Show Legals", 820, 750, font=app.font,
              size=18, fill='royalBlue', align='left')

def drawWin(app):
    drawRect(0, 0, app.width, app.height, opacity=10)
    drawRect(0, app.height / 3, app.width, app.height / 3,
             fill='skyBlue', opacity=30)
    drawLabel('YOU WON', app.width / 2, app.height / 2,
              font=app.font, fill='mediumTurquoise',
              size = 200, bold=True)

def drawBoard(app):
    for row in range(app.rows):
        for col in range(app.cols):
            drawCell(app, row, col)
            if app.showLegals:
                drawLegals(app, row, col)

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

#draw numbers to select in the box
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


def drawCell(app, row, col):
    cellLeft, cellTop = getCellLeftTop(app, row, col)
    cellWidth, cellHeight = getCellSize(app)
    #highlight color
    if (row, col) == app.selection and app.states[0].board[row][col] == '0':
        color = 'lightBlue'
    elif (app.board[row][col] != '0' and
        app.board[row][col] != app.solution[row][col]):
        color = 'salmon'
    else: color = None
    if app.states[0].board[row][col] != '0':
        color = 'darkGray'
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

def drawLegals(app, row, col):
    legals = app.legals[row][col]
    if legals == None or app.board[row][col] != '0': return
    cellLeft, cellTop = getCellLeftTop(app, row, col)
    cellWidth, cellHeight = getCellSize(app)
    for legal in legals:
        drow, dcol = legalToPosition(int(legal))
        x, y = cellLeft + dcol * cellWidth / 4, cellTop + drow * cellHeight / 4
        drawLabel(legal, x, y)

def legalToPosition(number):
    row = math.ceil(number / 3)
    col = (number - 1) % 3 + 1
    return row, col

def getCell(app, x, y):
    dx = x - app.boardLeft
    dy = y - app.boardTop
    cellWidth, cellHeight = getCellSize(app)
    row = math.floor(dy / cellHeight)
    col = math.floor(dx / cellWidth)
    if inBounds(app, row, col): return (row, col)
    else: return None

def getCellSize(app):
    cellWidth = app.boardWidth / app.cols
    cellHeight = app.boardHeight / app.rows
    return (cellWidth, cellHeight) 

def getCellLeftTop(app, row, col):
    cellWidth, cellHeight = getCellSize(app)
    cellLeft = app.boardLeft + col * cellWidth
    cellTop = app.boardTop + row * cellHeight
    return (cellLeft, cellTop)

def getCellMiddle(app, row, col):
    cellWidth, cellHeight = getCellSize(app)
    cellLeft = app.boardLeft + col * cellWidth
    cellTop = app.boardTop + row * cellHeight
    cx = cellLeft + cellWidth / 2
    cy = cellTop + cellHeight / 2
    return (cx, cy)

#hover on cells
def game_onMouseMove(app, mouseX, mouseY):
    Button.checkHover(app, __name__, mouseX, mouseY)
    if app.controls == 1: return
    selectedCell = getCell(app, mouseX, mouseY)
    if selectedCell != None:
        app.selection = selectedCell
    
#select a cell
def game_onMousePress(app, mouseX, mouseY):
    Button.checkClick(app, __name__, mouseX, mouseY)
    if app.controls == 1: return
    selectedCell = getCell(app, mouseX, mouseY)
    if selectedCell != None:
        row, col = selectedCell
        if app.states[0].board[row][col] == '0':
            app.selecting = True
    
#hover over numbers
def game_onMouseDrag(app, mouseX, mouseY):
    if app.controls == 1: return
    if app.selection != None and app.selecting:
        cx, cy = getCellMiddle(app, *app.selection)
        dx, dy = mouseX - cx, mouseY - cy
        r = (dx ** 2 + dy ** 2) ** 0.5
        theta = (90 + math.degrees(math.atan2(dy, dx))) % 360
        if 25 <= r <= 95:
            app.selectNum = 1 + (math.floor((theta + 20) / 40) % 9)
        elif r < 25:
            app.selectNum = 0

#unselects cell
def game_onMouseRelease(app, mouseX, mouseY):
    if app.controls == 1: return
    if app.selectNum != None: enterNum(app, *app.selection, app.selectNum)
    app.selection = app.selectNum = None
    app.selecting = False

def game_onKeyPress(app, key):
    if key == 'c': changeControls(app)
    if app.controls == 2: return
    elif key == 'right': moveSelection(app, 0, 1)
    elif key == 'left': moveSelection(app, 0, -1)
    elif key == 'up': moveSelection(app, -1, 0)
    elif key == 'down': moveSelection(app, 1, 0)
    elif key == 'space':
        app.selecting = not app.selecting
    elif key == 'escape':
        app.message = Message('haha you need help')
        setActiveScreen('help')
    elif key in '123456789' and app.selecting:
        app.selectNum = int(key)
        enterNum(app, *app.selection, app.selectNum)
        app.selectNum = None
        app.selecting = False
    elif key == 'z': undo(app)
    elif key == 'y': redo(app)
    elif key == 'r': 
        restart(app)
        setActiveScreen('start')
    elif key == 's': singleton(app)
    elif key == 'S': singleton(app, everything=True)
    elif key == 'l': toggleEnterMode(app)
    elif key == 'L': toggleLegals(app)

def moveSelection(app, drow, dcol):
    app.selecting = False
    if app.selection == None: #if nothing is selecting default to corners
        directionMap = {(-1, 0): (app.rows - 1, app.cols - 1),
                        (0, 1): (app.rows - 1, 0),
                        (1, 0): (0, 0),
                        (0, -1): (0, app.cols - 1)}
        row, col = directionMap[(drow, dcol)]
    else:
        row, col = app.selection
        #make the move if it will be in bounds
        if inBounds(app, row + drow, col + dcol):
            row += drow
            col += dcol 
    #keep moving past grayed out values
    while (inBounds(app, row + drow, col + dcol) and
        app.states[0].board[row][col] != '0'):
        row += drow
        col += dcol
    app.selection = row, col
    

def inBounds(app, row, col):
    return (0 <= row < app.rows) and (0 <= col < app.cols)

def enterNum(app, row, col, number):
    if app.enterMode == 'normal':
        app.board[row][col] = str(number)
        app.legals = getLegals(app.board)
    elif app.enterMode == 'legals':
        legals = app.legals[row][col]
        if str(number) in legals:
            app.legals[row][col] = legals - set([str(number)])
        else: app.legals[row][col] = legals | set([str(number)])
    #if we undid previously and are doing new moves
    if app.stateIndex != len(app.states) - 1:
        app.states = app.states[:app.stateIndex + 1]
    app.states.append(State(app.board, app.legals))
    app.stateIndex += 1
    checkWin(app)

def undo(app):
    if app.stateIndex <= 0: 
        app.message = Message("Can't undo anymore!")
        return
    app.stateIndex -= 1
    app.states[app.stateIndex].load(app)
    app.message = Message("Undid move")

def redo(app):
    if app.stateIndex == len(app.states) - 1:
        app.message = Message("Can't redo anymore!")
        return
    app.stateIndex += 1
    app.states[app.stateIndex].load(app)
    app.message = Message("Redid move")

def toggleLegals(app):
    app.showLegals = not app.showLegals
    for button in Button.buttons[__name__]:
        if button.label == 'x': button.label = ' '
        elif button.label == ' ': button.label = 'x'

def toggleEnterMode(app):
    app.enterMode = 'legals' if app.enterMode == 'normal' else 'normal'
    app.message = Message(f'Enter Mode: {app.enterMode.capitalize()}')
    for button in Button.buttons[__name__]:
        if button.label.startswith('Enter Mode'):
            button.label = f"Enter Mode: {app.enterMode.capitalize()}"

def changeControls(app):
    controls = ['Standard', 'Keyboard', 'Mouse']
    app.controls = (app.controls + 1) % 3
    for button in Button.buttons[__name__]:
        if button.label.startswith('Controls'):
            button.label = f"Controls: {controls[app.controls]}"

def singleton(app, everything = False):
    singleTonExists = True
    while singleTonExists:
        singleTonExists = False
        for row in range(app.rows):
            for col in range(app.cols):
                if len(app.legals[row][col]) == 1:
                    singleTonExists = True
                    enterNum(app, row, col, app.legals[row][col].pop())
                    app.selection = row, col
                    if not everything: return
        if not singleTonExists: 
            app.message = Message("No more singletons :(")

def checkWin(app):
    if app.board == app.solution: app.win = True

def game_onStep(app):
    if not app.win: app.counter += 1