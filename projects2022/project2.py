import sqlite3
import json
import tools
from lxml import etree
from lxml.etree import _Element

# CONSTANTS

# Select 50 seventeenth-century people from authorities
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
    50
"""

SQLITEFILE = "/home/tdeneire/projects/InformationScience/course/data/authorities.sqlite"
THESAURUS_PREFIX = (
    "https://data.cerl.org/thesaurus/_sru?version=1.2&operation=searchRetrieve&query="
)
SRW_NS = r"{http://www.loc.gov/zing/srw/}"
MARC21_NS = r"{http://www.loc.gov/MARC21/slim}"
SRU_INCREMENT = 50


# FUNCTIONS


def query_sqlite(sqlitefile: str, query: str) -> list:
    """
    Perform a query on a SQLite database
    """
    connection = sqlite3.connect(sqlitefile)
    cursor = connection.cursor()
    cursor.execute(query)
    data = [row for row in cursor.fetchall()]
    connection.close()
    return data


def get_CERL_records(query: str) -> _Element:
    """
    Get all relevant CERL thesaurus records
    """
    query = tools.clean(query)

    # Get total
    url = THESAURUS_PREFIX + query
    root = tools.read_xml_from_url(url)
    total = 0
    for element in root.iter(f"{SRW_NS}numberOfRecords"):
        total = int(element.text)

    # Get result in chunks
    root = etree.Element("root")
    offset = 1
    while offset < total:
        url = (
            THESAURUS_PREFIX
            + query
            + f"&startRecord={offset}"
            + f"&maximumRecords={SRU_INCREMENT}"
            + "&recordSchema=marcxml"
        )
        data = tools.read_xml_from_url(url)
        root.append(data)
        offset += SRU_INCREMENT

    return root


def CQL_query(data: tuple) -> str:
    """
    Construct CQL query
    """
    query = ""
    family_name = data[5]
    family_name = tools.clean(family_name)
    if family_name is not None:
        query += f"cql.anywhere={family_name}"
    else:
        name = data[7]
        name = tools.clean(name)
        query += f"cql.anywhere={name}"
    first_name = data[6]
    if first_name is not None:
        first_name = tools.clean(first_name)
        query += f" and cql.anywhere={first_name}"

    query = query.lstrip(" and ")

    return query


def match(data: tuple, verbose: bool) -> list:
    """
    Perform query for database record and return matches
    """
    query = CQL_query(data)
    result = get_CERL_records(query)
    matches = []
    for record in result.iter(f"{SRW_NS}record"):
        parsed_record = tools.parse_MARC_RECORD(record, MARC21_NS, control=True)
        CERL_id = parsed_record["001"]
        matches.append({CERL_id: parsed_record})
        if verbose:
            print("CERL =", parsed_record)
    return matches


def run(verbose=False, sample=False):
    """
    - Perform SQL query
    - Iterate over data
        - Construct CQL
        - Handle XML reponse
    """

    dataset = query_sqlite(SQLITEFILE, QUERY)

    if sample:
        dataset = dataset[0:10]

    result = {}

    for person in dataset:
        au_id = person[0]
        result[au_id] = []
        if verbose:
            print("au =", *person)

        matches = match(person, verbose=verbose)
        for item in matches:
            for key in item:
                result[au_id].append(key)

    print(json.dumps(result, indent=4))


# MAIN
if __name__ == "__main__":
    run(verbose=True, sample=True)

"""
result 04-07-2022

{
    "au::34": [],
    "au::391": [],
    "au::469": [],
    "au::881": [
        "cnp02308697",
        "cnp01494285",
        "cnp01875720",
        "cnp01504531",
        "cnp01440674"
    ],
    "au::912": [],
    "au::1173": [],
    "au::1492": [],
    "au::1573": [
        "cnp01316076",
        "cnp01310438",
        "cni00092418",
        "cnp02167031",
        "cnp01019872",
        "cnp01337027",
        "cnp01905251"
    ],
    "au::1832": [
        "cnp00951119",
        "cnp02309456",
        "cnp01323558",
        "cnp01004392"
    ],
    "au::2098": [
        "cnp01339081",
        "cnp00542790"
    ],
    "au::2489": [],
    "au::2631": [
        "cnp00361150",
        "cnp02226251"
    ],
    "au::2633": [],
    "au::2992": [],
    "au::3026": [
        "cnp00566800",
        "cnp01335048",
        "cnp00566797",
        "cnp00566795",
        "cnp00585621",
        "cnp02308520",
        "cnp02313819"
    ],
    "au::3104": [],
    "au::3235": [],
    "au::3453": [],
    "au::3488": [
        "cni00017724",
        "cnp01327747",
        "cni00019284",
        "cnp02161747",
        "cnp00388767"
    ],
    "au::3660": [],
    "au::3802": [],
    "au::3935": [],
    "au::3961": [
        "cni00037214",
        "cnc00018045"
    ],
    "au::4504": [],
    "au::4607": [],
    "au::4756": [],
    "au::5260": [],
    "au::6058": [
        "cnp00582219",
        "cnp00572650"
    ],
    "au::6188": [],
    "au::6334": [
        "cnp01339762",
        "cni00014538"
    ],
    "au::6511": [
        "cnp00907140",
        "cnp01322867"
    ],
    "au::6600": [],
    "au::6622": [],
    "au::6713": [
        "cnp00051811",
        "cnp02310872"
    ],
    "au::6893": [],
    "au::7030": [],
    "au::7380": [],
    "au::7391": [],
    "au::7640": [],
    "au::8151": [],
    "au::8380": [],
    "au::8389": [],
    "au::8530": [
        "cnp00399849",
        "cnp00354901",
        "cnp01330916",
        "cnp01875654"
    ],
    "au::9305": [],
    "au::10166": [],
    "au::10191": [
        "cnp01935605",
        "cnp00570483"
    ]
}


"""
