from gensim.models import KeyedVectors  # KeyedVectors
from nltk.corpus import words
from random import choices

class Separator(object):
    def __init__(self, file_name : str = "information/words.bin", word_list: str = "information/common.txt") -> None:
        """Creates a Separator object, which contains three attributes:
        A KeyedVectors object containing the GoogleNews information to help create a list.
        A Set containing every english word
        A Set containing every unique key within the KeyedVectors object
        A Guess List containing every guess guessed for the day.
        A Random Start and End Word
        A Boolean Representing if the Game is Finished for the Day"""
        self._mod = KeyedVectors.load(file_name)
        self._eng_words = set(words.words())
        self._vocab = set(self._mod.key_to_index.keys())
        self._random_list = []
        word_file = open(word_list, 'r')
        for line in word_file:
            self._random_list.append(line.strip().lower())
        word_file.close()
        self._start_word, self._end_word = self._generate_random()
        self._current_word = self._start_word
        self._guess_list = [self._sim(self._start_word, self._end_word)]
        self._guess_count = 0
        self._finished = False

    def reset(self) -> None:
        """ Resets the Separator object, resetting the key variables for each day. This function is expected to be called each day."""

        self._guess_list = []
        self._guess_count = 0
        self._finished = False
        self._start_word, self._end_word = self._generate_random()
        self._current_word =  self._start_word

    def guess_word(self, guess_word : str) -> None:
        """ Checks to see if guess word is valid """
        if not self._finished:
            self._guess_count += 1
            guess_word = guess_word.strip().lower()
            similarity = self._similar_enough(self._current_word, guess_word)
            if similarity: 
                self._guess_list.append(self._sim(guess_word, self._end_word))
                val = "{:.2f}".format(self._guess_list[-1][1])
                print(f"{guess_word}: {val}")
                self._current_word = guess_word

                if guess_word == self._end_word:
                    self._finished = True
            else:
                print("Invalid guess, not similar enough.")
   
    def guess_list(self) -> list[tuple[str, float]]:
        """ Returns a list containing all the guesses. """
        return self._guess_list

    def guess_count(self) -> int:
        """ Returns the total amount of guesses, including invalid guesses. """
        return self._guess_count

    def start_word(self) -> str:
        """ Returns the starting word """
        return self._start_word

    def end_word(self) -> str:
        """ Returns the goal word """
        return self._end_word

    def current_word(self) -> str:
        """ Returns the current guess """
        return self._current_word

    def finished(self) -> bool:
        """ Checks to see if the game is finished. """
        return self._finished or self._current_word == self._end_word

    def _generate_top(self, base_word: str) -> list[tuple[str,float]]:
        gen_list = []
        starting = 5000
        while len(gen_list) < 1000:
            gen_list = [
                value[0] 
                for value in self._mod.similar_by_key(base_word, starting)
                if (value[0].isalpha() and value[0].islower() and value[0] in self._eng_words)
            ]
            starting += 2000
        return set(gen_list[:1000])

    def _similar_enough(self, base_word: str, guess_word: str) -> bool:
        """Takes in the base word and guess word as input.
        Generates a word list containing the 1500 most similar words excluding multi-word words and company names.
        If guess word is in the word list, returns True and is able to be guessed.
        Otherwise, returns False."""

        if base_word not in self._vocab or guess_word not in self._vocab:
            return False

        values = self._generate_top(base_word)
        #print(len(values))
        #print(values)
        for word in values:
            if guess_word == word:
                return True
        return False

    def _generate_random(self) -> list[str, str]:
        """ Function used to determine the random two words of the day. """
        return choices(self._random_list, k = 2)

    def _sim(self, word_one: str, relative_word: str) -> tuple[str, float]:
        """Takes two words as inputs and calculates the first word's similarity to the relative word.
        Returns a tuple pair containing the first word and it's relative similarity to the word."""

        return (word_one, self._mod.similarity(word_one, relative_word) * 100)

    def __repr__(self) -> str:
        """ Converts a Separator Object into a string """

        return_string = f"Start Word: {self._start_word} \nEnd Word: {self._end_word} \n"
        if self._finished:
            return_string += "Final Guess List: \n"
        else:
            return_string += "Current Guess List: \n"
        for value in self._guess_list:
            sim = "{:.2f}".format(value[1])
            return_string += f"Word: {value[0]}    Similarity: {sim} \n"
        return_string += f"Total Guess Count: {self._guess_count}\n"
        return_string += f"Valid Guess Count: {len(self._guess_list) - 1}\n"
        return return_string

