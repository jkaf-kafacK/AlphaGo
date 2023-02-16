from . import VERBOSE, LOG_F


class Backpagation:
    def backpropagate(node, winner, current_player):
        if VERBOSE:
            print('Backpropagation on :', file=LOG_F)
        node.update_uct()
        node.print('backpropagate-node', VERBOSE)

        while node.parent:
            node.visits += 1
            if winner == current_player:
                node.wins += 1
            node.update_uct()
            current_player = node.state.flip(current_player)
            node = node.parent

        node.update_uct()
