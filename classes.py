try: from cmu_cs3_graphics import *
except: from cmu_graphics import *
import copy
from collections import defaultdict

class State(object):
    def __init__(self, board ,legals):
        self.board = copy.deepcopy(board)
        self.legals = copy.deepcopy(legals)

    def load(self, app):
        app.board = copy.deepcopy(self.board)
        app.legals = copy.deepcopy(self.legals)

    def __repr__(self):
        return f"{self.board}"

class Button(object):
    buttons = defaultdict(list)

    def __init__(self, screen, label, x, y, width, height, **kwargs):
        self.fill = kwargs.get('fill', 'cornflowerBlue')
        self.border = kwargs.get('border', None)
        self.borderWidth = kwargs.get('borderWidth', 0)
        self.labelFill = kwargs.get('labelFill', 'lightCyan')
        self.size = kwargs.get('size', 18)
        self.bold = kwargs.get('bold', False)
        self.label = label
        self.x, self.y = x, y
        self.width, self.height = width, height
        self.hover = False
        self.onClick = self.args = None
        Button.buttons[screen].append(self)
    
    def hover(self):
        self.hover = not self.hover

    @staticmethod
    def drawButtons(app, screen):
        for button in Button.buttons[screen]:
            multiplier = (1 + button.hover * 0.2)
            width = button.width * multiplier
            height = button.height * multiplier
            drawBox(app, button.x, button.y, width, height,
                    fill=button.fill, border=button.border,
                    borderWidth = button.borderWidth)
            drawLabel(button.label, button.x, button.y, font=app.font,
                      size=button.size*multiplier, fill=button.labelFill,
                      bold=button.bold)

    @staticmethod
    def checkHover(app, screen, x, y):
        for button in Button.buttons[screen]:
            if (abs(button.x - x) < button.width * 0.55 and
                abs(button.y - y) < button.height * 0.55):
                button.hover = True
            else: button.hover = False
    
    @staticmethod
    def checkClick(app, screen, x, y):
        for button in Button.buttons[screen]:
            if (button.onClick != None and
                abs(button.x - x) < button.width * 0.55 and
                abs(button.y - y) < button.height * 0.55):
                if isinstance(button.args, tuple):
                    button.onClick(*button.args)
                else: button.onClick(button.args)
                

class Message(object):
    message = None

    def __init__(self, label):
        self.label = label
        self.opacity = 100
        Message.message = self        

    def draw(self, app):
        if self.opacity <= 0: return
        x, y = 860, 50
        drawBox(app, x, y, 220, 40,
                border='black', opacity=self.opacity)
        drawLabel(self.label, x, y, size=14,
                  font=app.font,
                  opacity=self.opacity)
        self.opacity -= 2


#very lengthy, but makes rounded edges
def drawBox(app, x, y, width, height, **kwargs):
    opacity = kwargs.get('opacity', 100)
    fill = kwargs.get('fill', None)
    border = kwargs.get('border', fill)
    borderWidth = kwargs.get('borderWidth', 2)
    r = min(width, height) / 5
    for signX in [-1, 1]:
        for signY in [-1, 1]:
            cx, cy = x + signX * (width / 2 - r), y + signY * (height / 2 - r)
            drawCircle(cx, cy, r, fill=fill, border=border,
                    borderWidth=borderWidth, opacity=opacity)
            signsToTheta = {(-1, -1): 0, (1, -1): 90, (1, 1): 180, (-1, 1): 270}
            if fill == None:
                drawArc(cx, cy, r * 2.2, r * 2.2, signsToTheta[(signX, signY)],
                        270, fill='white')
    if fill == None: #draws lines for edges
        drawLine(x - width / 2 + r, y + height / 2, x + width / 2 - r,
                 y + height / 2, fill=border, opacity=opacity)
        drawLine(x - width / 2 + r, y - height / 2, x + width / 2 - r, 
                 y - height / 2, fill=border, opacity=opacity)
        drawLine(x - width / 2, y - height / 2 + r, x - width / 2,
                 y + height / 2 - r, fill=border, opacity=opacity)
        drawLine(x + width / 2, y - height / 2 + r, x + width / 2,
                 y + height / 2 - r, fill=border, opacity=opacity)
    else: #draws rectangles across whole box
        drawRect(x, y, width - 2 * r, height, fill=fill, align='center')
        drawRect(x, y, width, height - 2 * r, fill=fill, align='center')