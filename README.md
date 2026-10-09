# Text Autocorrector for Error-Free Writing

An AI/NLP-based project that detects and corrects spelling mistakes in text.

## Features
- Detects misspelled words using a dictionary and edit distance
- Suggests the closest correct word
- Keeps capitalization and punctuation intact

## Tech Stack
- Python 3
- pyspellchecker

## Installation

```bash
git clone https://github.com/Swasan-vortex/text-autocorrector.git
cd text-autocorrector
python -m venv venv
venv\Scripts\activate
python -m pip install -r requirements.txt
```

## Usage

```bash
python corrector.py
```

## Example

```
Before: I realy like lerning about artifical inteligence.
After:  I really like learning about artificial intelligence.
```

## Future Work
- Grammar correction using a pre-trained T5 model
- Contextual corrections (their / there)
- Web interface using Streamlit

## Author
Swasan-vortex# text-auto-corrector
