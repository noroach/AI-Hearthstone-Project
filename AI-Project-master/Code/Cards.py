import copy
from Card import Card

class UnknownCard(Card):
    def __init__(self, idNumber, controllingPlayer, position, zone):
        Card.__init__(self, idNumber, controllingPlayer, position, zone)
        self.idNumber = idNumber
        self.name = "Unknown Card"
        self.type = "Unknown"
        self.normalHealth = 0
        self.normalAttack = 0
        self.maxHealth = copy.copy(self.normalHealth)
        self.currentHealth = copy.copy(self.normalHealth)
        self.currentAttack = copy.copy(self.normalAttack)
        self.manaCost = 12

#Frostbolt
class CS2_024(Card):
    def __init__(self, idNumber, controllingPlayer, position, zone):
        Card.__init__(self, idNumber, controllingPlayer, position, zone)
        self.idNumber = idNumber
        self.name = "Frostbolt"
        self.type = "Spell"
        self.manaCost = 2
        self.needsTarget = True
        self.canTargetHeroes = True
        self.effectCanHitHeroes = True
        self.effectCanHitMinions = True
        self.effectDamage = 3

    def OnPlay(self, target=None):
        if target != None:
            target.TakeDamage(3)
            target.frozen = True
        else:
            self.controllingPlayer.cardWaitingForTarget = self

    def TargetWithEffect(self, target=None):
        if target != None:
            target.TakeDamage(3)
            target.frozen = True

#Arcane Explosion
class CS2_025(Card):
    def __init__(self, idNumber, controllingPlayer, position, zone):
        Card.__init__(self, idNumber, controllingPlayer, position, zone)
        self.idNumber = idNumber
        self.name = "Arcane Explosion"
        self.type = "Spell"
        self.manaCost = 2
        self.effectCanHitMinions = True

    def OnPlay(self, target=None):
        for card in self.controllingPlayer.opponentPlayer.board:
            if card.type != "Hero":
                card.TakeDamage(1)

#Arcane Intellect
class CS2_023(Card):
    def __init__(self, idNumber, controllingPlayer, position, zone):
        Card.__init__(self, idNumber, controllingPlayer, position, zone)
        self.idNumber = idNumber
        self.name = "Arcane Intellect"
        self.type = "Spell"
        self.manaCost = 3
        self.randomMechanic = ["DrawCard", 2]

    def OnPlay(self, target=None):
        if self.controllingPlayer.playerName == "AIPlayer":
            self.controllingPlayer.DrawCard(None,None, "UnknownCard")
            self.controllingPlayer.DrawCard(None,None, "UnknownCard")

#Blessing of Might
class CS2_087(Card):
    def __init__(self, idNumber, controllingPlayer, position, zone):
        Card.__init__(self, idNumber, controllingPlayer, position, zone)
        self.idNumber = idNumber
        self.name = "Blessing of Might"
        self.type = "Spell"
        self.manaCost = 1
        self.needsTarget = True
        self.effectCanHitMinions = True

    def OnPlay(self, target=None):
        if target != None and target.type != "Hero":
            target.BuffAttack(3)
        else:
            self.controllingPlayer.cardWaitingForTarget = self

    def TargetWithEffect(self, target):
        if target != None and target.type != "Hero":
            target.BuffAttack(3)
        self.controllingPlayer.cardWaitingForTarget = None

#Bloodfen Raptor
class CS2_172(Card):
   def __init__(self, idNumber, controllingPlayer, position, zone):
        Card.__init__(self, idNumber, controllingPlayer, position, zone)
        self.idNumber = idNumber
        self.name = "Bloodfen Raptor"
        self.type = "Minion"
        self.normalHealth = 2
        self.normalAttack = 3
        self.maxHealth = copy.copy(self.normalHealth)
        self.currentHealth = copy.copy(self.normalHealth)
        self.currentAttack = copy.copy(self.normalAttack)
        self.manaCost = 2

#Boulderfist Ogre
class CS2_200(Card):
    def __init__(self, idNumber, controllingPlayer, position, zone):
        Card.__init__(self, idNumber, controllingPlayer, position, zone)
        self.idNumber = idNumber
        self.name = "Boulderfist Ogre"
        self.type = "Minion"
        self.normalHealth = 7
        self.normalAttack = 6
        self.maxHealth = copy.copy(self.normalHealth)
        self.currentHealth = copy.copy(self.normalHealth)
        self.currentAttack = copy.copy(self.normalAttack)
        self.manaCost = 6

