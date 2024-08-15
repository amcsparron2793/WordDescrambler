# given a list of letters, find any words that can be made with them (use wordlist) - perfect for multithreading
from pathlib import Path
from itertools import permutations
from nltk.corpus import words


class WordDescrambler:
    def __init__(self, candidate_letters: str, path_to_wordlist: Path or str = None, **kwargs):
        self.use_all_letters = kwargs.get('use_all_letters', True)
        self.candidate_letters = [x for x in candidate_letters.lower()]
        self.path_to_wordlist = path_to_wordlist
        if self.path_to_wordlist:
            self.path_to_wordlist = Path(path_to_wordlist)
        else:
            self.path_to_wordlist = None
        self._wordlist = set()
        self.match_list = set()
        self.limit_length = kwargs.get('limit_length', None)

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
                self._wordlist = {x for x in words.words()}
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

        if self.use_all_letters:
            self._run_permutations(len(self.candidate_letters))
        elif self.limit_length:
            self._run_permutations(self.limit_length)
        else:
            for r in range(4, len(self.candidate_letters)):
                self._run_permutations(r)

        print(f"{len(self.match_list)} matches found.")
        if print_matches:
            print("Matching Words: ")
            for m in self.match_list:
                print(f"\t{m}")






if __name__ == '__main__':
    WD = WordDescrambler(candidate_letters='stfaamnrc', use_all_letters=False)#, limit_length=5)#'stfaamnrc')
    WD.search(print_matches=True)
    #print('craftsman' in [''.join(x) for x in permutations('stfaamnrc')])