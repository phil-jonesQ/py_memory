""" Version 1.00 - simple version of the memory card game..
Set of standard playing cards

Numbered 1 - 52

Separated by suites

Laid out, face down on an invisble grid of 64 cells for Game Engine Design

Player clicks first and second choice

Cards are revealed - if they match they stay revealed

if they don't match they go back to hidden

the players click attempts are tracked

the game is over when all cards are revealed
Phil Jones - Jan 2021

Version 1.01 - Add Docstring
Version 1.02 - Add visual reveal after shuffle i.e. start or restart of game

"""


import pygame
import sys
import os
import random
from random import randint
from MemoryCard import Card


# Initialise Constants
suites = ['hearts', 'diamonds', 'spades', 'clubs']
values = ['ace', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten', 'jack', 'queen', 'king']

BLACK = (0, 0, 0)
WHITE = (200, 200, 200)
RED = (255, 0, 0)
WINDOW_HEIGHT = 700
WINDOW_WIDTH = 600
ROWS = 8
DECK_LIMIT = 52

cell_sz = WINDOW_HEIGHT // ROWS
surface_sz = ROWS * cell_sz

pygame.font.init()  # you have to call this at the start,
thefont = pygame.font.SysFont('Courier New', 20)

cards_to_images = {
                    'ace of clubs': 'AC.png',
                    'ace of diamonds': 'AD.png',
                    'ace of hearts': 'AH.png',
                    'ace of spades': 'AS.png',
                    'two of clubs': '2C.png',
                    'two of diamonds': '2D.png',
                    'two of hearts': '2H.png',
                    'two of spades': '2S.png',
                    'three of clubs': '3C.png',
                    'three of diamonds': '3D.png',
                    'three of hearts': '3H.png',
                    'three of spades': '3S.png',
                    'four of clubs': '4C.png',
                    'four of diamonds': '4D.png',
                    'four of hearts': '4H.png',
                    'four of spades': '4S.png',
                    'five of clubs': '5C.png',
                    'five of diamonds': '5D.png',
                    'five of hearts': '5H.png',
                    'five of spades': '5S.png',
                    'six of clubs': '6C.png',
                    'six of diamonds': '6D.png',
                    'six of hearts': '6H.png',
                    'six of spades': '6S.png',
                    'seven of clubs': '7C.png',
                    'seven of diamonds': '7D.png',
                    'seven of hearts': '7H.png',
                    'seven of spades': '7S.png',
                    'eight of clubs': '8C.png',
                    'eight of diamonds': '8D.png',
                    'eight of hearts': '8H.png',
                    'eight of spades': '8S.png',
                    'nine of clubs': '9C.png',
                    'nine of diamonds': '9D.png',
                    'nine of hearts': '9H.png',
                    'nine of spades': '9S.png',
                    'ten of clubs': '10C.png',
                    'ten of diamonds': '10D.png',
                    'ten of hearts': '10H.png',
                    'ten of spades': '10S.png',
                    'jack of clubs': 'JC.png',
                    'jack of diamonds': 'JD.png',
                    'jack of hearts': 'JH.png',
                    'jack of spades': 'JS.png',
                    'queen of clubs': 'QC.png',
                    'queen of diamonds': 'QD.png',
                    'queen of hearts': 'QH.png',
                    'queen of spades': 'QS.png',
                    'king of clubs': 'KC.png',
                    'king of diamonds': 'KD.png',
                    'king of hearts': 'KH.png',
                    'king of spades': 'KS.png',
                    'card background': 'red_back.png'
}

# Load Card Image set
# Store in a dictionary so we can map the image to name
card_images = {}
path = "assets/cards"
for name, file_name in cards_to_images.items():
    image = pygame.transform.scale(pygame.image.load(path + os.sep + file_name), (70, 90))
    card_images[name] = image


# Setup New Deck of Cards iterating and instantiating a deck of card objects
deck = [Card(value, suite) for value in values for suite in suites]

# Track the game state by storing each cell's card and if it's been revealed (True|False)
cell_tracker = {}
compare_tracker = {}
matched_cells_tracker = []


def shuffle():
    random.shuffle(deck)
    repeat = 20
    cell_state_initialise()
    update_grid()
    while repeat > 0:
        repeat -= 1
        cell_state_initialise()
        cell_state_reveal()
        update_grid()
        if repeat == 0:
            cell_state_initialise()
            update_grid()


def reset():
    cell_tracker.clear()
    compare_tracker.clear()
    matched_cells_tracker.clear()
    shuffle()
    update_grid()


def main():
    global SCREEN, CLOCK
    global TURNS
    global enabled
    global attempts
    TURNS = 2
    attempts = 0
    pygame.init()
    SCREEN = pygame.display.set_mode((surface_sz, surface_sz))
    CLOCK = pygame.time.Clock()
    shuffle()
    update_grid()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    attempts = 0
                    reset()
            if event.type == pygame.MOUSEBUTTONDOWN:
                enabled = True
                # Set the x, y positions of the mouse click
                x, y = event.pos
                # Translate x, y pos to grid coord
                clicked_col = (event.pos[0] // cell_sz) + 1
                clicked_row = (event.pos[1] // cell_sz) + 1
                # Translate col_row coord to a cell number
                cell_to_update = translate_row_cols_to_cell(clicked_col, clicked_row)
                # Check to see if the cell has already been matched
                # If it has set the enabled flag to false
                for check in range(len(matched_cells_tracker)):
                    if cell_to_update == matched_cells_tracker[check][0]:
                        enabled = False
                    if cell_to_update == matched_cells_tracker[check][1]:
                        enabled = False
                # Process the turns and check for matches
                if cell_to_update < DECK_LIMIT and enabled:
                    update_cell_state(cell_to_update)
                    update_cell_tracker(cell_to_update)
                    TURNS = TURNS - 1
                    update_grid()
                if TURNS < 1 < len(compare_tracker) and enabled:
                    TURNS = 2
                    check_for_pairs()
                    attempts += 1
                else:
                    TURNS = 1
        game_stats_display()


def game_stats_display():
    attempts_string = "ATTEMPTS " + str(attempts)
    matches_string = "MATCHES " + str((len(matched_cells_tracker)))
    message_string = "SPACE TO RESTART.."

    textsurface1 = thefont.render(attempts_string, False, (0, 255, 0))
    textsurface2 = thefont.render(matches_string, False, (0, 255, 0))
    textsurface3 = thefont.render(message_string, False, (255, 0, 0))

    SCREEN.blit(textsurface1, (WINDOW_WIDTH - 150, WINDOW_HEIGHT - 100))
    SCREEN.blit(textsurface2, (WINDOW_WIDTH - 150, WINDOW_HEIGHT - 150))
    SCREEN.blit(textsurface3, (WINDOW_WIDTH - 200, WINDOW_HEIGHT - 75))
    pygame.display.update()
    pygame.display.flip()


def translate_cell_to_coord(cell):
    coord = tuple((cell * cell_sz, cell * cell_sz))
    return coord


def translate_cell_to_row_cols(cell):
    counter = 0
    for ROW in range(ROWS):
        for COL in range(ROWS):
            if counter == cell:
                return tuple((COL, ROW))
            counter += 1
    return tuple((COL, ROW))


def translate_row_cols_to_cell(cols, rows):
    counter = -ROWS - 1
    for ROW in range(ROWS):
        for COL in range(ROWS):
            counter = counter + 1
            if ROW == rows and COL == cols - 1:
                return counter
    return counter


def cell_state_initialise():
    counter = 0
    repeat = 20
    while repeat > 0:
        repeat -= 1
        for ROW in range(ROWS):
            for COL in range(ROWS):
                if counter < DECK_LIMIT:
                    cell_tracker[counter] = (deck[counter].value, deck[counter].suite, False)
                counter += 1


def cell_state_reveal():
    counter = 0
    for ROW in range(ROWS):
        for COL in range(ROWS):
            for _ in range(ROWS):
                value = randint(0, DECK_LIMIT - 1)
            if counter < DECK_LIMIT:
                update_cell_state(value)
            counter += 1


def update_cell_state(target_cell):
    cell_tracker[target_cell] = (deck[target_cell].value, deck[target_cell].suite, True)


def update_cell_tracker(target_cell):
    compare_tracker[target_cell] = (deck[target_cell].value, deck[target_cell].suite, True)


def check_for_pairs():

    comp1 = list(compare_tracker.values())[0][0]
    comp2 = list(compare_tracker.values())[1][0]
    print(comp1, comp2)
    if comp1 == comp2:
        # Store a pairing in the matched_cells_tracker
        cell1 = list(compare_tracker.keys())[0]
        cell2 = list(compare_tracker.keys())[1]
        matched_cells_tracker.append(tuple((cell1, cell2)))
    else:
        for key in compare_tracker.keys():
            cell_tracker[key] = (deck[key].value, deck[key].suite, False)
    compare_tracker.clear()


def update_grid():
    SCREEN.fill(BLACK)
    counter = 0
    for ROW in range(ROWS):
        for COL in range(ROWS):
            counter += 1
            for key in cell_tracker.keys():
                if cell_tracker[key][2] is True and counter < DECK_LIMIT:
                    row_col = translate_cell_to_row_cols(key)
                    card = str(cell_tracker[key][0])
                    suite = str(cell_tracker[key][1])
                    card_key = card + " of " + suite
                    SCREEN.blit(card_images[card_key], (translate_cell_to_coord(row_col[0])[0] + 5, translate_cell_to_coord(row_col[1])[1] + 5))
                if cell_tracker[key][2] is False:
                    if key == counter - 1:
                        SCREEN.blit(card_images['card background'],
                                    ((translate_cell_to_coord(COL)[0]) + 5, (translate_cell_to_coord(ROW)[1]) + 5))
    pygame.display.update()
    pygame.display.flip()


main()

