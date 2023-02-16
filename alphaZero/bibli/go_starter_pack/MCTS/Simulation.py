from . import VERBOSE, LOG_F
import random

def simulate(node):
    '''
        Given a state node this function will do random playout to determine a winner 
    '''
    if VERBOSE: print('Simulation on :', file=LOG_F)
    node.print('simulate-node', VERBOSE)

    state = node.state
    
    while not state.is_game_over():
        moves = state.legal_moves()
        move = random.choice(moves)
        state = state.resulting_state(move)
    winner = state.determine_winner()
    return winner
