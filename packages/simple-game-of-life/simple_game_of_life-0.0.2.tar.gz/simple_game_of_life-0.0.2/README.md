# Game Of Life

Simple way to play Conway's game of life in python.
You can import your own map as json file name "save.json", using `get_MAP` methode
All you custom maps (in the save.json file) are available in the list `custom_maps`
Two other custom maps are available : `my_map_1` and `my_map_2`

## Installation

Run the following command to install:
``` pip install simple-game-of-life ```

## Usage

```python
from simple_game_of_life import GameOfLife
game = GameOfLife(50) 
game.start_animation()
```

```python
from simple_game_of_life import GameOfLife, maps
from random import choice
game = GameOfLife(custom_map=choice(maps))
game.start_animation()
```