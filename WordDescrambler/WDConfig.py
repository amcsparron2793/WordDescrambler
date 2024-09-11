from BetterConfigAJM import BetterConfigAJM
from pathlib import Path

class WordDescramblerConfig(BetterConfigAJM):
    def __init__(self, *args, **kwargs):
        self.default_config = [{
            'DEFAULT': {
                'use_all_letters': False,
                'limit_length': 0,
                'min_match_length': 3,
                'verbose_mode': False
            },
            'RUNTIME': {
                'use_timedelta': True,
                'save_file_path': './Misc_Project_Files/last_runtime.txt'
            },
            'RUNTIME_OUTPUT': {
                'as_json': True,
                'as_text': False
            },
            'WORDLIST': {
                'path_to_wordlist': '',
                'use_basic_wordlist': False,

            },
            'SEARCH': {
                'print_matches': True,
                'use_columns': True,
                'words_per_column': 0,
                'column_number': 3
            }
        }]
        super().__init__(*args, **kwargs)

        if 'config_list_dict' in kwargs:
            self.config_list_dict = kwargs['config_list_dict']
        else:
            self.config_list_dict = self.default_config
        # making this resolve to an absolute path
        self.config_location = Path(self.config_location).resolve()
