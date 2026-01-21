# pipelines/query/normalize.py
from spellchecker import SpellChecker

_spell = SpellChecker()

def normalize_query(query: str) -> str:
    corrected = []
    for word in query.split():
        if word.lower() in _spell:
            corrected.append(word)
        else:
            corrected.append(_spell.correction(word) or word)
    return " ".join(corrected)
