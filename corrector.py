import re
from spellchecker import SpellChecker

spell = SpellChecker()

def correct_text(text):
    # Text ko words aur punctuation mein todna
    parts = re.findall(r"[A-Za-z']+|[^A-Za-z']+", text)
    result = []
    for part in parts:
        if part.isalpha() and part.lower() in spell.unknown([part.lower()]):
            fix = spell.correction(part.lower())
            if fix:
                part = fix.capitalize() if part[0].isupper() else fix
        result.append(part)
    return "".join(result)

if __name__ == "__main__":
    sample = "I realy like lerning about artifical inteligence."
    print("Before:", sample)
    print("After: ", correct_text(sample))