#Elven Archer
class CS2_189(Card):
    def __init__(self, idNumber, controllingPlayer, position, zone):
        Card.__init__(self, idNumber, controllingPlayer, position, zone)
        self.idNumber = idNumber
        self.name = "Elven Archer"
        self.type = "Minion"
        self.normalHealth = 1
        self.normalAttack = 1
        self.maxHealth = copy.copy(self.normalHealth)
        self.currentHealth = copy.copy(self.normalHealth)
        self.currentAttack = copy.copy(self.normalAttack)
        self.manaCost = 1
        self.needsTarget = True
        self.effectCanHitHeroes = True
        self.effectCanHitMinions = True
        self.effectDamage = 1
        
    def OnPlay(self, target=None):
        if target != None:
            target.TakeDamage(1)
        else:
            self.controllingPlayer.cardWaitingForTarget = self

    def TargetWithEffect(self, target):
        target.TakeDamage(1)
        self.controllingPlayer.cardWaitingForTarget = None

#Fireball
class CS2_029(Card):
    def __init__(self, idNumber, controllingPlayer, position, zone):
        Card.__init__(self, idNumber, controllingPlayer, position, zone)
        self.idNumber = idNumber
        self.name = "Fireball"
        self.type = "Spell"
        self.manaCost = 4
        self.needsTarget = True
        self.effectCanHitHeroes = True
        self.effectCanHitMinions = True
        self.effectDamage = 6

    def OnPlay(self, target=None):
        if target != None:
            target.TakeDamage(6)
        else:
            self.controllingPlayer.cardWaitingForTarget = self

    def TargetWithEffect(self, target):
        if target != None:
            target.TakeDamage(6)
        self.controllingPlayer.cardWaitingForTarget = None

#Fireblast
class CS2_034(Card):
    def __init__(self, idNumber, controllingPlayer, position, zone):
        Card.__init__(self, idNumber, controllingPlayer, position, zone)
        self.idNumber = idNumber
        self.name = "Fireblast"
        self.type = "Hero Power"
        self.manaCost = 2
        self.needsTarget = True
        self.effectCanHitHeroes = True
        self.effectCanHitMinions = True
        self.effectDamage = 1

    def OnPlay(self, target=None):
        if target != None:
            self.exhausted = True
            target.TakeDamage(1)
        else:
            self.controllingPlayer.cardWaitingForTarget = self

    def TargetWithEffect(self, target):
        if target != None:
            self.exhausted = True
            target.TakeDamage(1)
        self.controllingPlayer.cardWaitingForTarget = None

#Gnomish Inventor
class CS2_147(Card):
    def __init__(self, idNumber, controllingPlayer, position, zone):
        Card.__init__(self, idNumber, controllingPlayer, position, zone)
        self.idNumber = idNumber
        self.name = "Gnomish Inventor"
        self.type = "Minion"
        self.normalHealth = 4
        self.normalAttack = 2
        self.maxHealth = copy.copy(self.normalHealth)
        self.currentHealth = copy.copy(self.normalHealth)
        self.currentAttack = copy.copy(self.normalAttack)
        self.manaCost = 4
        self.randomMechanic = ["DrawCard", 1]

    def OnPlay(self, target=None):
        if self.controllingPlayer.playerName == "AIPlayer":
            self.controllingPlayer.DrawCard(None,None, "UnknownCard")

#Goldshire Footman
class CS1_042(Card):
    def __init__(self, idNumber, controllingPlayer, position, zone):
        Card.__init__(self, idNumber, controllingPlayer, position, zone)
        self.idNumber = idNumber
        self.name = "Goldshire Footman"
        self.type = "Minion"
        self.normalHealth = 2
        self.normalAttack = 1
        self.maxHealth = copy.copy(self.normalHealth)
        self.currentHealth = copy.copy(self.normalHealth)
        self.currentAttack = copy.copy(self.normalAttack)
        self.manaCost = 1

    def OnPlay(self, target=None):
        self.GainTaunt()

#Hammer of Wrath
class CS2_094(Card):
    def __init__(self, idNumber, controllingPlayer, position, zone):
        Card.__init__(self, idNumber, controllingPlayer, position, zone)
        self.idNumber = idNumber
        self.name = "Hammer of Wrath"
        self.type = "Spell"
        self.manaCost = 4
        self.randomMechanic = ["DrawCard", 1]
        self.needsTarget = True
        self.effectCanHitHeroes = True
        self.effectCanHitMinions = True
        self.effectDamage = 3
    
    def OnPlay(self, target=None):
        if controllingPlayer.name == "AIPlayer":
            self.controllingPlayer.DrawCard(None, None, "UnknownCard")
        if target != None:
            target.TakeDamage(3)
        else:
            self.controllingPlayer.cardWaitingForTarget = self

    def TargetWithEffect(self, target):
        if target != None:
            target.TakeDamage(3)
        self.controllingPlayer.cardWaitingForTarget = None

