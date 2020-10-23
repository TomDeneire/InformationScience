# Chapter 4: Databases

![](images/data.jpeg)

Credit: unknown

## Information vs Database Models

Formal discussions of the concept "information" might start with a treatment of different information models, as does chapter 3 of *Modern Information Retrieval* (see course description):

> Modeling in IR is a complex process aimed at producing a ranking function, i.e., a function that assigns scores to documents with regard to a given query. This process consists of two main tasks: (a) the conception of a logical framework for representing documents and queries and (b) the definition of a ranking function that computes a rank for each document with regard to a given query.

While IR models are obviously very interesting, the discussion is also highly theoretical and requires no small amount of mathematics (set theory, algebra, probability theory, ...). Therefore, it seems more practical and applicable to talk about databases instead as different "models" of information. Indeed, in most real-world applications of information science, you will most likely have to deal with information stored in a database.


## Databases

[Wikipedia](https://en.wikipedia.org/wiki/Database) defines a database as a "an organized collection of data, generally stored and accessed electronically from a computer system". Such a broad definition allows for many different kinds of databases, ranging from a single text file (e.g. the line `apples,oranges,grapes` is a database) to complex database management systems (DBMS) like MySQL that operate on large data structures.

### Database models

The classification of databases is a topic for a course on its own. For now, it will suffice to say that the development of database technology can be divided into three eras based on data model or structure: navigational, relational/SQL, and post-relational.

#### Navigational

[Wikipedia](https://en.wikipedia.org/wiki/Navigational_database) says

>A navigational database is a type of database in which records or objects are found primarily by following references from other objects. The term was popularized by the title of Charles Bachman's 1973 Turing Award paper, The Programmer as Navigator. This paper emphasized the fact that the new disk-based database systems allowed the programmer to choose arbitrary navigational routes following relationships from record to record, contrasting this with the constraints of earlier magnetic-tape and punched card systems where data access was strictly sequential.

(...)

>Although Bachman described the concept of navigation in abstract terms, the idea of navigational access came to be associated strongly with the procedural design of the CODASYL Data Manipulation Language. Writing in 1982, for example, Tsichritzis and Lochovsky state that "The notion of currency is central to the concept of navigation." By the notion of currency, they refer to the idea that a program maintains (explicitly or implicitly) a current position in any sequence of records that it is processing, and that operations such as `GET NEXT` and `GET PRIOR` retrieve records relative to this current position, while also changing the current position to the record that is retrieved.

#### Relational/SQL

[Wikipedia1](https://en.wikipedia.org/wiki/Relational_model) and [Wikipedia2](https://en.wikipedia.org/wiki/Database) say:

>The relational model (...) is an approach to managing data using a structure and language consistent with first-order predicate logic, first described in 1969 by English computer scientist Edgar F. Codd, where all data is represented in terms of tuples, grouped into relations. (...) he described a new system for storing and working with large databases. Instead of records being stored in some sort of linked list of free-form records (...), Codd's idea was to organise the data as a number of "tables", each table being used for a different type of entity. Each table would contain a fixed number of columns containing the attributes of the entity. One or more columns of each table were designated as a primary key by which the rows of the table could be uniquely identified; cross-references between tables always used these primary keys, rather than disk addresses, and queries would join tables based on these key relationships, using a set of operations based on the mathematical system of relational calculus (from which the model takes its name). Splitting the data into a set of normalized tables (or relations) aimed to ensure that each "fact" was only stored once, thus simplifying update operations. Virtual tables called views could present the data in different ways for different users, but views could not be directly updated.

>The purpose of the relational model is to provide a declarative method for specifying data and queries: users directly state what information the database contains and what information they want from it, and let the database management system software take care of describing data structures for storing the data and retrieval procedures for answering queries.

>Most relational databases use the SQL data definition and query language; these systems implement what can be regarded as an engineering approximation to the relational model. 

#### Post-relational

[Wikipedia](https://en.wikipedia.org/wiki/NoSQL) says:

>A NoSQL (originally referring to "non-SQL" or "non-relational") database provides a mechanism for storage and retrieval of data that is modeled in means other than the tabular relations used in relational databases. Such databases have existed since the late 1960s, but the name "NoSQL" was only coined in the early 21st century (...) NoSQL databases are increasingly used in big data and real-time web applications. NoSQL systems are also sometimes called "Not only SQL" to emphasize that they may support SQL-like query languages or sit alongside SQL databases in polyglot-persistent architectures.

>Motivations for this approach include: simplicity of design, simpler "horizontal" scaling to clusters of machines (which is a problem for relational databases), finer control over availability and limiting the object-relational impedance mismatch. The data structures used by NoSQL databases (e.g. key–value pair, wide column, graph, or document) are different from those used by default in relational databases, making some operations faster in NoSQL. The particular suitability of a given NoSQL database depends on the problem it must solve. Sometimes the data structures used by NoSQL databases are also viewed as "more flexible" than relational database tables.

Categories of post-relational databases include:

* **key-value stores**, such as the MUMPS database by YottaDB that we use for Brocade, the University of Antwerp's Library Management System
* **document stores**, such as XML or JSON
* **triple stores**, such as RDF


### Databases as Linked Data

Another interesting way to think about databases is to consider them from the view point of Linked (open) Data.

At [w3.org](https://www.w3.org/2011/gld/wiki/5_Star_Linked_Data) we read:

>Tim Berners-Lee, the inventor of the Web and initiator of the Linked Data project, suggested a 5 star deployment scheme for Linked Data. The 5 Star Linked Data system is cumulative. Each additional star presumes the data meets the criteria of the previous step(s).

>☆ Data is available on the Web, in whatever format.	

>☆☆ Available as machine-readable structured data, (i.e., not a scanned image).

>☆☆☆ Available in a non-proprietary format, (i.e, CSV, not Microsoft Excel).	

>☆☆☆☆ Published using open standards from the W3C (RDF and SPARQL).	

>☆☆☆☆☆ All of the above and links to other Linked Open Data.

In this way, we can organize different database types into a data hierarchy like such:

![](images/5-star-steps-open-data-5-star-model.png)

* OL: Open License
* RE: Readable
* OF: Open format
* URI: Uniform Resource Identifier
* LD: Linked Data

For a good description of this summary, see [this article](https://www.ontotext.com/knowledgehub/fundamentals/five-star-linked-open-data/).

## Query Languages

When trying to retrieve information, we are obviously primarily interested in querying information, for which we use [query languages](https://en.wikipedia.org/wiki/Query_language). 

Formally, query languages can be classified according to whether they are **database query languages** or **information retrieval query languages**. The difference is that a database query language attempts to give factual answers to factual questions, while an information retrieval query language attempts to find documents containing information that is relevant to an area of inquiry. 

For the former we will discuss XML and SQL; for the latter CQL.

### CQL

Let's start with an example of an information retrieval query language: contextual query language:

>Contextual Query Language (CQL), previously known as Common Query Language, is a formal language for representing queries to information retrieval systems such as search engines, bibliographic catalogs and museum collection information. Based on the semantics of Z39.50, its design objective is that queries be human readable and writable, and that the language be intuitive while maintaining the expressiveness of more complex query languages. It is being developed and maintained by the Z39.50 Maintenance Agency, part of the Library of Congress.

Querying with CQL operates via SRU - Search/Retrieve via URL, which is a standard XML-based protocol for search queries.

You can find the [SRU](http://www.loc.gov/standards/sru/index.html) and [CQL](https://www.loc.gov/standards/sru/cql/spec.html) specifications at the Library of Congress website. 

A fun API that support SRU/CQL is offered by the [CERL (Consortium of European Research Libraries)](https://cerl.org/), which is responsible for the [CERL Thesaurus](https://data.cerl.org/thesaurus/_search), containing forms of imprint places, imprint names, personal names and corporate names as found in material printed before the middle of the nineteenth century - including variant spellings, forms in Latin and other languages, and fictitious names.

To use this API you just send a web request to `https://data.cerl.org/thesaurus/_sru?version=1.2&operation=searchRetrieve&query=` followed by your CQL query in double quotes (or rather: `%22` which is the URL-safe encoding of `"`), for instance: https://data.cerl.org/thesaurus/_sru?version=1.2&operation=searchRetrieve&query=%22Erasmus%22

The response will be an XML document (database) containing the relevant CERL thesaurus entries for this query.

### XML

XML is something most of you are already familiar with, as it is a recurring technology in digital text analysis. In fact, XML is ubiquitous in the information world. It is very actively used in the library world. Another example is invoicing; for instance, the Government of Flanders has been asking for XML e-invoices from its suppliers for all contracts since 2017.

If you need to brush up your understanding of XML, [w3schools](https://www.w3schools.com/xml/) is a good place to start. Here we will briefly return to the matter of **parsing XML**, which is the process of analyzing XML documents to extract their information.

For Python, two XML libraries are highly recommended:

- [beautifulsoup](https://pypi.org/project/beautifulsoup4/)
- [lxml](https://lxml.de/)

Both turn XML's hierarchical structure into a parse tree, which behaves like a Pythonic object that you can then iterate over.

### SQL

Unlike XML, SQL is a technology that is probably new to most of you. Therefore, we will spend some more time discussing it in this [presentation](https://docs.google.com/presentation/d/1hLpHtKFs79QJYS0NpN9u4RG_hNwqScwoLgObFJKmvy8/edit?usp=sharing)

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
data = []
# Call fetchall() to get a list of the matching rows
for x in c.fetchall():
    data.append(x)
for result in data[50:60]:
    print(result)
# Close the connection when you're done
conn.close()

## Assignment: JSON metadata harvester

### JSON

One (document) database technology which we have not discussed yet, is [JSON](https://www.json.org/json-en.html). If you need to brush up on your JSON skills, [w3schools](https://www.w3schools.com/js/js_json_intro.asp) is again a good starting point. 

However, JSON is much easier to work with than XML. Basically, you can just think about it as a dictionary and Python, for instance, allows you to access it just so, using the `json` library: 

from json import loads,dumps
contacts = """
{
	"1": {
		"lastname": "Doe",
		"firstname": "John"
	},
	"2": {
		"lastname": "Doe",
		"firstname": "Jane"
	}
}
"""
# Turn JSON into dict with loads()
contacts_dict = loads(contacts)
print(contacts_dict["2"]["lastname"])
# Turn dict into JSON with dumps()
contacts_dict["2"]["lastname"] = "Eyre"
contacts = dumps(contacts_dict)
print(contacts)

For your assignement you will be using the JSON data made available through the [Europeana Entities API](https://pro.europeana.eu/page/entity), which allows you to search on or retrieve information from named entities. These named entities (such as persons, topics and places) are part of the Europeana Entity Collection, a collection of entities in the context of Europeana harvested from and linked to controlled vocabularies, such as ​Geonames, Dbpedia and Wikidata. It is advisable to read the API's [documentation](https://pro.europeana.eu/page/entity) first.

Your assignement is simple. Write a Python script that prompts for user input of a named entity, query the API for that entity, parse the results and print them on standard output.

### Some tips:

- You can use `wskey=apidemo` for your API request.
- A good Python library to access URLs is `urllib`.
- Think about what we have seen already about standardizing/normalizing search strings, but take this to the next level.
- Try to anticipate what can go wrong. 
- Test your application with the following search strings: `Erasmus`, `Justus Lipsius` and `Django Spirelli`.

If this is an easy task for you, you might think about parsing the results and adding them to your own database structure, e.g. XML or SQLite. 