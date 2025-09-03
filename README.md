# DinoGame(T-Rex Runner)
T-Rex Runner is a simple, yet engaging, 2D endless runner game built with Python and the Pygame library. This project is a recreation of the popular Google Chrome offline game, complete with a state-based game loop, persistent high scores, and player management features.
## Features
- Classic Gameplay: Jump and duck to avoid obstacles in an endless runner format.
- State-Based Game Loop: The game transitions between a start menu, active gameplay, a game over screen, and high scores.
- Player & Score Management: Players can enter their name and save their high scores.
- Persistent High Scores: High scores are stored in a local SQLite database, so they are saved between sessions.
- CRUD Functionality: You can manage high score data directly from the game, with options to:
- Create: A new score is created at the end of each game.
- Read: High scores are displayed on the main menu.
- Update: You can click on a player's name in the high score list to update their name.
- Delete: You can also delete a player's score and record from the database.
# Getting Started
## Clone The Repository
    -git clone https://github.com/EdwardSnug/DinoGame.git
    -cd DinoGame
## Install dependencies
    -pip install pygame
## Getting started
Simply execute the main python script from your terminal within the DinoGame working repository
    -python src/main.py
## Controls
- Up Arrow or Spacebar: Jump
- Down Arrow: Duck
- Enter: Confirm name on the main menu.
- Escape: Access the options menu from the main screen.
- Mouse Click: Interact with buttons on the options and high scores screens.
## Project Structure
- main.py: The main game loop and logic, including the state machine.
- dino.py: Contains the Dinosaur class, which handles the player character's movement and animation.
- obstacles.py: Contains the Obstacle class for managing the obstacles the player must avoid.
- scores_db.py: Manages the SQLite database for high scores, with functions for saving, retrieving, deleting, and updating player data.
- scores.db: (Generated automatically) The database file that stores all the high scores.
## Contributing
Fell free to fork the repository and submit all pull requests. All contributions are welcome!
## License
This project is licensed under the MIT License