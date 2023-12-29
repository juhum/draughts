# Draughts

Draughts is a Python project that implements a draughts game with a graphical user interface and an artificial intelligence opponent.



## Installation
To get started with this project, clone this repository using git:

```bash
git clone https://github.com/juhum/draughts.git
```

To run the project, navigate to the draughts directory and install the necessary dependencies:

```bash
pip install -r requirements.txt
```
Then you can run the game:

```bash
python play.py
```

## Usage

Draughts is a two-player board game where each player has 12 pieces that can move and capture diagonally. The goal is to eliminate all the opponent's pieces or prevent them from moving. A piece becomes a king if it reaches the opposite end of the board, and can move and capture in any direction.



To play the game, click on a piece to select it, and then click on a valid square to move it. You can only move to empty squares. It is also possible to eliminate more than one of enemy pieces in a turn. 



It is possible to restart game by closing the window and clicking start game. 



## Features

- Graphical user interface powered by Pygame

- Artificial intelligence opponent using the minimax algorithm

- Sound effects

- Main menu and end-of-game menu


![showcase](https://github.com/juhum/draughts/blob/main/misc/showcase.gif)