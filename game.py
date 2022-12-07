from cmu_graphics import *
from classes import *
import math
from solver import *
from itertools import combinations
import time, sys

def game_onScreenActivate(app):
    Button.buttons[__name__] = list()
    game_makeButtons(app)
    app.startTime = time.time() if app.startTime == None else app.startTime
    app.hintCells = set()

def game_onAppStart(app):
    app.rows = app.cols = 9
    app.boardLeft = app.width/10
    app.boardTop = app.height/8
    app.boardWidth = app.boardHeight = min(app.width, app.height)*3/4
    app.cellBorderWidth = 1
    app.board = [['0']*app.cols for _ in range(app.rows)]
    app.controls = 0 # 0: standard, 1: kb, 2: mouse
    game_makeButtons(app)
    app.message = Message('Hello!')
    app.startTime = None

#kind of long sadly but there are many buttons
def game_makeButtons(app):
    quit = Button(__name__, 'Quit', app.width*3/27, app.height/16,
                  app.width*3/25, app.height/20)
    quit.onClick, quit.args = setActiveScreen, 'start'
    undoButton = Button(__name__, 'Undo', app.width*7/100,
                        app.height*15/16, app.width*7/100, app.height*3/80)
    undoButton.onClick, undoButton.args = undo, app
    redoButton = Button(__name__, 'Redo', app.width*17/100, app.height*15/16,
                        app.width*7/100, app.height*3/80)
    redoButton.onClick, redoButton.args = redo, app
    label = 'x' if app.difficulty != 'easy' else ' '
    enableLegals = Button(__name__, label, app.width*4/5, app.height*15/16,
                          app.height/40, app.height/40, fill=None,
                          border='black', labelFill='black', borderWidth = 2)
    enableLegals.onClick, enableLegals.args = toggleLegals, app
    singletons = Button(__name__, 'Singleton', app.width*7/20, app.height*15/16,
                        app.width*3/25, app.height*3/80, size=14)
    singletons.onClick, singletons.args = singleton, app
    allSingletons = Button(__name__, 'All Singletons', app.width/2,
                           app.height*15/16, app.width*3/25, 
                           app.height*3/80, size=14)
    allSingletons.onClick, allSingletons.args = singleton, (app, True)
    toggleMode = Button(__name__, 'Enter Mode: Normal',
                       app.width*43/50, app.height*26/32,
                       app.width*21/100, app.height/20)
    toggleMode.onClick, toggleMode.args = toggleEnterMode, app
    controls = Button(__name__, 'Controls: Standard',
                      app.width*43/50, app.height*23/32, 
                      app.width*21/100, app.height/20)
    controls.onClick, controls.args = changeControls, app
    bigHint = Button(__name__, 'Big hint', app.width*43/50, app.height*20/32,
                     app.width*3/25, app.height/20)
    bigHint.onClick, bigHint.args = hint2, app
    hint = Button(__name__, 'Hint', app.width*43/50, app.height*17/32,
                  app.width*3/25, app.height/20)
    hint.onClick, hint.args = hint1, app
    help = Button(__name__, 'Controls', app.width*43/50, app.height*14/32, 
                  app.width*3/25, app.height/20)
    help.onClick, help.args = setActiveScreen, 'help'

def game_redrawAll(app):
    drawLabel('Sudoku!', app.width*2/5, app.height/16, size=52, bold=True,
              font=app.font, fill='dimGray')
    drawBoard(app)
    drawBoardBorder(app)
    Button.drawButtons(app, __name__)
    drawSelecting(app)    
    drawButtonExtras(app)
    app.message.draw(app)
    drawTimer(app)
    if app.win: drawWin(app)

def drawTimer(app):
    if app.win: seconds = app.winTime
    else: seconds = int(time.time() - app.startTime)
    minutes = seconds // 60
    drawLabel(f"{int(minutes)}:{str(seconds % 60).zfill(2)}", app.width*43/50,
              app.height*8/32, size=54, font=app.font)

