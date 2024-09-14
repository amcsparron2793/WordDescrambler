from WordDescramblerCore import WordDescramblerCore
from GUI import WordDescramblerGUI
from WDLogger import WDLogger


class WordDescrambler(WordDescramblerGUI, WordDescramblerCore):
    def __init__(self, **kwargs):
        self.logger = kwargs.get('logger',
                                 WDLogger().UseLogger(root_log_location='./logs',
                                                      project_name=self.__class__.__name__).logger)
        self.DEFAULT_CONFIG_PATH = './cfg/config.ini'
        self.logger.debug(F"DEFAULT_CONFIG_PATH set to : {self.DEFAULT_CONFIG_PATH}")
        WordDescramblerGUI.__init__(self, logger=self.logger)
        self.logger.info("WordDescramblerGUI initialized")
        WordDescramblerCore.__init__(self, candidate_letters=None, logger=self.logger)
        self.logger.info("WordDescramblerCore initialized")
        # TODO: add GUI options support
        # TODO: add except_hook logic to __init__

    def run_tool(self):
        self.candidate_letters = self._candidate_letters_value.get()
        self.logger.info(f'candidate letters submitted: {self.candidate_letters}')
        self.search()

        match_string = self.print_matches()

        self.show_results(match_string, len(self.match_list))


if __name__ == '__main__':
    wd = WordDescrambler()
    wd.pack_and_run()
