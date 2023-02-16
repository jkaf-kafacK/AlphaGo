import numpy as np
available_moves = np.array([[1, 2], [2, 1], [0, 1]])
i, j = 2, 1
color = 1
move = np.array([i, j])
move_index = np.where(
    np.all(available_moves == [i, j], axis=1))[0]
print(move_index[0])
if len(move_index)>0:
    # board_mat[i, j] = color
    # print(move_index)
    available_moves = np.delete(available_moves, move_index[0], 0)
    res = True
else:
    res = False

print(res)
print(available_moves)
