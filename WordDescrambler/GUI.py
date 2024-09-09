import tkinter as tk
from WordDescrambler import WordDescrambler


class WordDescramblerGUI:
    """
    This module provides a graphical user interface (GUI) for the Word Descrambler program.
    It allows users to input candidate letters and submit them for descrambling.

    Classes:
        - WordDescramblerGUI: A class that represents the GUI for the Word Descrambler program.

    Methods:
        - __init__(self): Initializes the WordDescramblerGUI object and sets up the main window.
        - initialized_widgets(self): Returns a list of all initialized widgets in the GUI.
        - init_widgets(self): Initializes the required widgets for the GUI.
        - pack_widgets(self): Packs all initialized widgets into the main window.
        - pack_and_run(self): Packs all initialized widgets into the main window and starts the main event loop.

    Usage:
        To use the WordDescramblerGUI class, create an instance of it and call the pack_and_run() method.
        This will display the GUI and start the main event loop.

    Example:
        descrambler_gui = WordDescramblerGUI()
        descrambler_gui.pack_and_run()

    Attributes:
        - TITLE_TEXT: A string representing the title text for the main window.
    """
    TITLE_TEXT = "Word Descrambler"

    def __init__(self):
        self._main_title_label = None
        self._candidate_letters_value = None
        self._candidate_letters_label = None
        self._submit_button = None
        self._options_button = None
        self._initialized_widgets = None
        self._close_options_button = None
        self.options_window = None

        self.main_window = tk.Tk()
        self.main_window.title(self.TITLE_TEXT)

        self.init_main_widgets()

    def main_submit_pressed(self):
        # FIXME: this throws a file not found error when trying to write to ./Misc_Project_File
        #  config is being rewritten into ./WordDescrambler/cfg/config.ini - that's why this is happening i think?
        wd = WordDescrambler(self._candidate_letters_value.get())
        wd.search()
        wd.print_matches()
        print('submit was pressed')

    def options_pressed(self):
        self.options_window = tk.Tk('Options')
        self.init_options_widgets()
        for widget in self.options_window.winfo_children():
            widget.pack()
        print('options was pressed')

    @property
    def initialized_widgets(self):
        # FIXME: how do i add in secondary windows after the fact?
        self._initialized_widgets = [x for x in self.main_window.winfo_children()]
        return self._initialized_widgets

    def init_options_widgets(self):
        self._close_options_button = tk.Button(master=self.options_window, name='close_options_button',
                                              text='Close',
                                              command=self.options_window.destroy)



    def init_main_widgets(self):
        self._main_title_label = tk.Label(self.main_window, text=self.TITLE_TEXT,
                                          name='main_title')
        self._candidate_letters_label = tk.Label(self.main_window,
                                                 text='Candidate Letters',
                                                 name='candidate_letters_label')
        self._candidate_letters_value = tk.Entry(self.main_window,
                                                 name='candidate_letters')
        self._submit_button = tk.Button(master=self.main_window,
                                        text="Submit",
                                        name="submit_button",
                                        command=self.main_submit_pressed)
        self._options_button = tk.Button(master=self.main_window,
                                         text="Options",
                                         name="options_button",
                                         command=self.options_pressed)

    def pack_widgets(self):
        for widget in self.initialized_widgets:
            widget.pack()

    def pack_and_run(self):
        self.pack_widgets()
        self.main_window.mainloop()

if __name__ == '__main__':
    wd_GUI = WordDescramblerGUI()
    wd_GUI.pack_and_run()
