  /$$$$$$                  /$$           /$$                
 /$$__  $$                | $$          | $$                
| $$  \__/ /$$   /$$  /$$$$$$$  /$$$$$$ | $$   /$$ /$$   /$$
|  $$$$$$ | $$  | $$ /$$__  $$ /$$__  $$| $$  /$$/| $$  | $$
 \____  $$| $$  | $$| $$  | $$| $$  \ $$| $$$$$$/ | $$  | $$
 /$$  \ $$| $$  | $$| $$  | $$| $$  | $$| $$_  $$ | $$  | $$
|  $$$$$$/|  $$$$$$/|  $$$$$$$|  $$$$$$/| $$ \  $$|  $$$$$$/
 \______/  \______/  \_______/ \______/ |__/  \__/ \______/ 
                                                                                                  

Description
-----------
A minimalistic sudoku app with lots of the color blue! 

Usage
-----
main.py is the main file to run in order to start the app. help.py, game.py,
loadBoard.py, and start.py are all different files for different screens in the
app. In line 34 of main.py, initialScreen can be set to any of these other 
screens if you really want to see them for some reason.

classes.py contains the classes used in the app (State, Button, and Message).
solver.py contains the backtracking code for solving the Sudoku board and also
some helper functions for getting coordinates of regions and stuff.

Dependencies
------------
- Cmu graphics!: used for obvious reasons, the only library that actually needs
                 to be installed (https://academy.cs.cmu.edu/desktop)
- copy: for making deepcopies of 2d lists
- collections: used defaultdict from this module to create dictionaries
               with default values of lists in classes.py; maps screens
               to list of buttons on each screen
- random: for random boards, also helps generate title screen art
- itertools: used combinations to generate subsets of cells when looking for
             naked tuples
- time: for game timer because the in-app counter was being weird
- sys: to kill the app when you make a wrong move in competition mode

References
----------
Ascii art for this readme was generated at https://patorjk.com/software/taag/.
Everything else is cited in-line in code (ctrl f 'https' or something if you 
want to see).