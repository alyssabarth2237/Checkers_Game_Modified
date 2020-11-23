#this file contains the Sqr (square) class
from kivy.uix.widget import Widget
from kivy.graphics import Rectangle, Color

#*******************************************************
from config import dummyColor, lightSqrColor, darkSqrColor, darkSqrHighlightColor
#*******************************************************

class Sqr(Widget):
    def __init__(self, sqrColorIn, locIn, posIn, sizeIn, canvasIn,):
        self.sqrColor = sqrColorIn
        self.loc = locIn
        self.sqrPos = posIn #tupple of 2 not point
        self.sqrSize = sizeIn #tupple of 2 not point
        self.boardCanvas = canvasIn
        self.normColor = dummyColor
        self.highlightColor = dummyColor
        if self.sqrColor == "dark":
            self.normColor = darkSqrColor
            self.highlightColor = darkSqrHighlightColor
        else:
            self.normColor = lightSqrColor
            #no highlight color needed
        self.boardCanvas.add(Color(*self.normColor))
        self.shape = Rectangle(pos=self.sqrPos, size=self.sqrSize)
        self.boardCanvas.add(self.shape)
