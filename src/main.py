# Copyright 2020-present, Thomas Kittel
# All rights reserved.

import tkinter as tk
import numpy as np
import random
from PIL import Image
import os

"""
Emulates the game 'Codenames' to play remotely with friends via skype. 
"""

# path to save the image for the intelligence chiefs
image_path = os.path.expanduser("~/Dropbox/CoronaCodenames/Farbzuordnung.png")

# board size
board_size = 5

# choose the double agent's team
RED = True
BLUE = False
double_agent = bool(random.getrandbits(1))

# number of cards to guess for each team
nr_red_agents = 8
nr_blue_agents = 8
nr_rubbernecks = 7
nr_murderers = 1
if double_agent is RED:
    nr_red_agents += 1
else:
    nr_blue_agents += 1

# set colors and their rgb-code
red = 'red3'
green = 'yellow green'
blue = 'navy'
black = 'black'
white = 'white'
grey = 'grey'
color_code = dict()
color_code[red] = np.asarray([200, 0, 0])
color_code[green] = np.asarray([154, 205, 50])
color_code[blue] = np.asarray([0, 0, 128])
color_code[black] = np.asarray([20, 20, 20])
color_code[white] = np.asarray([255, 255, 255])
color_code[grey] = np.asarray([240, 240, 240])


def add_colors(color_list, nr, color):
    """
    takes a list of color strings and appends 'nr' strings of 'color'

    :param color_list: list of color strings
    :param nr: nr to append
    :param color: color to append
    """
    for _ in range(nr):
        color_list.append(color)


# build the list of possible board colors
board_color_list = list()
add_colors(board_color_list, nr_red_agents, red)
add_colors(board_color_list, nr_blue_agents, blue)
add_colors(board_color_list, nr_rubbernecks, green)
add_colors(board_color_list, nr_murderers, black)

# shuffle the colors to get a random game board
random.shuffle(board_color_list)

# create a 5x5 array out of the board colors
board_color_array = np.asarray(board_color_list)
board_color_array = np.reshape(board_color_array, (board_size, board_size))

# create the image for the intelligence chiefs
board_color_image = np.zeros(shape=(500, 500, 3), dtype=np.uint8)
for row in range(board_color_image.shape[0]):
    for col in range(board_color_image.shape[1]):
        if row % 100 < 5 or row % 100 > 94:
            board_color_image[row, col] = color_code['grey']
        elif col % 100 < 5 or col % 100 > 94:
            board_color_image[row, col] = color_code['grey']
        else:
            board_color_image[row, col] = color_code[board_color_array[row // 100, col // 100]]
board_color_image = Image.fromarray(board_color_image, 'RGB')
board_color_image.save(image_path, 'PNG')

# create the list of words in the game
word_list = ["Hund", "Feuer", "Wald", "Clownfisch", "Tisch",
             "Turm", "Stahl", "Schwert", "Schinken", "Kirsche",
             "Sport", "Mirkoskop", "Handy", "Student", "Gras",
             "Gericht", "Amerika", "Hut", "Nachspeise", "Nuss",
             "Tulpe", "Kugel", "Spannung", "Mond", "Biologie"]
# word_list = list()
# for i in range(25):
#     word = 'word' + str(i+1)
#     word_list.append(word)

# shuffle the words to get a random game board
random.shuffle(word_list)

# create a 5x5 array out of the words
word_array = np.asarray(word_list)
word_array = np.reshape(word_array, (board_size, board_size))


class App:
    """
    builds the GUI for the game
    """

    def __init__(self, master):

        frame = tk.Frame(master)
        frame.pack()

        # padding
        self.padx = 2
        self.pady = 2

        # number of remaining red and blue cards
        self.red_cnt = nr_red_agents
        self.blue_cnt = nr_blue_agents
        self.game_over = False

        # buttons for the word-cards
        self.button_array = np.empty(shape=(board_size, board_size), dtype=tk.Button)
        for row in range(word_array.shape[0]):
            for col in range(word_array.shape[1]):
                self.button_array[row, col] = tk.Button(frame,
                                                        text=word_array[row, col],
                                                        width=16,
                                                        height=5,
                                                        fg=black,
                                                        highlightthickness=4,
                                                        font=("Courier", 12, 'bold'),
                                                        command=lambda r=row, c=col: self.callback(r, c))
                self.button_array[row, col].grid(row=row, column=col, padx=self.padx, pady=self.pady)

        # label for the remaining cards of team red
        self.red_label = tk.Label(frame,
                                  text='Rot: ' + str(self.red_cnt),
                                  fg=red,
                                  anchor='w',
                                  width=10,
                                  height=2,
                                  font=("Courier", 16, 'bold'))
        self.red_label.grid(row=5, column=0, padx=self.padx, pady=self.pady)

        # label for the remaining cards of team blue
        self.blue_label = tk.Label(frame,
                                  text='Blau: ' + str(self.blue_cnt),
                                  fg=blue,
                                  anchor='w',
                                  width=10,
                                  height=2,
                                  font=("Courier", 16, 'bold'))
        self.blue_label.grid(row=5, column=1, padx=self.padx, pady=self.pady)

        # label for game termination
        self.winner_label = tk.Label(frame,
                                     text='',
                                     fg=black,
                                     anchor='e',
                                     width=18,
                                     height=2,
                                     font=("Courier", 20, 'bold'))
        self.winner_label.grid(row=5, column=3, columnspan=2, padx=self.padx, pady=self.pady)

    def callback(self, row, col):
        """
        callback function for pressed buttons: button changes
        colors according to board_color_array + numbers for
        remaining cards are decreased

        :param row: row of the button pressed
        :param col: column of the button pressed
        """

        # get the button's underlying color
        current_color = board_color_array[row, col]

        # change button color (text and border)
        self.button_array[row, col].configure(fg=current_color,
                                              highlightbackground=current_color)

        # decrease the counts for the remaining cards
        if current_color == red:
            self.red_cnt -= 1
            self.red_label.configure(text='Rot: ' + str(self.red_cnt))
            if self.red_cnt == 0 and not self.game_over:
                self.winner_label.configure(text='Rot gewinnt! :) ')
                self.game_over = True
        elif current_color == blue:
            self.blue_cnt -= 1
            self.blue_label.configure(text='Blau: ' + str(self.blue_cnt))
            if self.blue_cnt == 0 and not self.game_over:
                self.winner_label.configure(text='Blau gewinnt! :) ')
                self.game_over = True
        elif current_color == black and not self.game_over:
            self.winner_label.configure(text='TOD!!! ')
            self.game_over = True


# sets up the GUI
root = tk.Tk()
root.title("CoronaCodenames")
app = App(root)
root.mainloop()
