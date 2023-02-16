import random
import numpy as np
import math
import Goban
import copy
from collections import defaultdict


'''https://github.com/JoshVarty/AlphaZeroSimple/blob/master/monte_carlo_tree_search.py'''


new_board = Goban.Board()
move = new_board.generate_legal_moves()

class MCTSNode():
    def __init__(self,state ,parent=None,parent_action = None):
        self.state  =  state
        self.parent = parent
        self.parent_action = parent_action
        self.children = []
        self.number_of_visits = 0
        self.results = defaultdict(int)
        self.results[1] = 0
        self.results[-1]=0
        self.all_possible_action = None
        self.all_possible_action = self.__all_possible_actions()

        return
    
    def __all_possible_actions(self):
        self.all_possible_action = self.get_legal_actions()
        #print("all Legal Moves: ", [self.state.move_to_str(m) for m in self.all_possible_action])
        return self.all_possible_action

    def game(self):
        wins = self.results[1]
        loss = self.results[-1]
        print(wins)
        return wins - loss
    
    def node_visits(self):
        return self.number_of_visits
    
    
    def mini_expand(self,index):
        while index < len(self.all_possible_action):
            actions = self.all_possible_action[index]
            bord  = self.state
            bord.push(actions)
            next_state = bord
            child_node = MCTSNode(next_state,parent = self,parent_action=actions)
            self.children.append(child_node)
            return child_node

    def expand(self):
        for elt in range(len(self.all_possible_action)):
            
            child_node = self.mini_expand(elt)
            self.__all_possible_actions()
            self.all_possible_action.pop()

    def is_end_node(self):
        return self.state.is_game_over()
    
    
    def rollout_policy(self ,poss_moves):
        return poss_moves[np.random.randint(poss_moves)]



    def rollout(self):
        current_rollout_state = self.state
        new_state = self
        while not new_state.is_game_over():
            possible_moves = new_state.get_legal_actions()
            action = self.rollout_policy(possible_moves)
            new_state.move(action)
            new_board.pop()
        return new_state.game_result()



    
    def backpropagate(self,result):
        self.number_of_visits += 1.
        self.results[result] += 1.
        if self.parent:
           self.parent.backpropagate(result)
        
    def fully_expanded(self):
        return len(self.all_possible_action) == 0

    def best_child(self, param = 0.1):
        weights = [(child.game() / child.node_visits()) + param *np.sqrt((2 * np.log(self.node_visits())/ child.node_visits())) for child in self.children]
        return self.children[np.argmax(weights)]

   

    def tree_policy(self):
        current_node = self
        print("3333")
        while not current_node.is_end_node():
            
            if not current_node.fully_expanded():
                return current_node.expand()
            else:
                current_node = current_node.best_child()
                
                print("we are here - best chosen action")
                current_node.state.pretty_print()
                print("L'état courant du noeud",  current_node.is_fully_expanded())

        print(not current_node.is_terminal_node())
        return current_node
    
    def best_action(self):
         simulation_no = 100
         for i in range(simulation_no):
            v = self.tree_policy()
            reward = v.rollout()
            v.backpropagate(reward)
         return self.best_child(c_param=0)
           
        
        
    
    def reward(self):
        self.rol = self.rollout()
        liste_value = []
        liste_value.append(self.rol)
        best_el = np.max(np.array(liste_value), axis=0)

    def is_game_over(self):
        return self.state.is_game_over()
    
    def get_legal_actions(self):
        print(self.state)
        #return self.state.legal_moves()
        return self.state.generate_legal_moves()

    
    def game_result(self):
        results = self.state.result()
        if(results == "1-0"):
            return 1
        elif(results == "0-1"): 
            return -1
        else:
            return 0
        #return self.state.final_go_score()
    


    def move(self,action):
        return self.state.push(action)



root = MCTSNode(new_board,None,0)
selected_node = root.best_action()
#l = root.tree_policy()

print(selected_node)













