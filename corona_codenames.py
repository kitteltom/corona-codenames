# Copyright 2020-present, Thomas Kittel
# All rights reserved.

import tkinter as tk
import numpy as np
import random
from PIL import Image
import os
import csv
import argparse

"""
Emulates the game 'Codenames' to play remotely with friends via video
conference.
"""

# parser for command line arguments
parser = argparse.ArgumentParser()
parser.add_argument('-f', '--font_size', type=int, default=20,
                    help='Font size of the words in the game. Change to make'
                         'game better visible for other players. Note: This'
                         'also changes the overall size of the game window.')
parser.add_argument('-d', '--data_path', default='dat',
                    help='Path to the csv-file where the available words for'
                         'the game are saved.')
parser.add_argument('-c', '--cloud_path', default='~/Dropbox/CoronaCodenames',
                    help='Path to save the image for the intelligence chiefs.'
                         'Ideally this is a synced cloud folder, which can be'
                         'shared with other players.')
parser.add_argument('-v', '--version', type=int, default=0,
                    help='Version number in the naming of the image for the'
                         'intelligence chiefs. Helpful when playing several'
                         'rounds in a row.')

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


def launch_game(args):
    # read the arguments
    font_size = args.font_size
    data_path = os.path.expanduser(args.data_path)
    codenames_path = os.path.join(data_path, 'codenames.csv')
    used_names_path = os.path.join(data_path, 'used_names.csv')
    image_path = os.path.expanduser(args.cloud_path)
    image_path = os.path.join(
        image_path,
        'Farbzuordnung_v%d.png' % args.version
        )

    # size of the game (number of cards in a row/column)
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
    if double_agent == RED:
        nr_red_agents += 1
    elif double_agent == BLUE:
        nr_blue_agents += 1

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
    board_color_image = np.zeros(
        shape=(board_size*100, board_size*100, 3),
        dtype=np.uint8
        )
    for row in range(board_color_image.shape[0]):
        for col in range(board_color_image.shape[1]):
            if row % 100 < 5 or row % 100 > 94:
                board_color_image[row, col] = color_code['grey']
            elif col % 100 < 5 or col % 100 > 94:
                board_color_image[row, col] = color_code['grey']
            else:
                board_color_image[row, col] = color_code[
                    board_color_array[row // 100, col // 100]
                    ]
    board_color_image = Image.fromarray(board_color_image, 'RGB')
    board_color_image.save(image_path, 'PNG')

    # read all names from file
    word_list = read_words(codenames_path)

    # find length of the longest word
    # longest = 0
    # for word in word_list:
    #     if len(word) > longest:
    #         longest = len(word)
    # print(longest)

    # read all previously used names
    used_word_list = []
    if os.path.isfile(used_names_path):
        used_word_list = read_words(used_names_path)
    if len(word_list) - len(used_word_list) < board_size * board_size:
        used_word_list = []

    # delete already used words from word list
    for used_word in used_word_list:
        word_list.remove(used_word)

    # shuffle the words to get a random game board
    random.shuffle(word_list)

    # take the first 25 words only
    word_list = word_list[:board_size*board_size]
    used_word_list += word_list

    # add words to used words
    with open(used_names_path, 'w') as file:
        writer = csv.writer(file, delimiter=';')

        # write the header
        writer.writerow(['Nr', 'Name'])
        for i, word in enumerate(used_word_list):
            writer.writerow([str(i + 1), word])

    # create a 5x5 array out of the words
    word_array = np.asarray(word_list)
    word_array = np.reshape(word_array, (board_size, board_size))

    # sets up the GUI
    root = tk.Tk()
    root.title("CoronaCodenames")
    App(
        root,
        font_size,
        board_size,
        nr_red_agents,
        nr_blue_agents,
        word_array,
        board_color_array
        )
    root.mainloop()


def add_colors(color_list, nr, color):
    """
    takes a list of color strings and appends 'nr' strings of 'color'

    :param color_list: list of color strings
    :param nr: nr to append
    :param color: color to append
    """
    for _ in range(nr):
        color_list.append(color)


def read_words(csv_path):
    word_list = []
    with open(csv_path, 'r') as file:
        reader = csv.reader(file, delimiter=';')

        # skip the header
        next(reader)
        for row in reader:
            word_list.append(row[1])

    return word_list


class App:
    """
    builds the GUI for the game
    """

    def __init__(self, master, font_size, board_size, nr_red_agents,
                 nr_blue_agents, word_array, board_color_array):

        frame = tk.Frame(master)
        frame.pack()

        # padding
        self.padx = 2
        self.pady = 2
        self.font_size = font_size

        # number of remaining red and blue cards
        self.red_cnt = nr_red_agents
        self.blue_cnt = nr_blue_agents
        self.game_over = False

        # buttons for the word-cards
        self.button_array = np.empty(
            shape=(board_size, board_size),
            dtype=tk.Button
            )
        for row in range(word_array.shape[0]):
            for col in range(word_array.shape[1]):
                self.button_array[row, col] = tk.Button(
                    frame,
                    text=word_array[row, col],
                    width=14,
                    height=5,
                    fg=black,
                    highlightthickness=4,
                    font=("Courier", self.font_size, 'bold'),
                    command=lambda r=row, c=col: self.callback(
                        r,
                        c,
                        board_color_array
                        )
                    )
                self.button_array[row, col].grid(
                    row=row,
                    column=col,
                    padx=self.padx,
                    pady=self.pady
                    )

        # label for the remaining cards of team red
        self.red_label = tk.Label(
            frame,
            text='ROT: ' + str(self.red_cnt),
            fg=red,
            anchor='w',
            width=12,
            height=2,
            font=("Courier", self.font_size, 'bold')
            )
        self.red_label.grid(
            row=board_size,
            column=0,
            padx=self.padx,
            pady=self.pady
            )

        # label for the remaining cards of team blue
        self.blue_label = tk.Label(
            frame,
            text='BLAU: ' + str(self.blue_cnt),
            fg=blue,
            anchor='w',
            width=12,
            height=2,
            font=("Courier", self.font_size, 'bold')
            )
        self.blue_label.grid(
            row=board_size,
            column=1,
            padx=self.padx,
            pady=self.pady
            )

        # label for game termination
        self.winner_label = tk.Label(
            frame,
            text='',
            fg=black,
            anchor='e',
            width=24,
            height=2,
            font=("Courier", self.font_size, 'bold')
            )
        self.winner_label.grid(
            row=board_size,
            column=board_size-2,
            columnspan=2,
            padx=self.padx,
            pady=self.pady
            )

    def callback(self, row, col, board_color_array):
        """
        callback function for pressed buttons: button changes
        colors according to board_color_array + numbers for
        remaining cards are decreased

        :param row: row of the button pressed
        :param col: column of the button pressed
        :param board_color_array: the color for each field
        """

        # get the button's underlying color
        current_color = board_color_array[row, col]

        # change button color (text and border)
        self.button_array[row, col].configure(
            fg=current_color,
            highlightbackground=current_color
            )

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
            self.winner_label.configure(text='TOT!!! ')
            self.game_over = True


if __name__ == '__main__':
    launch_game(parser.parse_args())
