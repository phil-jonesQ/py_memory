import pygame
import sys
import itertools
import random
from MemoryCard import Card


# Initialise
suites = ['hearts', 'diamonds', 'spades', 'clubs']
values = ['ace', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten', 'jack', 'queen', 'king']

deck = [Card(value, suite) for value in values for suite in suites]

for i in range(52):
    print("Card is the ", deck[i].value, "Of ", deck[i].colour)


random.shuffle(deck)

for i in range(52):
    print("Card is the ", deck[i].value, "Of ", deck[i].colour)

#print(deck[0])
#count = 0
#for val, suit in deck:
    #count += 1
    #print('Counter %d The %s of %s' % (count, val, suit))


BLACK = (0, 0, 0)
WHITE = (200, 200, 200)
WINDOW_HEIGHT = 640
WINDOW_WIDTH = 640


def main():
    global SCREEN, CLOCK
    pygame.init()
    SCREEN = pygame.display.set_mode((WINDOW_HEIGHT, WINDOW_WIDTH))
    CLOCK = pygame.time.Clock()
    SCREEN.fill(BLACK)
    pygame.font.init()  # you have to call this at the start,
    # if you want to use this module.
    myfont = pygame.font.SysFont('Comic Sans MS', 10)

    while True:
        draw_grid()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()


def draw_grid():
    blockSize = 80 #Set the size of the grid block
    block_number = 0

    #print(deck)
    for x in range(WINDOW_WIDTH):
        for y in range(WINDOW_HEIGHT):
            rect = pygame.Rect(x*blockSize, y*blockSize,
                               blockSize, blockSize)
            pygame.draw.rect(SCREEN, WHITE, rect, 1)

            #text_string = deck[0][1]
            #print(text_string)
            #textsurface = myfont.render(text_string, False, (255, 255, 0))
            #SCREEN.blit(textsurface, (x * blockSize, y * blockSize))


main()
