from Player import Player
from AIPlayer import AIPlayer

class GameState:
    def __init__(self):
        self.friendlyPlayer = Player(self)
        self.opponentPlayer = Player(self)
        self.friendlyPlayer.opponentPlayer = self.opponentPlayer
        self.opponentPlayer.opponentPlayer = self.friendlyPlayer
        self.phase = "Mulligan"
        self.gameIsOver = False
        self.playerWhoLost = None
        self.existingCards = {}
        self.aiPlayer = AIPlayer(self)

    def PlayerLost(self, player):
        self.gameIsOver = True
        self.playerWhoLost = player

    def __repr__(self):
        gameString = "-----Current Game State-----\n-----Players: \n" + str(self.friendlyPlayer) + str(self.opponentPlayer)
        return gameString
    
