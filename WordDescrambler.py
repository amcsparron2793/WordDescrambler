# given a list of letters, find any words that can be made with them (use wordlist) - perfect for multithreading
from pathlib import Path
from itertools import permutations
from nltk.corpus import words


class WordDescrambler:
    max_candidate_length = 12
    def __init__(self, candidate_letters: str, path_to_wordlist: Path or str = None, **kwargs):
        # TODO: turn these into props so that they can be checked/compared.
        #  Limit length should not be allowed to be greater than total length,
        #  and limit length should not be allowed if use all letters is true
        self.use_all_letters = kwargs.get('use_all_letters', False)
        self.limit_length = kwargs.get('limit_length', None)

        self._candidate_letters = [x for x in candidate_letters.lower()]
        self.path_to_wordlist = path_to_wordlist
        if self.path_to_wordlist:
            self.path_to_wordlist = Path(path_to_wordlist)
        else:
            self.path_to_wordlist = None
        self._wordlist = set()
        self.match_list = set()

        # TODO: add use basic wordlist
        self.basic_wordlist = {w.lower() for w in words.words('en-basic')}
        self.full_wordlist = {w.lower() for w in words.words()}

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
                self._wordlist = self.full_wordlist
        return self._wordlist

    @Wordlist.setter
    def Wordlist(self, value):
        self._wordlist = value

    def _run_permutations(self, word_length: int):
        for p in permutations(''.join(self.candidate_letters), word_length):  # , self.Wordlist):
            if ''.join(p) in self.Wordlist:
                # print(f"{''.join(p)} was found in candidate letters.")
                self.match_list.add(''.join(p))

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
            print("Matching Words: ")
            for m in self.match_list:
                print(f"\t{m}")






if __name__ == '__main__':
    WD = WordDescrambler(candidate_letters='AndrewMCSpar',
                         use_all_letters=False)#, limit_length=5)#'stfaamnrc')
    WD.search(print_matches=True)
    #print('craftsman' in [''.join(x) for x in permutations('stfaamnrc')])