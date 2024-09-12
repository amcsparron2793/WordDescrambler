from WordDescramblerCore import WordDescramblerCore
from GUI import WordDescramblerGUI

class WordDescrambler(WordDescramblerGUI, WordDescramblerCore):
    def __init__(self):
        super().__init__()

    def run_tool(self):
        WordDescramblerCore.__init__(self, candidate_letters=self._candidate_letters_value.get())
        # FIXME: config works properly when running WordDescramblerCore, NOT here though
        #  something like this should work:
        #     class WordDescrambler(WordDescramblerGUI, WordDescramblerCore):
        #         def __init__(self):
        #             WordDescramblerGUI.__init__(self)
        #             WordDescramblerCore.__init__(self,
        #                                          candidate_letters=None)  # Initializing WordDescramblerCore with appropriate arguments
        #
        #         def run_tool(self):
        #             self.set_candidate_letters(self._candidate_letters_value.get())
        #             self.search()
        #
        #             match_string = self.print_matches()
        #
        #             self.show_results(match_string, len(self.match_list))
        #
        #         def set_candidate_letters(self, candidate_letters):
        #             # Ensure candidate letters are set for WordDescramblerCore
        #             self.candidate_letters = candidate_letters
        self.search()

        match_string = self.print_matches()

        self.show_results(match_string, len(self.match_list))

if __name__ == '__main__':
    wd = WordDescrambler()
    wd.pack_and_run()