#Hand of Protection
class EX1_371(Card):
    def __init__(self, idNumber, controllingPlayer, position, zone):
        Card.__init__(self, idNumber, controllingPlayer, position, zone)
        self.idNumber = idNumber
        self.name = "Hand of Protection"
        self.type = "Spell"
        self.manaCost = 1
        self.needsTarget = True
        self.effectCanHitMinions = True
    
    def OnPlay(self, target=None):
        if target != None:
            target.GainDivineShield()
        else:
            self.controllingPlayer.cardWaitingForTarget = self

    def TargetWithEffect(self, target):
        if target != None:
            target.GainDivineShield()
        self.controllingPlayer.cardWaitingForTarget = None

#Holy Light
class CS2_089(Card):
    def __init__(self, idNumber, controllingPlayer, position, zone):
        Card.__init__(self, idNumber, controllingPlayer, position, zone)
        self.idNumber = idNumber
        self.name = "Holy Light"
        self.type = "Spell"
        self.manaCost = 2
        self.needsTarget = True
        self.effectCanHitHeroes = True
        self.effectCanHitMinions = True
    
    def OnPlay(self, target=None):
        if target != None:
            target.Heal(6)
        else:
            self.controllingPlayer.cardWaitingForTarget = self

    def TargetWithEffect(self, target):
        if target != None:
            target.Heal(6)
        self.controllingPlayer.cardWaitingForTarget = None

#Ironforge Rifleman
class CS2_141(Card):
    def __init__(self, idNumber, controllingPlayer, position, zone):
        Card.__init__(self, idNumber, controllingPlayer, position, zone)
        self.idNumber = idNumber
        self.name = "Ironforge Rifleman"
        self.type = "Minion"
        self.normalHealth = 2
        self.normalAttack = 2
        self.maxHealth = copy.copy(self.normalHealth)
        self.currentHealth = copy.copy(self.normalHealth)
        self.currentAttack = copy.copy(self.normalAttack)
        self.manaCost = 3
        self.needsTarget = True
        self.effectCanHitHeroes = True
        self.effectCanHitMinions = True
        self.effectDamage = 1

    def OnPlay(self, target=None):
        if target != None:
            target.TakeDamage(1)
        else:
            self.controllingPlayer.cardWaitingForTarget = self

    def TargetWithEffect(self, target):
        if target != None:
            target.TakeDamage(1)
        self.controllingPlayer.cardWaitingForTarget = None

#Jaina Proudmoore
class HERO_08(Card):
    def __init__(self, idNumber, controllingPlayer, position, zone):
        Card.__init__(self, idNumber, controllingPlayer, position, zone)
        self.idNumber = idNumber
        self.name = "Jaina Proudmoore"
        self.type = "Hero"
        self.normalHealth = 30
        self.normalAttack = 0
        self.maxHealth = copy.copy(self.normalHealth)
        self.currentHealth = copy.copy(self.normalHealth)
        self.currentAttack = copy.copy(self.normalAttack)

#Light's Justice
class CS2_091(Card):
    def __init__(self, idNumber, controllingPlayer, position, zone):
        Card.__init__(self, idNumber, controllingPlayer, position, zone)
        self.idNumber = idNumber
        self.name = "Light's Justice"
        self.type = "Weapon"
        self.normalHealth = 4
        self.normalAttack = 1
        self.maxHealth = copy.copy(self.normalHealth)
        self.currentHealth = copy.copy(self.normalHealth)
        self.currentAttack = copy.copy(self.normalAttack)
        self.manaCost = 1

    def OnPlay(self, target=None):
        self.controllingPlayer.hero.EquipWeapon(self)

#Lord of the Arena
class CS2_162(Card):
    def __init__(self, idNumber, controllingPlayer, position, zone):
        Card.__init__(self, idNumber, controllingPlayer, position, zone)
        self.idNumber = idNumber
        self.name = "Lord of the Arena"
        self.type = "Minion"
        self.normalHealth = 5
        self.normalAttack = 6
        self.maxHealth = copy.copy(self.normalHealth)
        self.currentHealth = copy.copy(self.normalHealth)
        self.currentAttack = copy.copy(self.normalAttack)
        self.manaCost = 6

    def OnPlay(self, target=None):
        self.GainTaunt()

