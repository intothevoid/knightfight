# Knight Fight

> "Join the battle as a valiant knight, outsmart your opponent, and capture the enemy's king in this strategic and knightly game of Knight Fight Chess."

<img src="https://raw.githubusercontent.com/intothevoid/knightfight/main/assets/images/title_screen.png" width="70%" height="70%"></img>

Play chess on a pixelated retro board. Play against a CPU player or another friend.

<img src="https://raw.githubusercontent.com/intothevoid/knightfight/main/assets/images/sshot.png" width="70%" height="70%"></img>

<img src="https://raw.githubusercontent.com/intothevoid/knightfight/main/assets/images/sshot_go.png" width="70%" height="70%"></img>

<img src="https://raw.githubusercontent.com/intothevoid/knightfight/main/assets/images/sshot_settings.png" width="70%" height="70%"></img>

Grid lines and positions overlay (configurable)

<img src="https://raw.githubusercontent.com/intothevoid/knightfight/main/assets/images/sshot_debug.png" width="70%" height="70%"></img>


## Features
1. Multiple modes - Human v Human, CPU v Human, CPU vs CPU 
2. Follows standard Chess rules (Now powered by python-chess)
3. Retro sound effects and music!
4. Lots of configurable options
5. Debug mode to highlight positions and grid
6. Undo last move (press Ctrl+Z)
7. Change board styles
8. Multiplayer - coming soon!
9. Animated CPU piece moves
10. Retro title menu with options to save and load games
11. Smarter CPU player with multiple chess engines supported:
    - Stockfish
    - Piece Squares (Uses minimax algorithm)
    - Piece Squares v2 (Uses minimax algorithm) - Default
    - Basic Random Moves
12. Show possible moves for selected piece, and last move made

## Installation

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Usage

```bash
python3 main.py
```

## Optional - Install Stockfish (Powerful Chess Engine)

If you would like to play against a stronger CPU player, you can install Stockfish. Stockfish is a free, open source chess engine. It is the strongest chess engine in the world. 

1. Go to https://stockfishchess.org/download/ and download your version of the Stockfish chess engine
2. Copy the binary to assets/engines/stockfish (assets\engines\stockfish.exe for Windows)
3. Update the path in config.yml as shown below

### config.yml - Windows
```
cpu:
    stockfish_path: assets/engines/stockfish.exe
```

### config.yml - MacOS / Linux
```
cpu:
    stockfish_path: assets/engines/stockfish
```

## Powered By

<img src="https://raw.githubusercontent.com/intothevoid/knightfight/main/assets/images/pygame.png" height="25%" width="25%"></img>

PyGame https://www.pygame.org/

<img src="https://raw.githubusercontent.com/intothevoid/knightfight/main/assets/images/stockfish.png" height="25%" width="25%"></img>

Stockfish https://github.com/official-stockfish/Stockfish

Stockfish GPL 3.0 License - See https://github.com/official-stockfish/Stockfish/blob/master/Copying.txt

Stockfish Source Code - https://github.com/official-stockfish/Stockfish/tree/master/src

Dani Maccari's image assets https://dani-maccari.itch.io/

Music assets by wyver https://wyver9.itch.io/8-bit-beatem-up-soundtrack

Midjourney - Knight Fight Splash Image https://midjourney.com/

python-chess - https://python-chess.readthedocs.io/en/latest/

Simplified Evaluation Function - https://www.chessprogramming.org/Simplified_Evaluation_Function 
