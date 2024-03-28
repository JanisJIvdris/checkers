from .constants import RED, WHITE, SQUARE_SIZE, BROWN, CROWN
import pygame

class Piece:

    PADDING = 15  #nosaka cik pikseli ir no laucina malas, lidz kaulina malai
    OUTLINE = 2   # nosaka konturu

    def __init__(self, row, col, color): #kad tiek izveidots jauns kaulins parada ta parametrus
        self.row = row                   #define kada rinda atrodas kaulins
        self.col = col                   #define kada kollona atrodas kaulins
        self.color = color               # kada krasa
        self.king = False                # vai ir karalis
        self.x = 0                       # pozicija x asi
        self.y = 0                        #pozicija y asi
        self.calc_pos()                   #aprekina poziciju x un y asi

    def calc_pos(self): # aprekina kaulina poziciju x un y asi, izmantojot rindas un kollonas
        self.x = SQUARE_SIZE * self.col + SQUARE_SIZE // 2  # x asi ievieto tiesi pa vidu laucinam
        self.y = SQUARE_SIZE * self.row + SQUARE_SIZE // 2    # y asi ievieto tiesi pa vidu laucinam
                                                             # ^ nepieciesams jo tiks zimeti apali kaulini, un tie tiks zimeti no laucina centra 
    
    def make_king(self): #parveido parasto kaulinu par karala kaulinu
        self.king = True
    
    def draw(self, window):                                                            # tiek uzzimets kaulins
        radius = SQUARE_SIZE//2 - self.PADDING                                      # nosaka kaulina radiusu
        pygame.draw.circle(window, BROWN, (self.x, self.y), radius + self.OUTLINE)      # uzzime kaulina konturu
        pygame.draw.circle(window, self.color, (self.x, self.y), radius)               # uzzime pasu kaulina apli
        if self.king:
            window.blit(CROWN, (self.x - CROWN.get_width()//2, self.y - CROWN.get_height()//2)) #ja kaulins ir karalis, kaulina vidu ieliek attelu

    def move(self, row, col): 
        self.row = row  # atjauno kaulina jauno rindas novietojumu
        self.col = col  # atjauno kaulina jauno kollonas novietojumu
        self.calc_pos()  # aprekina kaulina poziciju

