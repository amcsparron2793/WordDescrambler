import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from logging import getLogger


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

    def __init__(self, **kwargs):
        self.logger = kwargs.get('logger', getLogger('dummy_logger'))
        self._main_title_label = None
        self._candidate_letters_value = None
        self._candidate_letters_label = None
        self.results_info = None
        self._submit_button = None
        self._options_button = None
        self._quit_button = None
        self._initialized_widgets = None
        self._close_options_button = None
        self.options_window = None
        self.results_window = None
        self._config_options = kwargs.get('config_options', {})

        self.main_window = tk.Tk()
        self.main_window.title(self.TITLE_TEXT)

        self.init_main_widgets()
        self.logger.info(f'{self.__class__.__name__} initialized')

    def _main_submit_pressed(self):
        self.logger.debug('submit button pressed')
        if self._candidate_letters_value.get() == '':
            messagebox.showerror("Please enter candidate letters",
                                 "Please enter candidate letters and submit again.")
            self.logger.warning("candidate letters cannot be None")
        else:
            self.run_tool()

    def run_tool(self):
        raise NotImplemented("this needs to be overwritten to function")

    def show_results(self, results_info, number_of_matches):
        self.results_window = tk.Tk('Results')
        self.init_results_widgets(results_info=results_info, number_of_matches=number_of_matches)

    def options_pressed(self):
        self.logger.debug('options was pressed')
        self.options_window = tk.Tk('Options')
        self.init_options_widgets()
        self.logger.info('all options widgets initialized and packed')

    @property
    def initialized_widgets(self):
        # FIXME: how do i add in secondary windows after the fact?
        self._initialized_widgets = [x for x in self.main_window.winfo_children()]
        self.logger.info(f"{len(self._initialized_widgets)} widgets initialized")
        self.logger.debug(f"including {self._initialized_widgets}")
        return self._initialized_widgets

    def init_options_widgets(self):
        # FIXME: this doesnt work exactly right, see output.
        for idx, (name, default) in enumerate(self._config_options):
            # Create a label for the option
            label = ttk.Label(self.options_window, text=name)
            label.grid(row=idx, column=0, padx=10, pady=5)

            # Create an entry widget for the option
            entry = ttk.Entry(self.options_window)
            entry.insert(0, default)
            entry.grid(row=idx, column=1, padx=10, pady=5)

        self._close_options_button = tk.Button(master=self.options_window, name='close_options_button',
                                              text='Close',
                                              command=self.options_window.destroy)

    def init_results_widgets(self, results_info, number_of_matches:int):
        self.results_info = tk.Text(self.results_window, name='results_info')#,text=results_info)
        self.results_info.insert(tk.END, f"{number_of_matches:,} Results:\n")
        self.results_info.insert(tk.END, results_info)
        self.results_close_button = tk.Button(master=self.results_window,
                                              name='results_close_button',
                                              text='Close',
                                              command=self.results_window.destroy)
        self.logger.info('results window widgets initialized')
        for widget in self.results_window.winfo_children():
            widget.pack()
        self.logger.info('results window widgets packed')

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
                                        command=self._main_submit_pressed)
        self._options_button = tk.Button(master=self.main_window,
                                         text="Options",
                                         name="options_button",
                                         command=self.options_pressed)
        self._quit_button = tk.Button(master=self.main_window,
                                         text="Quit",
                                         name="quit_button",
                                         command=self.main_window.quit)

        self.logger.info('main window widgets initialized')


    def pack_widgets(self):
        for widget in self.initialized_widgets:
            widget.pack()
        self.logger.info('all initialized widgets packed')


    def pack_and_run(self):
        self.pack_widgets()
        self.logger.info('widgets packed and main window starting...')
        self.main_window.mainloop()

