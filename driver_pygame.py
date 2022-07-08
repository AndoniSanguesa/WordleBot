import pygame as pg
from wordle_game import WordleGame
from wordle_main import run_game
from wordle_solver import WordleSolver
import threading
import time


def play_wordle(game_object):
    solver = WordleSolver()

    while not game_object.game_won:
        guess = solver.get_next_guess().strip().upper()
        print(guess)

        result = game_object.send_guess(guess)

        word_list = solver.update_model(guess, result)
        print(word_list)
        time.sleep(1)

    

screen = pg.display.set_mode([550, 800])
game_object = WordleGame(screen)

play_thread = threading.Thread(target=play_wordle, args=[game_object])

play_thread.start()

run_game(screen, game_object)

play_thread.join()