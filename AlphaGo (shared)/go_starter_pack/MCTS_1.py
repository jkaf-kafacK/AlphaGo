# https://github.com/ai-boson/mcts

import numpy as np
from collections import defaultdict
import time
from Goban import *
import copy

newGame = Board()
move = newGame.generate_legal_moves()


class MonteCarloTreeSearchNode():
    def __init__(self, game, parent=None, parent_action=None):
        # faire une copie pour chaque jeu
        self.state = copy.deepcopy(game)
        self.parent = parent
        self.parent_action = parent_action
        self.children = []
        self._number_of_visits = 1
        self._results = defaultdict(int)
        self._results[1] = 0
        self._results[0] = 0
        self._untried_actions = None
        self._untried_actions = self.untried_actions()
        return

    def untried_actions(self):
        self._untried_actions = self.get_legal_actions()
        return self._untried_actions

    def q(self):
        wins = self._results[1]
        loses = self._results[-1]
        return wins - loses

    def n(self):
        return self._number_of_visits

    def expand(self):
        action = self._untried_actions.pop()
        #print(len(self._untried_actions))
        if(len(self._untried_actions) != 81):
            self.state.pop()

        new_board = self.state
        new_board.push(self.parent_action)
        new_board.push(action)
        next_state = new_board
        new_board.pretty_print()
        child_node = MonteCarloTreeSearchNode(
            next_state, parent=self, parent_action=action)

        #child_node.state.pretty_print()
        child_node.rollout()
        self.children.append(child_node)
        return child_node

    def is_terminal_node(self):
        return self.state._gameOver

    def rollout(self):
        current_rollout_state = self.state
        new_state = copy.deepcopy(self)
        
        while not new_state.is_game_over():
           
            possible_moves = new_state.get_legal_actions()
            action = self.rollout_policy(possible_moves)
            new_state.move(action)
        return new_state.game_result()

    def reward(self):
        self.rol = self.rollout()
        liste_value = []
        liste_value.append(self.rol)
        best_el = np.max(np.array(liste_value), axis=0)

    def backpropagate(self, result):
        self._number_of_visits += 1.
        if(result == "1-0"):
            result_bis = 1
            self._results[result] += 1.
        if(result == "0-1"):
            result_bis = -1
            self._results[result] += 1.

        if self.parent:
            self.parent.backpropagate(result)

    def is_fully_expanded(self):
        return len(self._untried_actions) == 0

    def best_child(self, c_param=0.1):
        print("printing best child board")

        choices_weights = [(c.q() / c.n()) + c_param *
                           np.sqrt((2 * np.log(self.n()) / c.n())) for c in self.children]

        return self.children[np.argmax(choices_weights)]

    # value function
    def rollout_policy(self, possible_moves):

        return possible_moves[np.random.randint(len(possible_moves))]

    def best_action(self):
        simulation_no = 10
        for i in range(simulation_no):

            v = self._tree_policy()
            # rollout fait dès qu'un enfant est créé
            reward = v.rollout()
            v.backpropagate(reward)

        return self.best_child(c_param=0.)

    # à modifier
    def _tree_policy(self):
        current_node = self
        while not current_node.is_terminal_node():
            if not current_node.is_fully_expanded():
                current_node.expand()
            # for child in current_node.children:
            #     r = child.rollout()
            else:
                current_node = current_node.best_child()

                print("we are here - best chosen action")
               
                print("L'état courant du noeud",
                      current_node.is_fully_expanded())

        #print(not current_node.is_terminal_node())
        current_node.pretty_print()
        return current_node

    # choose if the MCTS will do SELECTION, EXPANSION, SIMULATION or BACKPROPAGATION

    def get_legal_actions(self):
        '''Modify according to your game or
        needs. Constructs a list of all
        possible states from current state.
        Returns a list.'''
        moves = self.state.legal_moves()
        return moves

    def is_game_over(self):
        '''
        Modify according to your game or 
        needs. It is the game over condition
        and depends on your game. Returns
        true or false
        '''
        return self.state.is_game_over()

    def game_result(self):
        '''
        Modify according to your game or 
        needs. Returns 1 or 0 or -1 depending
        on your state corresponding to win,
        tie or a loss.
        '''
        results = self.state.result()
        if(results == "1-0"):
            return 1
        elif(results == "0-1"):
            return -1
        else:
            return 0

    def move(self, action):
        '''
        Modify according to your game or 
        needs. Changes the state of your 
        board with a new value. For a normal
        Tic Tac Toe game, it can be a 3 by 3
        array with all the elements of array
        being 0 initially. 0 means the board 
        position is empty. If you place x in
        row 2 column 3, then it would be some 
        thing like board[2][3] = 1, where 1
        represents that x is placed. Returns 
        the new state after making a move.
        '''
        return self.state.push(action)

# def main():
#     root = MonteCarloTreeSearchNode(newGame,None,0)
#     selected_node = root.best_action()
#     return


root = MonteCarloTreeSearchNode(newGame, None, 0)

print(root.best_action())
#root.pretty_print()
# policy network outputs move probabilities
# a value network outputs position evaluation
