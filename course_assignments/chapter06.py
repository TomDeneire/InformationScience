"""
Assignment chapter 06
"""

import re
import os
import sys
from typing import Iterator

from whoosh import highlight
from whoosh.index import create_in, Index
from whoosh.lang import morph_en
from whoosh.fields import Schema, ID, TEXT
from whoosh.qparser import QueryParser


def make_index(documents_dir: str) -> Index:
    """
    Make index schema, folder, index and add documents from documents_dir
    """
    print("Building index...")
    # Create schema
    schema = Schema(title=TEXT(stored=True),
                    content=TEXT(stored=True),
                    path=ID(stored=True))
    # Create index
    if not os.path.exists("index"):
        os.mkdir("index")
    index_of_documents = create_in("index", schema)
    # Add documents
    writer = index_of_documents.writer()
    for document in os.listdir(documents_dir):
        if document.endswith(".txt"):
            with open(os.path.join(documents_dir, document), 'r') as text:
                writer.add_document(title=document,
                                    content=text.read(),
                                    path=document)
    writer.commit()
    print("Index finished")
    return index_of_documents


def query_index(query: str, index: Index) -> Iterator[tuple]:
    """
    Parse query string, search documents, fragment results as sentences,
    extract highlights from results
    """
    # Parse query string
    parser = QueryParser("content", schema=index.schema)
    myquery = parser.parse(query)
    # Search documents
    with index.searcher() as searcher:
        results = searcher.search(myquery, limit=None)
        # set sufficiently large maxchars to account for long sentences
        results.fragmenter = highlight.SentenceFragmenter(charlimit=None,
                                                          maxchars=2000)
        for hit in results:
            sentences = hit.highlights("content").split("...")
            # Using a generator instead of list, as large corpora
            # could result in returning a very large list
            yield (hit["title"], sentences)


def pretty(to_clean: str, variation: str) -> str:
    """
    Clean tags, line breaks and whitespace. Highlight hit in bold.
    """
    sub_no_space = [r'\<b.*?>', r'\<\/b>']
    sub_space = ['\n', '\t']
    for item in sub_space + sub_no_space:
        if item in sub_no_space:
            to_clean = re.sub(item, '', to_clean)
        else:
            to_clean = to_clean.replace(item, " ", -1)
    to_clean = clean_multiple_spaces(to_clean)
    # Using UNIX terminal codes for bold, see `man console_codes`
    if sys.platform == "linux":
        bold = '\033[1m' + variation + '\033[0m'
        to_clean = to_clean.replace(variation, bold, -1)
    return to_clean


def clean_multiple_spaces(to_clean: str) -> str:
    """
    Remove multiple spaces recursively
    """
    if "  " not in to_clean:
        return to_clean
    else:
        to_clean = to_clean.replace('  ', ' ', -1)
        return clean_multiple_spaces(to_clean)

# APPLICATION


if __name__ == "__main__":
    INDEX = make_index("corpus_of_british_fiction")
    my_query = ""
    while not my_query == "q:":
        my_query = input("Type word (or q: to quit): ")
        if my_query == 'q:':
            exit()
        else:
            for variation in morph_en.variations(my_query):
                for title, sentences in query_index(variation, INDEX):
                    for sentence in sentences:
                        sentence = pretty(sentence, variation)
                        print(sentence, f"({title})\n")


"""
Some points to take away from this assignment:

    1. Try to do time-intensive operations like building an index only once
    in your code.

    2. Try to write code that is cross-platform, or at least does not break
    when executed on a different platform than yours (e.g. os.path.join,
    sys.platform, ...)

    3. Especially for data science: account for large data structures (e.g.
    use of generator instead of list)

    4. In Python everything is an object. All of the modules in the Whoosh
    library returned an object with its own specific methods. Understanding
    this OOP design of Python will help a lot when reading documentation for
    external libraries.
"""
