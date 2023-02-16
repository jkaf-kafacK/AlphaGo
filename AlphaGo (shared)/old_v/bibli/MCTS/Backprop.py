from . import VERBOSE


class Backpagation:
    def backpropagate(node, winner, current_player):
        if VERBOSE:
            print('Backpropagation on :')
        node.print('backpropagate-node', VERBOSE)
        node.update_uct()

        while node.parent:
            node.visits += 1
            if winner == current_player:
                node.wins += 1
            node.update_uct()
            current_player = -current_player
            # node.print('lah lah')
            node = node.parent

        node.update_uct()
