# ************************** General Fixmes (In Order) *********************************
# Value Function Ideas:
# -- Adance in Mass: group clusters or two checkers next to each other?
# -- Take the Center of the Board: ??? Distance to Center if not a king and in your first row???
# -- Change distance to last row to either distance to most exposed last row piece or open last row space

# FIXME: MUST FIX VALUE FUNCTION TO HAVE AI CAPTURE PIECES WHEN THEY ARE FAR AWAY AT END OF GAME
# FIXME: Probably need to put more emphasis on kings and being closer to a king and less on edges at end of game
# FIXME: Also should probably put more weight into capturing pieces at end of game and being closer to pieces
# FIXME: Also need to check that it works as intended for even and odd numbers
# FIXME: MUST RESEARCH REINFORCEMENT LEARNING ALGORITHMS AND HOW TO SET REWARDS AND UPDATE FUNCTION
# FIXME: MUST RESEARCH WHAT OTHER PEOPLE HAVE DONE TO SEE IF I SHOULD USE A LINEAR MODEL OR A NEURAL NETWORK (ALONG WITH STRUCTURE)
# FIXME: MUST RESTRUCTURE CODE SO RUNS WITHOUT TRIGGERS FOR TRAINING
# FIXME: MUST TRAIN MODEL VS MINIMAX SEARCH
# FIXME: MUST LOOKUP WHETHER OR NOT I CAN USE A CHECKERS API TO TEST MY MODEL
# FIXME: MUST LIMIT USER MOVE CHOICES SO MUST TAKE JUMP IF ONE IS AVAILABLE (ONLY THE AI HAS TO DO THIS NOW)
# FIXME: MUST END GAME WHEN USER HAS NO LEGAL MOVES LEFT AND HAVE RED WIN
# FIXME: MUST VALIDATE AND GATHER DATA ON MY MODEL BY TUESDAY EVENING
# **************************************************************************************

# FIXME: FIX SO MUST TAKE JUMP ON FIRST MOVE IF AVAILABLE (CHECK RULES AND MAKE SURE THIS IS CORRECT AND ALL ARE FOLLOWED)


from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout
from kivy.graphics import Rectangle, Color, Ellipse
from kivy.core.window import Window
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.config import Config
from copy import deepcopy
from gc import collect
from sys import argv
#******************************
from config import windowSize, rows, cols, redMoveDir, blackMoveDir, pieceSize, redGUIPColor, \
    blackGUIPColor, dummyColor, lightSqrColor, darkSqrColor, redHighlightColor, blackHighlightColor, \
    darkSqrHighlightColor, moveLimit, moveRate, blackKingNorm, blackKingHighlight, redKingNorm, \
    redKingHighlight
from point import Point
from boardCheck import BoardCheck
from gamePiece import GamePiece, Pawn, King
from sqr import Sqr
from referee import Referee
from minimaxSearch import Tree, minimax, alphaMin, betaMax, randomMove
from testFunctions import ptListPrintStr
#******************************

# ***Important Notes***
# cols = x
# rows = y
# pieceGrid[x][y] = pieceGrid[col][row] = pieceGrid[j][i] (with j outer and i inner)
# for cols (for rows) = for x (for y)

dummyMove = (Point(-1, -1), [])


# *****Command Line Arguments******
normalMode = True
if len(argv) == 2:
    if str(argv[1]) == "random":
        normalMode = False

# *********************************


