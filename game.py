from json import load as load_file
from random import choice as pick_random

word_list = []

with open('words_dictionary.json') as file:
    word_list = [*load_file(file)]
    
class Game:
    def __init__(self, mention: str):
        self.already_playing = False
        self.guessed_letters = []
        self.word = ''
        self.answer_list = []
        self.mention = mention
        self.incorrect_left = 0
        
    def start(self) -> None:
        self.already_playing = True
        self.word = pick_random(word_list)
        self.answer_list = [c for c in self.word]
        self.incorrect_left = 6
        
    def quit(self) -> None:
        self.already_playing = False
        self.guessed_letters.clear()
        self.word = ''
        self.incorrect_left = 0
        
    def reset(self) -> None:
        self.already_playing = True
        self.word = pick_random(word_list)
        self.guessed_letters.clear()
        self.answer_list = [c for c in self.word]
        self.incorrect_left = 6
            
    def state(self):
        if not self.already_playing:
            return (f'{self.mention} there is no game', -1)
        
        if self.incorrect_left == 0:
            ans = (f'{self.mention} you lose, the word was {self.word}', 0)
            self.quit()
            return ans
        
        arr = [c if c in self.guessed_letters else '▉' for c in self.word]
        
        if not arr:
            return (f'{self.mention} word has not been initialized', -1)
        
        if arr == self.answer_list:
            ans = (f'{self.mention} congragulations, the word was {self.word}', -1)
            self.quit()
            return ans
        
        separator = ' '
        return (
            (
                f'{separator.join(arr)}\n'
                f'incorrect guesses left {self.incorrect_left}'
            ),
            self.incorrect_left
        )
        
    def guess(self, s: str):
        if len(s) > 1:
            if s == self.word:
                ans = (f'{self.mention} congragulations, the word was {self.word}', -1)
                self.quit()
                return ans
            else:
                self.incorrect_left -= 1
                return (
                    (
                        f'{self.mention} incorrect\n'
                        f'incorrect guesses left {self.incorrect_left}'
                    ),
                    self.incorrect_left
                )
            
        elif len(s) == 1:
            if s in self.guessed_letters:
                return (f'{self.mention} you already guessed {s}', -1)
            self.guessed_letters.append(s)
            if s not in self.word:
                self.incorrect_left -= 1
            return self.state()
        return (f'{self.mention} invalid input', -1)
                