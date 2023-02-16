from Goban import * 

newBoard = Board()

print(newBoard._board)

newBoard._pushBoard()
print(len(newBoard._board))
print(newBoard._positionHashes)
print(len(newBoard.legal_moves()))

newBoard._put_stone(12, 1)
print(newBoard._board)

newBoard.play_move(13)
print(newBoard._board)
print(newBoard.pretty_print())


