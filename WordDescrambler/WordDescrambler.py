# given a list of letters, find any words that can be made with them (use wordlist) - perfect for multithreading
import time
from os import system

from Runtime import Runtime
from pathlib import Path
from itertools import permutations
from nltk.corpus import words


def sleep_timer(total_sleep_seconds):
    """
    :param total_sleep_seconds: The total amount of time, in seconds, to sleep for.
    :return: None
    """
    counter = total_sleep_seconds
    while counter > 0:
        print(f'sleeping for {counter} more seconds')
        time.sleep(1)
        system('cls')
        counter -= 1

class WordDescrambler:
    """
    WordDescrambler class

    A class used to descramble words based on a given set of candidate letters.

    Parameters:
    - candidate_letters (str): The set of candidate letters used to descramble words.
    - path_to_wordlist (Path or str, optional): The path to a wordlist file. If not provided, the default wordlist will be used. Defaults to None.
    - **kwargs (optional): Additional keyword arguments.

    Attributes:
    - use_all_letters (bool): Whether to use all the candidate letters in a word. Defaults to False.
    - _limit_length (int): The maximum length of the generated words. Defaults to None.
    - _min_match_length (int): The minimum length of the matched words. Defaults to 3.
    - verbose_mode (bool): Whether to display verbose output during the word descrambling process. Defaults to False.
    - use_basic_wordlist (bool): Whether to use a basic wordlist. Defaults to False.
    - _candidate_letters (list): The list of candidate letters.
    - path_to_wordlist (Path): The path to the wordlist file.
    - _wordlist (set): The set of words in the wordlist.
    - match_list (set): The set of matched words.
    - basic_wordlist (set): The set of words in the basic wordlist.
    - full_wordlist (set): The set of words in the full wordlist.
    - guess_counter (int): The count of guesses made during the word descrambling process.

    Methods:
    - min_match_length(): Get the minimum match length based on the number of candidate letters.
    - limit_length(): Get the limit length for generated words.
    - candidate_letters(): Get the list of candidate letters.
    - Wordlist(): Get the wordlist based on the provided path or default wordlist.
    - Wordlist(value): Set the wordlist.
    - _run_permutations(word_length): Run permutations to generate all possible words of a given length.
    - search(print_matches): Search for words based on the candidate letters and print the matches.
    - print_matches(): Print the matched words.
    """
    max_candidate_length = 12
    def __init__(self, candidate_letters: str, path_to_wordlist: Path or str = None, **kwargs):
        self.use_all_letters = kwargs.get('use_all_letters', False)
        self._limit_length = kwargs.get('limit_length', None)
        self._min_match_length = kwargs.get('min_match_length', 3)
        self.verbose_mode = kwargs.get('verbose_mode', False)

        self.use_basic_wordlist = kwargs.get('use_basic_wordlist', False)

        self._candidate_letters = [x for x in candidate_letters.lower()]
        self.path_to_wordlist = path_to_wordlist
        if self.path_to_wordlist:
            self.path_to_wordlist = Path(path_to_wordlist)
        else:
            self.path_to_wordlist = None
        self._wordlist = set()
        self.match_list = set()

        self.basic_wordlist = {w.lower() for w in words.words('en-basic')}
        self.full_wordlist = {w.lower() for w in words.words()}
        self.guess_counter = 0

    @property
    def min_match_length(self):
        """
        Returns the minimum match length.

        :return: The minimum match length.
        :rtype: int
        :raises ValueError: If the minimum match length is less than the number of candidate letters.
        """
        if len(self.candidate_letters) >= self._min_match_length:
            #print(len(self.candidate_letters), self._min_match_length)
            pass
        else:
            raise ValueError("min_match_length must be greater than or equal to the number of candidate letters.")
        return self._min_match_length

    @property
    def limit_length(self):
        """
        :return: The limit length value

        This property is used to limit the length of the candidate letters.
        If the limit length is set to a value larger than the number of candidate letters, a ValueError is raised.
        If the flag `use_all_letters` is set to True, the limit length value is set to None,
        indicating that all candidate letters should be used.

        :rtype: int or None
        """
        if self._limit_length:
            if self._limit_length > len(self.candidate_letters):
                raise ValueError("limit length cannot be larger than candidate_letters")
            elif self.use_all_letters:
                self._limit_length = None
        return self._limit_length

    @property
    def candidate_letters(self):
        """
        Returns the list of candidate letters.

        If the candidate letters are already stored as a list, returns the list directly. If the candidate
        letters are stored as a string, converts each character of the string into a list element.

        If the length of the candidate letters exceeds the maximum candidate length, a `ValueError` is raised.

        :return: The list of candidate letters.
        """
        if isinstance(self._candidate_letters, list):
            pass
        elif isinstance(self._candidate_letters, str):
            self._candidate_letters = [x for x in self._candidate_letters]
        if len(self._candidate_letters) > self.max_candidate_length:
            raise ValueError(f'Too many candidate letters. '
                             f'Max characters supported is {self.max_candidate_length}')
        else:
            pass
        return self._candidate_letters

    @property
    def Wordlist(self):
        """
        :return: The wordlist for the software.
        """
        if not self._wordlist:
            if self.path_to_wordlist:
                if self.path_to_wordlist.is_dir():
                    pass
                elif self.path_to_wordlist.is_file():
                    with open(self.path_to_wordlist, "r") as f:
                        for word in f.readlines():
                            self._wordlist.add(word.strip().lower())
            else:
                if self.use_basic_wordlist:
                    self._wordlist = self.basic_wordlist
                else:
                    self._wordlist = self.full_wordlist
        return self._wordlist

    @Wordlist.setter
    def Wordlist(self, value):
        """
        Sets the value of the `Wordlist` property.

        :param value: The new value for the `Wordlist` property.
        """
        self._wordlist = value

    def _run_permutations(self, word_length: int):
        """
        :param word_length: The length of the words to generate permutations for.
        :return: None

        This method runs permutations of the candidate letters to find matches in the given word list.
        It increments the guess counter with each iteration and adds any matches found to the match list.
        If verbose mode is enabled, it also prints the guess number when a match is found.

        Example Usage:
            obj = Object()
            obj._run_permutations(4)
        """
        for p in permutations(''.join(self.candidate_letters), word_length):  # , self.Wordlist):
            self.guess_counter += 1
            if ''.join(p) in self.Wordlist:
                # print(f"{''.join(p)} was found in candidate letters.")
                self.match_list.add(''.join(p))
                if self.verbose_mode:
                    print(f"found a match at guess number {self.guess_counter:,}")

    def search(self, print_matches: bool = False):
        """
        This method searches for words in a Wordlist object based on certain search parameters and prints the results.

        :param print_matches: A boolean indicating whether to print the found matches.
        :return: None

        """
        if self.use_all_letters:
            self.Wordlist = {x.lower() for x in self.Wordlist if len(x) == len(self.candidate_letters)}
        else:
            self.Wordlist = {x.lower() for x in self.Wordlist}
        if self.limit_length:
            self.Wordlist = {x.lower() for x in self.Wordlist if len(x) == self.limit_length}

        print(f"Searching for words made up of {self.candidate_letters}...")
        if self.use_all_letters:
            self._run_permutations(len(self.candidate_letters))
        elif self.limit_length:
            self._run_permutations(self.limit_length)
        else:
            for r in range(self.min_match_length, len(self.candidate_letters)):
                self._run_permutations(r)

        print(f"{len(self.match_list)} matches found.")
        if print_matches:
            self.print_matches()

    def print_matches(self):
        """
        Prints the list of matching words.

        :return: None
        """
        print("Matching Words: ")
        for m in self.match_list:
            print(f"\t{m}")


if __name__ == '__main__':
    # TODO: GUI?
    start_time = time.time()
    rt = Runtime(start_time, use_timedelta=True)
    # sleep_timer(5)

    WD = WordDescrambler(candidate_letters='AndrewMcspar',
                         use_all_letters=False, use_basic_wordlist=False)#, limit_length=5)#'stfaamnrc')
    WD.search(print_matches=True)

    print(f"{rt.runtime_string}")
    rt.write_runtime(as_json=True)


    #print('craftsman' in [''.join(x) for x in permutations('stfaamnrc')])