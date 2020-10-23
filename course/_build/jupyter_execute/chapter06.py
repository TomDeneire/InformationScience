# Chapter 6: Indexing

## Searching

Very simply said, working with information often boils down to "searching stuff". Whether it be metadata stored in databases (e.g. searching a library catalogue), text stored in documents (e.g. a full-text search-engine for a website) or even multimedia information retrieval.

Searching and search optimization are a vast area of computer science distinct type of computational problem. For instance, Donald Knuth's monumental *The Art of Computer Programming" devotes an entire volume (3) to "Sorting and Searching". This means that we will only be able to briefly touch on the topic and, as always, from a very practical point of view.

At face value searching might seem easy. Let's look at finding a substring in a string. In Python, for instance, offers several ways to check for this:

my_string = "Hello world, this is me"
my_search = "me"
# one way
if my_search in my_string:
    print("Found!")
else:
    print("Not found")
# another way
if my_string.find(my_search) != -1:
    print("Found!")
else:
    print("Not found!")
# third way
from re import search
if search(my_search, my_string):
    print("Found!")
else:
    print("Not found!")


However, search operations can soon become complicated and especially time-consuming. One crucial issue is the quantity of data we need to search. The above example could afford to use a string method to look for a literal string, but obviously this is not realistic when you are searching for text millions of books (e.g. [Google Books contains >40.000.000 books](https://en.wikipedia.org/wiki/Google_Books)), or searching in huge metadata containers (e.g. [Spotify contains >50.000.000 songs](https://www.businessofapps.com/data/spotify-statistics/#:~:text=Source%3A%20Goodwater%20Capital-,Spotify%20Content%20Statistics,the%20largest%20music%20library%20available.)).

## Indexing

One way to deal with his issue is indexing. Simply said, an index is a data structure that improves the speed of data retrieval operations at the cost of additional writes and storage space to maintain the index data structure. 

Consider the following example. Let's say we have a large list of book titles and want to search them on a specific term.

Let's first use SQL and the STCV database from chapter 04 to make such a list.

import sqlite3
conn = sqlite3.connect('stcv.sqlite')
c = conn.cursor()
query = "select distinct title_ti from title"""
c.execute(query)
BOOK_TITLES = []
for title in c.fetchall():
    # *title = unpacking the tuple
    BOOK_TITLES.append(*title)
print(len(BOOK_TITLES), "titles")
for number, result in enumerate(BOOK_TITLES[100:110]):
    print(number + 100, '=', result)
conn.close()

Now let's consider the difference between searching for the word `English` with and without an index.

def make_word_index(corpus):
    index = {}
    for title in corpus:
        words = title.split(' ')
        for word in words:
            index.setdefault(word, [])
            index[word].append(title)
    return index

def search(search_string, index):
    # Note: global scoping can be dangerous!
    # Perhaps there are cleaner solutions than this?
    global BOOK_TITLES
    global BOOK_TITLES_INDEX
    if index:
        return BOOK_TITLES_INDEX[search_string]
    else:
        result = []
        for title in BOOK_TITLES:
            words = title.split(' ')
            if search_string in words:
                result.append(title)
        return result

BOOK_TITLES_INDEX = make_word_index(BOOK_TITLES)
result_no_index = search("English", False)
result_index = search("English", True)
for item in result_index:
    print(item)
print(result_no_index == result_index)


Obviously, the results of searching with and without a word index are the same. But what about the efficiency of the search? For this we can use Jupyter's handy feature `%timeit`: 

%timeit search("English", False)
%timeit search("English", True)


The difference is as large as microseconds versus nanoseconds! Remember, with STCV we are only search about 26,000 titles, but consider searching a collection like the Library of Congress, which holds over 170 million items... 

And of course, our example was only a simple one where we built an index that allowed to connect a word with a title. Real-world applications will often build several indices, cross-indices, include variant forms and allow for all kinds of complex searches such as searching with Boolean operators, proximity search, etcetera.

For instance, titles like "The Art of Computer Programming" and "Zen and the Art of Motorcycle Maintanance" could be turned into an AND-index like so:

from json import dumps
titles = ["The Art of Computer Programming", "Zen and the Art of Motorcycle Maintanance"]
AND_INDEX = {}
for title in titles:
    clean_title = title.casefold()
    for word in clean_title.split(' '):
        if not word in AND_INDEX:
            AND_INDEX[word] = {}
        for next_word in clean_title.split(' '):
            if not word == next_word:
                AND_INDEX[word].update({next_word: title})
print(dumps(AND_INDEX, indent=4))


In this way, searching with `AND` becomes easy in this index, e.g. books that combine "art" and "computer":

print(AND_INDEX["art"]["computer"])

## Excursus: Bitmap indexing

A lot more can be said about indexing. For one, you might wonder if indexing in itself might not lead to building overly large data structures that take up a lot of space and memory. As was clear from the above example of a combined index, indexing can quickly escalate.

One interesting technique to avoid such problems is bitmap indexing. [Wikipedia](https://en.wikipedia.org/wiki/Bitmap) says:

> In computing, a bitmap is a mapping from some domain (for example, a range of integers) to bits

Let's say you are a button factory and have produced 10,000,000 buttons of a certain type. Now you want to keep track of which buttons have been sold by recording their serial numbers. For instance:

from sys import getsizeof
import array

# using arrays which is more memory-efficient than lists
# https://docs.python.org/3/library/array.html
pens_sold = array.array('B', [1, 5, 10])
print(getsizeof(pens_sold), 'bytes')


So you need 67 bytes to store this information as a Python array. By the time all buttons have been sold the list will be this large:

all_pens_sold = array.array('L', [i for i in range(1,10000000)])
size = getsizeof(all_pens_sold) * 0.00000095367432
print(size, 'megabytes')


So you see, things can get out of hand quickly. But if you use a bitmapping system, things are radically different:

# setting a bit array here with array (https://docs.python.org/3/library/array.html)
# in real applications you should use https://pypi.org/project/bitmap/

import array

# a bit array of unsigned ints with bits 1, 5 and 10 set to 1 (= pens sold)
pens_sold = array.array('B', [0b1, 0b0, 0b0, 0b0, 0b1, 0b0, 0b0, 0b0, 0b0, 0b1])
print(getsizeof(pens_sold), 'bytes')

bitmap_of_all_pens_sold = array.array('B', [0b1 for i in range(1,10000000)])
size = getsizeof(bitmap_of_all_pens_sold) * 0.00000095367432
print(size, 'megabytes')


## Lucene

The leading software for indexing and searching text is definitely [Lucene](https://lucene.apache.org/). However, Lucene is a Java library, which is not easy to implement (especially crossplatform as would be the case in this course). 

There is a Python extension for accessing Java Lucene, called [PyLucene](https://lucene.apache.org/pylucene/). Its goal is to allow you to use Lucene's text indexing and searching capabilities from Python. Still, PyLucene is not a Lucene **port** but a Python **wrapper** around Java Lucene. PyLucene embeds a Java VM with Lucene into a Python process. This means that you still need Java Lucene to run PyLucene, and some additional tools (GNU `Make`, a C++ compiler, etc.).



## Whoosh

As text indexing/searching is bound to be really slow in Python (so it make good sense to stick to Java Lucene) there is no true pure-Python alternative to Lucene. However, there are some libraries that allow you to experiment with similar indexing/searching software.

One of these is [Whoosh](https://whoosh.readthedocs.io/en/latest/index.html), which is unfortunately no longer maintained. Still, the latest version, 2.7.4, still works fine for Python 3 and can easily be installed through `pip install Whoosh`.

In the [Whoosh introduction](https://whoosh.readthedocs.io/en/latest/intro.html) we read:

> **About Whoosh**
>- Whoosh is fast, but uses only pure Python, so it will run anywhere Python runs, without requiring a compiler.
>- By default, Whoosh uses the Okapi BM25F ranking function, but like most things the ranking function can be easily customized.
>- Whoosh creates fairly small indexes compared to many other search libraries.
>- All indexed text in Whoosh must be unicode.
>- Whoosh lets you store arbitrary Python objects with indexed documents.

> **What is Woosh**

>Whoosh is a fast, pure Python search engine library.

>The primary design impetus of Whoosh is that it is pure Python. You should be able to use Whoosh anywhere you can use Python, no compiler or Java required.

>Like one of its ancestors, Lucene, Whoosh is not really a search engine, it’s a programmer library for creating a search engine.

>Practically no important behavior of Whoosh is hard-coded. Indexing of text, the level of information stored for each term in each field, parsing of search queries, the types of queries allowed, scoring algorithms, etc. are all customizable, replaceable, and extensible.

Indeed, Whoosh is quite similar to Lucene, including its query language. It lets you connect terms with `AND` or `OR`, eleminate terms with `NOT`, group terms together into clauses with parentheses, do range, prefix, and wilcard queries, and specify different fields to search. By default it joins clauses together with `AND` (so by default, all terms you specify must be in the document for the document to match)

The following code shows you how to create and search a basic Whoosh index. For more information, see the [Whoosh quick start](https://whoosh.readthedocs.io/en/latest/quickstart.html) and documentation on the [query language](https://whoosh.readthedocs.io/en/latest/querylang.html).


"""
Whoosh quick start
Source: https://whoosh.readthedocs.io/en/latest/quickstart.html
"""

import os

from whoosh import highlight
from whoosh.index import open_dir, create_in
from whoosh.fields import Schema, STORED, ID, KEYWORD, TEXT
from whoosh.qparser import QueryParser
from whoosh.query import *

# Create schema
"""
To begin using Whoosh, you need an index object. The first time you create
an index, you must define the index’s schema. The schema lists the fields in
the index. A field is a piece of information for each document in the index,
such as its title or text content. A field can be indexed (meaning it can be
searched) and/or stored (meaning the value that gets indexed is returned with
the results; this is useful for fields such as the title).
"""

schema = Schema(title=TEXT(stored=True), content=TEXT(stored=True),
                path=ID(stored=True))

# Create index
"""
Once you have the schema, you can create an index.
At a low level, this creates a Storage object to contain the index.
A Storage object represents that medium in which the index will be stored.
Usually this will be FileStorage, which stores the index as a set of files
in a directory.
"""

if not os.path.exists("index"):
    os.mkdir("index")
ix = create_in("index", schema)

# Add documents
"""
OK, so we’ve got an Index object, now we can start adding documents.
The writer() method of the Index object returns an IndexWriter object that
lets you add documents to the index. The IndexWriter’s add_document(**kwargs)
method accepts keyword arguments where the field name is mapped to a value.

The documents we add, a small corpus of British fiction, are part of
the chapter06 repo.
"""

OS_SEP = os.sep  # take care, different OS use different filepath separators!

writer = ix.writer()

for document in os.listdir("corpus_of_british_fiction"):
    with open("corpus_of_british_fiction" + OS_SEP + document, 'r') as text:
        writer.add_document(title=document, content=str(text.read()),
                            path=document)
writer.commit()


# Parse a query string
"""
Woosh's Searcher (cf.infra) takes a Query object. You can construct query
objects directly or use a query parser to parse a query string.
To parse a query string, you can use the default query parser in the qparser
module. The first argument to the QueryParser constructor is the default field
to search. This is usually the "body text" field. The second optional argument
is a schema to use to understand how to parse the fields.
"""
myquery = QueryParser("content", ix.schema).parse('smattering')

# Search documents
"""
Once you have a Searcher and a query object, you can use the Searcher's
search() method to run the query and get a Results object. You can use the
highlights() method on the whoosh.searching.Hit object to get highlighted
snippets from the document containing the search terms.
"""
with ix.searcher() as searcher:
    results = searcher.search(myquery, limit=None)
    # https://whoosh.readthedocs.io/en/latest/highlight.html#the-character-limit
    results.fragmenter.charlimit = None
    for hit in results:
        print(hit.highlights("content", top=5))

## Assignment: Morphology tool

Use Whoosh to teach English morphology with examples from a given corpus. For instance, through the rules of morphology verbs can take different forms or be used to form nouns, adjectives and such, like:

- `render`: 'renders', 'rendered', 'rendering'
- `think`: 'thinks', 'thought', 'thinking', 'thinker', 'thinkers', 'thinkable'
- `put`: 'puts', 'putting', 'putter'
- `do`: 'does', 'did', 'done', 'doing', 'doings', 'doer', 'doers'

Forms like `put` and `do` illustrate that you cannot approach this problem in a mechanical or brute-force way. It is not as simple as adding 'ed', 'ing', etcetera to the verbs. Sometimes consonants are doubled, sometimes the verb stem changes (in the case of strong verbs), and so on.

Whoosh has a particular feature to deal with this. Use it to build a Python application that takes a word as input and returns a list of sentences from the British fiction corpus (folder `corpus_of_british_fiction` in this repo) that contain this word to illustrate its usage. Think about building the index first, so you can then reuse it (without having to rebuild it) for additional searches.

Also, try to display the results nicely, i.e. without the markup tags we saw in the above example. Maybe you can even print the matched word in bold?

If this is an easy task for you, try to convert this approach to look for examples of phrasal verbs, i.e. "to put off" (variant forms 'put off', 'puts off', 'putting off', etcetera)