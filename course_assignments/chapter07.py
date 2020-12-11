"""
Assignment for chapter07
"""

import os
import json

from chapter03 import onegrams
from jarowinkler import jaro_winkler


def build_dictionary(folder: str, dict_file: str) -> None:
    """
    Build a dictionary from a folder of text files
    and save it as a JSON file on disk.
    """
    dict_of_onegrams = {}
    for document in os.listdir(folder):
        if document.endswith(".txt"):
            words = onegrams(os.path.join(folder, document))
            dict_of_onegrams.update(words)
    with open(dict_file, 'w') as dictionary:
        dictionary.write(json.dumps(dict_of_onegrams))


def read_dictionary(dict_file: str) -> dict:
    """
    Read a JSON dictionary file and return it as Python dictionary
    """
    try:
        with open(dict_file, 'r') as dictionary:
            return json.loads(dictionary.read())
    except FileNotFoundError as err:
        exit(err)


def check(user_text: str, dictionary: dict) -> None:
    """
    Check user text and print suggestions for unrecognized words
    """
    # build tempfile for onegrams()
    with open("tempfile.txt", 'w') as tempfile:
        tempfile.write(user_text)
    words = onegrams("tempfile.txt")
    # remove tempfile
    os.remove("tempfile.txt")
    for word in words:
        if word not in dictionary:
            suggestions = [s for s in dictionary if jaro_winkler(word, s) > 0.9]
            if len(suggestions) > 0:
                print(word, "->", suggestions)
            else:
                print(word, "->", "No suggestions")


if __name__ == "__main__":
    DICTIONARY_FILE = "dict.json"
    CORPUS = "corpus_of_british_fiction"
    command = input("Build dictionary (B) or check spelling (C)? ")
    if command == "B":
        build_dictionary(CORPUS, DICTIONARY_FILE)
    if command == "C":
        dictionary = read_dictionary(DICTIONARY_FILE)
        to_check = input("\nText to check: ")
        print("\n")
        check(to_check, dictionary)
    else:
        exit()


"""
Some points to take away from this assignment:

    1. Using your own modules can be very helpful to create maneagable code
    files. This is why refactoring is so important. It follows the UNIX
    philosophy of building simple, short, clear, modular, and extensible code
    that does one thing and does one thing well.

    2. Because of the compatibility JSON <-> Python dict, JSON is a good choice
    for reading/writing a small database of permanent data in Python.
"""
