from GameState import GameState
from AIPlayer import AIPlayer

#NOTE: THE AI COPYS THE GAME STATE AND PRINTS MOVES. IT DOES NOT PLAY THEM.
# IF THE GAME STATE IS PRINTED AGAIN AT THE END OF THIS FILE THERE WILL BE NO CHANGE.

gameState = GameState()
#Play Uther and hero power
gameState.opponentPlayer.PlayCard(0, 1, "HERO_04")
gameState.opponentPlayer.PlayCard(0, 54, "CS2_101")

#Play Jaina and hero power
gameState.friendlyPlayer.PlayCard(0, 2, "HERO_08")
gameState.friendlyPlayer.PlayCard(0, 55, "CS2_034")

#Opponent gets 10 mana
gameState.opponentPlayer.StartTurn()
gameState.opponentPlayer.StartTurn()
gameState.opponentPlayer.StartTurn()
gameState.opponentPlayer.StartTurn()
gameState.opponentPlayer.StartTurn()
gameState.opponentPlayer.StartTurn()
gameState.opponentPlayer.StartTurn()
gameState.opponentPlayer.StartTurn()
gameState.opponentPlayer.StartTurn()
gameState.opponentPlayer.StartTurn()

#Friendly gets 10 mana
gameState.friendlyPlayer.StartTurn()
gameState.friendlyPlayer.StartTurn()
gameState.friendlyPlayer.StartTurn()
gameState.friendlyPlayer.StartTurn()
gameState.friendlyPlayer.StartTurn()
gameState.friendlyPlayer.StartTurn()
gameState.friendlyPlayer.StartTurn()
gameState.friendlyPlayer.StartTurn()
gameState.friendlyPlayer.StartTurn()
gameState.friendlyPlayer.StartTurn()


#Bloodfen Raptor
gameState.friendlyPlayer.DrawCard(0, 4, "CS2_172")
#Nightblade
gameState.friendlyPlayer.DrawCard(0, 5, "EX1_593")
#Oasis Snapjaw
gameState.friendlyPlayer.DrawCard(0, 6, "CS2_119")
#Arcane Explosion
gameState.friendlyPlayer.DrawCard(0, 7, "CS2_025")
#Stormwind Champion
gameState.friendlyPlayer.DrawCard(0, 10, "CS2_222")
#Fireball
gameState.friendlyPlayer.DrawCard(0, 34, "CS2_029")
#play Bloodfen
gameState.friendlyPlayer.PlayCard(3, 4)
#Stormwind Champion
gameState.opponentPlayer.PlayCard(1, 8, "CS2_222")
gameState.opponentPlayer.PlayCard(3, 45, "CS1_042")
gameState.friendlyPlayer.StartTurn()
#play Stormwind Champion
gameState.friendlyPlayer.PlayCard(7, 10)
print gameState
gameState.phase = "Main Play"
gameState.friendlyPlayer.StartTurn()
#Arcan Explosion
gameState.friendlyPlayer.DrawCard(0, 24, "CS2_025")