'''

import playerInterface
def ucb_score(parent, child):
    """
    The score for an action that would transition between the parent and child.
    return The strategy uses an evaluation function to optimally select nodes with the highest estimated value. 
    MCTS uses the Upper Confidence Bound (UCB)
    """
    prior_score = child.point * math.sqrt(parent._number_of_visits) / (child._number_of_visits + 1)
    if child._number_of_visits > 0:
        # The value of the child is from the perspective of the opposing player
        value_score = -child.value()
    else:
        value_score = 0

    return value_score + prior_score
    
class Node:
    def __init__(self, point, root_visit):
        self.point = point
        self._number_of_visits = 0
        self.sum_value = 0
        self.children = {}
        self.state = None
        self.root_visits = root_visit
        
        self.score = 0
        self.playout = 0


    def expanded(self):
        return len(self.children) > 0
    
    def value(self):
        if self._number_of_visits == 0:
            return 0
        return self.sum_value / self._number_of_visits
    

# Start from root R and select successive child nodes until a leaf node L is reached. The root is the current game state and 
# a leaf is any node that has a potential child from which no simulation (playout) has yet been initiated. The section below 
# says more about a way of biasing choice of child nodes that lets the game tree expand towards the most promising moves, which 
# is the essence of Monte Carlo tree search.

    

    def select_child(self):
        
        best_score = -np.inf
        best_action = -1
        best_child = None

        for action, child in self.children.items():
            score = ucb_score(self, child)
            if score > best_score:
                best_score = score
                best_action = action
                best_child = child
        return best_action, best_child


    

    def select_action(self,epsilone):
    
        visit_counts = np.array([child._number_of_visits for child in self.children.values()])
        actions = [action for action in self.children.keys()]
        
        if epsilone == 0:
            action = actions[np.argmax(visit_counts)]
        elif epsilone == float("inf"):
            action = np.random.choice(actions)
        else:
            
            visit_count_distribution = visit_counts ** (1 / epsilone)
            visit_count_distribution = visit_count_distribution / sum(visit_count_distribution)
            action = np.random.choice(actions, p=visit_count_distribution)

        return action
    
    def expand(self, state, to_play, action_probs):
       
        self.to_play = to_play
        self.state = state
        for a, prob in enumerate(action_probs):
            if prob != 0:
                self.children[a] = Node(point=prob, to_play=self.root_visits * -1)
    

    def backpropagate(self, search_path, value, to_play):
        
        for node in reversed(search_path):
            node.value_sum += value if node.to_play == to_play else -value
            node.visit_count += 1
    
class MCTS():

    def __init__(self, args):
        self.game = Goban.Board()
        
        self.args = args

    def run(self, state, to_play):

        root = Node(0, to_play)
        valid_moves = self.game.legal_moves()
        # EXPAND root
        value = np.random.choice(range(82))
        action_probs = np.random.uniform(size=82)
        print(action_probs)

        # Now we want to to put to 0 all impossible moves
        # SO we create multiplier with 0 everywhere and put 1 where the move is legal
        
        multiplier = np.zeros_like(action_probs)
        for some_move in valid_moves:
            x, y = Goban.Board.unflatten(some_move)
            multiplier[y * Goban.Board._BOARDSIZE + x] = 1
        
        #java(springboot) et angular, react, vue
        
        action_probs = action_probs * valid_moves  # mask invalid moves
        
        action_probs /= np.sum(action_probs)
        root.expand(state, to_play, action_probs)
        current_state = self.game.legal_moves()
        

        for _ in range(self.args['num_simulations']):
            node = root
            search_path = [node]

            # SELECT
            while node.expanded():
                action, node = node.select_child()
                search_path.append(node)

            parent = search_path[-2]
            state = parent.state
           
            next_state, _ = self.game.get_next_state(state, player=1, action=action)
            
            next_state = self.game.get_canonical_board(next_state, player=-1)

            
            value = self.game.get_reward_for_player(next_state, player=1)
            if value is None:
                

                action_probs, value = model.predict(next_state)
                valid_moves = self.game.get_valid_moves(next_state)
                action_probs = action_probs * valid_moves  # mask invalid moves
                action_probs /= np.sum(action_probs)
                node.expand(next_state, parent.to_play * -1, action_probs)

            self.backpropagate(search_path, value, parent.to_play * -1)

        return root

    def backpropagate(self, search_path, value, to_play):
        """
        At the end of a simulation, we propagate the evaluation all the way up the tree
        to the root.
        """
        for node in reversed(search_path):
            node.value_sum += value if node.to_play == to_play else -value
            node.visit_count += 1

'''
