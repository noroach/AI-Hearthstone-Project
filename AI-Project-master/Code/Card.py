import copy

class Card(object):
    def __init__(self, idNumber, controllingPlayer, position, zone):
        self.controllingPlayer = controllingPlayer
        self.name = "Unknown"
        self.type = "Unknown"
        self.idNumber = idNumber
        self.position = position
        self.zone = zone
        
        self.normalHealth = 0
        self.normalAttack= 0
        self.maxHealth = 0
        self.currentHealth = 0
        self.currentAttack = 0
        self.manaCost = 0
        self.totalDamageTaken = 0
        self.effectDamage = 0

        self.tokenMinion = False
        self.exhausted = False
        self.divineShield = False
        self.frozen = False
        self.taunt = False
        self.hasAuraEffect = False
        self.positionMatters = False
        self.needsTarget = False
        self.canTargetHeroes = False
        self.freezeDefenderOnAttack = False
        self.killOrReplace = False
        self.effectCanHitHeroes = False
        self.effectCanHitMinions = False
        self.charge = False
        self.randomMechanic = None

        self.cardsAffectedByAura = []

        #For Hero cards
        self.armor = 0
        self.hasWeapon = False
        self.weapon = None

    def OnPlay(self, target=None):
        if target != None:
            self.TargetWithEffect(target)

    #for cards that target something when played
    def TargetWithEffect(self, targetedCard):
        pass

    def Aura(self):
        pass

    def UndoAura(self):
        pass

    def BuffAttack(self, amount):
        self.currentAttack += amount

    def DebuffAttack(self, amount):
        self.currentAttack -= amount

    def BuffHealth(self, amount):
        self.currentHealth += amount
        self.maxHealth += amount

    def DebuffHealth(self, amount):
        self.maxHealth -= amount
        if self.currentHealth > self.maxHealth:
            self.currentHealth = copy.copy(self.maxHealth)

    def GainDivineShield(self):
        self.divineShield = True

    def LoseDivineShield(self):
        self.divineShield = False

    def GainTaunt(self):
        self.taunt = True

    def LoseTaunt(self):
        self.taunt = False

    def TakeDamage(self, amount):
        if not self.divineShield:
            self.currentHealth -= amount
            self.totalDamageTaken += amount
            self.CheckIfDead()
        elif amount > 0:
            self.LoseDivineShield()

    def Heal(self, amount):
        self.currentHealth += amount
        if self.currentHealth > self.maxHealth:
            self.currentHealth = copy.copy(self.maxHealth)
        self.totalDamageTaken -= amount
        if self.totalDamageTaken < 0:
            self.totalDamageTaken = 0

    def Attack(self, defender):
        if self.exhausted == False:
            if self.type != "Hero":
                if defender.type == "Minion":
                    self.TakeDamage(defender.currentAttack)
                defender.TakeDamage(self.currentAttack)
                self.exhausted = True
            else:
                if defender.type == "Minion":
                    self.TakeDamage(defender.currentAttack)
                defender.TakeDamage(self.weapon.currentAttack)
                self.weapon.TakeDamage(1)
                self.exhausted = True

    def CheckIfDead(self):
        if self.currentHealth <= 0:
            self.Die()

    def UpdatePosition(self, newPosition):
        self.position = newPosition
        if self.type == "Minion":
            for x in range(0,len(self.controllingPlayer.board)):
                card = self.controllingPlayer.board[x]
                if card.idNumber == self.idNumber:
                    self.position = x

    def EquipWeapon(self, weapon):
        if self.type == "Hero":
            self.hasWeapon = True
            self.weapon = weapon

    def ConfirmTotalDamageTaken(self, amount):
        if self.totalDamageTaken != amount:
            difference = self.totalDamageTaken - amount
            self.currentHealth += difference
            self.totalDamageTaken = amount
            self.CheckIfDead()

    def RemoveFromPlay(self):
        self.controllingPlayer.board.remove(self)

    def Die(self):
        if self.zone != "Graveyard":
            if self.type != "Weapon":
                if self.type == "Hero":
                    self.controllingPlayer.gameState.PlayerLost(self.controllingPlayer)
                self.UndoAura()
                self.controllingPlayer.board.remove(self)
                self.zone = "Graveyard"
            else:
                self.controllingPlayer.hero.weapon = None
                self.controllingPlayer.hero.hasWeapon = False
                self.zone = "Graveyard"

    def __repr__(self):
        return self.name + ": id=" + str(self.idNumber) + " zone=" + str(self.zone) + " Atk=" + str(self.currentAttack) + " Hp=" + str(self.currentHealth) + " NAtk=" + str(self.normalAttack) + " NHP=" + str(self.normalHealth) + " Pos=" + str(self.position) + " Exh=" + str(self.exhausted) + " DS=" + str(self.divineShield) + " Frz=" + str(self.frozen) + " Tnt=" + str(self.taunt)
