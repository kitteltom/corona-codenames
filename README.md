# Corona codenames

Emulates the game [Codenames](https://de.wikipedia.org/wiki/Codenames) to play remotely with friends via video conference. 

The game was developed and testet with Python3.7 on MacOS. 

## How to start
After cloning this repository you can launch the game with

```bash
cd $PWD/src
python corona_codenames.py -f 20 -v 0 -c path/to/your/desired/cloud/folder
```

where `-f` sets the desired font size and therefore the size of the game-window, `-v` sets the current version of the game and `-c` sets the path to a folder that is synced with a cloud. 

For help on the command line arguments simply execute

```bash
cd $PWD/src
python corona_codenames.py --help
```

## How to play
Make sure you are familiar with the rules of the game [Codenames](https://de.wikipedia.org/wiki/Codenames). 

Assuming you are in a video conference together with some friends you can launch this script (see above) and share your screen. With the flag `-f` you can set the size of the game-window such that it fits properly to your screen and the others can see everything. 

### Cloud folder

The flag `-c` sets the path to a folder that is synced with a cloud. After executing the script this folder will contain the file `Farbzuordnung_v<version>.png`, where `<version>` is set with the flag `-v`. This file shows the color of each card on the game-window. Share this folder with the other players. The 'Geheimdienstchefs' in the current game should be the only ones viewing this file. 

### During the game

By simply pressing the 'Cards' you can log in whatever words the teams choose. After pressing a 'Card' you will immediately see its color. The program will automatically count how many blue and red 'Cards' are left and print a message as soon as the game is finished. 

### Used names
The program will keep track of names used in previous games. Those names will be saved to the file `dat/used_names.csv`. Names in this file will not be used in the next game. If you want to use all names, simply delete this file. 
