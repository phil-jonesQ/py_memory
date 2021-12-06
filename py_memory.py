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
Version 1.03 - Convert to kids game using new asset set

"""


import pygame
import sys
import os
import random
from random import randint
from MemoryCard import Card


# Initialise Constants
suites = ['set1', 'set2']
values = ['cheese', 'cheese_burger', 'cherry', 'chilly', 'flame', 'hot_dog', 'ketchup', 'marsh_m_blue', 'marsh_m_pink', 'sausage']

BLACK = (0, 0, 0)
WHITE = (200, 200, 200)
RED = (255, 0, 0)
WINDOW_HEIGHT = 600
WINDOW_WIDTH = 600
ROWS = 6
DECK_LIMIT = 20

cell_sz = WINDOW_HEIGHT // ROWS
surface_sz = ROWS * cell_sz

pygame.font.init()  # you have to call this at the start,
thefont = pygame.font.SysFont('Courier New', 20)
thefont_larger = pygame.font.SysFont('Courier New', 40)
thefont_small = pygame.font.SysFont('Courier New', 12)

cards_to_images = {
                    'cheese of set1': 'cheese.png',
                    'cheese of set2': 'cheese_set2.png',
                    'cheese_burger of set1': 'cheese_burger.png',
                    'cheese_burger of set2': 'cheese_burger_set2.png',
                    'cherry of set1': 'cherry.png',
                    'cherry of set2': 'cherry_set2.png',
                    'chilly of set1': 'chilly.png',
                    'chilly of set2': 'chilly_set2.png',
                    'flame of set1': 'flame.png',
                    'flame of set2': 'flame_set2.png',
                    'hot_dog of set1': 'hot_dog.png',
                    'hot_dog of set2': 'hot_dog_set2.png',
                    'ketchup of set1': 'ketchup.png',
                    'ketchup of set2': 'ketchup_set2.png',
                    'marsh_m_blue of set1': 'marsh_m_blue.png',
                    'marsh_m_blue of set2': 'marsh_m_blue_set2.png',
                    'marsh_m_pink of set1': 'marsh_m_pink.png',
                    'marsh_m_pink of set2': 'marsh_m_pink_set2.png',
                    'sausage of set1': 'sausage.png',
                    'sausage of set2': 'sausage_set2.png',
                    'card background': 'card_background.png'
}

# Load Card Image set
# Store in a dictionary so we can map the image to name
card_images = {}
path = "assets/shapes"
for name, file_name in cards_to_images.items():
    image = pygame.transform.scale(pygame.image.load(path + os.sep + file_name), (80, 80))
    card_images[name] = image


# Setup New Deck of Cards iterating and instantiating a deck of card objects
deck = [Card(value, suite) for value in values for suite in suites]

# Track the game state by storing each cell's card and if it's been revealed (True|False)
cell_tracker = {}
compare_tracker = {}
matched_cells_tracker = []


def shuffle():
    random.shuffle(deck)
    repeat = 10
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
    global timer, attempts, ms, timer_run
    timer = 0
    attempts = 0
    ms = 0
    timer_run = True
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
    global timer
    global ms
    global timer_run
    TURNS = 2
    attempts = 0
    timer = 0
    ms = 0
    timer_run = True
    pygame.init()
    SCREEN = pygame.display.set_mode((surface_sz, surface_sz))
    CLOCK = pygame.time.Clock()
    FPS = 60
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

        CLOCK.tick(FPS)
        
        # Timer - floor it at 1000 seconds to avoid display issues
        ms += CLOCK.tick_busy_loop(60)
        if ms > 1000 and timer_run:
            timer += 1
            ms = 0
        if timer > 1000:
            timer = 1000

        # Check when player has one and freeze the timer
        if len(matched_cells_tracker) == (DECK_LIMIT / 2):
            timer_run = False

        game_stats_display()
        


def game_stats_display():
    global timer
    # Clear the timer area before drawing the HUD display items
    pygame.draw.rect(SCREEN, [0, 0, 0], [WINDOW_WIDTH // 4, WINDOW_HEIGHT - 120, 100, 100], 0)
    attempts_string = "ATTEMPTS " + str(attempts)
    matches_string = "MATCHES " + str((len(matched_cells_tracker)))
    message_string = "SPACE TO RESTART.."
    timer_string = str(timer)

    textsurface1 = thefont.render(attempts_string, False, (255, 0, 0))
    textsurface2 = thefont.render(matches_string, False, (0, 255, 0))
    textsurface3 = thefont.render(message_string, False, (255, 0, 0))
    textsurface4 = thefont_larger.render(timer_string, False, (255, 255, 255))

    SCREEN.blit(textsurface1, (WINDOW_WIDTH // 2, WINDOW_HEIGHT - 280))
    SCREEN.blit(textsurface2, (WINDOW_WIDTH // 2, WINDOW_HEIGHT - 220))
    SCREEN.blit(textsurface3, (WINDOW_WIDTH - 240, WINDOW_HEIGHT - 30))
    SCREEN.blit(textsurface4, (WINDOW_WIDTH // 4, WINDOW_HEIGHT - 120))
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
                    SCREEN.blit(card_images[card_key], (translate_cell_to_coord(row_col[0])[0] + 15, translate_cell_to_coord(row_col[1])[1] + 15))
                if cell_tracker[key][2] is False:
                    if key == counter - 1:
                        SCREEN.blit(card_images['card background'],
                                    ((translate_cell_to_coord(COL)[0]) + 12, (translate_cell_to_coord(ROW)[1]) + 15))
    
    # Add UI indicator when the cell was matched
    for ROW in range(ROWS):
        for COL in range(ROWS):
            match_counter = 0
            for matches in matched_cells_tracker:
                match_counter += 1
                row_col_1 = translate_cell_to_row_cols(matches[0])
                row_col_2 = translate_cell_to_row_cols(matches[1])
                matches_string = str(match_counter)
                text_surface = thefont_small.render(matches_string, False, (0, 255, 0))
                SCREEN.blit(text_surface, (translate_cell_to_coord(row_col_1[0])[0] + 2, translate_cell_to_coord(row_col_1[1])[1] + 15))
                SCREEN.blit(text_surface, (translate_cell_to_coord(row_col_2[0])[0] + 2, translate_cell_to_coord(row_col_2[1])[1] + 15))


    pygame.display.update()
    pygame.display.flip()


main()

