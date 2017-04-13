import copy
import Cards
import itertools

class AIPlayer:
    def __init__(self, GameState):
        self.realGameState = GameState
        self.gameState = copy.deepcopy(self.realGameState)
        self.gameStateScore = 0
        self.gameState.friendlyPlayer.playerName = "AIPlayer"
        self.cantKillTargets = []
        self.cardNotKilledProblem = None

    def MulliganPhase(self):
        self.UpdateGameStateAndScore()
        for card in self.realGameState.friendlyPlayer.hand:
            if card.manaCost > 3:
                print "****AI Suggests: Mulligan " + card.name

    def UpdateGameStateAndScore(self):
        self.gameState = copy.deepcopy(self.realGameState)
        self.gameStateScore = self.Evaluation(self.gameState)

    #Board evaluation method.
    def Evaluation(self, gamestate):
        value = gamestate.friendlyPlayer.currentFilledManaCrystals*2
        for card in gamestate.friendlyPlayer.board:
            if card.divineShield:
                value += ((card.currentHealth) + card.currentAttack)*1.5
            else:
                value += ((card.currentHealth) + card.currentAttack)
        if gamestate.friendlyPlayer.hero.hasWeapon:
            value += card.currentAttack
        for card in gamestate.opponentPlayer.board:
            if card.divineShield:
                value -= (card.currentHealth + (card.currentAttack*2))*1.5
            else:
                value -= (card.currentHealth + (card.currentAttack*2))
        if gamestate.opponentPlayer.hero.hasWeapon:
            value -= card.currentAttack*3
        return value

    def DamageOnBoard(self, gamestate):
        damage = 0
        attackers = []
        for card in gamestate.friendlyPlayer.board:
            if card.type == "Minion":
                if not card.exhausted and not card.frozen:
                    attackers.append(card)
                    damage += card.currentAttack
        attackers.sort(key=lambda x: x.currentAttack, reverse=True)
        return [damage, attackers]

    def DamageInHand(self, target, gamestate):
        mana = copy.copy(gamestate.friendlyPlayer.currentFilledManaCrystals)
        enemyTaunts = self.FindEnemyTaunts(gamestate)
        if mana > 0:
            damage = 0
            cards = []
            validBoardPosition = len(gamestate.friendlyPlayer.board)
            damageInHandCards = []
            heroPower = gamestate.friendlyPlayer.heroPower
            if not heroPower.exhausted:
                cards.append(heroPower)
            if target.type == "Hero":
                for card in gamestate.friendlyPlayer.hand:
                    if card.effectCanHitHeroes or (card.charge and len(enemyTaunts) == 0):
                        cards.append(card)
            else:
                for card in gamestate.friendlyPlayer.hand:
                    if card.effectCanHitMinions or (card.charge and (len(enemyTaunts) == 0 or target.tuant)):
                        cards.append(card)
            cards.sort(key=lambda x: (x.effectDamage or x.currentAttack), reverse=True)
            for x in range(0, len(cards)):
                if mana >= cards[x].manaCost:
                    damage += cards[x].effectDamage
                    damageInHandCards.append(["Play", validBoardPosition, cards[x], target])
                if mana == 0:
                    break
            return [damage, damageInHandCards]
        else:
            return [0, []]

    #do we have cards that just kill a target?
    def KillCardOptions(self, target, gamestate):
        options = []
        for card in gamestate.friendlyPlayer.hand:
            if card.killOrReplace == True:
                options.append(["Play", 0, card, target])
        return options

    def FindEnemyTaunts(self,gamestate):
        enemyTauntMinions = []
        for target in gamestate.opponentPlayer.board:
            if target.taunt:
                enemyTauntMinions.append(target)
        return enemyTauntMinions

    def OrderTargetsByTauntPriority(self, gamestate):
        hpt = self.OrderTargetsByGeneralPriority(gamestate)
        hpt.sort(key=lambda x: x[0].taunt, reverse=True)
        return hpt

    def OrderTargetsByGeneralPriority(self, gamestate):
        currentScore = self.Evaluation(gamestate)
        highPriorityTargets = []
        targets = self.gameState.opponentPlayer.board
        for target in targets:
            if not target.type == "Hero":
                simGS = copy.deepcopy(gamestate)
                simGS.existingCards[target.idNumber].Die()
                score = self.Evaluation(simGS)
                scoreDifference = score - currentScore
                node = [target, scoreDifference]
                highPriorityTargets.append(node)
        highPriorityTargets.sort(key=lambda x: x[1], reverse=True)
        return highPriorityTargets

    def CanKillTarget(self, target, gamestate):
        canKillTargetOptions = []
        killCards = []
        damageInHand = self.DamageInHand(target, gamestate)
        damageOnBoard = self.DamageOnBoard(gamestate)
        enemyTaunts = self.FindEnemyTaunts(gamestate)
        if gamestate.friendlyPlayer.coin != None:
            canKillTargetOptions.append(["Play", 0, gamestate.friendlyPlayer.coin, target])
        if target.currentHealth <= damageOnBoard[0]:
            if target.taunt or len(enemyTaunts) == 0:
                for card in gamestate.friendlyPlayer.board:
                    if (card.type == "Hero" and card.hasWeapon) or (card.type == "Minion" and card.currentAttack > 0):
                        canKillTargetOptions.append(["Attack", 0, card, target])
                return [True, "Need Minions Only", canKillTargetOptions]
        if target.currentHealth <= damageInHand[0]:
            canKillTargetOptions = damageInHand[1]
            for card in killCards:
                canKillTaretOptions.append(["Play", 0, card, target])
            return [True, "Need Hand Only", canKillTargetOptions]
        if target.currentHealth <= (damageInHand[0] + damageOnBoard[0]):
            if len(enemyTaunts) == 0 or target.taunt:
                canKillTargetOptions = damageInHand[1]
                for card in killCards:
                    canKillTargetOptions.append(["Play", 0, card, target])
                for card in gamestate.friendlyPlayer.board:
                    if (card.type == "Hero" and card.hasWeapon) or (card.type == "Minion" and card.currentAttack > 0):
                        canKillTargetOptions.append(["Attack", 0, card, target])
                return [True, "Need Minions In Play", canKillTargetOptions]
            else:
                return [False, "Need Minions In Play", canKillTargetOptions]
        killCards = self.KillCardOptions(target, gamestate)
        if target.type == "Minion":
            for card in killCards:
                canKillTargetOptions.append(["Play", 0, card, target])
        else:
            return [False, "Can't Kill", None]

    def PrintCombo(self, moves, target):
        print "****AI Moves For Killing " + target.name + "****"
        movesInner = moves[0]
        for move in movesInner:
            if move[0] == "Play":
                print "Play " + move[2].name + " in position " + str(move[1]) + " on " + move[3].name + " in position " + str(move[3].position)
            elif move[0] == "Attack":
                print "Attack " + move[3].name + " in position " + str(move[3].position) + " with " + move[2].name + " in position " + str(move[2].position)

    def FindKillCombinations(self, options, health, combs=[]):
        combos = []
        for i in range(0, 20):
            for combo in itertools.combinations(options, i):
                amount = 0
                for move in combo:
                    if move[0] == "Attack":
                        amount += move[2].currentAttack
                    if move[0] == "Play":
                        amount += move[2].effectDamage
                    if amount >= health:
                        combos.append(combo)
        return combos

    def FindBestKillCombo(self, target, options, gamestate):
        moves = []
        combos = self.FindKillCombinations(options, target.currentHealth)
        bestCombo = [-100000000000000000000, []]
        for combo in combos:
            simGS = copy.deepcopy(gamestate)
            for move in combo:
                if move[0] == "Attack":
                    simGS.existingCards[move[2].idNumber].Attack(simGS.existingCards[move[3].idNumber])
                if move[0] == "Play":
                    simGS.friendlyPlayer.PlayCard(move[1], move[2].idNumber, None, simGS.existingCards[move[3].idNumber])
            score = self.Evaluation(simGS)
            if bestCombo[0] < score or len(bestCombo[1]) > len(combo):
                bestCombo = [score, combo]
        moves.append(bestCombo[1])
        return moves

    # Plays the best combo so we just need to return the game state after target's death
    def PlayBestCombo(self, target, options, gamestate):
        moves = self.FindBestKillCombo(target, options, gamestate)
        self.PrintCombo(moves, target)
        movesInner = moves[0]
        for move in movesInner:
            if move[0] == "Play":
                gamestate.friendlyPlayer.PlayCard(move[1], move[2].idNumber, None, self.gameState.existingCards[move[3].idNumber])
            elif move[0] == "Attack":
                gamestate.existingCards[move[2].idNumber].Attack(self.gameState.existingCards[move[3].idNumber])
        return gamestate

    def PlayAttackMovesVsHero(self, gamestate):
        for card in gamestate.friendlyPlayer.board:
            if (card.type == "Hero" and card.hasWeapon) or card.type == "Minion":
                if not card.exhausted:
                    gamestate.existingCards[card.idNumber].Attack(gamestate.opponentPlayer.hero)
                    print "Attack " + gamestate.opponentPlayer.hero.name + " with " + card.name + " in position " + str(card.position)

    def PlayDrawCard(self, gamestate):
        for card in gamestate.friendlyPlayer.hand:
            mana = copy.copy(gamestate.friendlyPlayer.currentFilledManaCrystals)
            validBoardPosition = len(gamestate.friendlyPlayer.board)
            if card.manaCost <= mana:
                if card.randomMechanic is not None:
                    if card.randomMechanic[0] == "DrawCard":
                        print "****AI Suggests: Play " + card.name + " in position " + str(validBoardPosition) + " as what is drawn could be very helpful."

    def PlayMinionsFromHand(self, gamestate):
        options = []
        for card in gamestate.friendlyPlayer.hand:
            if card.type == "Minion" and gamestate.friendlyPlayer.currentFilledManaCrystals >= card.manaCost:
                if not card.charge:
                    simGS = copy.deepcopy(gamestate)
                    validBoardPosition = len(gamestate.friendlyPlayer.board)
                    simGS.friendlyPlayer.PlayCard(validBoardPosition, card.idNumber)
                    score = self.Evaluation(simGS)
                    option = [score, card]
                    options.append(option)
        options.sort(key=lambda x: x[0], reverse=True)
        for opt in options:
            mana = copy.copy(gamestate.friendlyPlayer.currentFilledManaCrystals)
            if opt[1].manaCost <= mana:
                validBoardPosition = len(gamestate.friendlyPlayer.board)
                gamestate.friendlyPlayer.PlayCard(validBoardPosition, opt[1].idNumber)
                print "Play " + opt[1].name + " in position " + str(validBoardPosition)

    def Search(self, highPriorityTargets):
        if len(highPriorityTargets) == 0:
            return
        #pick target
        targetScorePair = highPriorityTargets[0]
        target = targetScorePair[0]
        if not target in self.cantKillTargets:
            #can kill target at all?
            canKill = self.CanKillTarget(target, self.gameState)
            if canKill[0]:
                options = canKill[2]
                #update simulated game state
                self.gameState = self.PlayBestCombo(target, options, self.gameState)
                if self.gameState.existingCards[target.idNumber].zone != "Graveyard":
                    self.cardNotKilledProblem = target
                if self.cardNotKilledProblem == target:
                    return
                #update board score
                self.gameStateScore = self.Evaluation(self.gameState)
                #target killed might have changed the priority order so generate a new list
                newTargets = self.OrderTargetsByGeneralPriority(self.gameState)
                self.Search(newTargets)
            else:
                if canKill[1] == "Can't Kill":
                    #can't kill high priority target, get new target.
                    highPriorityTargets.remove(targetScorePair)
                    self.cantKillTargets.append(target)
                    self.Search(highPriorityTargets)
                elif canKill[1] == "Need Minions In Play":
                    #target blocked by taunt minion(s)
                    highPriorityTargets = self.OrderTargetsByTauntPriority(self.gameState)
                    self.Search(highPriorityTargets)
        else:
            highPriorityTargets.remove(targetScorePair)
            self.Search(highPriorityTargets)

    def Start(self):
        self.UpdateGameStateAndScore()
        if self.realGameState.phase == "Main Play":
            if self.realGameState.friendlyPlayer.aiWaitingForDraw == 0:
                #can win now? add up damage on board and damage in hand
                canKill = self.CanKillTarget(self.gameState.friendlyPlayer.opponentPlayer.hero, self.gameState)
                if canKill[0]:
                    if canKill[1] == "Need Minions In Play":
                        print "****AI Can Win: Use all available damage (minions in play and hand) on the opponent's hero starting with highest first."
                        return
                    elif canKill[1] == "Need Hand Only":
                        print "****AI Can Win: Use all available damge in your hand on the opponent's hero starting with highest first."
                        return
                highPriorityTargets = self.OrderTargetsByGeneralPriority(self.gameState)
                if len(highPriorityTargets) > 0:
                    self.Search(highPriorityTargets)
                self.PlayMinionsFromHand(self.gameState)
                self.PlayAttackMovesVsHero(self.gameState)
                self.PlayDrawCard(self.gameState)
                print "****End Turn****"
            else:
                self.realGameState.friendlyPlayer.aiWaitingForDraw -= 1
