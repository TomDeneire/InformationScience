# Exam project (2)

![](images/project.jpeg)

Credit: unknown

This document describes the **2022 second exam period** (22 August - 10 September 2022) exam project for the course "Information Science" for the UAntwerp Master of Linguistics (from 2021-2022 onwards: "Master of Digital Text Analysis").

## Description

This project can be described as an **Anet - CERL thesaurus data reconciliator**. The idea is to write a piece of software that tries to pair up  authority records (which describe entities such as people, places, organizations, ...) from the [Anet library network](https://en.wikipedia.org/wiki/Brocade_Library_Services)  with their [CERL Thesaurus](https://data.cerl.org/thesaurus/_search) matches.

For instance:

[au::6387](https://anet.be/record/isaarua/au::6387/E) matches [cnp02236021](https://data.cerl.org/thesaurus/cnp02236021)

## Metadata

This can be implemented using the **CERL Thesaurus SRU/CQL service**, see [https://data.cerl.org/thesaurus/_sru?version=1.2&operation=explain](https://data.cerl.org/thesaurus/_sru?version=1.2&operation=explain)

HPB offers metadata in several formats, including MARCXML, or the more explicit ctas. See, for instance, [https://data.cerl.org/thesaurus/_sru?version=1.2&operation=searchRetrieve&query=lipsius&startRecord=1&maximumRecords=10&recordSchema=marcxml](https://data.cerl.org/thesaurus/_sru?version=1.2&operation=searchRetrieve&query=lipsius&startRecord=1&maximumRecords=10&recordSchema=marcxml) or [https://data.cerl.org/thesaurus/_sru?version=1.2&operation=searchRetrieve&query=lipsius&startRecord=1&maximumRecords=10&recordSchema=ctas](https://data.cerl.org/thesaurus/_sru?version=1.2&operation=searchRetrieve&query=lipsius&startRecord=1&maximumRecords=10&recordSchema=ctas).

How you query the CERL Thesaurus and which metadata you use, is completely up to you.

For the Anet authority records dataset you will be using a sample from the **SQLite  export** (extract from `authorities.zip`) that is in the [course repository](https://github.com/TomDeneire/InformationScience/tree/main/course/data). This sample is defined as the following SQL query. This selects 100 records of type `P` (person), born in the seventeenth century, with all relevant metadata you will need.

``` python
QUERY = """
SELECT
    DISTINCT administration.LOI AS identifier,
    begin_in AS begin_date,
    begin_so AS begin_standardized,
    end_in AS end_date,
    end_so AS end_standardized,
    dsc_fn AS family_name,
    dsc_vn AS first_name,
    dsc_nm AS name,
    dsc AS description
FROM
    administration
    LEFT JOIN dates ON dates.LOI = administration.LOI
    LEFT JOIN identity ON identity.LOI = administration.LOI
WHERE
    administration.type = "P"
    AND begin_standardized LIKE "16%"
LIMIT
    100
"""
```

## Technical specification

The goal of the project is to write a Jupyter Notebook that looks for `authorities.sqlite` in the same directory as the notebook itself and produces an onscreen output of the potential matches in the form of authority identifier (`au::*`) = CERL Thesaurus identifier.

Just to be clear, the CERL Thesaurus identifier is the piece of data found in this XML element, e.g.:

``` xml
<srw:recordIdentifier>cnp00605296</srw:recordIdentifier>
```

You may choose to add additional information to the result, if you think it is relevant for the specific data reconciliation.

One authority record may have several potential CERL Thesaurus matches. Also keep in mind that people can be known under several different names (language variants, pseudonyms, abbreviated forms, etc.).

Please use only the `lxml` module to handle XML.

**Important!** I am not aware of any limitations on the [SRU interface to the CERL Thesaurus]<https://www.cerl.org/resources/cerl_thesaurus/sru>), but nevertheless, please take the following precautions to keep your usage of the service "friendly":

- as this application is not really performance-critical, combine each request with `time.sleep(2)`
- try to keep your test-volume down, e.g. test with only one record first and/or save the XML response and handle it as a local file

Please inform me if there are any API issues!

Hand in your project by setting up a private GitHub repository that you share with me (username [TomDeneire](https://github.com/TomDeneire)). Please take care to mention your **full name** in the exam notebook!

## Expectations

### Basic

- As with any exam, this project is strictly personal
- Please hand in only fully functional code
- Use only the Python standard library (except for `lxml`)
- Write clean and legible code

### Advanced

- Take into account the differences between CERL Thesaurus and authority metadata / cataloguing standards.
- Optimize your CQL queries with indices, Booleans, ...
- Simple queries will yield many results. Complex queries will yield fewer results. How can you find a balance?

## Timing

The final deadline to upload your code to GitHub is **5 September 2022**.
