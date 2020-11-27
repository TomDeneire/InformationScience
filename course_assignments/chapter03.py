"""
Assignment chapter 03
"""

import unicodedata


def clean(to_clean: str) -> str:
    """
    Remove unnecessary characters. Note: this is language specific!
    e.g. apostrophe is allowed in English (e.g. don't),
    but you can debate whether this is a separate word or not,
        e.g. "Dora's book" -> "Dora's" should not be become: "Dora" + "s"
    but "he said: 'Captain, ..." -> "'Captain" should become "Captain"!
    Therefore we deal with the apostrophe in the split() function.
    We keep numbers and such, this is also debatable.
    """
    for punc in "!\"#$%&()*+,-./:;<=>?@[\\]^_`{|}~\n":
        # checking for efficiency
        check = to_clean.count(punc)
        if check:
            to_clean = to_clean.replace(punc, " ", check)
    return to_clean


def normalize(word: str) -> str:
    """
    Normalize a word (remove case, whitespace, handle accents, ...)
    """
    word = word.casefold()
    word = word.strip()
    word = unicodedata.normalize("NFC", word)
    return word


def split(line: str) -> list:
    """
    Split a line into words, and deal with the ' apostrophe
    """
    words = []
    for word in line.split(' '):
        # Account for multiple spaces
        if word not in ["", " "]:
            # Account for ' apostrophe, but not perfectly:
            # remove at the start of word (e.g. he said: 'Captain,)
            #   however: 'tis -> should actually be kept
            # leave it elsewhere (e.g. goin', I'm, or genitive: students')
            #   however: closing single quote should actually be kept
            # Comment this code out and look at the difference for "the"
            if word[0] == "'":
                word = word.strip("'")
            words.append(word)
    return words


def onegrams(file: str) -> dict:
    """
    Extract onegrams from a text file
    """
    dict_of_onegrams = {}
    with open(file, 'r') as lines:
        # Do not use .readlines() or .read()
        # as both read the entire file in memory!
        for line in lines:
            # Clean lines not words!
            # Otherwise e.g. 'they would only answer--"Well, boys, here's the ark!"'
            # would yield words 'they', 'would', 'only', 'answer--"well', ...
            line = clean(line)
            words = split(line)
            for word in words:
                word = normalize(word)
                # If you don't know the setdefault-method, read this:
                # https://www.w3schools.com/python/ref_dictionary_setdefault.asp
                # it solves the `KeyError` you can get
                dict_of_onegrams.setdefault(word, 0)
                dict_of_onegrams[word] += 1
    return dict_of_onegrams


def show_most_common(onegrams: dict, count: int) -> None:
    """Print x most common entries from dictionary of onegrams"""
    # lambda function sorts objects using the object's indices
    # you can choose the variable name (e.g. x: x[1], item: item[1], etc.)
    # alternatively, you can use itemgetter() from the operator module
    onegrams_sorted = sorted(onegrams.items(),
                             key=lambda item: item[1], reverse=True)
    # sorted() always returns list!
    for index, item in enumerate(onegrams_sorted):
        if index < count:
            print(index + 1, item)


# Only run this part when namespace is "__main__"
# https://www.freecodecamp.org/news/if-name-main-python-example/
if __name__ == "__main__":
    dict_of_onegrams = onegrams('/home/tdeneire/projects/InformationScience/course/data/corpus.txt')
    show_most_common(dict_of_onegrams, 100)


"""
Some points to take away from this assignment:

    1. As pointed out in chapter03, handling data, including text, is always
    manipulating it and involves choices. So be careful and above all,
    be aware of this and (esp. in research) communicate about this manipulation!
    This exercise was not so much about getting the count right (which is
    debatable anyway, see the apostrophe question) but about questioning how
    to treat text when extracting words.

    2. Write clean code: use descriptive variable names (not `for x in ...`),
    break up your code into functions, use code comments, ...

    3. Write generic code: try to make your code so it is reusable later on
    in a different context, that it will run regardless of what OS you use,
    that it also works for 1 GB files instead of 1 MB files, ...

    4. It is usually recommended to try to the use the Python standard library
    as much as possible. Of course, you will often need to go beyond this.
    For this assignment, for instance, it was possible to take benefit from
    the `nltk` module.

    5. You can also use regular expressions to solve this, but remember that
    regular expressions are slow and often do not do quite what you want or
    expect. We will talk about regular expressions later on.

    6. Python is very versatile which means there are always several ways to
    implement something. Sometimes one way is better than other, sometimes it
    is equivalent. A lot of the times it will depend on your purpose (quick
    code, easy to write code, easy to read code, ...)
"""
