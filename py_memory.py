import pygame
import sys
import itertools
import random
from MemoryCard import Card


# Initialise
suites = ['hearts', 'diamonds', 'spades', 'clubs']
values = ['ace', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten', 'jack', 'queen', 'king']

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
        update_cell_state(25)
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
