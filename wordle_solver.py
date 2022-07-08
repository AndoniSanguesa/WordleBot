import math

class WordleSolver:
    def __init__(self):
        self.avail_words = []
        self.first_guess = "RAISE"
        self.has_guessed = False
        self.wrong_places = {}
        self.answer = [None, None, None, None, None]

        with open("words.txt") as f:
            self.avail_words.extend(list(map(lambda x: x.strip().upper(), f.readlines())))
        
        self.all_words = self.avail_words.copy()

    def get_information(self, word):
        word = word.strip()
        count_dict = {}

        for w in self.avail_words:
            w = w.strip()
            result = [0, 0, 0, 0, 0]

            yellow_cand = {}
            correct_count = {}

            for i, letter in enumerate(word):
                if letter not in correct_count:
                        correct_count[letter] = 0
                
                if w[i] == letter:
                    correct_count[letter] += 1

                    result[i] = 2
                else:
                    if letter not in yellow_cand:
                        yellow_cand[letter] = []
                    yellow_cand[letter].append(i)

            for cand in yellow_cand:
                if cand in w:
                    for i in range(min(w.count(cand) - correct_count[cand], len(yellow_cand[cand]))):
                        result[yellow_cand[cand][i]] = 1
                        
                        if tuple(result) not in count_dict:
                            count_dict[tuple(result)] = 0
                        
                        count_dict[tuple(result)] += 1
        
        bits = 0

        for pattern in count_dict:
            prob = count_dict[pattern] / len(self.avail_words)
            info = math.log2(1/prob)

            bits += prob * info

        #print(f"{word}: {bits}")

        return bits

    def get_next_guess(self):
        if not self.has_guessed:
            self.has_guessed = True
            return self.first_guess

        if None not in self.answer:
            return "".join(self.answer)
        
        if len(self.avail_words) == 1:
            return self.avail_words[0]

        return max(self.avail_words, key=lambda x: self.get_information(x))

    def update_model(self, guess, result):

        new_avail_words = []

        yellows = {}
        correct = {}

        for i, res in enumerate(result):
            if guess[i] not in correct:
                correct[guess[i]] = 0

            if res == 1:
                if guess[i] not in yellows:
                    yellows[guess[i]] = 0
                yellows[guess[i]] += 1

                if guess[i] not in self.wrong_places:
                    self.wrong_places[guess[i]] = []
                
                self.wrong_places[guess[i]].append(i)

            elif res == 2:
                correct[guess[i]] += 1
                self.answer[i] = guess[i]


        for word in self.avail_words:
            word = word.upper()
            word_valid = True

            for i, res in enumerate(result):
                if (res == 0 and guess[i] in word and word.count(guess[i]) != correct[guess[i]]) or \
                   (res == 2 and guess[i] != word[i]) or \
                   (res == 1 and word[i] in self.wrong_places and i in self.wrong_places[word[i]]):
                    word_valid = False
            
            for val in yellows:
                if word.count(val) - correct[val] < yellows[val]:
                     word_valid = False
            
            if word_valid:
                new_avail_words.append(word)

        self.avail_words = new_avail_words
        
        return new_avail_words