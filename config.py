#this module contains all of the global variables for the Checkers Game

windowSize = (725, 725)
rows = 8
cols = 8
#first coordinate is x and second is y
#0,0 is the bottom left square
gameGrid = [] #for centerpoints of squares
pieceGrid = [] #for locs of pieces
sqrGrid = []
redList = []
blackList = []
#black goes first
redMoveDir = -1
blackMoveDir = 1
pieceSize = (60, 60)
redGUIPColor = [(153 / 255.0), (213 / 255.0), (201 / 255.0), 1]
blackGUIPColor = [(45 / 255.0), (3 / 255.0), (32 / 255.0), 1]
dummyColor = [(255 / 255.0), (255 / 255.0), (255 / 255.0), 1]
lightSqrColor = [(212 / 255.0), (237 / 255.0), (232 / 255.0), 1]
#lightSqrColor = [(255 / 255.0), (237 / 255.0), (223 / 255.0), 1]
darkSqrColor = [(105 / 255.0), (86 / 255.0), (98 / 255.0), 1]
#darkSqrColor = [(218 / 255.0), (163 / 255.0), (117 / 255.0), 1]
redHighlightColor = [(255 / 255.0), (218 / 255.0), (185 / 255.0), 1]
blackHighlightColor = [(236 / 255.0), (122 / 255.0), (122 / 255.0), 1]
darkSqrHighlightColor = [(177 / 255.0), (148 / 255.0), (166 / 255.0), 1]
moveLimit = 200
moveRate = 3
blackKingNorm = "blackKingNorm.png"
blackKingHighlight = "blackKingHighlight.png"
redKingNorm = "redKingNorm.png"
redKingHighlight = "redKingHighlight.png"