def drawButtonExtras(app):
    drawLabel("Show Legals", app.width*4/5 + 15, app.height*15/16, font=app.font,
              size=18, fill='royalBlue', align='left')

def drawWin(app):
    drawRect(0, 0, app.width, app.height, opacity=10)
    drawRect(0, app.height/3, app.width, app.height/3,
             fill='skyBlue', opacity=30)
    drawLabel('YOU WON', app.width/2, app.height/2,
              font=app.font, fill='mediumTurquoise',
              size = 200 + 10 * ((7 * app.counter // app.stepsPerSecond) % 2), bold=True)

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
            drawRect(app.boardLeft + col*app.boardWidth/3,
                     app.boardTop + row*app.boardWidth/3,
                     app.boardWidth/3, app.boardHeight/3,
                     fill=None, border='dimGray',
                     borderWidth = 2*app.cellBorderWidth)
    drawRect(app.boardLeft, app.boardTop,app.boardWidth, app.boardHeight,
             fill=None, border='dimGray',
             borderWidth = 4*app.cellBorderWidth)

#draw numbers to select in the box
def drawSelecting(app):
    if app.selecting and app.selection != None:
        row, col = app.selection
        cx, cy = getCellMiddle(app, row, col)
        r = 80
        drawCircle(cx, cy, r + 20, opacity=45)
        for n in range(1, 10):
            theta = 90 - (n - 1)*360/9 #kinda like 9 numbers on clock
            x, y = radiusEndpoint(cx, cy, r, theta)
            #if number isn't legal
            fill = 'lightCyan' if str(n) in app.legals[row][col] else 'lightSalmon'
            #hover over number
            if app.selectNum == n: drawCircle(x, y, 20, fill='cornflowerBlue')
            drawLabel(n, x, y, font=app.font, size=26,
                      fill=fill, bold=True)

def radiusEndpoint(x, y, r, theta):
    theta = math.radians(theta)
    return int(x + r*math.cos(theta)), int(y - r*math.sin(theta))

def drawCell(app, row, col):
    cellLeft, cellTop = getCellLeftTop(app, row, col)
    cellWidth, cellHeight = getCellSize(app)
    color = getHighlight(app, row, col)
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

def getHighlight(app, row, col):
    if (app.wrongLabels and app.board[row][col] != '0' and
        app.board[row][col] != app.solution[row][col]):
        color = 'salmon'
    elif (app.wrongLabels and len(app.legals[row][col]) >= 1 and
          app.solution[row][col] not in app.legals[row][col]):
        color = 'salmon'
    elif (app.wrongLabels and len(app.legals[row][col]) == 0 and
          app.board[row][col] == '0'):
        color = 'salmon'
    elif (row, col) == app.selection and app.states[0].board[row][col] == '0':
        color = 'lightBlue'
    elif app.showHints and (row, col) in app.hintCells:
        color = 'plum'
    else: color = None
    if app.states[0].board[row][col] != '0':
        color = 'darkGray'
    return color

def drawLegals(app, row, col):
    legals = app.legals[row][col]
    if legals == None or app.board[row][col] != '0': return
    cellLeft, cellTop = getCellLeftTop(app, row, col)
    cellWidth, cellHeight = getCellSize(app)
    for legal in legals:
        drow, dcol = legalToPosition(int(legal))
        x, y = cellLeft + dcol*cellWidth/4, cellTop + drow*cellHeight/4
        drawLabel(legal, x, y)

def legalToPosition(number):
    row = math.ceil(number/3)
    col = (number - 1) % 3 + 1
    return row, col

def getCell(app, x, y):
    dx = x - app.boardLeft
    dy = y - app.boardTop
    cellWidth, cellHeight = getCellSize(app)
    row = math.floor(dy/cellHeight)
    col = math.floor(dx/cellWidth)
    if inBounds(app, row, col): return (row, col)
    else: return None

def getCellSize(app):
    cellWidth = app.boardWidth/app.cols
    cellHeight = app.boardHeight/app.rows
    return (cellWidth, cellHeight) 

def getCellLeftTop(app, row, col):
    cellWidth, cellHeight = getCellSize(app)
    cellLeft = app.boardLeft + col*cellWidth
    cellTop = app.boardTop + row*cellHeight
    return (cellLeft, cellTop)

def getCellMiddle(app, row, col):
    cellWidth, cellHeight = getCellSize(app)
    cellLeft = app.boardLeft + col*cellWidth
    cellTop = app.boardTop + row*cellHeight
    cx = cellLeft + cellWidth/2
    cy = cellTop + cellHeight/2
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
            app.selectNum = 1 + (math.floor((theta + 20)/40) % 9)
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
    elif key == 'escape': setActiveScreen('help')
    elif key in '123456789' and app.selecting:
        app.selectNum = int(key)
        enterNum(app, *app.selection, app.selectNum)
        app.selectNum = None
        app.selecting = False
    elif key == 'z': undo(app)
    elif key == 'y': redo(app)
    elif key == 'r': setActiveScreen('start')
    elif key == 's': singleton(app)
    elif key == 'S': singleton(app, everything=True)
    elif key == 'l': toggleEnterMode(app)
    elif key == 'L': toggleLegals(app)
    elif key == 'h': hint1(app)
    elif key == 'H': hint2(app)
    elif key == 'p': saveBoard(app)

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

def enterNum(app, row, col, number, mode=None):
    if app.win: return
    app.hintCells = set() #clear hint
    if mode == None: mode = app.enterMode
    if mode == 'normal':
        app.board[row][col] = str(number)
        app.legals = copy.deepcopy(app.legals)
        updateLegals(app.legals, row, col, str(number))
    elif mode == 'legals':
        legals = app.legals[row][col]
        if str(number) in legals:
            app.legals[row][col] = legals - set([str(number)])
        else: app.legals[row][col] = legals | set([str(number)])
    #die if wrong move in comp mode
    if (not app.wrongLabels and
        app.board[row][col] != app.solution[row][col]):
        sys.exit('Wrong.')
    #if we undid previously and are doing new moves
    if app.stateIndex != len(app.states) - 1:
        app.states = app.states[:app.stateIndex + 1]
    app.states.append(State(app.board, app.legals))
    app.stateIndex += 1
    checkWin(app)

def undo(app):
    app.hintCells = set() #clear hint
    if app.stateIndex <= 0: 
        app.message = Message("Can't undo anymore!")
        return
    app.stateIndex -= 1
    app.states[app.stateIndex].load(app)
    app.message = Message("Undid move")

def redo(app):
    app.hintCells = set() #clear hint
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
    if not app.showHints:
        app.message = Message("No auto-singletons in competition mode", 325)
        return
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

def hint1(app):
    if not app.showHints: 
        app.message = Message("Hints disabled in competition mode", 300)
        return
    hint = getHint(app, app.legals)
    if hint == None: 
        app.message = Message("No hints available", 240)
        return
    app.hintCells = hint.hintCells if hint.move == 'ban' else {hint.hintCells}

def hint2(app):
    if not app.showHints: 
        app.message = Message("Hints disabled in competition mode", 300)
        return
    hint = getHint(app, app.legals)
    if hint == None: 
        app.message = Message("No hints available", 240)
        return
    if hint.move == 'set':
        row, col = hint.moveCells
        app.message = Message(f"Filled in ({row}, {col})!")
        enterNum(app, row, col, hint.values.pop(), mode='normal')
        app.hintCells = {hint.hintCells}
    elif hint.move == 'ban':
        app.message = Message(f"Banned legals: {hint.values}", 240)
        for row, col in hint.moveCells:
            for legal in hint.values:
                if legal in app.legals[row][col]:
                    enterNum(app, row, col, legal, mode='legals')
        app.hintCells = hint.hintCells

def getHint(app, legals):
    singlesHint = nakedSingles(legals)
    if singlesHint != None: 
        app.message = Message('Singleton hint!')
        return singlesHint
    for n in range(2, 5):
        tuplesHint = nakedTuples(legals, n)
        if tuplesHint != None: 
            app.message = Message('Naked tuples here!')
            return tuplesHint
    xWingHint = xWing(legals)
    if xWingHint != None:
        app.message = Message('X-Wing!!')
        return xWingHint
    sidewaysXWing = xWingCols(legals)
    if sidewaysXWing != None:
        app.message = Message('X-Wing!!')
        return sidewaysXWing

def nakedSingles(legals):
    for row in range(9):
        for col in range(9):
            if len(legals[row][col]) == 1:
                cell = (row, col)
                setValue = copy.copy(legals[row][col])
                return Hint(cell, 'set', cell, setValue)

def nakedTuples(legals, n):
    for region in allRegionCoords():
        for target in combinations(region, n):
            targetLegals = [legals[row][col] for row, col in target]
            if set() in targetLegals: continue
            legalSet = set.union(*targetLegals)
            if len(legalSet) == n:
                banCells = list(set(region) - set(target))
                bans = [legals[row][col] for row, col in banCells]
                if legalSet & set().union(*bans) == set(): continue
                return Hint(set(target), 'ban', banCells, legalSet)

#strategy from https://www.sudokuwiki.org/X_Wing_Strategy
def xWing(legals):
    for legal in {'1', '2', '3', '4', '5', '6', '7', '8', '9'}:
        for startRow in range(9):
            cols = legalCols(getRow(legals, startRow), legal) #cols with naked double
            if len(cols) == 2:
                for endRow in range(startRow + 1, 9):
                    if legalCols(getRow(legals, endRow), legal) == cols:
                        startCol, endCol = cols
                        xWingCells = [(row, col) for row in [startRow, endRow] for col in [startCol, endCol]]
                        banCells = list()
                        #ban cells in the columns of the x wing that have the legal
                        for row, col in ([(row, startCol) for row in range(9) if row not in [startRow, endRow]] +
                                         [(row, endCol) for row in range(9) if row not in [startRow, endRow]]):
                            if legal in legals[row][col]: banCells.append((row, col))
                        if banCells != []: 
                            return Hint(xWingCells, 'ban', banCells, [legal])

def legalCols(rowCells, legal):
    return [col for col in range(9) if legal in rowCells[col]]

#above xwing checks rows, this checks cols
def xWingCols(legals):
    for legal in {'1', '2', '3', '4', '5', '6', '7', '8', '9'}:
        for startCol in range(9):
            rows = legalRows(getCol(legals, startCol), legal) #cols with naked double
            if len(rows) == 2:
                for endCol in range(startCol + 1, 9):
                    if legalRows(getCol(legals, endCol), legal) == rows:
                        startRow, endRow = rows
                        xWingCells = [(row, col) for row in [startRow, endRow] for col in [startCol, endCol]]
                        banCells = list()
                        for row, col in ([(startRow, col) for col in range(9) if col not in [startCol, endCol]] +
                                         [(endRow, col) for col in range(9) if col not in [startCol, endCol]]):
                            if legal in legals[row][col]: banCells.append((row, col))
                        if banCells != []: 
                            return Hint(xWingCells, 'ban', banCells, [legal])

def legalRows(colCells, legal):
    return [row for row in range(9) if legal in colCells[row]]

def writeFile(path, contents): #from https://www.cs.cmu.edu/~112-3/notes/term-project.html
    with open(path, "wt") as f:
        f.write(contents)

def checkWin(app):
    if app.board == app.solution: 
        app.win = True
        app.winTime = int(time.time() - app.startTime)
        if not app.showHints:
            try:
                saveBoard(app)
            except:
                app.message = Message('Board not saved :(')

def saveBoard(app):
    path = app.saveBoardPath + 'solved.txt'
    contents = ''
    for row in range(9):
        for col in range(9):
            contents += app.board[row][col] + ' '
        contents += '\n'
    writeFile(path, contents)
    app.message = Message('Board saved')

def game_onStep(app):
    app.counter += 1