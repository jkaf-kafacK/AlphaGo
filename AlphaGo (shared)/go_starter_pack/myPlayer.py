

import Goban
from playerInterface import *

import numpy as np
import matplotlib.pyplot as plt
import mcts


import Goban



class Myplayer(playerInterface):
    def __init__(self):
        self._board = Goban.Board()
        self._mcts = mcts.MCTS()
        self._mycolor = None

    def getPlayerName(self):
        return "myPlayer "

    def getplayermove(self):
        if self._board.is_game_over():
            print("game over")
            return "PASS"
        moves = self._board.legal_moves()
        moves1 = self._mcts.search(9)
        print("I am playing ", moves1)

    
    
    def playOpponentMove(self, move):
        #print("Opponent played ", move, "i.e. ", move) # New here
        # the board needs an internal represetation to push the move.  Not a string
        self._board.push(Goban.Board.name_to_flat(move))

    def newGame(self, color):
        self._mycolor = color
        self._opponent = Goban.Board.flip(color)

    def endGame(self, winner):
        if self._mycolor == winner:
            print("I won!!!")
        else:
            print("I lost :(!!")