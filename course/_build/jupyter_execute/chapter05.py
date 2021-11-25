# Chapter 5: Querying Information

## Query languages

Database operations can be summarized with the acronym `CRUD`: create, read, update and delete. From an information standpoint, the main focus is reading from the database. Most often though, we do not read directly as this is not possible (not all databases can be browsed), or practical (we get too much information). Instead, reading databases is usually done through **querying**, for which we use [query languages](https://en.wikipedia.org/wiki/Query_language). 

Actually, query languages surpass databases. Formally, query languages can be classified according to whether they are **database query languages** or **information retrieval query languages**. The difference is that a database query language attempts to give factual answers to factual questions, while an information retrieval query language attempts to find documents containing information that is relevant to an area of inquiry. 

For the latter we will discuss CQL, for the former SQL.

### CQL

Let's start with an example of an information retrieval query language: contextual query language or CQL. According to [Wikipedia](https://en.wikipedia.org/wiki/Contextual_Query_Language)

>Contextual Query Language (CQL), previously known as Common Query Language, is a formal language for representing queries to information retrieval systems such as search engines, bibliographic catalogs and museum collection information. (...) its design objective is that queries be human readable and writable, and that the language be intuitive while maintaining the expressiveness of more complex query languages. It is being developed and maintained by the Z39.50 Maintenance Agency, part of the Library of Congress.

Querying with CQL operates via SRU - Search/Retrieve via URL, which is an XML-based protocol for search queries.

You can find the specifications for [SRU](http://www.loc.gov/standards/sru/index.html) and [CQL](https://www.loc.gov/standards/sru/cql/spec.html) at the Library of Congress website. 

A fun example of an API that supports SRU/CQL is the [CERL (Consortium of European Research Libraries)](https://cerl.org/), which is responsible for the [CERL Thesaurus](https://data.cerl.org/thesaurus/_search), containing forms of imprint places, imprint names, personal names and corporate names as found in material printed before the middle of the nineteenth century - including variant spellings, forms in Latin and other languages, and fictitious names.

Below is an example of how to query this API with SRU/SQL from Python:

import urllib

CERL_THESAURUS = "https://data.cerl.org/thesaurus/_sru?version=1.2&operation=searchRetrieve&query="

def clean(string: str) -> str:
    """
    Clean input string and URL encode (e.g. Léon Degrelle)
    """
    string = '"' + string + '"'
    string = string.strip()
    string = string.casefold()
    string = urllib.parse.quote(string)
    return string


def query_Europeana(search: str) -> bytes:
    """
    Query Europeana Entities API, return response or exit with errorcode
    """
    search = clean(search)
    url = CERL_THESAURUS + search
    try:
        with urllib.request.urlopen(url) as query:
            return query.read()
    except urllib.error.HTTPError as HTTPerr:
        exit(HTTPerr.code)
    except urllib.error.URLError as URLerr:
        exit(URLerr)

user_input = input()
print(str(query_Europeana(user_input)[0:1000]) + "...")

### SQL/SQLite

SQL is a technology that is probably new to most of you. Unlike RDF, which libraries seem hesitant to adopt, SQL is ubiquitous, including outside of libraries. Moreover, SQL has for instance heavily influenced the aforementioned CQL, and also [SPARQL](https://en.wikipedia.org/wiki/SPARQL) , the query language for RDF. So knowing SQL will open many doors.

SQL is the query language for RDBMS, which are most often implemented in a *client-server* database engine. So for you to use SQL you would need a connection to a SQL database server, i.e. something like MySQL or PostgreSQL. However, there is also a very good standalone alternative, called [SQLite](https://en.wikipedia.org/wiki/SQLite). Simply said SQLite is just a single file, but you can query it just like a SQL database server. There are some minute differences between SQL syntax and the SQLite dialect, but these are really small. (If you want to know more about SQLite, I wrote this [blog](...) about it)

#### Relation database model

If we want to understand SQL, we first need to familiarize ourselves with the concept of relational databases ([chapter 4](https://tomdeneire.github.io/InformationScience/chapter04.html)). Simply said, a relational database is a **collection of tables** that share a common data element. Have a look at this simplified example of a library catalogue:

**Table 1: titles**
| LOI        | title                   | language |
| ---------- | ----------------------- | -------- |
| c:1        | The origin of species   | eng      |
| c:2        | History of Middle Earth | eng      |

**Table 2: authors**
| LOI        | name                    | function |
| ---------- | ----------------------- | -------  |
| c:1        | Darwin, Charles         | aut      |
| c:2        | Tolkien, J.R.R.         | aut      |
| c:2        | Tolkien, Christopher    | edt      |

**Table 3: subjects**
| LOI        | subject               |
| ---------- | --------------------- |
| c:1        | evolutionary biology  |
| c:1        | theology              |
| c:1        | history of science    |
| c:2        | fantasy               |
| c:2        | constructed languages |

Now imagine what would happen if we were to convert these three tables to one spreadsheet:

```
LOI, title, language, name1, name2, function, subject1, subject2, subject3
```

And imagine scaling this up: books might easily have five authors and ten subjects, and we have only a little bit of metadata here. What about imprints, editions, carries, holdings, and so on?
The advantages of relational databases are clear: they are perfect for storing and querying large amounts of related information in a flexible, decoupled way.

#### SQL queries

SQL queries always take the same basic form: we **select** data from a table (mandatory), **where** certain conditions apply (optional). We use **join** to add one or more tables to the selected table ([SQL cheat sheet](https://github.com/ABZ-Aaron/CheatSheets/blob/main/SQL-V2-Light.pdf)).

Let's look at a concrete example.

### sqlite3

Python's standard library contains the module [sqlite3](https://docs.python.org/3/library/sqlite3.html) which allows a SQL interface to a database.

For example, let's launch some SQL queries on a sqlite database of [STCV](https://vlaamse-erfgoedbibliotheken.be/en/dossier/short-title-catalogue-flanders-stcv/stcv), which is the Short Title Catalogue Flanders, an online database with extensive bibliographical descriptions of editions printed in Flanders before 1801. This database is available as part of the [Anet Open Data](https://www.uantwerpen.be/nl/projecten/anet/open-data/). A recent version of it is available in this repo under `data`.


import os
import sqlite3

# To use the module, you must first create a Connection object that represents the database
conn = sqlite3.connect(os.path.join('data', 'stcv.sqlite'))
# Once you have a Connection, you create a Cursor object
c = conn.cursor()
# To perform SQL commands you call the Cursor object's excute() method
query = """
        select distinct author_zvwr, title_ti, impressum_ju1sv from author
        join title on author.cloi = title.cloi
        join impressum on title.cloi = impressum.cloi
        group by author_zvwr
        """
c.execute(query)
# Call fetchall() to get a list of the matching rows
data = [row for row in c.fetchall()]
for row in data[50:60]:
    print(row)
# Close the connection when you're done
conn.close()

## Assignment: JSON metadata harvester

For your assignment you will be using the JSON data made available through the [Europeana Entities API](https://pro.europeana.eu/page/entity), which allows you to search on or retrieve information from named entities. These named entities (such as persons, topics and places) are part of the Europeana Entity Collection, a collection of entities in the context of Europeana harvested from and linked to controlled vocabularies, such as ​Geonames, DBpedia and Wikidata. It is advisable to read the API's [documentation](https://pro.europeana.eu/page/entity) first.

### What is an API?

A quick word in general about an [API](https://en.wikipedia.org/wiki/API), or Application Programming Interface.

Non-technical users mostly interact with data through a GUI or Graphical User Interface, either locally (e.g. you use DBbrowser to look at an SQLite database) or on the web (e.g. you use Wikidata's web page). However, when we try to interact with this data from a machine-standpoint, i.e. in programming, this GUI is not suitable. We need an interface that is geared towards computers. So we use a local (e.g. Python's `sqlite3` module) or remote (e.g. [Wikidata's Query Service](https://query.wikidata.org/)) API to get this data in a way that can be easily handled by computers.

In this way, an API is an intermediary structure, which has a lot of benefits. Wouldn't it be nicer to have direct access to a certain database? In a way, yes, but this would also cause problems. There are many, many different database architectures, but [API architectures](https://levelup.gitconnected.com/comparing-api-architectural-styles-soap-vs-rest-vs-graphql-vs-rpc-84a3720adefa) are generally quite predictable. They are often based on well-known technologies like JSON or XML, so you don't have to learn a new query language. Moreover, suppose Wikidata changes their database? All of your code that uses the database would need to be rewritten. By using the API intermediary structure Wikidata can change the underlying database, but make sure their API still functions in the same way as before. 

There are lots of free web APIs out there. The [NASA API](https://api.nasa.gov/), for instance, is quite incredible. Or this [Evil Insult Generator](https://evilinsult.com/generate_insult.php?lang=en&type=json), if you want to have some fun! You can find an extensive list of free APIs [here](https://github.com/public-apis/public-apis).
 

### Assignment

Your assignment is simple. Write a Python script that prompts for user input of a named entity, query the API for that entity, parse the results and print them on standard output.

#### Some tips:

- You can use the key `wskey=apidemo` for your API request.
- A good Python library to access URLs is `urllib`, an alternative (which is not in the standard library) is `requests`.
- Think about what we have seen already about standardizing/normalizing search strings, but take this to the next level.
- Try to anticipate what can go wrong so the program doesn't crash in unexpected situations.
- Test your application with the following search strings: `Erasmus`, `Justus Lipsius` and `Django Spirelli`.

If this is an easy task for you, you might think about parsing the results and adding them to your own database structure, e.g. XML or SQLite. 
