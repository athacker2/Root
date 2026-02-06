class GameState:
    def __init__(self):
        self.players = []
        self.board = None
        self.turn = 0

class Player:
    def __init__(self):
        self.score = 0


# Board/Map related classes
class Board:
    def __init__(self):
        self.clearings = []
    
    def initialize_board(self):
        # Initialize the board with clearings and connections
        self.clearings = [Clearing() for _ in range(12)]

        self.clearings[0].adjacentClearings = [self.clearings[4], self.clearings[3], self.clearings[1]]
        self.clearings[1].adjacentClearings = [self.clearings[0], self.clearings[2]]
        self.clearings[2].adjacentClearings = [self.clearings[1], self.clearings[3], self.clearings[7]]
        self.clearings[3].adjacentClearings = [self.clearings[0], self.clearings[5], self.clearings[2]]
        self.clearings[4].adjacentClearings = [self.clearings[0], self.clearings[8], self.clearings[5]]
        self.clearings[5].adjacentClearings = [self.clearings[4], self.clearings[8], self.clearings[10], self.clearings[6], self.clearings[3]]
        self.clearings[6].adjacentClearings = [self.clearings[5], self.clearings[11], self.clearings[7]]
        self.clearings[7].adjacentClearings = [self.clearings[2],self.clearings[6], self.clearings[11]]
        self.clearings[8].adjacentClearings = [self.clearings[4], self.clearings[5], self.clearings[9]]
        self.clearings[9].adjacentClearings = [self.clearings[8], self.clearings[10]]
        self.clearings[10].adjacentClearings = [self.cleartings[9], self.clearings[5], self.clearings[11]]
        self.clearings[11].adjacentClearings = [self.clearings[6], self.clearings[7], self.clearings[10]]
            



class Clearing:
    def __init__(self):
        self.adjacentClearings = []
        self.tiles = []
        self.suit = []