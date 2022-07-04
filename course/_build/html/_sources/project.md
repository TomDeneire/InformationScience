# Exam project

![](images/project.jpeg)

Credit: unknown

This document describes the exam project for the course "Information Science" for the UAntwerp Master of Digital Text Analysis.

## Description

This year's project can be described as an **STCV - HPB data reconciliator**. The idea is to write a piece of software that tries to pair up STCV (Short Title Catalogue Flanders) records with their HPB (Heritage of the Printed Book Database) matches.

For instance:

[c:stcv:12854444](https://anet.be/record/stcvopac/c:stcv:12854444/E) matches [FR-751131015.CG.FRBNF363412140000008](http://hpb.cerl.org/record/FR-751131015.CG.FRBNF363412140000008)

## Metadata

This can be implemented using **HPB's SRU/CQL service**, see [https://sru.gbv.de/hpb?version=2.0&operation=explain](https://sru.gbv.de/hpb?version=2.0&operation=explain)

HPB offers metadata in several formats, including MARC, Dublin Core, ... See, for instance, [https://sru.gbv.de/hpb?version=2.0&operation=searchRetrieve&query=lipsius&startRecord=1&maximumRecords=10&recordSchema=dc](https://sru.gbv.de/hpb?version=2.0&operation=searchRetrieve&query=lipsius&startRecord=1&maximumRecords=10&recordSchema=dc)

How you query HPB and which metadata you use, is completely up to you.

For the STCV dataset you will be using a sample from the **SQLite STCV export** that is in the [course repository](https://github.com/TomDeneire/InformationScience/tree/main/course/data). This sample is defined as the following SQL query. This selects 100 single-volume titles (multivolume titles pose specific reconciliation problems) with all relevant metadata you will need.

``` python
QUERY = """
SELECT
    DISTINCT title.cloi AS identifier,
    COUNT(title.cloi) AS id_count,
    author_vw AS author_standardized,
    author_zvwr AS author_original,
    author_zbd AS author_dates,
    corporateauthor_nm AS corporateauthor_standardized,
    corporateauthor_zvwr AS corporateauthor_original,
    title_ti AS title_title,
    title_lg AS title_language,
    collation_fm AS format,
    collation_ka AS quires,
    collation_pg AS pages,
    edition_ed AS edition_info,
    impressum_ju1sv AS year1,
    impressum_ju1ty AS year1_type,
    impressum_ju2sv AS year2,
    impressum_ju2ty AS year2_type,
    impressum_pl AS place,
    impressum_ug AS printer,
    language_lg AS language_info,
    number_nr AS fingerprint
FROM
    title
    LEFT JOIN author ON author.cloi = title.cloi
    LEFT JOIN COLLATION ON COLLATION.cloi = title.cloi
    LEFT JOIN corporateauthor ON corporateauthor.cloi = title.cloi
    LEFT JOIN edition ON edition.cloi = title.cloi
    LEFT JOIN impressum ON impressum.cloi = title.cloi
    LEFT JOIN language ON language.cloi = title.cloi
    LEFT JOIN number ON number.cloi = title.cloi
GROUP BY
    identifier
HAVING
    ID_COUNT = 2
LIMIT
    100
"""
```

## Technical specification

The goal of the project is to write a Jupyter Notebook that looks for `stcv.sqlite` in the same directory as the notebook itself and produces an onscreen output of the potential matches in the form of STCV identifier (`c:stcv:*`) = HPB identifier.

Just to be clear, the HPB identifier is the piece of data found in MARCXML field `035a`, e.g.:

``` xml
<datafield tag="035" ind1=" " ind2=" ">
<subfield code="a">IT-ICCU.TSAE008822</subfield>
</datafield>
```

You may choose to add additional information to the result, if you think it is relevant for the specific data reconciliation.

One STCV record may also have several HPB matches. Moreover, you may notice that some HPB records explicitely link to STCV, e.g. [http://hpb.cerl.org/record/BE-AnVE.c:stcv:12922627](http://hpb.cerl.org/record/BE-AnVE.c:stcv:12922627)? However, not all relevant HPB records will have such an explicit link. There is no continuous synchronization of HPB and STCV. Your software would be a good step in that direction. In other words, **any HPB id** can be a match for an STCV record, not only those HPB records which already contain an STCV link.

Please use only the `lxml` module to handle XML.

**Important!** I am not aware of any limitations on the [HPB SRU access](https://www.cerl.org/resources/hpb/technical/modes_of_access_to_the_hpb_database), but nevertheless, please take the following precautions to keep your usage of the service "friendly":

- as this application is not really performance-critical, combine each request with `time.sleep(2)`
- try to keep your test-volume down, e.g. test with only one record first and/or save the XML response and handle it as a local file

Please inform me if there are any API issues!

Just to give you an idea: the model solution for this project took me about 4 hours to write and test, and is about 250 lines long (including the query).

Hand in your project by setting up a private GitHub repository that you share with me (username [TomDeneire](https://github.com/TomDeneire)). Please take care to mention your **full name** in the exam notebook!

## Expectations

### Basic

- As with any exam, this project is strictly personal
- Please hand in only fully functional code
- Use only the Python standard library (except for `lxml`)
- Write clean and legible code

### Advanced

- Take into account the differences between STCV and HPB metadata / cataloguing standards.
- Optimize your CQL queries with indices, Booleans, ...
- Simple queries will yield many results. Complex queries will yield fewer results. How can you find a balance?

## Timing

The final deadline to upload your code to GitHub is **Sunday 30 January, 23h59**.
