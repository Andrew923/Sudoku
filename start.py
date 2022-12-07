from cmu_graphics import *
from classes import *
from solver import *
import random

def start_onScreenActivate(app):
    Button.buttons[__name__] = list()
    start_makeButtons(app)

def start(app): 
    app.enterMode = 'normal'
    app.win = False
    app.selection = app.selectNum = None
    app.selecting = False
    app.counter = 0
    app.states, app.stateIndex = list(), 0
    loadBoard(app, app.difficulty)
    app.showLegals = (app.difficulty != 'easy')
    setActiveScreen('game')

#for reading files, from https://www.cs.cmu.edu/~112-3/notes/term-project.html
def readFile(path):
    with open(path, "rt") as f:
        return f.read()

#loads app.board from file
def loadBoard(app, difficulty, boardNumber = None):
    difficultyToRange = {'easy': (1, 50),
                         'medium': (1, 50),
                         'hard': (1, 50),
                         'expert': (1, 25),
                         'evil': (1, 25)}
    random.seed()
    if boardNumber == None: boardNumber = str(random.randint(*difficultyToRange[difficulty]))
    path = f'boards/boards/{difficulty}-{boardNumber.zfill(2)}.png.txt'
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

def start_redrawAll(app):
    drawLogo(app)
    drawExtras(app)
    Button.drawButtons(app, __name__)

def drawExtras(app):
    drawLabel(f"Difficulty: {app.difficulty.capitalize()}", app.width/2,
              app.height*29/40, size=50, fill='royalBlue', bold=True, font=app.font)
    drawLabel("Competition Mode", app.width/2 - 80, app.height*15/16, font=app.font,
              size=18, fill='royalBlue', align='left')

def drawLogo(app):
    width = app.width/27
    letters = 'SUDOKU'
    for i in range(len(letters)):
        letter = getLetter(letters[i])
        rows, cols = len(letter), len(letter[0])
        top, left = app.height*7/40 + (5 - rows)*width, (4*i + 2)*width
        numbers = list(range(1, 10))
        random.seed(135)
        for row in range(rows):
            for col in range(cols):
                if letter[row][col]:
                    x, y = left + col*width, top + row*width
                    num = random.choice(numbers)
                    numbers.remove(num)
                    if numbers == []: numbers = list(range(1, 10))
                    fill = None if random.randint(0, 1) else 'darkGray'
                    drawRect(x, y, width, width, fill=fill, border='black')
                    drawLabel(num, x + width/2, y + width/2,
                              font=app.font, fill='royalBlue', size=16)
        
    
#very long unfortunately; just letters in list form
def getLetter(letter):
    S = [[1, 1, 1],
         [1, 0, 0],
         [1, 1, 1],
         [0, 0, 1],
         [1, 1, 1]]

    U = [[1, 0, 1],
         [1, 0, 1],
         [1, 1, 1]]

    D = [[0, 0, 1],
         [0, 0, 1],
         [1, 1, 1],
         [1, 0, 1],
         [1, 1, 1]]
         
    O = [[1, 1, 1],
         [1, 0, 1],
         [1, 1, 1]]
    
    K = [[1, 0, 0],
         [1, 0, 0],
         [1, 0, 1],
         [1, 1, 0],
         [1, 0, 1]]
    
    return eval(letter)

def start_makeButtons(app):
    difficulties = ['easy', 'medium', 'hard', 'expert', 'evil']
    for i in range(len(difficulties)):
        button = Button(__name__, difficulties[i].capitalize(), 
                        (i + 1)*app.width/6, app.height*7/8, app.width*3/20, 
                        app.height/16, size=26)
        button.onClick, button.args = changeDifficulty, (app, difficulties[i])
    play = Button(__name__, 'PLAY', app.width/2, app.height*23/40, 
                  app.width/5, app.height/8, bold=True, size=60)
    play.onClick, play.args = start, app
    loadBoard = Button(__name__, 'Load Board', app.width*3/27, app.height/16, 
                       app.width*3/25, app.height/20)
    loadBoard.onClick, loadBoard.args = load, app
    competition = Button(__name__, ' ', app.width/2 - 100, app.height*15/16,
                         app.height/40, app.height/40, fill=None,
                         border='black', labelFill='black', borderWidth = 2)
    competition.onClick, competition.args = competitionMode, app

def competitionMode(app):
    app.showHints = not app.showHints
    app.wrongLabels = not app.wrongLabels
    for button in Button.buttons[__name__]:
        if button.label == 'x': button.label = ' '
        elif button.label == ' ': button.label = 'x'

#load from file or graphically
def load(app):
    app.board = [['0']*app.cols for _ in range(app.rows)]
    setActiveScreen('loadBoard')

def changeDifficulty(app, difficulty):
    app.difficulty = difficulty

def start_onMouseMove(app, mouseX, mouseY):
    Button.checkHover(app, __name__, mouseX, mouseY)

def start_onMousePress(app, mouseX, mouseY):
    Button.checkClick(app, __name__, mouseX, mouseY)

def start_onKeyPress(app, key):
    if key == 'c': competitionMode(app)