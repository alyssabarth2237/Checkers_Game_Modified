from config import dummyColor, rows, cols, blackMoveDir, redMoveDir
from point import Point
from gamePiece import GamePiece


class VirtualPiece(GamePiece):
    def __init__(self, pColorIn, locIn, canvasIn, pieceNumIn, pieceGrid, gameGrid):
        super().__init__(pColorIn, locIn, canvasIn, pieceNumIn, pieceGrid, gameGrid)
        self.type = "virtual"
        if pColorIn == "red":
            if redMoveDir == -1:
                self.lastRow = 0
            else:
                self.lastRow = 7
            self.moveDir = redMoveDir
        elif pColorIn == "black":
            if blackMoveDir == 1:
                self.lastRow = 7
            else:
                self.lastRow = 0
            self.moveDir = blackMoveDir
        else:
            #throw error
            self.lastRow = -2
            self.moveDir = -10
            self.guiPColor = dummyColor





def makeTestBoard():
    #returns a virtual pieceGrid (currently the starting position)
    pieceGrid = []
    redPoints = []
    blackPoints = []

    for x in range(cols):
        currColPiece = []  # for dummys in pieceGrid
        for y in range(int(rows / 2)):

            currColPiece.append(GamePiece(dummyColor, Point(x, (y * 2)), "canvas", -1, pieceGrid, "gameGrid"))

            currColPiece.append(GamePiece(dummyColor, Point(x, (y * 2 + 1)), "canvas", -1, pieceGrid, "gameGrid"))

        pieceGrid.append(currColPiece)

    firstY = 0
    lastY = 0
    if blackMoveDir == 1:
        firstY = 0
        lastY = 2
    else:
        firstY = 5
        lastY = 7

    lastY = 1
    for y in range(firstY, lastY + 1):
        for x in range(int(cols / 2)):
            pieceGrid[x * 2 + (y % 2)][y] = VirtualPiece("black", Point(x * 2 + (y % 2), y), "canvas", -1, pieceGrid, "gameGrid")
            blackPoints.append(Point(x * 2 + (y % 2), y))
    pieceGrid[0][2] = VirtualPiece("black", Point(0, 2), "canvas", -1, pieceGrid, "gameGrid")
    blackPoints.append(Point(0, 2))
    pieceGrid[6][2] = VirtualPiece("black", Point(6, 2), "canvas", -1, pieceGrid, "gameGrid")
    blackPoints.append(Point(6, 2))
    pieceGrid[4][4] = VirtualPiece("black", Point(4, 4), "canvas", -1, pieceGrid, "gameGrid")
    blackPoints.append(Point(4, 4))
    pieceGrid[5][5] = VirtualPiece("black", Point(5, 5), "canvas", -1, pieceGrid, "gameGrid")
    blackPoints.append(Point(5, 5))
    # creating red pieces
    if redMoveDir == -1:
        firstY = 5
        lastY = 7
    else:
        firstY = 0
        lastY = 2
    blah = 0
    for y in range(firstY, lastY + 1):
        for x in range(int(cols / 2)):
            if ((x * 2 + (y % 2)) == 2) and (y == 6):
                blah += 1
            elif ((x * 2 + (y % 2)) == 5) and (y == 5):
                blah += 1
            else:
                pieceGrid[x * 2 + (y % 2)][y] = VirtualPiece("red", Point(x * 2 + (y % 2), y), "canvas", -1, pieceGrid, "gameGrid")
                redPoints.append(Point(x * 2 + (y % 2), y))
    pieceGrid[0][4] = VirtualPiece("red", Point(0, 4), "canvas", -1, pieceGrid, "gameGrid")
    redPoints.append(Point(0, 4))

    # for y in range(firstY, lastY + 1):
    #     for x in range(int(cols / 2)):
    #         pieceGrid[x * 2 + (y % 2)][y] = VirtualPiece("black", Point(x * 2 + (y % 2), y), "canvas", -1, pieceGrid, "gameGrid")
    # # creating red pieces
    # if redMoveDir == -1:
    #     firstY = 5
    #     lastY = 7
    # else:
    #     firstY = 0
    #     lastY = 2
    # for y in range(firstY, lastY + 1):
    #     for x in range(int(cols / 2)):
    #         pieceGrid[x * 2 + (y % 2)][y] = VirtualPiece("red", Point(x * 2 + (y % 2), y), "canvas", -1, pieceGrid, "gameGrid")

    blackStr = "[ "
    for blackPt in blackPoints:
        blackStr += blackPt.printStr()
        if (blackPt != blackPoints[-1]):
            blackStr += ', '
    blackStr += ' ]'
    print("Black Points:")
    print(blackStr)
    redStr = "[ "
    for redPt in redPoints:
        redStr += redPt.printStr()
        if (redPt != redPoints[-1]):
            redStr += ', '
    redStr += ' ]'
    print("Red Points:")
    print(redStr)


    return pieceGrid

def ptListPrintStr(listIn):
    str = "[ "
    for pt in listIn:
        str += f"({pt.x}, {pt.y})"
        if pt != listIn[-1]:
            str+= ", "
    str += " ]"
    return str

