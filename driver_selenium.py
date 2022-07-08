from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from wordle_solver import WordleSolver
from bs4 import BeautifulSoup
import time

def submit_guess(key_input, guess):
    key_input.send_keys(guess)
    key_input.send_keys(Keys.ENTER)

def get_result(app, guess_num):
    result = [-1, -1, -1, -1, -1]
    
    guess = "tbd"

    while "tbd" in str(guess):
        time.sleep(0.1)
        
        html = app.get_attribute('innerHTML')
        soup = BeautifulSoup(html, "html.parser")

        guess = soup.find_all('div', class_="Row-module_row__dEHfN")[guess_num] 

    tiles = guess.find_all('div', class_="Tile-module_tile__3ayIZ")
    
    for i, tile in enumerate(tiles):
        if tile["data-state"] == "absent":
            result[i] = 0
        elif tile["data-state"] == "present":
            result[i] = 1
        elif tile["data-state"] == "correct":
            result[i] = 2

    print(result)

    return result

selenium_driver = webdriver.Chrome()

selenium_driver.get('https://www.nytimes.com/games/wordle/index.html')

selenium_driver.find_element(By.CLASS_NAME, 'Modal-module_closeIcon__b4z74').click()

key_input = selenium_driver.find_element(By.CLASS_NAME, 'pz-dont-touch')

solver = WordleSolver()

result = [0, 0, 0, 0, 0]
guesses_submitted = 0
last_guess = None

while guesses_submitted < 6 and not all(result):
    guess = solver.get_next_guess()
    print(guess)
    last_guess = guess
    time.sleep(2)
    submit_guess(key_input, guess)
    result = get_result(key_input, guesses_submitted)
    solver.update_model(guess, result)
    print(solver.avail_words)
    guesses_submitted += 1

if result != [2, 2, 2, 2, 2]:
    print("Failed to solve wordle")
else:
    print(f"Solution: {last_guess}")