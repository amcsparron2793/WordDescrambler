import tkinter as tk

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

        self.main_window = tk.Tk()
        self.main_window.title(self.TITLE_TEXT)
        self.init_widgets()

    @property
    def initialized_widgets(self):
        self._initialized_widgets = [x for x in self.main_window.winfo_children()]
        return self._initialized_widgets

    def init_widgets(self):
        self._main_title_label = tk.Label(self.main_window, text=self.TITLE_TEXT,
                                          name='main_title')
        self._candidate_letters_label = tk.Label(self.main_window,
                                                 text='Candidate Letters',
                                                 name='candidate_letters_label')
        self._candidate_letters_value = tk.Entry(self.main_window,
                                                 name='candidate_letters')
        self._submit_button = tk.Button(master=self.main_window, text="Submit", name="submit_button")
        self._options_button = tk.Button(master=self.main_window, text="Options", name="options_button")


    def pack_widgets(self):
        for widget in self.initialized_widgets:
            widget.pack()

    def pack_and_run(self):
        self.pack_widgets()
        self.main_window.mainloop()

if __name__ == '__main__':
    wd = WordDescramblerGUI()
    wd.pack_and_run()