#Murloc Raider
class CS2_168(Card):
    def __init__(self, idNumber, controllingPlayer, position, zone):
        Card.__init__(self, idNumber, controllingPlayer, position, zone)
        self.idNumber = idNumber
        self.name = "Murloc Raider"
        self.type = "Minion"
        self.normalHealth = 1
        self.normalAttack = 2
        self.maxHealth = copy.copy(self.normalHealth)
        self.currentHealth = copy.copy(self.normalHealth)
        self.currentAttack = copy.copy(self.normalAttack)
        self.manaCost = 1

#Nightblade
class EX1_593(Card):
    def __init__(self, idNumber, controllingPlayer, position, zone):
        Card.__init__(self, idNumber, controllingPlayer, position, zone)
        self.idNumber = idNumber
        self.name = "Nightblade"
        self.type = "Minion"
        self.normalHealth = 4
        self.normalAttack = 4
        self.maxHealth = copy.copy(self.normalHealth)
        self.currentHealth = copy.copy(self.normalHealth)
        self.currentAttack = copy.copy(self.normalAttack)
        self.manaCost = 5
        self.effectCanHitHeroes = True
        self.effectDamage = 3

    def OnPlay(self, target=None):
        self.controllingPlayer.opponentPlayer.hero.TakeDamage(3)

#Chillwind Yeti
class CS2_182(Card):
    def __init__(self, idNumber, controllingPlayer, position, zone):
        Card.__init__(self, idNumber, controllingPlayer, position, zone)
        self.idNumber = idNumber
        self.name = "Chillwind Yeti"
        self.type = "Minion"
        self.normalHealth = 5
        self.normalAttack = 4
        self.maxHealth = copy.copy(self.normalHealth)
        self.currentHealth = copy.copy(self.normalHealth)
        self.currentAttack = copy.copy(self.normalAttack)
        self.manaCost = 4
        
#Novice Engineer
class EX1_015(Card):
    def __init__(self, idNumber, controllingPlayer, position, zone):
        Card.__init__(self, idNumber, controllingPlayer, position, zone)
        self.idNumber = idNumber
        self.name = "Novice Engineer"
        self.type = "Minion"
        self.normalHealth = 1
        self.normalAttack = 1
        self.maxHealth = copy.copy(self.normalHealth)
        self.currentHealth = copy.copy(self.normalHealth)
        self.currentAttack = copy.copy(self.normalAttack)
        self.manaCost = 2
        self.randomMechanic = ["DrawCard", 1]

    def OnPlay(self, target=None):
        if self.controllingPlayer.playerName == "AIPlayer":
            self.controllingPlayer.DrawCard(None,None, "UnknownCard")

#Oasis Snapjaw
class CS2_119(Card):
    def __init__(self, idNumber, controllingPlayer, position, zone):
        Card.__init__(self, idNumber, controllingPlayer, position, zone)
        self.idNumber = idNumber
        self.name = "Oasis Snapjaw"
        self.type = "Minion"
        self.normalHealth = 7
        self.normalAttack = 2
        self.maxHealth = copy.copy(self.normalHealth)
        self.currentHealth = copy.copy(self.normalHealth)
        self.currentAttack = copy.copy(self.normalAttack)
        self.manaCost = 4

#Polymorph ****The Sheep will be picked up by the parser as a played card, so this class does not need to create a sheep unless the user is AIPlayer.
class CS2_022(Card):
    def __init__(self, idNumber, controllingPlayer, position, zone):
        Card.__init__(self, idNumber, controllingPlayer, position, zone)
        self.idNumber = idNumber
        self.name = "Polymorph"
        self.type = "Spell"
        self.manaCost = 4
        self.needsTarget = True
        self.killOrReplace = True
        self.effectCanHitMinions = True

    def OnPlay(self, target=None):
        if target != None and self.controllingPlayer.playerName == "AIPlayer":
            target.Die()
            target.controllingPlayer.PlayCard(target.position, "CS2_tk1")
        else:
            self.controllingPlayer.cardWaitingForTarget = self

    def TargetWithEffect(self, target):
        target.Die()
        self.controllingPlayer.cardWaitingForTarget = None

