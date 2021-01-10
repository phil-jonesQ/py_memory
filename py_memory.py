import pygame
import sys
import itertools
import random
from MemoryCard import Card


# Initialise
suites = ['hearts', 'diamonds', 'spades', 'clubs']
values = ['ace', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten', 'jack', 'queen', 'king']

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
                    'queen of clubs': 'KC.png',
                    'queen of diamonds': 'KD.png',
                    'queen of hearts': 'KH.png',
                    'queen of spades': 'KS.png',
                    'king of clubs': 'KC.png',
                    'king of diamonds': 'KD.png',
                    'king of hearts': 'KH.png',
                    'king of spades': 'KS.png'
}

deck = [Card(value, suite) for value in values for suite in suites]
random.shuffle(deck)

cell_tracker = {}

BLACK = (0, 0, 0)
WHITE = (200, 200, 200)
RED = (255, 0, 0)
WINDOW_HEIGHT = 640
WINDOW_WIDTH = 640
SCALE = 30
ROWS = 8
DECK_LIMIT = 52

cell_sz = WINDOW_HEIGHT // ROWS
surface_sz = ROWS * cell_sz

pygame.font.init()  # you have to call this at the start,
myfont = pygame.font.SysFont('Comic Sans MS', 15)


def main():
    global SCREEN, CLOCK
    pygame.init()
    SCREEN = pygame.display.set_mode((surface_sz, surface_sz))
    CLOCK = pygame.time.Clock()
    SCREEN.fill(BLACK)
    draw_grid()
    cell_state_initialise()
    print(cell_tracker)

    while True:
        draw_grid()
        update_grid()
        update_cell_state(0)
        update_cell_state(14)
        update_cell_state(51)
        #cell_state_updater()
        #print(cell_tracker)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
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


def cell_state_initialise():
    counter = 0
    for ROW in range(ROWS):
        for COL in range(ROWS):
            if counter < DECK_LIMIT:
                cell_tracker[counter] = (deck[counter].value, deck[counter].suite, False)
            counter += 1


def update_cell_state(target_cell):
    cell_tracker[target_cell] = (deck[target_cell].value, deck[target_cell].suite, True)


def update_grid():
    counter = 0
    for ROW in range(ROWS):
        for COL in range(ROWS):
            counter += 1
            for key in cell_tracker.keys():
                #print(key, cell_tracker[key][1], cell_tracker[key][2])
                if cell_tracker[key][2] is True and counter < DECK_LIMIT:
                    #print(COL, ROW, key, counter, cell_tracker[key][0], cell_tracker[key][1], cell_tracker[key][2])
                    row_col = translate_cell_to_row_cols(key)
                    text_string1 = cell_tracker[key][0]
                    text_string2 = "of"
                    text_string3 = cell_tracker[key][1]
                    textsurface1 = myfont.render(text_string1, False, (0, 255, 0))
                    textsurface2 = myfont.render(text_string2, False, (0, 255, 0))
                    textsurface3 = myfont.render(text_string3, False, (0, 255, 0))
                    SCREEN.blit(textsurface1,
                                ((translate_cell_to_coord(row_col[0])[0]) + 10, (translate_cell_to_coord(row_col[1])[1]) + 10))
                    SCREEN.blit(textsurface2,
                                ((translate_cell_to_coord(row_col[0])[0]) + 10, (translate_cell_to_coord(row_col[1])[1]) + 25))
                    SCREEN.blit(textsurface3,
                                ((translate_cell_to_coord(row_col[0])[0]) + 10, (translate_cell_to_coord(row_col[1])[1]) + 40))
                if cell_tracker[key][2] is False:
                    if key == counter - 1:
                        text_string = str(counter)
                    else:
                        text_string = ""
                    textsurface = myfont.render(text_string, False, (255, 0, 0))
                    SCREEN.blit(textsurface,
                                ((translate_cell_to_coord(COL)[0]) + 10, (translate_cell_to_coord(ROW)[1]) + 10))
                else:
                    text_string = ""
                    textsurface = myfont.render(text_string, False, (255, 0, 0))
                    SCREEN.blit(textsurface,
                                ((translate_cell_to_coord(COL)[0]) + 10, (translate_cell_to_coord(ROW)[1]) + 10))


def draw_grid():
    SCREEN.fill(BLACK)
    for ROW in range(ROWS):
        for COL in range(ROWS):
            rect = pygame.Rect(COL*cell_sz, ROW*cell_sz,
                               cell_sz, cell_sz)
            pygame.draw.rect(SCREEN, WHITE, rect, 1)


main()
