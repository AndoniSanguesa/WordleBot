from mimetypes import guess_all_extensions
import pygame as pg
import random
from pygame_object import PyGameObject
from wordle_guess import WordleGuess
from wordle_keyboard import WordleKeyboard

class WordleGame(PyGameObject):
    def __init__(self, screen):
        super().__init__(screen)
        self.width, self.height = self.screen.get_size()
        self.header_height = 150
        self.keyboard_height = 270
        self.guesses_height = self.height - self.header_height - self.keyboard_height - 20
        self.guess_height = (self.guesses_height - 50) // 6
        self.guesses = []
        self.answer = self.select_answer()
        self.game_won = False
        self.play_again_button = pg.Rect(self.width/2 - 100, self.height/2 + 100, 200, 50)
        for i in range(6):
            xpos = 50
            ypos = self.header_height + 10 + (i*(self.guess_height + 10))
            guess = WordleGuess(self.screen, xpos, ypos, self.guess_height, self.width-80)
            self.guesses.append(guess)
        
        self.keyboard = WordleKeyboard(self.screen, 550)
    
    def select_answer(self):
        with open("words.txt") as f:
            words = f.read().splitlines()
            return random.choice(words).upper()

    def draw(self):
        font = pg.font.SysFont('Comic Sans MS', 50)
        text = font.render("Wordle", True, (255, 255, 255))
        self.screen.blit(text, (60, 60))

        for guess in self.guesses:
            guess.draw()

        self.keyboard.draw()

        if self.game_won:
            pg.draw.rect(self.screen, (0, 0, 0, 0.3), (0, 0, self.width, self.height))
            font = pg.font.SysFont('Comic Sans MS', 100)
            text = font.render("You won!", True, (255, 255, 255))
            self.screen.blit(text, (self.width/2 - text.get_width()/2, self.height/2 - text.get_height()/2))

            pg.draw.rect(self.screen, (255, 255, 255), self.play_again_button, 3)
            pg.draw.rect(self.screen, (0, 0, 0), self.play_again_button, 0)
            font = pg.font.SysFont('Comic Sans MS', 30)
            text = font.render("Play again", True, (255, 255, 255))
            self.screen.blit(text, (self.width/2 - text.get_width()/2, self.height/2 + 100))

    def reset(self):
        self.game_won = False
        for guess in self.guesses:
            guess.reset()
        self.keyboard.reset()
        self.answer = self.select_answer()

    def send_guess(self, submitted_guess):
        for guess in self.guesses:
            if guess.is_guess_full() and guess.is_guess_submitted():
                continue
            for letter in submitted_guess:
                guess.add_letter(letter)
            
            won = guess.submit_guess(self.answer)
            if won is not None:
                self.keyboard.submit_guess(self.answer, guess.get_guess())
            if won:
                self.game_won = True
            
            return guess.get_result()

    def handle_event(self, event):
        key_pressed = self.keyboard.handle_event(event)
        
        if self.game_won:
            if event.type == pg.MOUSEBUTTONDOWN:
                if self.play_again_button.collidepoint(event.pos):
                    self.reset()
                    return True
            return

        if not key_pressed and event.type == pg.KEYDOWN:
            if event.key == pg.K_BACKSPACE:
                key_pressed = "BACK"
            elif event.key == pg.K_RETURN:
                key_pressed = "ENTER"
            else:
                try:
                    key_pressed = chr(event.key).capitalize()
                    print(key_pressed)
                except ValueError:
                    key_pressed = None

        if key_pressed:
            for guess in self.guesses:
                if guess.is_guess_full() and guess.is_guess_submitted():
                    continue

                if key_pressed == "BACK":
                    guess.remove_letter()
                elif key_pressed == "ENTER":
                    if guess.is_guess_full():
                        won = guess.submit_guess(self.answer)
                        if won is not None:
                            self.keyboard.submit_guess(self.answer, guess.get_guess())
                        if won:
                            self.game_won = True
                elif not guess.is_guess_full():
                    guess.add_letter(key_pressed)
                    break
                break