from typing import List, Tuple

import nltk

# try:
#     nltk.data.find("tokenizers/punkt")
# except LookupError:
#     nltk.download("cmudict")
# try:
#     nltk.data.find("tokenizers/punkt")
# except LookupError:
#     nltk.download("punkt")
from nltk.tokenize import word_tokenize
from nltk.corpus import cmudict
from g2p_en import G2p

from ..constants import G2P_PHONEMES_TO_SAY_PHONEMES


G2P = None
CMU = None


def word_to_g2p_phonemes(text: str) -> List[str]:
    global G2P
    if not G2P:
        G2P = G2p()
    return G2P(text)


def word_to_say_phonemes(text: str) -> List[str]:
    return [G2P_PHONEMES_TO_SAY_PHONEMES.get(p, "") for p in word_to_g2p_phonemes(text)]


def word_to_syllable_count(word: str) -> int:
    global CMU
    if not CMU:
        CMU = cmudict.dict()
    try:
        return [len(list(y for y in x if y[-1].isdigit())) for x in CMU[word.lower()]][
            0
        ]
    except KeyError:
        # if word not found in cmudict
        # referred from stackoverflow.com/questions/14541303/count-the-number-of-syllables-in-a-word
        count = 0
        vowels = "aeiouy"
        word = word.lower()
        if word[0] in vowels:
            count += 1
        for index in range(1, len(word)):
            if word[index] in vowels and word[index - 1] not in vowels:
                count += 1
        if word.endswith("e"):
            count -= 1
        if word.endswith("le"):
            count += 1
        if count == 0:
            count += 1
        return count


def process_text_for_say(text) -> List[Tuple[int, List[str], str]]:
    """
    Get a list of phonemes + syllable counts for each word in a text
    """
    return [
        (word_to_syllable_count(word), word_to_say_phonemes(word), word)
        if word not in [",", ".", "?", "!", "-", ":", ";"]
        else (1, ["%"], "")  # silence
        for word in word_tokenize(text)
    ]