#Raid Leader
class CS2_122(Card):
    def __init__(self, idNumber, controllingPlayer, position, zone):
        Card.__init__(self, idNumber, controllingPlayer, position, zone)
        self.idNumber = idNumber
        self.name = "Raid leader"
        self.type = "Minion"
        self.normalHealth = 2
        self.normalAttack = 2
        self.maxHealth = copy.copy(self.normalHealth)
        self.currentHealth = copy.copy(self.normalHealth)
        self.currentAttack = copy.copy(self.normalAttack)
        self.manaCost = 3
        self.hasAuraEffect = True
        self.aoeBuff = True

    def OnPlay(self, target=None):
        self.Aura()

    def Aura(self):
        for card in self.controllingPlayer.board:
            if card.type != "Hero" and card not in self.cardsAffectedByAura and card != self:
                card.BuffAttack(1)
                self.cardsAffectedByAura.append(card)

    def RemoveFromPlay(self):
        self.controllingPlayer.board.remove(self)
        self.UndoAura()

    def UndoAura(self):
        for card in self.cardsAffectedByAura:
            card.DebuffAttack(1)

#Reinforce ***See Polymorph***
class CS2_101(Card):
    def __init__(self, idNumber, controllingPlayer, position, zone):
        Card.__init__(self, idNumber, controllingPlayer, position, zone)
        self.idNumber = idNumber
        self.name = "Reinforce"
        self.type = "Hero Power"
        self.manaCost = 2

    def OnPlay(self, target=None):
        if self.controllingPlayer.playerName == "AIPlayer":
            self.exhausted = True
            self.controllingPlayer.PlayCard(7,-2, "CS2_101t")

#River Crocolisk
class CS2_120(Card):
    def __init__(self, idNumber, controllingPlayer, position, zone):
        Card.__init__(self, idNumber, controllingPlayer, position, zone)
        self.idNumber = idNumber
        self.name = "River Crocolisk"
        self.type = "Minion"
        self.normalHealth = 3
        self.normalAttack = 2
        self.maxHealth = copy.copy(self.normalHealth)
        self.currentHealth = copy.copy(self.normalHealth)
        self.currentAttack = copy.copy(self.normalAttack)
        self.manaCost = 2

#Sen'jin Shieldmasta
class CS2_179(Card):
    def __init__(self, idNumber, controllingPlayer, position, zone):
        Card.__init__(self, idNumber, controllingPlayer, position, zone)
        self.idNumber = idNumber
        self.name = "Sen'jin Shieldmasta"
        self.type = "Minion"
        self.normalHealth = 5
        self.normalAttack = 3
        self.maxHealth = copy.copy(self.normalHealth)
        self.currentHealth = copy.copy(self.normalHealth)
        self.currentAttack = copy.copy(self.normalAttack)
        self.manaCost = 4

    def OnPlay(self, target=None):
        self.GainTaunt()

#Sheep
class CS2_tk1(Card):
    def __init__(self, idNumber, controllingPlayer, position, zone):
        Card.__init__(self, idNumber, controllingPlayer, position, zone)
        self.idNumber = idNumber
        self.name = "Sheep"
        self.type = "Minion"
        self.normalHealth = 1
        self.normalAttack = 1
        self.maxHealth = copy.copy(self.normalHealth)
        self.currentHealth = copy.copy(self.normalHealth)
        self.currentAttack = copy.copy(self.normalAttack)
        self.manaCost = 0
        self.tokenMinion = True

#Silver Hand Recruit
class CS2_101t(Card):
    def __init__(self, idNumber, controllingPlayer, position, zone):
        Card.__init__(self, idNumber, controllingPlayer, position, zone)
        self.idNumber = idNumber
        self.name = "Silver Hand Recruit"
        self.type = "Minion"
        self.normalHealth = 1
        self.normalAttack = 1
        self.maxHealth = copy.copy(self.normalHealth)
        self.currentHealth = copy.copy(self.normalHealth)
        self.currentAttack = copy.copy(self.normalAttack)
        self.manaCost = 1
        self.tokenMinion = True

#Stormpike Commando
class CS2_150(Card):
    def __init__(self, idNumber, controllingPlayer, position, zone):
        Card.__init__(self, idNumber, controllingPlayer, position, zone)
        self.idNumber = idNumber
        self.name = "Stormpike Commando"
        self.type = "Minion"
        self.normalHealth = 2
        self.normalAttack = 4
        self.maxHealth = copy.copy(self.normalHealth)
        self.currentHealth = copy.copy(self.normalHealth)
        self.currentAttack = copy.copy(self.normalAttack)
        self.manaCost = 5
        self.needsTarget = True
        self.effectCanHitHeroes = True
        self.effectCanHitMinions = True
        self.effectDamage = 2

    def OnPlay(self, target=None):
        if target != None:
            self.TargetWithEffect(target)
        else:
            self.controllingPlayer.cardWaitingForTarget = self

    def TargetWithEffect(self, target):
        if target != None:
            target.TakeDamage(2)
        self.controllingPlayer.cardWaitingForTarget = None

