import pygame     
import tkinter                                                   
from checkers.constants import WIDTH, HEIGHT, SQUARE_SIZE, RED, WHITE  #tiek importētas konstantes
from checkers.game import Game                                         #tiek importēts game package no game.py
from minimax.algorithm import minimax                                  # tiek importēts minimax algoritms no  algorithm.py
import tkinter.messagebox                                      #tiek importēts messege box


FPS = 60   #

# tiek izvadits logs un tam pieskirts apraksts
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))              #no constants.py tiek importets loga izmers
pygame.display.set_caption('Checkers by Janis Jekabs Ivdris, 191RDB248')


def get_row_col_from_mouse(pos):   # pec peles atrasanas vietas izvada row un col
    x, y = pos
    row = y // SQUARE_SIZE  
    col = x // SQUARE_SIZE
    return row, col

# main

def main():
    #run = True
    clock = pygame.time.Clock()     #nodrošina ka galvenais event loop nenotiek parak atri vai leni
    game = Game(WINDOW)             # padod speles logu

    #izvele kurs uzsak speli

    answer = tkinter.messagebox.askquestion('It is time to play some checkers!','Do you want to go first?') #tiek izvadīts messegebox ar jautajumu
    if answer == 'yes':                   #ja atbilde ir ja, spele tiek palaista
     run = True
    else:
     answer == 'no'                  #ja atbilde ir ne
     run = True                 #spele tiek palaista un tiek izlaista karta
     game.change_turn()        #tiek izlaista karta, lai dators varetu veikt pirmo soli

    while run:       #main event loop
        clock.tick(FPS)
        
        if game.turn == WHITE:
            value, new_board = minimax(game.get_board(), 2, WHITE, game)
            game.ai_move(new_board)

        if game.winner() != None: # ja spelei ir uzvaretajs
            print(game.winner())   # izvadit uzvaretaju
            tkinter.messagebox.showinfo('Its DaBabby!','Game over!')  #palaist pazinojumu

            answer = tkinter.messagebox.askquestion('Game Over','Do you want to play again?')  # uzdot vai velas atkartot speli
            if answer == 'yes':
                main()
                run = True
            else:
                answer == 'no'
                run = False


        for event in pygame.event.get():   #parbauda vai kadi notikumi ir notikuši
            if event.type == pygame.QUIT:    #ja ir noticis notikums- iziet no speles
                run = False                  # speles darbiba tiek partraukta, tiek partraukts loop
            
            if event.type == pygame.MOUSEBUTTONDOWN:    #ja ir noticis notikums, uzspiest uz peles taustiņa
                pos = pygame.mouse.get_pos()          # nolasa peles atrasanas vietu
                row, col = get_row_col_from_mouse(pos)   #no peles atrasanas vietas iegust rindu un kolonu
                game.select(row, col) # tiek izsaukta select metode

        
        game.update() #atjauno informaciju uz ekrana
    
    pygame.quit()

main()