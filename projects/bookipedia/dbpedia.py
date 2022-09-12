"""
DBpedia API module
"""

import json
import lxml.etree
import urllib.request
import urllib.error
import urllib.parse
import urllib.response
import re
import sys


import tools

# CONSTANTS

DBPEDIA_ONTOLOGY_PREFIX = "http://dbpedia.org/ontology"
W3_PREFIX = "http://www.w3.org"

# FUNCTIONS


def getAPIprefix() -> str:
    """
    Detect functioning DBpedia lookup API
    """
    # 11-02-2021 different responses from these APIs!
    prefixes = ["https://lookup.dbpedia.org/api/search/PrefixSearch?QueryString=",
                "http://lookup.dbpedia.org/api/search/PrefixSearch?QueryString=",
                "https://lookup.dbpedia.org/api/search?query=",
                "http://lookup.dbpedia.org/api/search?query=",
                "https://lookup.dbpedia.org/api/prefix?query=",
                "http://lookup.dbpedia.org/api/prefix?query=",
                "http://akswnc7.informatik.uni-leipzig.de/lookup/api/search?query="]
    for prefix in prefixes:
        try:
            with urllib.request.urlopen(prefix + "Antwerp") as test:
                if test.status == 200:
                    return prefix
        except Exception as exc:
            print(exc)
    sys.exit("No functioning DBpedia lookup API found!")


def query(search: str) -> bytes:
    """
    Query DBpedia, return response or exit with errorcode
    """
    search = tools.clean(search, "search")
    url = getAPIprefix() + search
    return tools.url_reader(url)


def get_hits(xml: bytes) -> dict:
    """
    Parse DBpedia XML, return metadata for book hits
    """
    hits = {}
    root = lxml.etree.fromstring(xml)
    index = 0
    for result in root.iter("Result"):
        for result_class in result.iter("Class"):
            for label in result_class.iter("Label"):
                if label.text == "Book":
                    index += 1
                    hits[index] = {}
                    for item in result:
                        for tag in ["Label", "URI", "Refcount"]:
                            if item.tag == tag:
                                hits[index].update({tag: item.text})
    return hits


def lookup_hit(URI: str, source: str) -> bytes:
    """
    Look up DBpedia, Wikidata or Wikimedia data,
    return response or exit with errorcode
        e.g. http://dbpedia.org/resource/To_Kill_a_Mockingbird ->
        http://dbpedia.org/data/To_Kill_a_Mockingbird.json
    or
        e.g. http://www.wikidata.org/entity/Q212340 ->
        https://www.wikidata.org/wiki/Special:EntityData/Q212340.json
    or
        Wikimedia Commons -> no transformation
    """
    url = ""
    if source == "dbpedia":
        url = URI.replace("resource", "data") + ".json"
    elif source == "wikidata":
        url = URI.replace("entity", "/wiki/Special:EntityData") + ".json"
    elif source == "commons":
        url = URI
    return tools.url_reader(url)


def process_hit(JSON: bytes, URI: str) -> dict:
    """
    Process hit
    """
    result = {}
    # e.g. Leviathan
    if JSON == b'{ }\n':
        result["label"] = f"No further information found at {URI}"
        return result
    metadata = isolate_hit(JSON, URI)
    sections_with_language = {
        "label": f"{W3_PREFIX}/2000/01/rdf-schema#label",
        "abstract": f"{DBPEDIA_ONTOLOGY_PREFIX}/abstract"
    }
    sections_without_language = {
        "externallinks": f"{DBPEDIA_ONTOLOGY_PREFIX}/wikiPageExternalLink",
        "author": f"{DBPEDIA_ONTOLOGY_PREFIX}/author",
        "wikidata": f"{W3_PREFIX}/2002/07/owl#sameAs"
    }
    result = get_sections(metadata, sections_with_language,
                          result, lang=True)
    result = get_sections(metadata, sections_without_language,
                          result, lang=False)
    result = enrich_hit(result)
    result = add_images(result)
    return result


def enrich_hit(result: dict) -> dict:
    """
    Add extra metadata (author) via DBpedia Linked Data
    """
    if result.get("author") is None:
        return result
    URI = result["author"]
    author = lookup_hit(URI, "dbpedia")
    metadata = isolate_hit(author, URI)
    sections_with_language = {
        "authorabstract": f"{DBPEDIA_ONTOLOGY_PREFIX}/abstract",
        "authorlabel": f"{W3_PREFIX}/2000/01/rdf-schema#label",
        "authorwikidata": f"{W3_PREFIX}/2002/07/owl#sameAs",
    }
    result = get_sections(metadata, sections_with_language,
                          result, lang=True)
    sections_without_language = {
        "birthDate": f"{DBPEDIA_ONTOLOGY_PREFIX}/birthDate",
        "deathDate": f"{DBPEDIA_ONTOLOGY_PREFIX}/deathDate"
    }
    result = get_sections(metadata, sections_without_language,
                          result, lang=False)
    return result


def add_images(result: dict) -> dict:
    """
    Add image links via Wikidata Linked Data
    """
    # TO DO: add license information and show in result
    COMMONS = "https://commons.wikimedia.org/wiki/File:"
    images = {}
    for section in result:
        if "wikidata" in section:
            wikidata = lookup_hit(result[section], "wikidata")
            wikidata = json.loads(wikidata)
            qcode = result[section].split("/")[-1]
            image = wikidata["entities"][qcode]["claims"].get("P18")
            if image is None:
                return result
            imageref = image[0]["mainsnak"]["datavalue"].get("value")
            imageref = tools.clean(imageref.replace(" ", "_"), "url")
            imagelink = COMMONS + imageref
            imagelink = imagelink
            images[section + "image"] = get_commonslink(imagelink)
    newresult = {**result, **images}
    return newresult


def get_commonslink(URL: str) -> str:
    '''
    Open Wikimedia Commons page and return "original file" link
    <div class = "fullMedia" > <p > <a href =
    "https://upload.wikimedia.org/wikipedia/commons/4/4f/To_Kill_a_Mockingbird_%28first_edition_cover%29.jpg"
    class = "internal" title = "To Kill a Mockingbird (first edition cover).jpg" > Original file < /a >
    '''
    commons = lookup_hit(URL, "commons")
    commons = str(commons)
    fullMedia = re.compile(r'div class="fullMedia.*?\.jpg')
    link = re.findall(fullMedia, commons)[0]
    link = link.split('href="')[1]
    return link


def get_sections(metadata: dict, sections: dict, result: dict, lang: bool) -> dict:
    """
    Helper function to get certain items from a JSON dict metadata
    """
    for element, section in sections.items():
        for key, item in metadata.items():
            if key == section:
                for piece in item:
                    for _, part in piece.items():
                        if lang:
                            if part == "en":
                                result[element] = piece.get("value")
                        else:
                            if "wikidata" in element:
                                if "wikidata.org/entity" in piece.get("value"):
                                    result[element] = piece.get("value")
                            else:
                                result[element] = piece.get("value")
    return result


def isolate_hit(JSON: bytes, URI: str) -> dict:
    """
    Isolate the proper URI section from JSON bytes
    """
    hit = json.loads(JSON)
    metadata = {}
    for item in hit.items():
        if item[0] == URI:
            metadata = item[1]
    return metadata


if __name__ == "__main__":
    pass
