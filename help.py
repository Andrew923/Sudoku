from cmu_graphics import *
from classes import *

def help_onScreenStart(app):
    app.keyboardUrl = 'images/keyboard-layout.jpg'
    help_makeButtons(app)

def help_makeButtons(app):
    back = Button(__name__, 'Back', app.width * 3 / 27, 50, 120, 40)
    back.onClick, back.args = setActiveScreen, 'game'

def help_redrawAll(app):
    drawLabel('Controls', app.width / 2, 50, size=52, bold=True,
              font=app.font, fill='dimGray')
    drawImage(app.keyboardUrl, 50 ,100, width = app.width - 75)
    drawMovementControls(app)
    drawNumberControls(app)
    drawOtherControls(app)
    Button.drawButtons(app, __name__)

def drawMovementControls(app):  
    color = 'royalBlue'
    left, startY = 50, 420
    drawLabel('Movement', left, startY, size=32, bold=True,
              font=app.font, fill=color, align='left')
    labels = ["Left:", " Move left (duh)",
              "Right:", " Move right",
              "Up:", " Move up",
              "Down:", " You won't believe it",
              "Space:", " Toggle selection"]
    for i in range(len(labels)):
        drawLabel(labels[i], left, startY + 30 * (i + 1), size=18,
                  font=app.font, align='left')
    
def drawNumberControls(app):
    color = 'cyan'
    left, startY = 50 + (app.width - 100) / 3, 420
    drawLabel('Numbers', left, startY, size=32, bold=True,
              font=app.font, fill=color, align='left')
    labels = ["1-9:", " Enter numbers"]
    for i in range(len(labels)):
        drawLabel(labels[i], left, startY + 30 * (i + 1), size=18,
                  font=app.font, align='left')

def drawOtherControls(app):
    color = rgb(60, 172, 222)
    left, startY = 50 + 2 * (app.width - 100) / 3, 420
    drawLabel('Other', left, startY, size=32, bold=True,
              font=app.font, fill=color, align='left')
    labels = ["Esc: Open help screen",
              "z: Undo last move",
              "y: Redo move",
              "s: Play a singleton",
              "S: Play all singletons",
              "l: Toggle entering mode",
              "L:  Toggle legals",
              "r: Restart"]
    for i in range(len(labels)):
        drawLabel(labels[i], left, startY + 30 * (i + 1), size=18,
                  font=app.font, align='left')

def help_onMouseMove(app, mouseX, mouseY):
    Button.checkHover(app, __name__, mouseX, mouseY)

def help_onMousePress(app, mouseX, mouseY):
    Button.checkClick(app, __name__, mouseX, mouseY)

def help_onKeyPress(app, key):
    if key == 'escape': setActiveScreen('game')