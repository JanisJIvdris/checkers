import pygame
# tiek definētas vertibas: laukuma izmeri(garums,platums), rindu un kollonu skaits, un viena lauciņa izmērs 
WIDTH, HEIGHT = 800, 800            
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH//COLS

# tiek definētas izmantojamas rgb krasas
RED = (254, 57, 57)
WHITE = (255, 253, 208)
BLACK = (0, 0, 0)
BLUE = (153, 255, 255)
BROWN = (164,125,67)
CREAM = (252,242,216)


# tiek definets karala kaulina attels
CROWN = pygame.transform.scale(pygame.image.load('assets/king.png'),(60, 60))
