import re
import time
import sys
from GameState import GameState

class HearthstoneLogParser ():
    def __init__(self):
        self.gameState = GameState()
        self.gameIsOver = False
        self.playersAndTheirNumbers = []
        self.myPlayerNumber = 0
        self.myPlayerName = 'Friendly Player'
        self.opponentPlayerNumber = 0
        self.opponentPlayerName = 'Opponent Player'
        self.lastLineByte = 0
        self.gameOver = re.compile(r'[[]Power.*GameState.DebugPrintPower.*TAG_CHANGE Entity=(.*)tag=PLAYSTATE value=LOST')
        self.playerNameAndNumber = re.compile(r'[[]Power.*GameState.DebugPrintPower.*Entity=(.*)tag=PLAYER_ID value=(\d*)')
        self.friendlyDrawnCards = re.compile(r'[[]Zone.*name=(.*)id=(\d*).*cardId=(.*) player=(\d*).*to FRIENDLY HAND')
        self.friendlyMulliganedCards = re.compile(r'[[]Power.*GameState.DebugPrintPower.*HIDE_ENTITY.*name=(.*).*id=(\d*).*cardId=(.*) player=(\d*).*tag=ZONE value=DECK')
        self.friendlyPlayedCards = re.compile(r'[[]Zone.*name=(.*)id=(\d*).*zone=(?!SETASIDE).*zonePos=(\d*).*cardId=(.*) player=(\d*).*from (FRIENDLY HAND | )->( FRIENDLY PLAY \(Weapon\)| FRIENDLY PLAY| )$')
        self.playerHeroOrHeroPower = re.compile(r'[[]Zone.*name=(.*)id=(\d*).*zonePos=(\d*).*cardId=(.*) player=(\d*).*to (FRIENDLY|OPPOSING) (PLAY.*Hero|PLAY.*Hero Power)')
        self.cardAttackedCard = re.compile(r'[[]Power.*PowerTaskList.DebugPrintPower.*name=(.*)id=(\d*).*zonePos=(\d*).*cardId=(.*) player=(\d*).*BlockType=ATTACK.*Target=[[]name=(.*)id=(\d*).*zonePos=(\d*).*cardId=(.*) player=(\d*)')
        self.opponentDrawnCards = re.compile(r'[[]Zone.*id.*player=2.*to OPPOSING HAND')
        self.opponentPlayedCard = re.compile(r'[[]Zone.*name=(.*)id=(\d*).*zone=(?!SETASIDE).*zonePos=(\d*).*cardId=(.*) player=(\d*).*from (OPPOSING HAND | )->( OPPOSING PLAY \(Weapon\)| OPPOSING PLAY| )$')
        self.usedHeroPower = re.compile(r'[[]Power.*GameState.DebugPrintPower.*ACTION_START Entity=.*name=(.*)id.*cardId=(.*) player=(\d*).*BlockType=POWER.*Index=.*Target')
        self.zonePositionChange = re.compile(r'[[]Zone.*name=(.*).*id=(\d*).*zone=(.*)zonePos=.*cardId=(.*) player=(\d*).*pos from (\d*) -> (\d*)')
        self.cardTargetedCard = re.compile(r'[[]Power.*PowerTaskList.DebugPrintPower.*name=(.*)id=(\d*).*zonePos=(\d*).*cardId=(.*) player=(\d*).*BlockType=POWER.*Target=[[]name=(.*)id=(\d*).*zonePos=(\d*).*cardId=(.*) player=(\d*)')
        self.cardTotalDamage = re.compile(r'[[]Power.*PowerTaskList.DebugPrintPower.*name=(.*)id=(\d*).*zonePos=(\d*).*cardId=(.*) player=(\d*).*tag=DAMAGE value=(\d*)')
        self.turnEnd = re.compile(r'[[]Power.*PowerTaskList.DebugPrintPower.*Entity=(.*)tag=CURRENT_PLAYER value=0')
        self.turnStart = re.compile(r'[[]Power.*PowerTaskList.DebugPrintPower.*Entity=(.*)tag=CURRENT_PLAYER value=1')
        self.mulliganStart = re.compile(r'[[]Power.*GameState.DebugPrintPower.*TAG_CHANGE Entity=GameEntity tag=STEP value=BEGIN_MULLIGAN')
        self.mulliganWaitingForChoices = re.compile(r'[[]Power.*GameState.DebugPrintPower.*TAG_CHANGE Entity=(.*)tag=MULLIGAN_STATE value=INPUT')
        self.mulliganEnd = re.compile(r'[[]Power.*GameState.DebugPrintPower.*TAG_CHANGE Entity=(.*)tag=MULLIGAN_STATE value=DONE')
        self.lostDevineShield = re.compile(r'[[]Power.*PowerTaskList.DebugPrintPower.*TAG_CHANGE Entity=.*name=(.*).*id=(\d*).*cardId=(.*) player=(\d*).*tag=DIVINE_SHIELD value=0')

    def FindPlayerNamesAndNumbers(self):
        finished = False
        while not finished:
            with open("C:\Program Files (x86)\Hearthstone\Hearthstone_Data\output_log.txt", "r+") as logFile:
                for line in logFile:
                    matchPlayerNameAndNumber = re.match(self.playerNameAndNumber,line)
                    if matchPlayerNameAndNumber is not None:
                        possiblePair = [matchPlayerNameAndNumber.group(1),matchPlayerNameAndNumber.group(2)]
                        if possiblePair not in self.playersAndTheirNumbers:
                            self.playersAndTheirNumbers.append([matchPlayerNameAndNumber.group(1),matchPlayerNameAndNumber.group(2)])
                    if len(self.playersAndTheirNumbers) == 2:
                        finished = True
                logFile.close()
        print "*****Found player names and numbers.*****"
        self.SetPlayerNamesAndNumbers()

    def SetPlayerNamesAndNumbers(self):
        finished = False
        while not finished:
            with open("C:\Program Files (x86)\Hearthstone\Hearthstone_Data\output_log.txt", "r+") as logFile:
                for line in logFile:
                    matchFriendlyDrawnCards = re.match(self.friendlyDrawnCards,line)
                    if matchFriendlyDrawnCards is not None:
                        self.myPlayerNumber = matchFriendlyDrawnCards.group(4)
                        for playerNumberPair in self.playersAndTheirNumbers:
                            if self.myPlayerNumber == playerNumberPair[1]:
                                self.myPlayerName = playerNumberPair[0]
                                self.gameState.friendlyPlayer.UpdatePlayerName(self.myPlayerName)
                                self.gameState.friendlyPlayer.UpdatePlayerNumber(self.myPlayerNumber)
                            else:
                                self.opponentPlayerNumber = playerNumberPair[1]
                                self.gameState.opponentPlayer.UpdatePlayerNumber(self.opponentPlayerNumber)
                                self.opponentPlayerName = playerNumberPair[0]
                                self.gameState.opponentPlayer.UpdatePlayerName(self.opponentPlayerName)
                        finished = True
                logFile.close()
        print "*****Players' names and numbers resolved.*****"
        self.FindPlayersHeroAndHeroPowers()

    def FindPlayersHeroAndHeroPowers(self):
        finished = False
        while not finished:
            with open("C:\Program Files (x86)\Hearthstone\Hearthstone_Data\output_log.txt", "r+") as logFile:
                for line in logFile:
                    matchPlayerHeroOrHeroPower = re.match(self.playerHeroOrHeroPower,line)
                    if matchPlayerHeroOrHeroPower is not None:
                        if matchPlayerHeroOrHeroPower.group(5) == self.myPlayerNumber:
                            self.gameState.friendlyPlayer.PlayCard(int(matchPlayerHeroOrHeroPower.group(3)), int(matchPlayerHeroOrHeroPower.group(2)), matchPlayerHeroOrHeroPower.group(4))
                        else:
                            self.gameState.opponentPlayer.PlayCard(int(matchPlayerHeroOrHeroPower.group(3)), int(matchPlayerHeroOrHeroPower.group(2)), matchPlayerHeroOrHeroPower.group(4))
                if self.gameState.friendlyPlayer.hero != None and self.gameState.friendlyPlayer.heroPower != None and self.gameState.opponentPlayer.hero != None and self.gameState.opponentPlayer.heroPower != None:
                    finished = True
                logFile.close()
        print "*****Found and set player's heroes and hero powers. Now parsing Mulligan Phase.*****"
        self.ParseMulliganPhaseChoices()

    def ParseMulliganPhaseChoices(self):
        finished = False
        while not finished:
            with open("C:\Program Files (x86)\Hearthstone\Hearthstone_Data\output_log.txt", "r+") as logFile:
                logFile.seek(self.lastLineByte)
                for line in logFile:
                    matchFriendlyDrawnCards = re.match(self.friendlyDrawnCards,line)
                    if matchFriendlyDrawnCards is not None:
                        self.gameState.friendlyPlayer.DrawCard(0, int(matchFriendlyDrawnCards.group(2)), matchFriendlyDrawnCards.group(3))
                        print "" + self.myPlayerName + " drew " + matchFriendlyDrawnCards.group(1) + " with id= " + matchFriendlyDrawnCards.group(2)

                    matchZonePositionChange = re.match(self.zonePositionChange,line)
                    if matchZonePositionChange is not None:
                        card = self.gameState.existingCards[int(matchZonePositionChange.group(2))]
                        card.controllingPlayer.ChangeCardPosition(card, int(matchZonePositionChange.group(7)))
                        if matchZonePositionChange.group(5) == self.myPlayerNumber:
                            print "" + self.myPlayerName + "'s " + matchZonePositionChange.group(1) + " with id= " + matchZonePositionChange.group(2) + " position changed to " + matchZonePositionChange.group(7)
                        else:
                            print "" + self.opponentPlayerName + "'s " + matchZonePositionChange.group(1) + " with id= " + matchZonePositionChange.group(2) + " position changed to " + matchZonePositionChange.group(7)

                    matchMulliganWaitingForChoices = re.match(self.mulliganWaitingForChoices,line)
                    if matchMulliganWaitingForChoices is not None:
                        if matchMulliganWaitingForChoices.group(1) == self.myPlayerName:
                            finished = True
                            self.gameState.aiPlayer.MulliganPhase()
                            break
                self.lastLineByte = logFile.tell()
            logFile.close()
        print "*****Found " + self.myPlayerName +"'s options and now waiting for the player's decision.*****"
        self.ParseMulliganPhaseEnd()
                        
    def ParseMulliganPhaseEnd(self):
        finished = False
        while not finished:
            with open("C:\Program Files (x86)\Hearthstone\Hearthstone_Data\output_log.txt", "r+") as logFile:
                logFile.seek(self.lastLineByte)
                for line in logFile:
                    matchTurnStart = re.match(self.turnStart,line)
                    if matchTurnStart is not None:
                        if matchTurnStart.group(1) == self.myPlayerName:
                            self.gameState.friendlyPlayer.StartTurn()
                        else:
                            self.gameState.opponentPlayer.StartTurn()
                        print "" + matchTurnStart.group(1) + " has started their turn"
                    
                    matchFriendlyMulliganedCards = re.match(self.friendlyMulliganedCards,line)
                    if matchFriendlyMulliganedCards is not None and matchFriendlyMulliganedCards.group(4) == self.myPlayerNumber:
                        self.gameState.friendlyPlayer.ReturnCardToDeck(int(matchFriendlyMulliganedCards.group(2)))
                        print "" + self.myPlayerName + " put " + matchFriendlyMulliganedCards.group(1) + " with id= " + matchFriendlyMulliganedCards.group(2) + " back into their deck"

                    matchFriendlyDrawnCards = re.match(self.friendlyDrawnCards,line)
                    if matchFriendlyDrawnCards is not None:
                        self.gameState.friendlyPlayer.DrawCard(0, int(matchFriendlyDrawnCards.group(2)), matchFriendlyDrawnCards.group(3))
                        print "" + self.myPlayerName + " drew " + matchFriendlyDrawnCards.group(1) + " with id= " + matchFriendlyDrawnCards.group(2)

                    matchZonePositionChange = re.match(self.zonePositionChange,line)
                    if matchZonePositionChange is not None:
                        card = self.gameState.existingCards[int(matchZonePositionChange.group(2))]
                        card.controllingPlayer.ChangeCardPosition(card, int(matchZonePositionChange.group(7)))
                        if matchZonePositionChange.group(5) == self.myPlayerNumber:
                            #print "" + self.myPlayerName + "'s " + matchZonePositionChange.group(1) + " with id= " + matchZonePositionChange.group(2) + " position changed to " + matchZonePositionChange.group(7)
                            pass
                        else:
                            #print "" + self.opponentPlayerName + "'s " + matchZonePositionChange.group(1) + " with id= " + matchZonePositionChange.group(2) + " position changed to " + matchZonePositionChange.group(7)
                            pass

                    matchMulliganEnd = re.match(self.mulliganEnd,line)
                    if matchMulliganEnd is not None:
                        if matchMulliganEnd.group(1) == self.myPlayerName:
                            finished = True
                            break
                self.lastLineByte = logFile.tell()
                logFile.close()
        self.gameState.phase = "Main Play"
        print "*****Mulligan Phase over. Now parsing Main Play.*****"
        self.ParseMainPlay()

    def ParseMainPlay(self):
        while not self.gameState.gameIsOver:
            with open("C:\Program Files (x86)\Hearthstone\Hearthstone_Data\output_log.txt", "r+") as logFile:
                logFile.seek(self.lastLineByte)
                for line in logFile:
                    matchFriendlyPlayedCards = re.match(self.friendlyPlayedCards, line)
                    if matchFriendlyPlayedCards is not None and matchFriendlyPlayedCards.group(5) == self.myPlayerNumber:
                        print "" + self.myPlayerName + " played " + matchFriendlyPlayedCards.group(1) + " with id= " + matchFriendlyPlayedCards.group(2) + " in position " + matchFriendlyPlayedCards.group(3)
                        self.gameState.friendlyPlayer.PlayCard(int(matchFriendlyPlayedCards.group(3)), int(matchFriendlyPlayedCards.group(2)), matchFriendlyPlayedCards.group(4))

                    matchUsedHeroPower = re.match(self.usedHeroPower,line)
                    if matchUsedHeroPower is not None and matchUsedHeroPower.group(3) == self.opponentPlayerNumber:
                        print "" + self.opponentPlayerName + " used their Hero Power: " + matchUsedHeroPower.group(1)
        
                    matchTurnEnd = re.match(self.turnEnd,line)
                    if matchTurnEnd is not None:
                        print "" + matchTurnEnd.group(1) + " has ended their turn"

                    matchTurnStart = re.match(self.turnStart,line)
                    if matchTurnStart is not None:
                        if matchTurnStart.group(1) == self.myPlayerName:
                            self.gameState.friendlyPlayer.StartTurn()
                        else:
                            self.gameState.opponentPlayer.StartTurn()
                        print "" + matchTurnStart.group(1) + " has started their turn"
                      
                    matchFriendlyDrawnCards = re.match(self.friendlyDrawnCards,line)
                    if matchFriendlyDrawnCards is not None:
                        print "" + self.myPlayerName + " drew " + matchFriendlyDrawnCards.group(1) + " with id= " + matchFriendlyDrawnCards.group(2)
                        self.gameState.friendlyPlayer.DrawCard(0, int(matchFriendlyDrawnCards.group(2)), matchFriendlyDrawnCards.group(3))

                    matchLostDevineShield = re.match(self.lostDevineShield,line)
                    if matchLostDevineShield is not None:
                        card = self.gameState.existingCards[int(matchLostDevineShield.group(2))]
                        card.LoseDivineShield()
                        #print "" + self.myPlayerName + "'s " + matchLostDevineShield.group(1) + " with id= " + matchLostDevineShield.group(2) + " lost it's devine shield"
                        
                    matchCardAttackedCard = re.match(self.cardAttackedCard,line)
                    if matchCardAttackedCard is not None:
                        if matchCardAttackedCard.group(5) == self.myPlayerNumber:
                            print "" + self.myPlayerName + "'s " + matchCardAttackedCard.group(1) + " with id= " + matchCardAttackedCard.group(2) + " attacked " + self.opponentPlayerName +"'s " + matchCardAttackedCard.group(6) + " with id= " + matchCardAttackedCard.group(7)
                        else:
                            print "" + self.opponentPlayerName + "'s " + matchCardAttackedCard.group(1) + " with id= " + matchCardAttackedCard.group(2) + " attacked " + self.myPlayerName +"'s " + matchCardAttackedCard.group(6) + " with id= " + matchCardAttackedCard.group(7)
                        card = self.gameState.existingCards[int(matchCardAttackedCard.group(2))]
                        card.Attack(self.gameState.existingCards[int(matchCardAttackedCard.group(7))])

                    matchOpponentPlayedCard = re.match(self.opponentPlayedCard,line)
                    if matchOpponentPlayedCard is not None and matchOpponentPlayedCard.group(5) == self.opponentPlayerNumber:
                        try:
                            self.gameState.opponentPlayer.PlayCard(int(matchOpponentPlayedCard.group(3)), int(matchOpponentPlayedCard.group(2)), matchOpponentPlayedCard.group(4))
                            print "" + self.opponentPlayerName + " played " + matchOpponentPlayedCard.group(1) + " with id= " + matchOpponentPlayedCard.group(2) + " in position " + matchOpponentPlayedCard.group(3)
                        except:
                            pass 

                    matchZonePositionChange = re.match(self.zonePositionChange,line)
                    if matchZonePositionChange is not None:
                        card = self.gameState.existingCards[int(matchZonePositionChange.group(2))]
                        card.controllingPlayer.ChangeCardPosition(card, int(matchZonePositionChange.group(7)))
                        if matchZonePositionChange.group(5) == self.myPlayerNumber:
                            #print "" + self.myPlayerName + "'s " + matchZonePositionChange.group(1) + " with id= " + matchZonePositionChange.group(2) + " position changed to " + matchZonePositionChange.group(7)
                            pass
                        else:
                            #print "" + self.opponentPlayerName + "'s " + matchZonePositionChange.group(1) + " with id= " + matchZonePositionChange.group(2) + " position changed to " + matchZonePositionChange.group(7)
                            pass

                    matchCardTargetedCard = re.match(self.cardTargetedCard,line)
                    if matchCardTargetedCard is not None:
                        card = self.gameState.existingCards[int(matchCardTargetedCard.group(2))]
                        card.TargetWithEffect(self.gameState.existingCards[int(matchCardTargetedCard.group(7))])
                        if matchCardTargetedCard.group(5) == self.myPlayerNumber:
                            if matchCardTargetedCard.group(10) == self.myPlayerNumber:
                                print "" + self.myPlayerName + "'s " + matchCardTargetedCard.group(1) + " with id= " + matchCardTargetedCard.group(2) + " targeted " + self.myPlayerName +"'s " + matchCardTargetedCard.group(6) + " with id= " + matchCardTargetedCard.group(7)
                            else:
                                print "" + self.myPlayerName + "'s " + matchCardTargetedCard.group(1) + " with id= " + matchCardTargetedCard.group(2) + " targeted " + self.opponentPlayerName+"'s " + matchCardTargetedCard.group(6) + " with id= " + matchCardTargetedCard.group(7)
                        else:
                            if matchCardTargetedCard.group(10) == self.myPlayerNumber:
                                print "" + self.opponentPlayerName + "'s " + matchCardTargetedCard.group(1) + " with id= " + matchCardTargetedCard.group(2) + " targeted " + self.myPlayerName +"'s " + matchCardTargetedCard.group(6) + " with id= " + matchCardTargetedCard.group(7)
                            else:
                                print "" + self.opponentPlayerName + "'s " + matchCardTargetedCard.group(1) + " with id= " + matchCardTargetedCard.group(2) + " targeted " + self.opponentPlayerName +"'s " + matchCardTargetedCard.group(6) + " with id= " + matchCardTargetedCard.group(7)
                                
                    #This block handles the total damage that any card in play has taken since it was played. Use this to confirm the life total that cards should have.
                    #Prevents the problem of dealing damage to something twice. For example if something attacks another, ParseMainPlay() will call Attack(attacker, attacker id, defender, defender id)
                    #and that will deal damage, but then ParseMainPlay() will confirm by calling something like ConfirmTotalDamge(5, card, id, player). In the event of random damage there will be no way to keep track of it
                    #besides this if-block calling ConfirmTotalDamage(#, card, id, player). Keep track of totalDamgeThisGame in the card class, if the total damage is => that cards maxHealth, card is dead/destroyed.
                    matchCardTotalDamage = re.match(self.cardTotalDamage,line)
                    if matchCardTotalDamage is not None and matchCardTotalDamage.group(6) is not '0':
                        card = self.gameState.existingCards[int(matchCardTotalDamage.group(2))]
                        card.ConfirmTotalDamageTaken(int(matchCardTotalDamage.group(6)))
                        if matchCardTotalDamage.group(5) == self.myPlayerNumber:
                            print "" + self.myPlayerName + "'s " + matchCardTotalDamage.group(1) + " with id= " + matchCardTotalDamage.group(2) + " has taken " + matchCardTotalDamage.group(6) + " total damage"
                        else:
                            print "" + self.opponentPlayerName + "'s " + matchCardTotalDamage.group(1) + " with id= " + matchCardTotalDamage.group(2) + " has taken " + matchCardTotalDamage.group(6) + " total damage"

                    matchGameOver = re.match(self.gameOver,line)
                    if matchGameOver is not None:
                        if matchGameOver.group(1) == self.myPlayerName:
                            self.gameState.PlayerLost(self.gameState.friendlyPlayer)
                        else:
                            self.gameState.PlayerLost(self.gameState.opponentPlayer)
                self.lastLineByte = logFile.tell()
                logFile.close()
            time.sleep(1)
        print "*****The game is over and " + self.gameState.playerWhoLost.playerName + " lost.*****"

if __name__ == '__main__':
    parser = HearthstoneLogParser()
    parser.FindPlayerNamesAndNumbers()
