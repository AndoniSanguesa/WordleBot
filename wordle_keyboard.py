from wordle_letter import WordleLetter
from pygame_object import PyGameObject

ROWS = [["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"], ["A", "S", "D", "F", "G", "H", "J", "K", "L"], ["ENTER", "Z", "X", "C", "V", "B", "N", "M", "BACK"]]
ROW_XS = [55, 75, 25]

class WordleKeyboard(PyGameObject):
    def __init__(self, screen, y):
        super().__init__(screen)
        self.width, self.height = self.screen.get_size()

        self.keys = []
        
        for i, key in enumerate(ROWS[0]):
            xpos = ROW_XS[0] + (i*45)
            ypos = y
            key = WordleLetter(self.screen, xpos, ypos, 35, 40, key)
            self.keys.append(key)

        for i, key in enumerate(ROWS[1]):
            xpos = ROW_XS[1] + (i*45)
            ypos = y + 55
            key = WordleLetter(self.screen, xpos, ypos, 35, 40, key)
            self.keys.append(key)

        for i, key in enumerate(ROWS[2]):
            xpos = ROW_XS[2] + (max(i-1, 0)*45) + (100 if i > 0 else 0)
            ypos = y + 110
            key = WordleLetter(self.screen, xpos, ypos, 35 if key not in ["ENTER", "BACK"] else 90, 40, key)
            self.keys.append(key)

    def draw(self):
        for key in self.keys:
            key.draw()

    def handle_event(self, event):
        to_ret = None
        for key in self.keys:
            if key.handle_event(event):
                to_ret = key.letter
        return to_ret

    def reset(self):
        for key in self.keys:
            key.set_color(None)
    
    def submit_guess(self, answer, guess):
        good = []
        bad = []
        for i in guess:
            if i in answer:
                good.append(i)
            else:
                bad.append(i)
        
        for key in self.keys:
            if key.letter in good:
                all_in_place = True
                for i in range(5):
                    if answer[i] != guess[i] and answer[i] == key.letter:
                        all_in_place = False
                
                if all_in_place:
                    key.set_color((0, 255, 0))
                else:
                    key.set_color((255, 123, 0))
            elif key.letter in bad:
                key.set_color((30, 30, 30))
