from WordDescramblerCore import WordDescramblerCore
from GUI import WordDescramblerGUI

class WordDescrambler(WordDescramblerGUI, WordDescramblerCore):
    def __init__(self):
        super().__init__()

    def run_tool(self):
        WordDescramblerCore.__init__(self, candidate_letters=self._candidate_letters_value.get())
        # FIXME: bug where config.ini doesnt work?
        self.search()

        match_string = self.print_matches()

        self.show_results(match_string, len(self.match_list))

if __name__ == '__main__':
    wd = WordDescrambler()
    wd.pack_and_run()
