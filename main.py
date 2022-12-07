from cmu_graphics import *
from start import *
from game import *
from help import *
from loadBoard import *
from collections import defaultdict

#Extra Stuff:
#1. Hopefully the UI doesn't look terrible; you can see buttons
#   and messages in classes.py
#2. I think the backtracker is decent? idk I tried my best;
#   all the testing can bee seen in test.ipynb
#3. added X-Wing hint generation (ctrl f xwing in game.py)

#reload buttons when resize
def onResize(app):
    app.boardLeft = app.width/10
    app.boardTop = app.height/8
    app.boardWidth = app.boardHeight = min(app.width, app.height)*3/4
    Button.buttons = defaultdict(list)
    start_makeButtons(app)
    game_makeButtons(app)
    loadBoard_makeButtons(app)

def onAppStart(app):
    app.difficulty = 'easy'
    app.font = 'monospace'
    app.showHints = app.wrongLabels = True
    app.saveBoard = False
    app.saveBoardPath = "solvedBoards/"
    app.stepsPerSecond = 120

def main():
    runAppWithScreens(initialScreen='start', height=800, width=1000)

main()