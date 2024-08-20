# given a list of letters, find any words that can be made with them (use wordlist) - perfect for multithreading
import time
from os import system

from Runtime import Runtime
from pathlib import Path
from itertools import permutations
from nltk.corpus import words


def sleep_timer(total_sleep_seconds):
    counter = total_sleep_seconds
    while counter > 0:
        print(f'sleeping for {counter} more seconds')
        time.sleep(1)
        system('cls')
        counter -= 1

class WordDescrambler:
    max_candidate_length = 12
    def __init__(self, candidate_letters: str, path_to_wordlist: Path or str = None, **kwargs):
        # TODO: turn these into props so that they can be checked/compared.
        #  Limit length should not be allowed to be greater than total length,
        #  and limit length should not be allowed if use all letters is true
        self.use_all_letters = kwargs.get('use_all_letters', False)
        self.limit_length = kwargs.get('limit_length', None)
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
    def candidate_letters(self):
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
        self._wordlist = value

    def _run_permutations(self, word_length: int):
        for p in permutations(''.join(self.candidate_letters), word_length):  # , self.Wordlist):
            self.guess_counter += 1
            if ''.join(p) in self.Wordlist:
                # print(f"{''.join(p)} was found in candidate letters.")
                self.match_list.add(''.join(p))
                print(f"found a match at guess number {self.guess_counter:,}")

    def search(self, print_matches: bool = False):
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
            for r in range(3, len(self.candidate_letters)):
                self._run_permutations(r)

        print(f"{len(self.match_list)} matches found.")
        if print_matches:
            self.print_matches()

    def print_matches(self):
        print("Matching Words: ")
        for m in self.match_list:
            print(f"\t{m}")


if __name__ == '__main__':
    # TODO: GUI?
    start_time = time.time()
    rt = Runtime(start_time)
    #sleep_timer(5)

    WD = WordDescrambler(candidate_letters='Andrewmcspar',
                         use_all_letters=False, use_basic_wordlist=False)#, limit_length=5)#'stfaamnrc')
    WD.search(print_matches=True)
    print(f"{rt}")
    with open('./Misc_Project_Files/last_runtime.txt', 'w') as f:
        f.write(str(rt))

    #print('craftsman' in [''.join(x) for x in permutations('stfaamnrc')])