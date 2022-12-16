# Chapter 5: Querying Information

![](images/algorithms.png)

Credit: [xkcd](https://xkcd.com/1831/)

> *TL;DR: Querying data is at the heart of information retrieval, whether we query for data or for documents that contain data.*

## Query languages

Database operations can be summarized with the acronym `CRUD`: create, read, update and delete. 

From an information standpoint, the main focus is **reading** from the database. Most often though, we do not read directly, as this is not possible (not all databases can be browsed), or practical (we get too much information). Instead, reading databases is usually done through **querying**, for which we use [query languages](https://en.wikipedia.org/wiki/Query_language). 

Actually, query languages surpass databases. Formally, query languages can be classified as **database query languages** versus **information retrieval query languages**. The difference is that a database query language attempts to give factual answers to factual questions, while an information retrieval query language attempts to find documents containing information that is relevant to an area of inquiry. 

For the former we will discuss SQL, for the latter CQL.

### Database querying: SQL/SQLite

SQL is a technology that is probably new to most of you. Unlike RDF, which some libraries seem hesitant to adopt, SQL is ubiquitous, including outside of libraries. Moreover, SQL has for instance heavily influenced the aforementioned CQL, and also [SPARQL](https://en.wikipedia.org/wiki/SPARQL), the query language for RDF. So knowing SQL will open many doors.

SQL is the query language for RDBMS, which are most often implemented in a *client-server* database engine. So for you to use SQL you would need a connection to a SQL database **server,** i.e. something like [MySQL](https://en.wikipedia.org/wiki/MySQL) or [PostgreSQL](https://en.wikipedia.org/wiki/PostgreSQL), which you can see, for instance, running on my local machine like so:

```
tdeneire@XPS-13-9370:~/tmp$ ps -ef | grep postgres

postgres    1258       1  0 07:01 ?        00:00:00 /usr/lib/postgresql/12/bin/postgres -D /var/lib/postgresql/12/main -c config_file=/etc/postgresql/12/main/postgresql.conf
postgres    1286    1258  0 07:01 ?        00:00:00 postgres: 12/main: checkpointer   
postgres    1287    1258  0 07:01 ?        00:00:00 postgres: 12/main: background writer   
postgres    1288    1258  0 07:01 ?        00:00:00 postgres: 12/main: walwriter   
postgres    1289    1258  0 07:01 ?        00:00:00 postgres: 12/main: autovacuum launcher   
postgres    1290    1258  0 07:01 ?        00:00:00 postgres: 12/main: stats collector   
postgres    1291    1258  0 07:01 ?        00:00:00 postgres: 12/main: logical replication launcher
```

However, there is also a very good **standalone** alternative, called [SQLite](https://en.wikipedia.org/wiki/SQLite). 

Simply said SQLite is just a single file, but you can query it just like a SQL database server. Moreover, you can access SQLite databases from many programming languages (C, Python, PHP, Go, ...), but you can also handle them with GUIs like [DB Browser](https://sqlitebrowser.org/), which makes them also very suitable for non-technical use.

If you want to know more about SQLite, I wrote this [blog](https://tomdeneire.medium.com/the-most-widely-used-database-in-the-world-d0cd87f7c482) about why it is the most widely-used database in the world...

#### SQL queries

There are some minute differences between SQL syntax and the SQLite dialect, but these so small they can be neglected.

SQL queries always take the same basic form: we **select** data from a table (mandatory), **where** certain conditions apply (optional). We can use **join** (in different forms) to add one or more tables to the selected table:

![](images/sql.png)

This [SQL cheat sheet](https://github.com/ABZ-Aaron/CheatSheets/blob/main/SQL-V2-Light.pdf) also offers a great summary.

Let's look at a concrete example.

#### Python sqlite3

Python's standard library contains the module [sqlite3](https://docs.python.org/3/library/sqlite3.html) which offers an API for a SQLite database. (We will discuss API's in general later in this chapter).

For example, let's launch some SQL queries on a SQLite database of [STCV](https://vlaamse-erfgoedbibliotheken.be/en/dossier/short-title-catalogue-flanders-stcv/stcv), which is the Short Title Catalogue Flanders, an online database with extensive bibliographical descriptions of editions printed in Flanders before 1801. This database is available as part of the [Anet Open Data](https://www.uantwerpen.be/nl/projecten/anet/open-data/). A version of it is available in this repo under `data`.


import os
import sqlite3

# To use the module, you must first create a Connection object that represents the database
conn = sqlite3.connect(os.path.join('data', 'stcv.sqlite'))
# Once you have a Connection, you create a Cursor object
c = conn.cursor()
# To perform SQL commands you call the Cursor object's .execute() method
query = """
        SELECT DISTINCT 
            author.author_zvwr, 
            title.title_ti, 
            impressum.impressum_ju1sv FROM author
        JOIN 
            title ON author.cloi = title.cloi
        JOIN 
            impressum ON title.cloi = impressum.cloi
        ORDER BY 
            author.author_zvwr DESC
        """
c.execute(query)
# Call fetchall() to get a list of the matching rows
data = [row for row in c.fetchall()]
# Print sample of result
for row in data[50:60]:
    print(row)
# Close the connection when you're done
conn.close()

Becoming fully versed in SQL is beyond the scope of this course. In this context, it is enough to understand the capabilities of SQL and the basic anatomy of a SQL query. This will help you to better understand RDBM systems as a whole or learn new querying technologies, such as the aforementioned SPARQL, which is effectively a variant of SQL:

Consider this example:

```sql
SELECT DISTINCT 
    ?resource, ?name, ?birthDate, ?deathDate
WHERE {
    ?resource rdfs:label "Hugo Claus"@en; 
              rdfs:label ?name; 
              rdf:type dbo:Person
    OPTIONAL {?resource dbp:birthDate ?birthDate}.
    OPTIONAL {?resource dbp:deathDate ?deathDate}
    FILTER(?name = "Hugo Claus"@en)
}
```

Execute this query against the [DBPedia SPARQL endpoint](https://dbpedia.org/sparql?default-graph-uri=http%3A%2F%2Fdbpedia.org&query=++++++++++++SELECT+DISTINCT+%0D%0A%3Fresource%2C+%3Fname%2C+%3FbirthDate%2C+%3FdeathDate%0D%0A++++++++++++WHERE+%7B%3Fresource+rdfs%3Alabel+%22Hugo+Claus%22%40en%3B+rdfs%3Alabel+%3Fname%3B+rdf%3Atype+dbo%3APerson%0D%0A++++++++++++OPTIONAL+%7B%3Fresource+dbp%3AbirthDate+%3FbirthDate%7D.%0D%0A++++++++++++OPTIONAL+%7B%3Fresource+dbp%3AdeathDate+%3FdeathDate%7D%0D%0A++++++++++++FILTER%28%3Fname+%3D+%22Hugo+Claus%22%40en%29%7D%0D%0A&format=application%2Fsparql-results%2Bjson&timeout=10000&signal_void=on&signal_unconnected=on).

### Information retrieval querying: CQL/SRU

Contextual query language or **CQL** is an example of an information retrieval query language. According to [Wikipedia:Contextual_Query_Language](https://en.wikipedia.org/wiki/Contextual_Query_Language)

>Contextual Query Language (CQL), previously known as Common Query Language, is a formal language for representing queries to information retrieval systems such as search engines, bibliographic catalogs and museum collection information. (...) its design objective is that queries be human readable and writable, and that the language be intuitive while maintaining the expressiveness of more complex query languages. It is being developed and maintained by the Z39.50 Maintenance Agency, part of the Library of Congress.

Querying with CQL operates via **SRU** - Search/Retrieve via URL, which is an XML-based protocol for search queries.

You can find the full specifications for [CQL](https://www.loc.gov/standards/sru/cql/spec.html) and [SRU](http://www.loc.gov/standards/sru/index.html) at the Library of Congress website, what is offered here is only the basics.

#### SRU

SRU (Search/Retrieve via URL) is a standard search protocol for Internet search queries. In the context of libraries, SRU is mainly used for search and retrieval of bibliographic records from the catalog.

A valid SRU request always contains a reference to the SRU "version" and an "operation", optionally enriched with "parameters".

The **explain** operation allows a client to retrieve a description of the facilities available at an SRU server. It can then be used by the client to self-configure and provide an appropriate interface to the user. The response includes list of all the searchable **indexes**.

e.g. [https://data.cerl.org/thesaurus/_sru?version=1.2&operation=explain](https://data.cerl.org/thesaurus/_sru?version=1.2&operation=explain)

The **searchRetrieve** operation is the main operation of SRU. It allows the client to submit a search and retrieve request for matching records from the server. This operation needs to be combined with the **query** parameter

e.g. [https://data.cerl.org/thesaurus/_sru?version=1.2&operation=searchRetrieve&query=erasmus](https://data.cerl.org/thesaurus/_sru?version=1.2&operation=searchRetrieve&query=erasmus)

Note the tag `<srw:numberOfRecords>`. Most SRU servers will not give you the entire response in one go. You can use the parameters `&startRecord=` and `&maximumRecords=` to harvest the whole result in chunks. For instance:

[http://sru.gbv.de/hpb?version=2.0&operation=searchRetrieve&query=lipsius](http://sru.gbv.de/hpb?version=2.0&operation=searchRetrieve&query=lipsius)

->

[http://sru.gbv.de/hpb?version=2.0&operation=searchRetrieve&query=lipsius&startRecord=1&maximumRecords=10](http://sru.gbv.de/hpb?version=2.0&operation=searchRetrieve&query=lipsius&&startRecord=1&maximumRecords=10)


#### CQL

A SRU search statement, i.e. the `&query=` part, is expressed in [CQL syntax](http://zing.z3950.org/cql/intro.html).

The simplest CQL queries are unqualified **single terms**:

e.g. [https://data.cerl.org/thesaurus/_sru?version=1.2&operation=searchRetrieve&query=lipsius&startRecord=1](https://data.cerl.org/thesaurus/_sru?version=1.2&operation=searchRetrieve&query=lipsius&startRecord=1)

Queries may be joined together using the three **Boolean operators**, `and`, `or` and `not`. We use spaces, or rather their URL encoded version `%20` to separate CQL words:

e.g. [https://data.cerl.org/thesaurus/_sru?version=1.2&operation=searchRetrieve&query=lipsius%20or%20erasmus&startRecord=1](https://data.cerl.org/thesaurus/_sru?version=1.2&operation=searchRetrieve&query=lipsius%20or%20erasmus&startRecord=1)

The queries discussed so far are targeted at whole records. Sometimes we need to be more specific, and limit a search to a particular field of the records we're interested in. In CQL, we do this using **indexes**. An index is generally attached to its search-term with an equals sign (=). Indexes indicate what part of the records is to be searched - in implementation terms, they frequently specify which index is to be inspected in the database. For information about which specific indexes you can use, use the `explain` operation:

e.g. [https://data.cerl.org/thesaurus/_sru?version=1.2&operation=searchRetrieve&query=ct.imprintname=moretus&startRecord=1](https://data.cerl.org/thesaurus/_sru?version=1.2&operation=searchRetrieve&query=ct.imprintname=moretus&startRecord=1)

SRU also allows other **relations** than equality (`=`) which we have just used (e.g. `publicationYear < 1980`) and **pattern matching**:

e.g. [https://data.cerl.org/thesaurus/_sru?version=1.2&operation=searchRetrieve&query=m*retus&startRecord=1](https://data.cerl.org/thesaurus/_sru?version=1.2&operation=searchRetrieve&query=m*retus&startRecord=1)


#### Example: CERL thesaurus

Let's have a more detailed look at one of the examples used frequently in the above. This source that supports SRU/CQL is the [CERL (Consortium of European Research Libraries)](https://cerl.org/), which is responsible for the [CERL Thesaurus](https://data.cerl.org/thesaurus/_search), containing forms of imprint places, imprint names, personal names and corporate names as found in material printed before the middle of the nineteenth century - including variant spellings, forms in Latin and other languages, and fictitious names.

Below is an example of how to query this source with SRU/CQL from Python:

import urllib.parse
import urllib.request
import urllib.error

CERL_SRU_PREFIX = "https://data.cerl.org/thesaurus/_sru?version=1.2&operation=searchRetrieve&query="

def clean(string: str) -> str:
    """
    Clean input string and URL encode
    """
    string = string.strip()
    string = string.casefold()
    string = urllib.parse.quote(string)
    return string


def query_CERL(search: str) -> bytes:
    """
    Query CERL thesaurus, return response or exit with errorcode
    """
    cql_query = clean(search)
    url = CERL_SRU_PREFIX + cql_query
    try:
        with urllib.request.urlopen(url) as query:
            return query.read()
    except urllib.error.HTTPError as HTTPerr:
        exit(HTTPerr.code)
    except urllib.error.URLError as URLerr:
        exit(str(URLerr))

user_input = input()
print(str(query_CERL(user_input)[0:1000]) + "...")

## APIs

An SRU server is an example of a web [API](https://en.wikipedia.org/wiki/API), or Application Programming Interface.

Non-technical users mostly interact with data through a GUI or Graphical User Interface, either locally (e.g. you use DBbrowser to look at an SQLite database) or on the web (e.g. you use Wikidata's web page). However, when we try to interact with this data from a machine-standpoint, i.e. in programming, this GUI is not suitable. We need an interface that is geared towards computers. So we use a local API (e.g. Python's `sqlite3` module) or web API (e.g. [Wikidata's Query Service](https://query.wikidata.org/)) to get this data in a way that can be easily handled by computers.

In this way, an API is an intermediary structure, which has a lot of benefits. Wouldn't it be nicer to have direct access to a certain database? In a way, yes, but this would also cause problems. There are many, many different database architectures, but [API architectures](https://levelup.gitconnected.com/comparing-api-architectural-styles-soap-vs-rest-vs-graphql-vs-rpc-84a3720adefa) are generally quite predictable. They are often based on well-known technologies like JSON or XML, so you don't have to learn a new query language. Moreover, suppose Wikidata changes their database. All of your code that uses the database would need to be rewritten. By using the API intermediary structure Wikidata can change the underlying database, but make sure their API still functions in the same way as before. 

There are lots of free web APIs out there. The [NASA API](https://api.nasa.gov/), for instance, is quite incredible. For book information there is [OpenLibrary](https://openlibrary.org/dev/docs/api/books). Or this [Evil Insult Generator](https://evilinsult.com/generate_insult.php?lang=en&type=json), if you want to have some fun! You can find an extensive list of free APIs [here](https://github.com/public-apis/public-apis).

## Exercise: Europeana Entities API

For this exercise you will be using the JSON data made available through the [Europeana Entities API](https://pro.europeana.eu/page/entity), which allows you to search on or retrieve information from named entities. These named entities (such as persons, topics and places) are part of the Europeana Entity Collection, a collection of entities in the context of Europeana harvested from and linked to controlled vocabularies, such as [GeoNames](https://www.geonames.org/), [DBPedia](https://www.dbpedia.org/about/) and [Wikidata](https://www.wikidata.org/wiki/Wikidata:Main_Page). 

It is advisable to read the API's [documentation](https://pro.europeana.eu/page/entity) first.

### Task

The task is simple. Write a Python script that prompts for user input of a named entity, query the API for that entity, parse the results and print them on standard output.

#### Some tips:

- You can use the key `wskey=apidemo` for your API request.
- A good Python library to access URLs is `urllib`, an alternative (which is not in the standard library) is `requests`.
- Think about what we have seen already about standardizing/normalizing search strings, but take this to the next level.
- Try to anticipate what can go wrong so the program doesn't crash in unexpected situations.
- Test your application with the following search strings: `Erasmus`, `Justus Lipsius` and `Django Spirelli`.