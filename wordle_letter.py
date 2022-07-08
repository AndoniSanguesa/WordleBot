import pygame as pg
from pygame_object import PyGameObject


class WordleLetter(PyGameObject):

    def __init__(self, screen, x, y, width, height, letter=None):
        super().__init__(screen)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rad = 10
        self.letter = letter
        self.prev_color = None
        self.color = None
        self.result = -1
        self.text_color = (255, 255, 255)
        self.pressed = False
    
    def draw(self):
        rectangle = pg.Rect(self.x, self.y, self.width, self.height)
        pg.draw.rect(self.screen, (0, 0, 0), rectangle, 3, self.rad)
        if self.color is not None:
            pg.draw.rect(self.screen, self.color, rectangle, 0, self.rad)
        
        if self.letter is not None:
            font = pg.font.SysFont('Comic Sans MS', int(self.height*0.5))
            text = font.render(self.letter, True, self.text_color)
            self.screen.blit(text, (self.x+self.width/2-4 - len(self.letter)*6, self.y+10))
        

    def change_letter(self, letter):
        self.letter = letter

    def set_color(self, color):
        self.color = color
    
    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if self.color:
                print(self.color)
            self.prev_color = self.color
            if self.x < event.pos[0] < self.x+self.width and self.y < event.pos[1] < self.y+self.height:
                self.color = (255, 255, 255)
                self.text_color = (0, 0, 0)
                self.pressed = True
                return True
        elif event.type == pg.MOUSEBUTTONUP:
            # if self.prev_color:
            #     print(self.prev_color)
            self.color = self.prev_color
            self.text_color = (255, 255, 255)
            self.pressed = False
        
        return False
            