import pygame  #tiek importeta pygame biblioteka
from .constants import BLACK, CREAM, ROWS, RED, SQUARE_SIZE, COLS, WHITE, CREAM #tiek importetas konstantes
from .piece import Piece #tiek importeta info par kauliņiem no piece.py

class Board:   #board klase atbild par laukuma uzzimesanu, kaulinu parvietosanu un nonemsanu
    def __init__ (self):                   #tiek defineti board class atributi
        self.board = []                    #apzime laukumu (divdimensiju lists)
        self.selected_piece = None         # nosaka vai ir izvelets kaulins vai ne
        self.red_left = self.white_left = 12   #tiek noteikts kaulinu skaits
        self.red_kings = self.white_kings = 0   #tiek noteikts karalu skaits
        self.create_board()                      #izsauc laukuma izveidosanas metodi
    
    def draw_squares(self, window):     #uz laukuma tiek sazimeti laucini(kvadratini)
        window.fill(BLACK)              # laukums tiek aizpildits ar melnu krasu
        for row in range(ROWS):      
            for col in range(row % 2, COLS, 2): #izveido rutainu laukumu
                pygame.draw.rect(window, CREAM, (row*SQUARE_SIZE, col *SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)) # uz melna laukuma tiek sazimeti balti kvadrati
                                             #  ^ tiek aprekinats kur jabut rutaina laukuma augsejiem sturiem, ka ari noteikti laucina izmeri

    def evaluate(self):
        return self.white_left - self.red_left + (self.white_kings * 0.5 - self.red_kings * 0.5)

    def get_all_pieces(self, color):
        pieces = []
        for row in self.board:
            for piece in row:
                if piece != 0 and piece.color == color:
                    pieces.append(piece)
        return pieces

    def move(self, piece, row, col):
        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col] #kaulinus samaina vietam
        piece.move(row, col)   
        
        if row == ROWS - 1 or row == 0: # ja kaulins atrodas pirmaja vai pedeja rinda
            piece.make_king()           # kaulinu padara par karali
            if piece.color == WHITE:    
                self.white_kings += 1   # ja kaulins ir balts, balto karalu skaitam pieskaita viens
            else:
                self.red_kings += 1     # ja kaulins ir sarkans, sarkano kaulinu skaitam pieskaita viens

    def get_piece(self, row, col):
        return self.board[row][col]  #iezmantojot rindu un kollonu, tiek ieguts kaulins
    
    def create_board(self):  #tiek izveidots laukuma apzimejums
        for row in range(ROWS):
            self.board.append([]) # tiek izveidots lists ar katras rindas saturu
            for col in range(COLS):
                if col % 2 == ((row +  1) % 2): # nosak "pamīšus" kaulinu izvietojumu
                    if row < 3:
                        self.board[row].append(Piece(row, col, WHITE)) # kaulini kas atrodas tuvāk par 3 rindu ir balti
                    elif row > 4:
                        self.board[row].append(Piece(row, col, RED))   # kaulini kas atrodas talak par 4 rindu ir sarkani
                    else:
                        self.board[row].append(0)
                else:                                    #parejos laucinos nav kaulini
                    self.board[row].append(0)

    def draw(self, window):
        self.draw_squares(window)  # loga uzzimē visus lauciņus
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]   #izejot cauri loopam uzzimē kaulinus atbilstošajas pozicijas
                if piece != 0:       
                    piece.draw(window)  #ja kaulins nav vienads ar 0, tad to iezimet laukuma

    def remove(self, pieces):
        for piece in pieces:
            self.board[piece.row][piece.col] = 0 # parmekle un noņem nevajadzigos kauliņus
            if piece != 0: # ja kulinu skaits nav 0
                if piece.color == RED: # ja kaulina krasa ir sarkana
                    self.red_left -= 1  # no sarkano kaulinu skaita -1
                else:
                    self.white_left -= 1 # no balto kaulinu skaita -1

    def winner(self):  # izvada kura krasa uzvareja
        if self.red_left <= 0:   # ja sarkano kaulinu skaits ir mazaks par nulli
            return WHITE         #izvada blats
        elif self.white_left <= 0:# ja balto kaulinu skaits ir mazaks par nulli
            return RED         # izvada sarkans
        
        return None 
    
    def get_valid_moves(self, piece):
        moves = {}    #uzglaba iespejamos gajienus
        left = piece.col - 1   #nolasa kreiso diognali
        right = piece.col + 1   #nolasa labo diognali
        row = piece.row

        if piece.color == RED or piece.king: # ja kaulins ir sarkans vai karalis
            moves.update(self._traverse_left(row -1, max(row-3, -1), -1, piece.color, left))   #apluko iespejamos gajienus pa kreiso/labo diognali,ne tālāk par diviem lauciņiem
            moves.update(self._traverse_right(row -1, max(row-3, -1), -1, piece.color, right)) #^ no pasreizejas pozicijas, -1 pavirza vienu uz augšu implimentējot šo for loopu , nosaka krasu un virzienu
        if piece.color == WHITE or piece.king:# ja kaulins ir balts vai karalis
            moves.update(self._traverse_left(row +1, min(row+3, ROWS), 1, piece.color, left))  #notiek tas pats kas augstak ar sarkanas krasas kauliniem, tikai attiecigi no otra laukuma gala(preteji)
            moves.update(self._traverse_right(row +1, min(row+3, ROWS), 1, piece.color, right))

        return moves # adds to dictionary

    def _traverse_left(self, start, stop, step, color, left, skipped=[]): #pārluko kreiso diognali
        moves = {}
        last = []
        for r in range(start, stop, step): # sola sakums, beigas un kads ir solis
            if left < 0: # ja kreisaja puse ir laukuma mala, break
                break
            
            current = self.board[r][left]  
            if current == 0:  # ja ir atrasts tukšs lauciņš
                if skipped and not last: # ja ir izlaists un last nav definets, break
                    break
                elif skipped:
                    moves[(r, left)] = last + skipped # ja laucins ir tukss un tiek parlekts citam laucinam
                else:
                    moves[(r, left)] = last
                
                if last:
                    if step == -1:
                        row = max(r-3, 0)
                    else:
                        row = min(r+3, ROWS)
                    moves.update(self._traverse_left(r+step, row, step, color, left-1,skipped=last))
                    moves.update(self._traverse_right(r+step, row, step, color, left+1,skipped=last))
                break
            elif current.color == color:
                break
            else:
                last = [current]

            left -= 1
        
        return moves
    
    def _traverse_right(self, start, stop, step, color, right, skipped=[]): # parluko labo diognali
        moves = {}
        last = []
        for r in range(start, stop, step):
            if right >= COLS:
                break
            
            current = self.board[r][right]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r,right)] = last + skipped
                else:
                    moves[(r, right)] = last
                
                if last:
                    if step == -1:
                        row = max(r-3, 0)
                    else:
                        row = min(r+3, ROWS)
                    moves.update(self._traverse_left(r+step, row, step, color, right-1,skipped=last))
                    moves.update(self._traverse_right(r+step, row, step, color, right+1,skipped=last))
                break
            elif current.color == color:
                break
            else:
                last = [current]

            right += 1
        
        return moves