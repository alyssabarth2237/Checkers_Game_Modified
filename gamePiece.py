#this file contains the GamePiece, Pawn, and King classes

from kivy.uix.widget import Widget
from kivy.graphics import Color, Ellipse

#*******************************************************
from config import redMoveDir, blackMoveDir, pieceSize, redGUIPColor, blackGUIPColor, \
    dummyColor, redHighlightColor, blackHighlightColor, blackKingNorm, \
    blackKingHighlight, redKingNorm, redKingHighlight
from boardCheck import BoardCheck
#*******************************************************

class GamePiece(Widget):
    def __init__(self, pColorIn, locIn, canvasIn, pieceNumIn, pieceGrid, gameGrid):
        self.type = "None"
        self.pColor = pColorIn
        self.loc = locIn
        self.lastRow = -2
        self.moveDir = -10
        self.guiPColor = dummyColor
        self.boardCheck = BoardCheck()
        self.boardCanvas = canvasIn
        self.shape = "None"
        self.pieceNum = pieceNumIn
        self.highlightColor = dummyColor

    @property
    def type(self):
        return self._type
    @type.setter
    def type(self, val):
        self._type = val
    @property
    def pColor(self):
        return self._pColor
    @pColor.setter
    def pColor(self, val):
        self._pColor = val
    @property
    def loc(self):
        return self._loc
    @loc.setter
    def loc(self, val):
        self._loc = val
    @property
    def lastRow(self):
        return self._lastRow
    @lastRow.setter
    def lastRow(self, val):
        self._lastRow = val
    @property
    def moveDir(self):
        return self._moveDir
    @moveDir.setter
    def moveDir(self, val):
        self._moveDir = val
    @property
    def guiPColor(self):
        return self._guiPColor
    @guiPColor.setter
    def guiPColor(self, val):
        self._guiPColor = val
    @property
    def boardCanvas(self):
        return self._boardCanvas
    @boardCanvas.setter
    def boardCanvas(self, val):
        self._boardCanvas = val
    @property
    def shape(self):
        return self._shape
    @shape.setter
    def shape(self, val):
        self._shape = val
    @property
    def pieceNum(self):
        return self._pieceNum
    @pieceNum.setter
    def pieceNum(self, val):
        self._pieceNum = val
    @property
    def highlightColor(self):
        return self._highlightColor
    @highlightColor.setter
    def highlightColor(self, val):
        self._highlightColor = val

class Pawn(GamePiece):
    def __init__(self, pColorIn, locIn, canvasIn, pieceNumIn, pieceGrid, gameGrid):
        #print("Pawn init Called...")
        super().__init__(pColorIn, locIn, canvasIn, pieceNumIn, pieceGrid, gameGrid)
        self.type = "pawn"
        if pColorIn == "red":
            if redMoveDir == -1:
                self.lastRow = 0
            else:
                self.lastRow = 7
            self.moveDir = redMoveDir
            self.guiPColor = redGUIPColor
            self.highlightColor = redHighlightColor
        elif pColorIn == "black":
            if blackMoveDir == 1:
                self.lastRow = 7
            else:
                self.lastRow = 0
            self.moveDir = blackMoveDir
            self.guiPColor = blackGUIPColor
            self.highlightColor = blackHighlightColor
        else:
            #throw error
            self.lastRow = -2
            self.moveDir = -10
            self.guiPColor = dummyColor
        #pos=(gameGrid[locIn.x][locIn.y].x, gameGrid[locIn.x][locIn.y].y)

        if (self.boardCheck.isOpen(pieceGrid, self.loc) == True) and (self.boardCheck.isInvalid(self.loc) == False):
            self.boardCanvas.add(Color(*self.guiPColor))
            self.shape = Ellipse(pos=(gameGrid[locIn.x][locIn.y].x - (pieceSize[0] / 2), gameGrid[locIn.x][locIn.y].y - (pieceSize[1] / 2)), size=pieceSize)
            self.pos = (gameGrid[locIn.x][locIn.y].x - (pieceSize[0] / 2), gameGrid[locIn.x][locIn.y].y - (pieceSize[1] / 2))
            self.boardCanvas.add(self.shape)
        else:
            #throw error
            print('error')

    @property
    def pos(self):
        return self._pos
    @pos.setter
    def pos(self, value):
        self._pos = value
        self.shape.pos = self._pos

class King(GamePiece):
    def __init__(self, pColorIn, locIn, canvasIn, pieceNumIn, pieceGrid, gameGrid):
        super().__init__(pColorIn, locIn, canvasIn, pieceNumIn, pieceGrid, gameGrid)
        self.moveDir = 1 #1 vs -1 doesn't matter but picked one to make life easier
        self.type = "king"
        if pColorIn == "red":
            if redMoveDir == -1:
                self.lastRow = 0
            else:
                self.lastRow = 7
            self.guiPColor = redKingNorm
            self.highlightColor = redKingHighlight
        elif pColorIn == "black":
            if blackMoveDir == 1:
                self.lastRow = 7
            else:
                self.lastRow = 0
            self.guiPColor = blackKingNorm
            self.highlightColor = blackKingHighlight
        else:
            #throw error
            self.lastRow = -2
            self.moveDir = -10
            self.guiPColor = dummyColor

        #************************

        if (self.boardCheck.isOpen(pieceGrid, self.loc) == True) and (self.boardCheck.isInvalid(self.loc) == False):
            self.boardCanvas.add(Color(*dummyColor))
            self.shape = Ellipse(pos=(gameGrid[locIn.x][locIn.y].x - (pieceSize[0] / 2), gameGrid[locIn.x][locIn.y].y - (pieceSize[1] / 2)), size=pieceSize, source=self.guiPColor)
            self.pos = (gameGrid[locIn.x][locIn.y].x - (pieceSize[0] / 2), gameGrid[locIn.x][locIn.y].y - (pieceSize[1] / 2))
            self.boardCanvas.add(self.shape)
        else:
            #throw error
            print('error')

    @property
    def pos(self):
        return self._pos
    @pos.setter
    def pos(self, value):
        self._pos = value
        self.shape.pos = self._pos


