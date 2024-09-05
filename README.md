# Sokoban Game

Sokoban is a classic puzzle game where the player pushes boxes onto designated storage locations in a maze.
This version of Sokoban supports custom level creation, allowing users to design their own puzzles.

## Installation & Setup

1. Install the required dependencies:
   ```bash
   pip install pygame
   ```
2. Run the game:
    ```bash
    python main.py
    ```

## Controls
- **Arrow keys**: Move the player up, down, left, or right.
- **Space**: Restart the current level.
- **Backspace**: Undo the last move.
- **Esc**: Quit the level or level builder.

## How to Play
The goal of the game is to push all the boxes onto the storage locations.
The player can only push one box at a time and cannot pull boxes.
A box placed on a storage location is marked dark color to indicate success.

## Custom Levels
You can create your own levels by following the format used for level design:
- Design the maze layout with walls, boxes, storage locations, and the player starting position.
- Ensure the level is solvable by completing it before adding it to the game.