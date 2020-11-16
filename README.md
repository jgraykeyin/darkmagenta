# Dark Magenta PyGame Challenge Project

![Screenshot](https://github.com/jgraykeyin/darkmagenta/blob/main/images/screenshot.png)

This is a local two-player game where both players compete to collect
mushrooms that will be used to craft an exit-door to win the round.
Players can also win a round if the opponent loses all their health
from touching poison mushrooms. Players must craft two 'Exit Orbs' before
they can craft the final 'Exit Door'. HP and Speed bonuses can also be
crafted. All crafting must be done at the 'Camp Fire' which players must
battle for control.

Crafting chart:
Mushroom A x5: Heart (+1 HP)
Mushroom A x10: Exit Orb
Mushroom B x5: Speed Bonus (Speed x2 for 30 seconds)
Mushroom B x10: Exit Orb
Mushroom C x5: Spore Magic Spell (Turns most mushrooms into poison)
Mushroom C x10: Exit Door

When a player uses the 'Exit Door' they win the match and receive 5 points.
When a player loses from poison (0 HP) their opponent receives 1 point. 
After a match ends, the scores are saved and a new round can begin.

Pygame must be installed for the progrqma to run:
pip3 install pygame  or  python3 -m install pygame

The game can then be started using the 2player.py program:
python3 2player.py

The official game manual can be found in the game's directory under the
filename game_manual.pdf.

Player 1 is controlled using: A,W,S,D for movement and 1,2,3 for crafting.
Player 2 is controlled using: Left,Up,Down,Right for movement and 8,9,0 for crafting.

scorePoint(player,points):
- Description: Add points to P1 or P2
- Parameters:
    player - "p1" or "p2"
    points - amount of points to add
Returns: Nothing

generateMap():
- Description: Generates a tiled map at the start of a round
- Parameters: None
- Returns:
    List of tile numbers

resetInventory():
- Description: Initializes the inventory for the beginning of a match
- Parameters: None
- Returns:
    List of inventory items

craft_message(msg):
- Descriptio: Displays a message on the screen during gameplay
- Parameters:
    msg - Message that will be displayed as a string
- Returns: Nothing

spore_magic(tile_map):
- Description: Checks every mushroom on the board with a chance of changing it to a poison mushroom
- Parameters:
    tile_map - Tilemap to check, should be the game's current map
- Returns: Nothing

main_menu():
- Description: Main menu that will display a graphic and wait for the user to start the game
- Parameters: None
- Returns: Nothing

game_over():
- Description: End-game screen that displays the score and waits for the user to play again or quit the program
- Parameters: None
- Returns: Nothing

game_loop():
- Description: The main gameplay loop that initializes many of our settings and loads the generated tilemap. 
             We then check for keyboard events to move the characters on the screen.
- Parameters: None
- Returns: Nothing

Further extensions will be adding controller support for both players once hardware
can be acquired for testing. 


