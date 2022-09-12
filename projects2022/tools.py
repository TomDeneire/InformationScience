import sys
import time
from urllib.parse import quote
from urllib.request import urlopen
from urllib.error import HTTPError, URLError
from lxml import etree
from lxml.etree import _Element


def clean(string: str) -> str:
    """
    Clean string and URL encode
    """
    string = string.strip()
    string = string.casefold()
    string = quote(string)
    return string


def read_xml_from_url(URL: str) -> _Element:
    """
    Read URL, return response or sys.exit with errorcode
    Enforce delay to prevent DOS suspicions.
    """
    try:
        time.sleep(2)
        with urlopen(URL) as query:
            root = etree.fromstring(query.read())
            return root
    except HTTPError as HTTPerr:
        sys.exit(HTTPerr)
    except URLError as URLerr:
        sys.exit(URLerr)


def parse_MARC_RECORD(record: _Element, NS: str, control: bool) -> dict:
    """
    Parse MARC-XML datafields (and optionally controlfields) into dict
    Structure: dict[field tag] = [{subfield code: subfield text}, ...]
    """
    result = {}
    for datafield in record.iter(f"{NS}datafield"):
        for key, value in datafield.items():
            if key == "tag":
                for subfield in datafield:
                    for _, code in subfield.items():
                        result.setdefault(value, [])
                        result[value].append({code: subfield.text})
    if control:
        for controlfield in record.iter(f"{NS}controlfield"):
            for _, value in controlfield.items():
                result[value] = controlfield.text
    return result
