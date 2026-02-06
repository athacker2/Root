from rootgame.engine.types import Board, Clearing

def build_board():
    board = Board(clearings=[Clearing() for _ in range(12)])

    board.clearings[0].adjacentClearings = [4, 3, 1]
    board.clearings[1].adjacentClearings = [0, 2]
    board.clearings[2].adjacentClearings = [1, 3, 7]
    board.clearings[3].adjacentClearings = [0, 5, 2]
    board.clearings[4].adjacentClearings = [0, 8, 5]
    board.clearings[5].adjacentClearings = [4, 8, 10, 6, 3]
    board.clearings[6].adjacentClearings = [5, 11, 7]
    board.clearings[7].adjacentClearings = [2, 6, 11]
    board.clearings[8].adjacentClearings = [4, 5, 9]
    board.clearings[9].adjacentClearings = [8, 10]
    board.clearings[10].adjacentClearings = [9, 5, 11]
    board.clearings[11].adjacentClearings = [6, 7, 10]

    return board