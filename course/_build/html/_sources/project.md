# Exam project

![](images/project.jpeg)

This document describes the exam project for the course "Information Science" for the UAntwerp Master of Linguistics (from 2021-2022 onwards: "Master of Digital Text Analysis").

## Description

This year's project can be described as an **STCV - HPB data reconciliator**. The idea is to write a piece of software that tries to pair up STCV (Short Title Catalogue Flanders) records with their HPB (Heritage of the Printed Book Database) matches.

For instance:

[c:stcv:12854444](https://anet.be/record/stcvopac/c:stcv:12854444/E) matches [FR-751131015.CG.FRBNF363412140000008](http://hpb.cerl.org/record/FR-751131015.CG.FRBNF363412140000008)

## Metadata

This can be implemented using **HPB's SRU/CQL service**, see [https://sru.gbv.de/hpb?version=2.0&operation=explain](https://sru.gbv.de/hpb?version=2.0&operation=explain)

HPB offers metadata in several formats, including MARC, Dublin Core, ... See, for instance, [https://sru.gbv.de/hpb?version=2.0&operation=searchRetrieve&query=lipsius&startRecord=1&maximumRecords=10&recordSchema=dc](https://sru.gbv.de/hpb?version=2.0&operation=searchRetrieve&query=lipsius&startRecord=1&maximumRecords=10&recordSchema=dc)

How you query HPB and which metadata you use, is completely up to you.

For the STCV dataset you will be using a sample from the **SQLite STCV export** that is in the [course repository](https://github.com/TomDeneire/InformationScience/tree/main/course/data). This sample is defined as the following SQL query:

``` python
# Select 100 single-volume titles from STCV
# with detailed bibliographic information
QUERY = """
SELECT DISTINCT
    title.cloi as identifier,
    COUNT(title.cloi) as id_count,
    author_vw as author_standardized,
    author_zvwr as author_original,
    author_zbd as author_dates,
    corporateauthor_nm as corporateauthor_standardized,
    corporateauthor_zvwr as corporateauthor_original,
    title_ti as title_title,
    title_lg as title_language,
    collation_fm as format,
    collation_ka as quires,
    collation_pg as pages,
    edition_ed as edition_info,
    impressum_ju1sv as year1,
    impressum_ju1ty as year1_type,
    impressum_ju2sv as year2,
    impressum_ju2ty as year2_type,
    impressum_pl as place,
    impressum_ug as printer,
    language_lg as language_info,
    number_nr as fingerprint
    FROM title
LEFT JOIN author on author.cloi = title.cloi
LEFT JOIN collation on collation.cloi = title.cloi
LEFT JOIN corporateauthor on corporateauthor.cloi = title.cloi
LEFT JOIN edition on edition.cloi = title.cloi
LEFT JOIN impressum on impressum.cloi = title.cloi
LEFT JOIN language on language.cloi = title.cloi
LEFT JOIN number on number.cloi = title.cloi
GROUP BY identifier
HAVING ID_COUNT=2
LIMIT 100
"""
```

## Goal

The goal of the project is to write a Jupyter Notebook that looks for `stcv.sqlite` in the same directory as the notebook itself and produces an onscreen output of the potential matches in the form of STCV identifier (`c:stcv:*`) = HPB identifier.

Just to be clear, the HPB identifier is the piece of data found in MARCXML field `035a`, e.g.:

``` xml
<datafield tag="035" ind1=" " ind2=" ">
<subfield code="a">IT-ICCU.TSAE008822</subfield>
</datafield>
```

You may choose to add additional information to the result, if you think it is relevant for the specific data reconciliation.

One STCV record may also have several HPB matches.

Please use only the `lxml` module to handle XML.

Just to give you an idea: the model solution for this project took me about 4 hours to write and test, and is about 250 lines long (including the query).
