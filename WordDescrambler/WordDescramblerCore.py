# given a list of letters, find any words that can be made with them (use wordlist) - perfect for multithreading
import threading
import time
from os import system
from typing import Optional

from Runtime import Runtime
from pathlib import Path
from nltk.corpus import words
from WDConfig import WordDescramblerConfig

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

class WordDescramblerCore:
    """
        This class represents a word descrambler tool. It allows the user to descramble a given set of candidate letters
        and find matching words from a word list.

        Attributes:
            MAX_CANDIDATE_LENGTH (int): The maximum number of candidate letters supported.
            DEFAULT_CONFIG_PATH (str): The default configuration file path.

        Args:
            candidate_letters (str): The set of candidate letters.
            path_to_wordlist (Path or str, optional): The path to the word list file. If not provided, the default path
                specified in the configuration file will be used.
            kwargs: Additional keyword arguments.

        Raises:
            FileNotFoundError: If the word list file is not found at the specified path.

        Properties:
            min_match_length (int): The minimum match length.
            limit_length (int or None): The limit length for candidate letters.
            candidate_letters (list): The list of candidate letters.
            wordlist (set): The wordlist for the software.

        Methods:
            search(): Perform a search with multiple threads.
            print_matches(): Prints the list of matching words.

        Static Methods:
            _load_config(config_full_file_location: str) -> WordDescramblerConfig: Load and return the configuration.

        Private Methods:
            __init__(self, candidate_letters: str, path_to_wordlist: Path or str = None, **kwargs): Initialize the WordDescramblerCore object.
            _initialize_runtime_settings(self, kwargs: dict): Initialize the runtime settings.
            _initialize_wordlists(self): Initialize the wordlists.
            _extract_candidate_letters(letters: str) -> list: Convert the given letters to a list.
            _search_worker(self, words_to_search): Search for words in a given list that match certain conditions.
            _add_match(self, word): Add a matching word to the match list.
            _load_wordlist(self): Load the wordlist from the path or use the basic/full wordlist.
            _run_permutations(self, word_length: int): Run permutations of the candidate letters to find matches.
            _chunks(iterable, size): Yield successive n-sized chunks from an iterable.
            _get_words_per_column(self, **kwargs): Get the number of words per column for printing matches.

        Attributes:
            config (WordDescramblerConfig): The configuration object.
            path_to_wordlist (Path): The path to the wordlist file.
            config_full_file_location (str): The full file location of the configuration file.
            _candidate_letters (list): The list of candidate letters.
            guess_counter (int): The number of guesses made.
            match_list_lock (threading.Lock): The lock for accessing the match list.
            num_threads (int): The number of threads to use.
            _use_timedelta (bool): Flag to use timedelta for runtime.
            _rt_save_file_path (str): The path to save the runtime information.
            _rt_export_as_json (bool): Flag to export runtime information as JSON.
            _rt_export_as_text (bool): Flag to export runtime information as text.
            _use_all_letters (bool): Flag to use all candidate letters for matching.
            _limit_length (int or None): The limit length for candidate letters.
            _min_match_length (int): The minimum match length.
            _verbose_mode (bool): Flag for verbose mode.
            _print_matches (bool): Flag to print matches.
            _use_basic_wordlist (bool): Flag to use the basic wordlist.
            runtime (Runtime): The runtime object.
            _wordlist (set): The wordlist.
            match_list (set): The list of matching words.
            basic_wordlist (set): The set of words from the basic wordlist.
            full_wordlist (set): The set of words from the full wordlist.
    """
    MAX_CANDIDATE_LENGTH = 5000
    DEFAULT_CONFIG_PATH = '../cfg/config.ini'

    def __init__(self, candidate_letters: str, path_to_wordlist: Path or str = None, **kwargs):
        self.config = self._load_config(kwargs.get('config_full_file_location', self.DEFAULT_CONFIG_PATH))

        self._initialize_runtime_settings(kwargs)

        self.path_to_wordlist = Path(path_to_wordlist) if path_to_wordlist else Path(
            self.config.get('WORDLIST', 'path_to_wordlist'))

        self._candidate_letters = self._extract_candidate_letters(candidate_letters)
        self._initialize_wordlists()

        self.guess_counter = 0

        self.match_list_lock = threading.Lock()
        self.num_threads = kwargs.get('num_threads', 4)

    @staticmethod
    def _load_config(config_full_file_location: str) -> WordDescramblerConfig:
        config_full_file_location = Path(config_full_file_location)
        config_filename = config_full_file_location.stem + config_full_file_location.suffix
        return WordDescramblerConfig(config_filename=config_filename,
                                     config_dir=config_full_file_location.parent).GetConfig()

    def _initialize_runtime_settings(self, kwargs: dict):
        self._use_timedelta = kwargs.get('use_timedelta', self.config.getboolean('RUNTIME', 'use_timedelta'))
        self._rt_save_file_path = kwargs.get('rt_save_file_path', self.config.get('RUNTIME', 'save_file_path'))
        self._rt_export_as_json = kwargs.get('rt_export_as_json', self.config.getboolean('RUNTIME_OUTPUT', 'as_json'))
        self._rt_export_as_text = kwargs.get('rt_export_as_text', self.config.getboolean('RUNTIME_OUTPUT', 'as_text'))
        self._use_all_letters = kwargs.get('use_all_letters', self.config.getboolean('DEFAULT', 'use_all_letters'))
        self._limit_length = kwargs.get('limit_length', self.config.getint('DEFAULT', 'limit_length'))
        if self._limit_length <= 0:
            self._limit_length = None
        self._min_match_length = kwargs.get('min_match_length', self.config.getint('DEFAULT', 'min_match_length'))
        self._verbose_mode = kwargs.get('verbose_mode', self.config.getboolean('DEFAULT', 'verbose_mode'))
        self._print_matches = kwargs.get('print_matches', self.config.getboolean('SEARCH', 'print_matches'))
        self._use_basic_wordlist = kwargs.get('use_basic_wordlist',
                                              self.config.getboolean('WORDLIST', 'use_basic_wordlist'))
        self.runtime = Runtime(time.time(), use_timedelta=self._use_timedelta)

    def _initialize_wordlists(self):
        self._wordlist = set()
        self.match_list = set()
        self.basic_wordlist = {w.lower() for w in words.words('en-basic')}
        self.full_wordlist = {w.lower() for w in words.words()}

    @staticmethod
    def _extract_candidate_letters(letters: str) -> list:
        return list(letters.lower())

    def _search_worker(self, words_to_search):
        """
        Searches for words in a given list that match certain conditions.

        :param words_to_search: A list of words to search for matches.
        :return: None

        """
        for word in words_to_search:
            self.guess_counter += 1
            if len(word) < self.min_match_length:
                pass
            elif self._use_all_letters and set(word) == set(self._candidate_letters):
                self._add_match(word)
                if self._verbose_mode:
                    print(f"found a match at guess number {self.guess_counter:,}")

            elif not self._use_all_letters and all(letter in self._candidate_letters for letter in word):
                self._add_match(word)
                if self._verbose_mode:
                    print(f"found a match at guess number {self.guess_counter:,}")
    @property
    def min_match_length(self) -> int:
        if len(self.candidate_letters) < self._min_match_length:
            raise ValueError("min_match_length must be greater than or equal to the number of candidate letters.")
        return self._min_match_length

    @property
    def limit_length(self) -> Optional[int]:
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
            elif self._use_all_letters:
                self._limit_length = None
        return self._limit_length

    @property
    def candidate_letters(self) -> list:
        if len(self._candidate_letters) > self.MAX_CANDIDATE_LENGTH:
            raise ValueError(f'Too many candidate letters. Max characters supported is {self.MAX_CANDIDATE_LENGTH}')
        return self._candidate_letters

    @property
    def wordlist(self):
        """
        :return: The wordlist for the software.
        """
        if not self._wordlist:
            self._load_wordlist()
        return self._wordlist

    @wordlist.setter
    def wordlist(self, value: set):
        self._wordlist = value

    def _load_wordlist(self):
        if self.path_to_wordlist.is_file():
            with self.path_to_wordlist.open("r") as file:
                self._wordlist = {line.strip().lower() for line in file.readlines()}
                return
        elif self.path_to_wordlist is not None and len(str(self.path_to_wordlist)) > 2:
            raise FileNotFoundError(f"wordlist not found at {self.path_to_wordlist}")
        elif self._use_basic_wordlist:
            self._wordlist = self.basic_wordlist
        else:
            self._wordlist = self.full_wordlist

    def _add_match(self, word):
        with self.match_list_lock:
            self.match_list.add(word)

    def search(self):
        """
        Perform a search with multiple threads.

        :return: None
        """
        chunk_size = len(self.wordlist) // self.num_threads
        threads = []

        for i in range(self.num_threads):
            start_index = i * chunk_size
            end_index = None if i == self.num_threads - 1 else (i + 1) * chunk_size
            thread = threading.Thread(target=self._search_worker, args=(list(self.wordlist)[start_index:end_index],))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        print(f"{len(self.match_list):,} matches found.")
        print(f"{self.runtime.runtime_string}")
        self.runtime.write_runtime(as_json=True, file_path=self._rt_save_file_path)


    @staticmethod
    def _chunks(iterable, size):
        """
        Yield successive n-sized chunks from an iterable.

        :param iterable: The iterable to chunk.
        :param size: The size of each chunk.
        :return: Generator of chunks.
        """
        for i in range(0, len(iterable), size):
            yield iterable[i:i + size]

    def _get_words_per_column(self, **kwargs):
        words_per_column = kwargs.get('words_per_column', self.config.getint('SEARCH', 'words_per_column'))
        column_number = kwargs.get('column_number', self.config.getint('SEARCH', 'column_number'))

        if words_per_column >= 1 and column_number != 0:
            raise AttributeError('words_per_column and column number kwargs cannot be used at the same time.')
        elif words_per_column >= 1:
            column_number = int(len(self.match_list) / words_per_column)
            if column_number == 0:
                column_number = 1

        return column_number

    def print_matches(self, **kwargs):
        """
        Prints the list of matching words.

        :return: None
        """
        use_columns = kwargs.get('use_columns', self.config.getboolean('SEARCH', 'use_columns'))
        final_str = str()
        print("Matching Words:")
        if use_columns:
            column_number = self._get_words_per_column(**kwargs)

            for chunk in self._chunks(sorted(list(self.match_list)), column_number):
                print(f"\t{', '.join(chunk)}")
                final_str += f"\t{', '.join(chunk)}\n"
        else:
            for match in self.match_list:
                print(f"\t{match}")
                final_str += f"\t{match}\n"
        print(f"{len(self.match_list):,} matches found.")
        return final_str


if __name__ == '__main__':
    WD = WordDescramblerCore(candidate_letters='AndrewJamesMcSparron')#, use_basic_wordlist=True,)
    WD.search()
    WD.print_matches()