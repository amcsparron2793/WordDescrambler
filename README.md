# Word Descrambler

## Overview

The **Word Descrambler** is a Python-based tool designed to descramble words based on a given set of candidate letters. It utilizes a configurable runtime environment and wordlist to find and output potential matches.

## Features

- Configurable runtime settings via an INI file.
- Supports descrambling with various constraints (length, verbose mode, etc.).
- Leverages both basic and full wordlists for matching.
- Outputs results in text and JSON formats.
- Runtime performance tracking.

## Installation

1. Ensure you have Python 3.12.3 installed on your system.
2. Install the required dependencies using pip:

    ```bash
    pip install click nltk
    ```

3. Download or clone the project repository to your local machine.

## Configuration

The configuration is managed through an INI file located at `./cfg/config.ini`. You can customize the settings to fit your needs. The project is designed to look for this configuration file by default, but you can specify a different path if needed.

### Example Configuration File (`config.ini`)

```ini
[RUNTIME]
use_timedelta = True
save_file_path = ./results/words.txt

[RUNTIME_OUTPUT]
as_json = True
as_text = True

[DEFAULT]
use_all_letters = False
limit_length = 10
min_match_length = 3
verbose_mode = False

[SEARCH]
print_matches = True

[WORDLIST]
use_basic_wordlist = False
path_to_wordlist = ./wordlists/default.txt
```

## Usage

### Command Line Interface

You can use the Word Descrambler via the command line:

```bash
python word_descrambler.py --letters "example"
```

### Script

Here's an example of how to utilize the `WordDescrambler` class in your Python scripts:

```python
from pathlib import Path
from WordDescrambler.WordDescrambler import WordDescrambler

# Configuration and candidate letters
candidate_letters = "example" 
config_path = Path("./cfg/config.ini")

# Instantiate and run the word descrambler
descrambler = WordDescrambler(candidate_letters, config_path, use_timedelta=True)
descrambler.search()
descrambler.print_matches()
```

## Classes and Methods

### `WordDescrambler` Class

#### Constructor

```python
def __init__(self, candidate_letters: str, path_to_wordlist: Path or str = None, **kwargs):
    ...
```

- `candidate_letters (str)`: The set of candidate letters used to descramble words.
- `path_to_wordlist (Path or str, optional)`: The path to a wordlist file. If not provided, the default wordlist will be used. Defaults to None.
- `**kwargs (optional)`: Additional keyword arguments to customize runtime settings.

#### Methods

- `_load_config(config_full_file_location: str) -> ConfigParser`
- `_initialize_runtime_settings(kwargs: dict)`
- `_extract_candidate_letters(letters: str) -> list`
- `_initialize_wordlists()`
- `search(self, **kwargs)`: Search for words based on the candidate letters and print the matches.
- `print_matches(self, **kwargs)`: Print the matched words.

### `WordDescramblerConfig` Class

Handles the loading and parsing of configuration settings from the INI file.

### `Runtime` Class

Tracks runtime performance and provides runtime statistics.

## Contributing

1. Fork the repository.
2. Create a new branch: `git checkout -b feature/your-feature`.
3. Make your changes and commit them: `git commit -m 'Add some feature'`.
4. Push the changes to your branch: `git push origin feature/your-feature`.
5. Open a pull request.

