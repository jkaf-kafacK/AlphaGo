from bibli.TTT.TicTacToe import TicTacToe, Board
from bibli.TTT.Players import MCTSPlayer, RandomPlayer
from bibli.MCTS.Node import Node
from tqdm import tqdm

N_GAMES = 100
MTCS_ITERS = 5
CPARAMS = [0.3]
VERBOSE = True
BOARD_PRINT = False
    

# -1 0 1
p1 = RandomPlayer('Randy')
for c in CPARAMS:
    print(f'\n### Preparing results for c = {c} ###')
    p2 = MCTSPlayer('Monte Carlo', MTCS_ITERS, c)
    game = TicTacToe(p1, p2, VERBOSE, BOARD_PRINT)
    results = [0, 0, 0]
    for _ in tqdm(range(N_GAMES)):
        res = game.start_game()
        # print(res)
        results[res+1] += 1
    print(results)
