import pygame
from .constants import RED, WHITE, BLUE, SQUARE_SIZE        # tiek importets viss vajadzigais
from checkers.board import Board

class Game:

    def __init__(self, window):
        self._init() # inicalize speli
        self.window = window
    

    def update(self):  # šo metodi izsauc lai updateotu speli
        self.board.draw(self.window)   #uzzime no jauna speles laukumu
        self.draw_valid_moves(self.valid_moves)  # uzzime pieejamos logus
        pygame.display.update()   # atjauno displeju

    def _init(self): #metode ir privata un to atseviški nevar izsaukt, tapec ir jaizsauc __init vai reset metodes
        self.selected = None  #nosaka vai ir izvelets kaulins
        self.board = Board()  # 
        self.turn = RED
        self.valid_moves = {} #pasaka iespejamos gajienus

    def select(self, row, col):  #select
        if self.selected: #ja ir izvelets kaulins,
            result = self._move(row, col)  #  parvieto to uz  izveleto rindu un kollonu izmantojot _move metodi, ja tur var parvietot kaulinu
            if not result:   #ja nevar parvietot tur kaulinu
                self.selected = None  # neko neatzime(neselecto)
                self.select(row, col)# no jauna izsauc metodi
        
        piece = self.board.get_piece(row, col)      
        if piece != 0 and piece.color == self.turn: # ja izvelas aiznemtu laucinu un tas ir speletaja krasas kaulns
            self.selected = piece          #izvelas to kaulinu
            self.valid_moves = self.board.get_valid_moves(piece)  # paradit iespejamos gajienus                     
            return True
            
        return False

    def _move(self, row, col):
        piece = self.board.get_piece(row, col)         # izveletais kaulins 
        if self.selected and piece == 0 and (row, col) in self.valid_moves:  #ja ir izvelets kaulins ir == ar 0 un vieta kur velas parvietot nav ainemta
            self.board.move(self.selected, row, col)    #izveletais kaulins tiek parvietots uz padoto laucinu
            skipped = self.valid_moves[(row, col)]   # parbauda vai veicot gajienu tika izlaists kaulins
            if skipped:
                self.board.remove(skipped)     #ja tika izlaists kaulins, noņem izlaisto kauliņu(nokauj)
            self.change_turn()
        else:
            return False

        return True
    def winner(self):
        return self.board.winner()  #izsauc metodi winner no board.py

    def reset(self):
        self._init() #inicalize speli, attiecigi no jauna sak speli



    def draw_valid_moves(self, moves): # nolasa iespejamos gajienus
        for move in moves:  #nolasa vai gajiens ir iespejams no moves
            row, col = move  
            pygame.draw.circle(self.window, BLUE, (col * SQUARE_SIZE + SQUARE_SIZE//2, row * SQUARE_SIZE + SQUARE_SIZE//2), 10) #lauciņa vidu ieliek zilu punktu


    def change_turn(self):   # nomaina kārtu
        self.valid_moves = {}
        if self.turn == RED:  # ja karta ir sarkanajam, nomaina kartu uz baltu
            self.turn = WHITE
        else:
            self.turn = RED  # ja karta ir baltajam, nomaina kartu uz sarkanu

    def get_board(self):
        return self.board

    def ai_move(self, board):
        self.board = board
        self.change_turn()