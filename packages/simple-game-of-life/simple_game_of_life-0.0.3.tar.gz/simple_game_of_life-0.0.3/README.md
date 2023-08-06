# Game Of Life

Simple way to play Conway's game of life in python.<br>
You can import your own map as json file name "save.json", using `get_MAP` methode.<br>
All you custom maps (in the save.json file) are available in the list `custom_maps`.<br>
Two other custom maps are available : `my_map_1` and `my_map_2`.
<br>
<br>
NOTE : Two artificials borders are created for each map, 
The first one is visible while playing, it's in black
The second one is white (invisible) just after the black border, no cell can born here


## Installation

Run the following command to install:
```$ pip install simple-game-of-life ```

## Usage

for a random map
```python
from simple_game_of_life import GameOfLife
game = GameOfLife(50) 
game.start_animation()
```

for a custom map
```python
from simple_game_of_life import GameOfLife, maps
from random import choice
game = GameOfLife(custom_map=choice(maps))
game.start_animation()
```