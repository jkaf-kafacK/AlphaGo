import numpy as np
import random
import copy
# from Players import *


class Board:
    def __init__(self, verbose=False) -> None:
        self.board_mat = np.zeros((3, 3))
        self.available_moves = np.argwhere(self.board_mat == 0)
        self.verbose = verbose
        self.rules = Rules()
        self.m_color = 0
        self.last_move = None

    def legal_moves(self):
        return self.available_moves
    
    def is_terminal(self):
        no_available_moves = len(self.legal_moves()) == 0
        win_1 = self.rules.check_state(self.board_mat, 1)
        win_2 = self.rules.check_state(self.board_mat, -1)
        return no_available_moves or win_1 or win_2

    def determine_winner(self):
        assert self.is_terminal()
        if self.rules.check_state(self.board_mat, self.m_color):
            return self.m_color
        else:
            return -self.m_color

    def move(self, color, i, j):
        # print('move', color)
        assert color == 1 or color == -1
        move = np.array([i, j])
        move_index = np.where(
            np.all(self.available_moves == [i, j], axis=1)
        )[0]
        if len(move_index) > 0:
            self.board_mat[i, j] = color
            self.m_color = color
            self.available_moves = np.delete(
                self.available_moves, move_index[0], axis=0)
            self.win = self.rules.check_state(self.board_mat, color)
            self.last_move = i,j 
            return True, self.win
        else:
            return False, False

    def resulting_state(self, move):
        # print('resulting_move')
        i, j = move
        res_state = copy.deepcopy(self)
        c = -self.m_color if self.m_color in (-1,1) else 1
        res_state.move(c, i, j)
        return res_state

    
    def print_board(self):
        if self.verbose:
            res = [self.print_row(i) for i in range(len(self.board_mat))]
            for row in res:
                print(row)
            print('-----')

    def print_row(self, i):
        row = self.board_mat[i]
        res = [self.print_tile(i, j) for j in range(len(row))]
        res = ' '.join(res)
        return res

    def print_tile(self, i, j):
        tile = self.board_mat[i, j]
        return f"{'X' if tile == 1 else 'O' if tile == -1 else '.'}"


class TurnManager:
    def __init__(self, player1, player2):
        self.q = [player2, player1]
        self.assign_colors(self.q)

    def assign_colors(self, players):
        assert len(players) == 2
        colors = [-1, 1]
        for i, p in enumerate(players):
            p.assign_color(colors[i])

    def get_player(self):
        player = self.q.pop()
        self.q.insert(0, player)
        return player


class Rules:
    def __init__(self):
        self.horizontal_wins = [[_, _+1, _+2] for _ in [0, 3, 6]]
        self.vertical_wins = [[_, _+3, _+6] for _ in [0, 1, 2]]
        self.diagonal_wins = [[_, 4, 8-_] for _ in [0, 2]]
        self.win_conditions = self.horizontal_wins + \
            self.vertical_wins + self.diagonal_wins
        # print(np.array(self.win_conditions))
        self.winning_move = None
        self.winner = None
            
    def check_state(self, board_mat, color):
        # returns True for a win and False for an unfinished game, if we have win, also returns win condition
        for win_con in self.win_conditions:
            win_con_prob = 0
            for tile_i in win_con:
                if board_mat.flatten()[tile_i]!=color:
                    break
                else :
                    win_con_prob += 1
            if win_con_prob == 3:
                self.winning_move = win_con
                self.winner = color
                return True
        return False
        


class TicTacToe:
    def __init__(self, player1, player2, verbose = True, board_print=False):
        self.board = Board(verbose=board_print)
        self.turn_manager = TurnManager(player1, player2)
        self.board_print = board_print
        self.verbose = verbose

    def start_game(self):
        self.board = Board(verbose=self.board_print)
        self.board.print_board()
        i = 0
        end = False
        while len(self.board.legal_moves()) != 0:
            # print(len(self.board.legal_moves()))
            player = self.turn_manager.get_player()
            valid, end = player.play(self.board)
            self.board.print_board()
            if end :
                if self.verbose : print(f"{player.name} has won with move {self.board.rules.winning_move}")
                return self.board.rules.winner
        if not end:
            if self.verbose : print("Draw")
            return 0

# 3*r+c==x => r == x//3 && c == x%3