"""
Assignment chapter 05
"""

import lxml.etree
import urllib.request
import urllib.error

import crosswalk

# CONSTANTS

OAI_MARC21_PREFIX = "https://anet.be/oai/catgeneric/server.phtml?verb=GetRecord&metadataPrefix=marc21&identifier="
OAI_XML_NS = r"{http://www.openarchives.org/OAI/2.0/}"  # raw string is safer


# FUNCTIONS

def harvest(loi: str) -> bytes:
    """
    Harvest MARC metadata from Anet OAI-PMH server
    """
    url = OAI_MARC21_PREFIX + loi
    try:
        with urllib.request.urlopen(url) as query:
            return query.read()
    except (urllib.error.HTTPError, urllib.error.URLError) as err:
        exit(err)


def parse(oai: bytes) -> dict:
    """
    Parse MARCXML to dict with structure:
        {index number: {"tag": tag, "code": code, "data": data}}
    """
    # .fromstring() method only works on ... bytes
    # see https://lxml.de/parsing.html#parsers
    root = lxml.etree.fromstring(oai)
    metadata = {}
    index = 0
    # iter() method to iterate over elements
    for datafield in root.iter(f"{OAI_XML_NS}datafield"):
        # XML attributes are dicts
        for key, value in datafield.items():
            if key == "tag":
                for subfield in datafield:
                    index += 1
                    for _, code in subfield.items():
                        metadata[index] = {"tag": value,
                                           "code": code,
                                           "data": subfield.text}
    return metadata


def convert_to_DC(MARC: dict) -> dict:
    """
    Use Library of Congress crosswalk to convert MARC21 to Dublin Core
    """
    table = crosswalk.table()
    dc = {}
    for index, datafield in MARC.items():
        for name, category in table.items():
            if datafield["tag"] + datafield["code"] in category:
                dc[index] = {name: datafield["data"]}
    return dc


def build_xml(dc_dict: dict) -> bytes:
    """
    Convert Dublin Core metadata dict to XML
    """
    root = lxml.etree.Element("metadata")
    dc = lxml.etree.SubElement(root,
                               "dc",
                               xmlns="http://purl.org/dc/elements/1.1/")
    for _, values in dc_dict.items():
        for category, data in values.items():
            field = lxml.etree.SubElement(dc,
                                          category)
            field.text = data
    dc_xml = lxml.etree.tostring(root)
    return dc_xml


def write_file(xml: bytes, loi: str) -> None:
    """
    Write Dublin Core XML to file in present working directory
    """
    # write in binary mode (for bytes)
    filename = loi.split(":")[2] + ".xml"
    with open(filename, 'wb') as xml_file:
        xml_file.write(xml)
        print(filename, "created succesfully!")


# APPLICATION


if __name__ == "__main__":
    loi = ""
    while not loi == "q:":
        loi = input("Type LOI (or q: to quit): ")
        if loi == 'q:':
            exit()
        else:
            # 1) Harvest MARCXML
            oai_response = harvest(loi)
            # 2) Parse MARCXML to intermediary dict
            metadata = parse(oai_response)
            # 3) Translate intermediary dict to DC dict
            dc = convert_to_DC(metadata)
            # 4) Turn DC dict into XML
            dc_xml = build_xml(dc)
            # 5) Write DCXML to file
            write_file(dc_xml, loi)

"""
Some points to take away from this assignment:

    1. Refactoring code is important to keep things manageable. In this example,
    we refactored the crosswalk to a different file and used it as a module.
    This makes the code more readable. By importing it as a constant in the
    main scope and not in a function scope, we avoid having to create the table
    with each conversion request.

    2. This is a real-world example. As explained in chapter05, OAI-PMH is
    the GLAM industry standard for exchanging metadata. As the DC format is
    mandatory in OAI, it means we have already implemented it in Brocade.
    So you can double check your solution and see a real-world implementation
    of this (including e.g. the correct XML namespaces for OAI-PMH) here:
    https://anet.be/oai/catgeneric/server.phtml?verb=GetRecord&metadataPrefix=oai_dc&identifier=c:lvd:123456

    3. Using proper variable names and explicit indentation helps a lot to keep
    code manageable and readable.
"""