class CheckersGame(GridLayout):
    def __init__(self, **kwargs):
        super(CheckersGame, self).__init__(**kwargs)
        # first coordinate is x and second is y
        # 0,0 is the bottom left square
        self.gameGrid = []  # for centerpoints of squares
        self.pieceGrid = []  # for locs of pieces
        self.sqrGrid = []
        self.redList = []
        self.blackList = []
        self.board = RelativeLayout()
        self.board.pos = ((Window.height/10), (Window.height/10))
        self.board.size = (8*(Window.height/10), 8*(Window.height/10))
        self.add_widget(self.board)

        self.pieces = RelativeLayout()
        self.pieces.pos = ((Window.height/10), (Window.height/10))
        self.pieces.size = (8*(Window.height/10), 8*(Window.height/10))
        self.add_widget(self.pieces)

        self.selected = Point(-1, -1)
        self.referee = Referee()
        self.turn = "None"
        self.lightSqrs = []
        self.selectedSqr = Point(-1, -1)
        self.moveCount = 0
        self.alreadyCaptured = False
        self.isJumping = False
        self.prevMoveMax = dummyMove
        self.prevPrevMoveMax = dummyMove
        self.prevMoveMin = dummyMove
        self.prevPrevMoveMin = dummyMove
        self.tempCurrPtMin = Point(-1, -1)
        self.tempCurrEndPtsMin = []

        #**************************
        self.redPiecePt = Point(-1, -1)
        self.redEndPts = []
        #**************************

        fstColor = dummyColor
        fstColorName = "None"
        sndColor = dummyColor
        sndColorName = "None"
        for x in range(cols):
            currColGame = [] #append from bottom (y = 0) to top (y = 7)
            currColPiece = [] #for dummys in pieceGrid
            currColSqr = [] #for board square rectangles
            for y in range(int(rows/2)):
                if (x % 2) == 0:
                    fstColor = darkSqrColor
                    fstColorName = "dark"
                    sndColor = lightSqrColor
                    sndColorName = "light"
                else:
                    fstColor = lightSqrColor
                    fstColorName = "light"
                    sndColor = darkSqrColor
                    sndColorName = "dark"

                #Color(*fstColor)
                sqrPos = (x * (self.board.height / 8.0), (y * 2.0) * (self.board.height / 8.0))
                sqrSize = (self.board.height / 8.0, self.board.height / 8.0)
                currColSqr.append(Sqr(fstColorName, Point(x, y * 2), sqrPos, sqrSize, self.board.canvas))
                centerPt = Point(x * (self.board.height / 8.0) + (self.board.height / 8.0) / 2.0,  (y * 2.0) * (self.board.height / 8.0) + (self.board.height / 8.0) / 2.0)
                currColGame.append(centerPt)
                currColPiece.append(GamePiece(dummyColor, Point(x, (y * 2)), self.pieces.canvas, -1, self.pieceGrid, self.gameGrid))

                #Color(*sndColor)
                sqrPos = (x * (self.board.height / 8.0), (y * 2.0 + 1.0) * (self.board.height / 8.0))
                sqrSize = (self.board.height / 8.0, self.board.height / 8.0)
                currColSqr.append(Sqr(sndColorName, Point(x, (y * 2 + 1)), sqrPos, sqrSize, self.board.canvas))
                centerPt = Point(x * (self.board.height / 8.0) + (self.board.height / 8.0) / 2.0, (y * 2.0 + 1.0) * (self.board.height / 8.0) + (self.board.height / 8.0) / 2.0)
                currColGame.append(centerPt)
                currColPiece.append(GamePiece(dummyColor, Point(x, (y * 2 + 1)), self.pieces.canvas, -1, self.pieceGrid, self.gameGrid))

            self.gameGrid.append(currColGame)
            self.pieceGrid.append(currColPiece)
            self.sqrGrid.append(currColSqr)

        self.btn = Button(text='New Game', font_size=14, background_color=(1, 0, 0, 1), pos=(0, 0), size=(Window.height / 10, Window.height / 10))
        self.add_widget(self.btn)
        self.btn.bind(on_press=self.startingPieces)


    def clearPiece(self, pieceIn):
        #print("Clearning Piece...")
        self.pieces.canvas.remove(pieceIn.shape)
        #self._entities.remove(entity)
        return

    def startingPieces(self, instance):
        #handles pieceGrid, redList, and blackList
        #make sure board was cleared before if restarting
        self.clearBoard("dummy input")
        #create all pieces
        #creating black pieces
        firstY = 0
        lastY = 0
        if blackMoveDir == 1:
            firstY = 0
            lastY = 2
        else:
            firstY = 5
            lastY = 7
        pieceNum = 0
        for y in range(firstY, lastY + 1):
            for x in range(int(cols/2)):
                #print("Black: (%i, %i)" % (x * 2 + (y % 2), y))
                self.pieceGrid[x * 2 + (y % 2)][y] = Pawn("black", Point(x * 2 + (y % 2), y), self.pieces.canvas, pieceNum, self.pieceGrid, self.gameGrid)
                self.blackList.append(pieceNum)
                #print(self.pieceGrid[x * 2 + (y % 2)][y].type)
                pieceNum += 1
        #creating red pieces
        if redMoveDir == -1:
            firstY = 5
            lastY = 7
        else:
            firstY = 0
            lastY = 2
        for y in range(firstY, lastY + 1):
            for x in range(int(cols / 2)):
                #print("Red: (%i, %i)" % (x * 2 + (y % 2), y))
                self.pieceGrid[x * 2 + (y % 2)][y] = Pawn("red", Point(x * 2 + (y % 2), y), self.pieces.canvas, pieceNum, self.pieceGrid, self.gameGrid)
                self.redList.append(pieceNum)
                #print(self.pieceGrid[x * 2 + (y % 2)][y].type)
                pieceNum += 1
        print("Done creating pieces...")
        self.turn = "black"
        print(" { Black's Turn }")
        return

    def clearBoard(self, instance):
        # TODO: Fixed
        #print("clearBoard Called...")
        #clear all current pieces from board
        # handles pieceGrid, redList, and blackList
        #self.clearPiece(self.pawn)
        for x in range(cols):
            for y in range(rows):
                if (self.pieceGrid[x][y].type != "None"):
                    #print("Calling clearPiece...")
                    self.clearPiece(self.pieceGrid[x][y])
                    self.pieceGrid[x][y] = GamePiece(dummyColor, Point(x, y), self.pieces.canvas, -1, self.pieceGrid, self.gameGrid)
        #now must clear redList and blackList
        self.redList.clear()
        self.blackList.clear()
        self.selected = Point(-1, -1)
        self.turn = "None"
        self.lightSqrs = []
        self.selectedSqr = Point(-1, -1)
        self.moveCount = 0
        self.alreadyCaptured = False
        self.isJumping = False
        self.prevMoveMax = dummyMove
        self.prevPrevMoveMax = dummyMove
        self.prevMoveMin = dummyMove
        self.prevPrevMoveMin = dummyMove

        return

    def selectObj(self, pt):
        if (pt != Point(-1, -1)):
            #actual piece is selected
            if (self.pieceGrid[pt.x][pt.y].type != "None"):
                #game piece and not square
                #self.pieces.canvas.remove(self.pieceGrid[pt.x][pt.y].shape)
                if self.pieceGrid[pt.x][pt.y].type == "pawn":
                    self.pieces.canvas.remove(self.pieceGrid[pt.x][pt.y].shape)
                    self.pieces.canvas.add(Color(*self.pieceGrid[pt.x][pt.y].highlightColor))
                    self.pieces.canvas.add(self.pieceGrid[pt.x][pt.y].shape)
                else:
                    self.pieceGrid[pt.x][pt.y].shape.source = self.pieceGrid[pt.x][pt.y].highlightColor
                self.selected = pt
        return
    def deselectObj(self):
        if (self.selected != Point(-1, -1)):
            #actual piece or sqr is selected
            if self.pieceGrid[self.selected.x][self.selected.y].type != "None":
                #game piece selected
                if self.pieceGrid[self.selected.x][self.selected.y].type == "pawn":
                    self.pieces.canvas.remove(self.pieceGrid[self.selected.x][self.selected.y].shape)
                    self.pieces.canvas.add(Color(*self.pieceGrid[self.selected.x][self.selected.y].guiPColor))
                    self.pieces.canvas.add(self.pieceGrid[self.selected.x][self.selected.y].shape)
                else:
                    self.pieceGrid[self.selected.x][self.selected.y].shape.source = self.pieceGrid[self.selected.x][self.selected.y].guiPColor

                self.delHighlightSqrs()
                self.selected = Point(-1, -1)
        return

    def highlightSqrs(self, ptList):
        #highlight sqrs for possible moves based on selected piece
        for pt in ptList:
            self.board.canvas.remove(self.sqrGrid[pt.x][pt.y].shape)
            self.board.canvas.add(Color(*self.sqrGrid[pt.x][pt.y].highlightColor))
            self.board.canvas.add(self.sqrGrid[pt.x][pt.y].shape)
            self.lightSqrs.append(pt)
        return

    def delHighlightSqrs(self):
        #stored in self.lightSqrs
        if self.lightSqrs: #self.lightSqrs is not an empty list
            for pt in self.lightSqrs:
                self.board.canvas.remove(self.sqrGrid[pt.x][pt.y].shape)
                self.board.canvas.add(Color(*self.sqrGrid[pt.x][pt.y].normColor))
                self.board.canvas.add(self.sqrGrid[pt.x][pt.y].shape)
                self.lightSqrs = []
        return

    def on_touch_down(self, touch):
        # TODO: must handle color's turns with being able to select stuff
        #will check for possible moves before selecting here
        #will not select if no moves are possible or if its not the color's turn
        #print("on_touch_down Called...")
        if (touch.x > self.board.pos[0]) and (touch.x < (Window.height - self.board.pos[0])) and (touch.y > self.board.pos[1]) and (touch.y < (Window.height - self.board.pos[1])):
            #determine which square for piece
            #get x pos
            print((touch.x, touch.y))
            x = (touch.x - self.board.pos[0]) / (self.board.height / 8.0)
            x = int(x)
            #get y pos
            y = (touch.y - self.board.pos[1]) / (self.board.height / 8.0)
            y = int(y)
            pt = Point(x, y)
            if self.selectedSqr == Point(-1, -1):
                if (self.pieceGrid[x][y].type != "None") and (self.isJumping == False):
                    # print(" * Clicked Piece")
                    if (self.pieceGrid[x][y].pColor == self.turn):
                        if (self.selected != pt):
                            #select object
                            #deselect selected piece
                            self.deselectObj()
                            #select new piece
                            self.selectObj(pt)
                            #now must highlightSqrs(list) any possible move sqrs
                            howCanMoveRslt = self.referee.howCanMove(pt, self.pieceGrid) #returns a list of possible moves (in pt form) for current piece at pt
                            endPts = howCanMoveRslt[0]
                            if endPts:
                                self.highlightSqrs(endPts)

                        else:
                            #second click to deselect already selected obj
                            self.deselectObj()
                            #now must deHighlightSqrs() any self.lightSqrs from prev. selection

                else:
                    # print(" * Clicked Sqr")
                    #(must be able to select highlighted squares for next move)
                    if pt in self.lightSqrs:
                        # can select square
                        self.selectedSqr = pt

                        if self.tempCurrPtMin == Point(-1, -1):
                            self.tempCurrPtMin = self.selected
                        self.tempCurrEndPtsMin.append(pt)


                        #set self.isJumping to true if jumping here
                        if abs(self.selectedSqr.x - self.selected.x) > 1:
                            #jumping
                            self.isJumping = True


            #   #this is where the move piece function will be called
        elif (touch.x > 0) and (touch.x < self.board.pos[0]) and (touch.y > 0) and (touch.y < self.board.pos[1]):
            self.startingPieces("dummy instance")

        return

    def capture(self, pt):
        print(" * Piece Captured *")
        self.pieces.canvas.remove(self.pieceGrid[pt.x][pt.y].shape)
        if self.pieceGrid[pt.x][pt.y].pColor == "black":
            self.blackList.remove(self.pieceGrid[pt.x][pt.y].pieceNum)
        else:
            self.redList.remove(self.pieceGrid[pt.x][pt.y].pieceNum)
        self.pieceGrid[pt.x][pt.y] = GamePiece(dummyColor, pt, self.pieces.canvas, -1, self.pieceGrid, self.gameGrid)
        self.alreadyCaptured = True

    def pawnToKing(self):
        if self.pieceGrid[self.selected.x][self.selected.y].type == "pawn":
            #self.delHighlightSqrs()
            samePColor = self.pieceGrid[self.selected.x][self.selected.y].pColor
            samePieceNum = self.pieceGrid[self.selected.x][self.selected.y].pieceNum
            self.pieces.canvas.remove(self.pieceGrid[self.selected.x][self.selected.y].shape)
            self.pieceGrid[self.selected.x][self.selected.y] = GamePiece(dummyColor, self.selected, self.pieces.canvas, -1, self.pieceGrid, self.gameGrid)
            self.pieceGrid[self.selected.x][self.selected.y] = King(samePColor, self.selected, self.pieces.canvas, samePieceNum, self.pieceGrid, self.gameGrid)

            self.selected = Point(-1, -1)
        else:
            print(" << ERROR: pawnToKing CALLED ON KING PIECE >>")

        return


    def movePiece(self):
        #TODO: HANDLE COLLISIONS

        #print(" * movePiece Called")
        currCenterPt = Point(self.pieceGrid[self.selected.x][self.selected.y].pos[0] + (pieceSize[0] / 2), self.pieceGrid[self.selected.x][self.selected.y].pos[1] + (pieceSize[1] / 2))
        if currCenterPt != self.gameGrid[self.selectedSqr.x][self.selectedSqr.y]:
            # not there yet so keep moving piece
            xMoveDir = 0
            yMoveDir = 0
            if currCenterPt.x < self.gameGrid[self.selectedSqr.x][self.selectedSqr.y].x:
                xMoveDir = 1
            else:
                xMoveDir = -1
            if currCenterPt.y < self.gameGrid[self.selectedSqr.x][self.selectedSqr.y].y:
                yMoveDir = 1
            else:
                yMoveDir = -1
            xInc = 0
            yInc = 0
            if abs(xMoveDir * moveRate) < abs(self.gameGrid[self.selectedSqr.x][self.selectedSqr.y].x - currCenterPt.x):
                xInc = xMoveDir * moveRate
            else:
                xInc = self.gameGrid[self.selectedSqr.x][self.selectedSqr.y].x - currCenterPt.x
            if abs(yMoveDir * moveRate) < abs(self.gameGrid[self.selectedSqr.x][self.selectedSqr.y].y - currCenterPt.y):
                yInc = yMoveDir * moveRate
            else:
                yInc = self.gameGrid[self.selectedSqr.x][self.selectedSqr.y].y - currCenterPt.y
            currX = self.pieceGrid[self.selected.x][self.selected.y].pos[0]
            currY = self.pieceGrid[self.selected.x][self.selected.y].pos[1]
            self.pieceGrid[self.selected.x][self.selected.y].pos = (currX + xInc, currY + yInc)


            #handle collisions here
            if abs(self.selectedSqr.x - self.selected.x) > 1:
                if self.alreadyCaptured == False:
                    #jump so there will be a collision either now or after it has moved some
                    #collide_widget doesn't work
                    #find collision centerPt
                    collisionLoc = Point(self.selected.x + int((self.selectedSqr.x - self.selected.x) / 2), self.selected.y + int((self.selectedSqr.y - self.selected.y) / 2))
                    collisionCenterPt = self.gameGrid[collisionLoc.x][collisionLoc.y]
                    #check if moving piece is within a certain distance of centerPt
                    currCenterPt = Point(self.pieceGrid[self.selected.x][self.selected.y].pos[0] + (pieceSize[0] / 2), self.pieceGrid[self.selected.x][self.selected.y].pos[1] + (pieceSize[1] / 2))
                    if (abs(collisionCenterPt.x - currCenterPt.x) < ((pieceSize[0] / 2) - 10)) or (abs(collisionCenterPt.y - currCenterPt.y) < ((pieceSize[1] / 2) - 10)):
                        #close enough for capture
                        print("Capture!")
                        self.capture(collisionLoc)

        else:
            #done moving so reset everything
            #must handle multiple jumps by automatically selecting piece again and highlighting sqrs

            #* must update loc of piece and pieceGrid *
            self.pieceGrid[self.selected.x][self.selected.y].loc = self.selectedSqr
            self.pieceGrid[self.selectedSqr.x][self.selectedSqr.y] = self.pieceGrid[self.selected.x][self.selected.y]
            self.pieceGrid[self.selected.x][self.selected.y] = GamePiece(dummyColor, self.selected, self.pieces.canvas, -1, self.pieceGrid, self.gameGrid)
            self.selected = self.selectedSqr
            self.selectedSqr = Point(-1, -1)
            self.delHighlightSqrs()
            self.alreadyCaptured = False

            #check for another jump and if not then deselect and else keep selected and highlight new sqrs
            endPts = []
            if (self.isJumping == True):
                endPts = self.referee.nextJumps(self.selected, self.pieceGrid)
            if not endPts:
                #executes if was never jumping or is done jumping

                if (self.pieceGrid[self.selected.x][self.selected.y].type != "pawn") or (self.selected.y != self.pieceGrid[self.selected.x][self.selected.y].lastRow):
                    #normal
                    self.deselectObj()
                else:
                    #pawnToKing
                    self.pawnToKing()
                self.isJumping = False  # multiple jumps are over so can select/deselect a piece again
                if self.turn == "black":
                    self.prevPrevMoveMin = self.prevMoveMin
                    self.prevMoveMin = (self.tempCurrPtMin, self.tempCurrEndPtsMin)
                    self.tempCurrPtMin = Point(-1, -1)
                    self.tempCurrEndPtsMin = []
                    self.turn = "red"
                    print(" { Red's Turn }")
                    self.aiTurn()
                else:
                    self.turn = "black"
                    print(" { Black's Turn }")

            else:
                self.highlightSqrs(endPts)
                if self.turn == "black":
                    print(" { Still Black's Turn }")
                else:
                    print(" { Still Red's Turn }")
                    if self.redEndPts:
                        self.moveAI()
                    else:
                        print("***  ERROR: AI FINISHED JUMPING TOO SOON  ***")

            self.moveCount += 1
            #check for if red or black has won
            if (len(self.redList) == 0) and (len(self.blackList) > 0):
                # black has won!
                print("   *** BLACK WON! ***")
                print("   *** GAME OVER ***")
                App.get_running_app().stop()
            elif (len(self.blackList) == 0) and (len(self.redList) > 0):
                # red has won!
                print("   *** RED WON! ***")
                print("   *** GAME OVER ***")
                App.get_running_app().stop()
            #FIXME: CHECK FOR DRAWS
            if self.moveCount == moveLimit:
                #FIXME: check for draws or too long of a game
                #no winner!
                print("   *** MOVE LIMIT EXCEEDED! ***")
                print("   *** GAME OVER ***")
                App.get_running_app().stop()
        return

    def update(self, dt):
        if (self.selectedSqr != Point(-1, -1)):
            self.movePiece()
        return

    def moveAI(self):
        if self.redPiecePt != Point(-1, -1):
            self.prevPrevMoveMax = self.prevMoveMax
            self.prevMoveMax = (self.redPiecePt, deepcopy(self.redEndPts))
            endPt = self.redEndPts[0]
            if self.isJumping == False:
                self.selectObj(self.redPiecePt)
                # now must highlightSqrs(list) any possible move sqrs
                howCanMoveRslt = self.referee.howCanMove(self.redPiecePt, self.pieceGrid)
                endPts = howCanMoveRslt[0]
                if endPts:
                    #FIXME: ONLY SET NECESSARY VARIABLES AND DON'T HIGHLIGHT SQUARES
                    self.highlightSqrs(endPts)
                else:
                    print("ERROR!!! CANNOT MOVE HERE")
            # (must be able to select highlighted squares for next move)
            if endPt in self.lightSqrs:
                # can select square
                self.selectedSqr = endPt
                # set self.isJumping to true if jumping here
                if abs(self.selectedSqr.x - self.selected.x) > 1:
                    # jumping
                    self.isJumping = True
            self.redEndPts.pop(0)
            self.redPiecePt = endPt
        else:
            # ********************************************************************************************
            # executes if AI looses because it has no legal moves available
            print("   *** RED HAS NO LEGAL MOVES ***")
            print("   *** BLACK WON! ***")
            print("   *** GAME OVER ***")
            App.get_running_app().stop()

            # print(" { Red Passes }")
            #
            # self.deselectObj()
            # self.turn = "black"
            # print(" { Black's Turn }")
            # self.moveCount += 1
            # # don't need to check for if someone won
            # if self.moveCount == moveLimit:
            #     # no winner!
            #     print("   *** MOVE LIMIT EXCEEDED! ***")
            #     print("   *** GAME OVER ***")
            #     App.get_running_app().stop()
            # ********************************************************************************************

        return


    def aiTurn(self):
        prevMoveStr = "[ "
        for pt in self.prevMoveMax[1]:
            prevMoveStr += pt.printStr()
            if pt != self.prevMoveMax[1][-1]:
                prevMoveStr += ", "
        prevMoveStr += " ]"
        prevPrevMoveStr = "[ "
        for pt in self.prevPrevMoveMax[1]:
            prevPrevMoveStr += pt.printStr()
            if pt != self.prevPrevMoveMax[1][-1]:
                prevPrevMoveStr += ", "
        prevPrevMoveStr += " ]"
        print(f'prevMove: {self.prevMoveMax[0].printStr()}  {prevMoveStr}    prevPrevMove: {self.prevPrevMoveMax[0].printStr()}  {prevPrevMoveStr}')
        tree = Tree(self.pieceGrid, self.prevMoveMax, self.prevPrevMoveMax, self.prevMoveMin, self.prevPrevMoveMin, "red")
        alpha = alphaMin
        beta = betaMax
        #FIXME: ADDED NORMAL AND RANDOM
        bestTup = (0, 0, 0)  # garbage init
        if normalMode == True:
            bestTup = minimax(tree.rootInd, tree, alpha, beta)
        else:
            bestTup = randomMove(tree)
        # FIXME: DELETES
        del tree
        collect()
        self.redPiecePt = bestTup[0]
        self.redEndPts = bestTup[1]
        print(f"Red Move Value: {bestTup[2]}")
        if self.redPiecePt != Point(-1, -1):
            print(f"Best Val: ( {self.redPiecePt.printStr()}, {ptListPrintStr(self.redEndPts)} )")
        self.moveAI()
        return



class CheckersApp(App):
    def build(self):
        # print mode to terminal
        if normalMode == True:
            print("*** Using Normal AI ***")
        else:
            print("*** Using Random AI ***")
        Config.set('graphics', 'resizeable', '0')
        Window.size = windowSize
        game = CheckersGame()
        Clock.schedule_interval(game.update, 1.0 / 60.0)  # in 1.0 s 60.0 frames
        return game

CheckersApp().run()


