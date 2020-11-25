# NOTE: NOT USED IN GAME (OLD CODE)

from minimaxSearch import Tree, minimax, alphaMin, betaMax
from testFunctions import makeTestBoard, ptListPrintStr



#main script for testing minimax search without app
board = makeTestBoard()
tree = Tree(board)
tree.levelOrderPrint()
alpha = alphaMin
beta = betaMax
# def minimax(nodeInd, tree, alpha, beta):
bestTup = minimax(0, tree, alpha, beta)
print(f"Best Val: ( {bestTup[0].printStr()}, {ptListPrintStr(bestTup[1])}, {bestTup[ 2]} )")
print("Exiting Program...")

