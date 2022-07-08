import pygame as pg
from wordle_letter import WordleLetter
from pygame_object import PyGameObject

class WordleGuess(PyGameObject):
    def __init__(self, screen, x, y, height, width):
        super().__init__(screen)
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.current_guess = ""
        self.letters = []
        self.submitted = False
        for i in range(5):
            letter_width = (self.width-60)//5
            xpos = self.x + (i*(letter_width + 10))
            
            letter = WordleLetter(self.screen, xpos, self.y, letter_width, self.height)
            self.letters.append(letter)
    
    def reset(self):
        self.current_guess = ""
        for letter in self.letters:
            letter.change_letter("")
            letter.set_color(None)
        self.submitted = False

    def draw(self):
        for letter in self.letters:
            letter.draw()

    def add_letter(self, letter):
        self.current_guess += letter
        self.letters[len(self.current_guess)-1].change_letter(letter)

    def remove_letter(self):
        self.current_guess = self.current_guess[:-1] if self.current_guess else ""
        self.letters[len(self.current_guess)].change_letter("")

    def valid_guess(self):
        with open("words.txt") as f:
            words = f.read().splitlines()
            if self.current_guess.lower() in words:
                return True
        return False

    def get_result(self):
        result = [0, 0, 0, 0, 0]
        for i, letter in enumerate(self.letters):

            result[i] = letter.result

        return result

    def submit_guess(self, answer):
        if not self.valid_guess():
            return None
        
        self.submitted = True

        for i, let in enumerate(self.current_guess):
            if let == answer[i]:
                self.letters[i].set_color((0, 255, 0))
                self.letters[i].result = 2
            elif let in answer:
                num_in_answer = answer.count(let)
                num_in_correct_place = 0
                num_in_correct_upto = 0

                for j in range(5):
                    if answer[j] == let and self.current_guess[j] == let:
                        if j < i:
                            num_in_correct_upto += 1
                        num_in_correct_place += 1
                
                num_to_color = num_in_answer - num_in_correct_place + num_in_correct_upto

                if self.current_guess[:i+1].count(let) <= num_to_color:
                    self.letters[i].set_color((255, 123, 0))
                    self.letters[i].result = 1
                else:
                    self.letters[i].set_color((30, 30, 30))
                    self.letters[i].result = 0
                    
            else:
                self.letters[i].set_color((30, 30, 30))
                self.letters[i].result = 0

        if answer == self.current_guess:
            return True
        return False

    def is_guess_full(self):
        if len(self.current_guess) == 5:
            return True
        return False
    
    def is_guess_submitted(self):
        return self.submitted

    def get_guess(self):
        return self.current_guess