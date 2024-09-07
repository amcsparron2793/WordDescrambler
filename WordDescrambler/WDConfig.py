from BetterConfigAJM import BetterConfigAJM
from pathlib import Path

class WordDescramblerConfig(BetterConfigAJM):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.default_config = [{
            'DEFAULT': {
                'use_all_letters': False,
                'use_basic_wordlist': False
            },
            'RUNTIME': {
                'use_timedelta': False,
                'save_file_path': './Misc_Project_Files/last_runtime.txt'
            },
            'RUNTIME_OUTPUT': {
                'as_json': True,
                'as_text': False
            }
        }]
        if 'config_list_dict' in kwargs:
            self.config_list_dict = kwargs['config_list_dict']
        else:
            self.config_list_dict = self.default_config
        # making this resolve to an absolute path
        self.config_location = Path(self.config_location).resolve()
