# pythoban

just another sokoban clone, written in python.

Find more information about it here: http://www.sokobano.de/wiki/index.php?title=Main_Page

## how to run the game

open main game folder in console and run main.py file:
```
python main.py
```

Pythoban is working both with Python 2.7 and 3.x, except for the level solver (see details below)

## main menu

After running a game, you will see a menu with following options:

* ```NEW GAME``` runs new game
* ```LOAD GAME``` (not working at the moment. see below for details about loading level files.)
* ```OPTIONS``` (not working at the moment)
* ```EXIT``` exits the game

You can use both keyboard and mouse to navigate!

## how to play

After selecting ```NEW GAME``` in main menu, the first level will be loaded. From now on, you can use following keys to navigate:

* ```Arrow keys``` to move the player
* ```WSAD keys``` to move the camera (very useful on bigger maps)
* ```N / B keys``` to load next / previous level in current file
* ```ESC / BACKSPACE keys``` to restart current level
* ```C key``` to use level solver and see the best solution. check more details below.

You will see count of your steps and current level number in the bottom left corner of the screen.

## how to load different level file

Firstly make sure that your level file meets the requirements you will find here: http://www.sokobano.de/wiki/index.php?title=Level_format 

If so, put it in the /assets/ folder. Then edit ```MAP_FILE``` value on top of ```game.py``` file, putting full maps filename (with file extension):

```python
MAPS_FILE = "starPusherLevels.txt"
```

It will be replaced with proper window prompt...

## How to check the map solution

While playing the game, you are able to check the level solution by using ```C key```. Level solver will try to find most optimal solution for the current level and will display it on the bottom of the screen, right after steps counter.

Warning 1: It may take a while, depending on your processor. Also longer solutions will probably not fit on the sreen, so they will be also printed on console.

Warning 2: Although the game itself is working both with Python 2.7 and 3.x, the level solver operates with 2.7 only. I hope solving this issue some day.
