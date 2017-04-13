import copy
import Cards
from AIPlayer import AIPlayer

class Player:
    def __init__(self, GameState=None, name="Test Player", playerNumber=0, mana=0):
        self.gameState = GameState
        self.opponentPlayer = None
        self.manaCrystals = mana
        self.maxManaCrystals = 10
        self.currentFilledManaCrystals = mana
        self.playerDeckCount = 30
        self.maxHandSize = 10
        #7 minions plus 1 hero. Hero is always in board position 0.
        self.maxBoardSize = 8
        self.fatigueDamage = 1
        self.playerName = name
        self.playerNumber = playerNumber
        self.hand = []
        self.board = []
        self.hero = None
        self.heroPower = None
        self.cardWaitingForTarget = None
        self.coin = None
        #Set to a number and everytime DrawCard is called it will subract from this number.
        #The AI will check for this number when it tells us to play an rng draw card and then
        #when it is back to 0 the AI will continue.
        self.aiWaitingForDraw = 0

    def UpdatePlayerName(self, newName):
        self.playerName = newName

    def UpdatePlayerNumber(self, newNumber):
        self.playerNumber = newNumber

    #Opponent Players do not draw
    def DrawCard(self, position, cardId, cardName):
        if self.playerDeckCount > 0:
            card = None
            try:
                card = self.gameState.existingCards[cardId]
                if card.zone != "Hand":
                    card.zone = "Hand"
                if card.name == "The Coin":
                    self.coin = card
            except KeyError:
                card = self.CreateCard(position, cardId, cardName, "Hand")
                self.gameState.existingCards[cardId] = card
            if len(self.hand) < self.maxHandSize:
                self.hand.append(card)
            else:
                card.zone = "Graveyard"
            self.playerDeckCount -= 1
            if self.aiWaitingForDraw > 0:
                self.aiWaitingForDraw -= 1
            else:
                self.gameState.aiPlayer.Start()
        else:
            self.hero.TakeDamage(self.fatigueDamage)
            self.fatigueDamage += 1
            if self.aiWaitingForDraw > 0:
                self.aiWaitingForDraw -= 1
            else:
                self.gameState.aiPlayer.Start()

    def UseMana(self, amount):
        self.currentFilledManaCrystals -= amount

    def DiscardCardFromHand(self, cardId):
        card = self.gameState.existingCards[cardId]
        self.hand.remove(card)
        card.zone = "Graveyard"

    def ReturnCardToDeck(self, cardId):
        card = self.gameState.existingCards[cardId]
        self.hand.remove(card)
        card.zone = "Deck"

    #Opponent Players only ever play cards
    def PlayCard(self, position, cardId, cardName=None, target=None):
        card = None
        try:
            card = self.gameState.existingCards[cardId]
            if card.type != "Hero Power":
                self.hand.remove(card)
            if card.name == "The Coin":
                self.coin = None
            if card.type == "Hero":
                return
        except KeyError:
            card = self.CreateCard(position, cardId, cardName, "Hand")
            if card.type == "Hero Power":
                self.heroPower = card
            if card.type == "Hero":
                self.hero = card
        if card.type == "Minion" or card.type == "Hero":
            self.board.insert(position, card)
            if card.type != "Hero":
                card.exhausted = True
        card.UpdatePosition(position)
        card.OnPlay(target)
        if not card.tokenMinion and card.zone == "Hand":
            self.UseMana(card.manaCost)
        if card.type == "Hero Power" and card.zone == "Play":
            self.UseMana(card.manaCost)
        card.zone = "Play"
        self.UpdateBoardAuras()

    def UpdateBoardAuras(self):
        for card in self.board:
            if card.hasAuraEffect:
                card.Aura()

    def CreateCard(self, position, cardId, cardName, zone):
        card = getattr(Cards, cardName)(cardId, self, position, zone)
        self.gameState.existingCards[cardId] = card
        return card

    def ChangeCardPosition (self, card, newPosition):
        if card.zone != "Graveyard":
            if card.zone == "Hand":
                self.hand.remove(card)
                self.hand.insert(newPosition-1, card)
            else:
                self.board.remove(card)
                self.board.insert(newPosition, card)
            card.UpdatePosition(newPosition)

    def StartTurn(self):
        if self.manaCrystals != self.maxManaCrystals:
            self.manaCrystals += 1
        self.currentFilledManaCrystals = copy.copy(self.manaCrystals)
        self.heroPower.exhausted = False
        for card in self.board:
            if card is not None:
                card.exhausted = False
                if card.frozen:
                    card.frozen = False
    
    def __repr__(self):
        playerString = "Player " + str(self.playerNumber) + " : " + self.playerName + ":" + "\n\t" + "manaCrystals, maxManaCrystals, currentFilledManaCrystals: " + str(self.manaCrystals) + " " + str(self.maxManaCrystals) + " " + str(self.currentFilledManaCrystals) + "\n\t" + "current hand: " + str(self.hand) + "\n\t" + "current board: " + str(self.board) + "\n"
        return playerString