#Stormwind Champion
class CS2_222(Card):
    def __init__(self, idNumber, controllingPlayer, position, zone):
        Card.__init__(self, idNumber, controllingPlayer, position, zone)
        self.idNumber = idNumber
        self.name = "Stormwind Champion"
        self.type = "Minion"
        self.normalHealth = 6
        self.normalAttack = 6
        self.maxHealth = copy.copy(self.normalHealth)
        self.currentHealth = copy.copy(self.normalHealth)
        self.currentAttack = copy.copy(self.normalAttack)
        self.manaCost = 7
        self.hasAuraEffect = True
        self.aoeBuff = True

    def OnPlay(self, target=None):
        self.Aura()

    def Aura(self):
        for card in self.controllingPlayer.board:
            if card.type != "Hero" and card not in self.cardsAffectedByAura and card != self:
                card.BuffAttack(1)
                card.BuffHealth(1)
                self.cardsAffectedByAura.append(card)

    def RemoveFromPlay(self):
        self.controllingPlayer.board.remove(self)
        self.UndoAura()

    def UndoAura(self):
        for card in self.cardsAffectedByAura:
            card.DebuffAttack(1)
            card.DebuffHealth(1)

#Stormwind Knight
class CS2_131(Card):
    def __init__(self, idNumber, controllingPlayer, position, zone):
        Card.__init__(self, idNumber, controllingPlayer, position, zone)
        self.idNumber = idNumber
        self.name = "Stormwind Knight"
        self.type = "Minion"
        self.normalHealth = 5
        self.normalAttack = 2
        self.maxHealth = copy.copy(self.normalHealth)
        self.currentHealth = copy.copy(self.normalHealth)
        self.currentAttack = copy.copy(self.normalAttack)
        self.manaCost = 4

    def OnPlay(self, target=None):
        self.exhausted = False

#The Coin
class GAME_005(Card):
    def __init__(self, idNumber, controllingPlayer, position, zone):
        Card.__init__(self, idNumber, controllingPlayer, position, zone)
        self.idNumber = idNumber
        self.name = "The Coin"
        self.type = "Spell"
        self.manaCost = 0

    def OnPlay(self, target=None):
        self.controllingPlayer.currentFilledManaCrystals += 1

#Uther Lightbringer
class HERO_04(Card):
    def __init__(self, idNumber, controllingPlayer, position, zone):
        Card.__init__(self, idNumber, controllingPlayer, position, zone)
        self.idNumber = idNumber
        self.name = "Uther Lightbringer"
        self.type = "Hero"
        self.normalHealth = 30
        self.normalAttack = 0
        self.maxHealth = copy.copy(self.normalHealth)
        self.currentHealth = copy.copy(self.normalHealth)
        self.currentAttack = copy.copy(self.normalAttack)

#Stonetusk Boar
class CS2_171(Card):
    def __init__(self, idNumber, controllingPlayer, position, zone):
        Card.__init__(self, idNumber, controllingPlayer, position, zone)
        self.idNumber = idNumber
        self.name = "Stonetusk Boar"
        self.type = "Minion"
        self.normalHealth = 1
        self.normalAttack = 1
        self.maxHealth = copy.copy(self.normalHealth)
        self.currentHealth = copy.copy(self.normalHealth)
        self.currentAttack = copy.copy(self.normalAttack)
        self.manaCost = 1
        self.charge = True

    def OnPlay(self, target=None):
        self.exhausted = False

#Wolfrider
class CS2_124(Card):
    def __init__(self, idNumber, controllingPlayer, position, zone):
        Card.__init__(self, idNumber, controllingPlayer, position, zone)
        self.idNumber = idNumber
        self.name = "Wolfrider"
        self.type = "Minion"
        self.normalHealth = 1
        self.normalAttack = 3
        self.maxHealth = copy.copy(self.normalHealth)
        self.currentHealth = copy.copy(self.normalHealth)
        self.currentAttack = copy.copy(self.normalAttack)
        self.manaCost = 3
        self.charge = True

    def OnPlay(self, target=None):
        self.exhausted = False
