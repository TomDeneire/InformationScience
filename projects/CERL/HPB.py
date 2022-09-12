import sqlite3
import json
import tools
from lxml import etree
from lxml.etree import _Element

# CONSTANTS

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

SQLITEFILE = "/home/tdeneire/projects/InformationScience/course/data/stcv.sqlite"
HPB_PREFIX = "https://sru.gbv.de/hpb?version=2.0&operation=searchRetrieve&query="
OASIS_NS = r"{http://docs.oasis-open.org/ns/search-ws/sruResponse}"
MARC21_NS = r"{http://www.loc.gov/MARC21/slim}"
SRU_INCREMENT = 100


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


def get_HPB_records(query: str) -> _Element:
    """
    Get all relevant HPB records
    """
    query = tools.clean(query)

    # Get total
    url = HPB_PREFIX + query
    root = tools.read_xml_from_url(url)
    total = 0
    for element in root.iter(f"{OASIS_NS}numberOfRecords"):
        total = int(element.text)

    # Get result in chunks
    root = etree.Element("root")
    offset = 1
    while offset < total:
        url = (
            HPB_PREFIX
            + query
            + f"&startRecord={offset}"
            + "&maximumRecords={SRU_INCREMENT}"
        )
        data = tools.read_xml_from_url(url)
        root.append(data)
        offset += SRU_INCREMENT

    return root


def basic_CQL(data: tuple) -> str:
    """
    Construct a basic CQL query that aims at getting a lot of matches
    """
    query = ""
    author = data[2]
    if author is not None:
        # family name only
        author = author.partition(",")[0]
        query += f"pica.per={author}"
    title = data[7]
    if title is not None:
        try:
            # first three words only
            # to avoid false negatives because of spelling differences
            title = " ".join(title.split(" ")[0:3])
        except IndexError:
            pass
        query += f" and pica.tit={title}"
    year = data[13]
    if year is not None:
        query += f" and pica.yop={year}"

    query = query.lstrip(" and ")

    return query


def advanced_CQL(data: tuple) -> str:
    """
    Construct an advanced CQL query that enriches a basic query
    and aims at narrowing down matches
    """
    query = basic_CQL(data)
    place = data[17]
    if place is not None:
        if not place.lower() == "s.l.":
            query += f" and pica.plc={place}"
    printer = data[18]
    if printer is not None:
        if not printer.lower() == "s.n.":
            query += f" and pica.drx={printer}"
    language = data[19]
    if language is not None:
        query += f" and pica.spr={language}"

    return query


# WRAPPERS


def match(data: tuple, mode: str, verbose: bool) -> list:
    if mode == "basic":
        query = basic_CQL(data)
    else:
        query = advanced_CQL(data)
    result = get_HPB_records(query)
    matches = []
    for record in result.iter(f"{MARC21_NS}record"):
        parsed_record = tools.parse_MARC_RECORD(record, MARC21_NS, control=False)
        hpb_id = parsed_record["035"][0]["a"]
        matches.append(hpb_id)
        if verbose:
            print(f"HPB ({mode})=", parsed_record)
    return matches


def run(verbose=False, sample=False):
    """
    - Perform SQL query
    - Iterate over results
        - Construct basic CQL
        - Quit if basic < 2 results
        - Construct advanced CQL
        - Compare and keep crossection of both
    """

    dataset = query_sqlite(SQLITEFILE, QUERY)

    if sample:
        dataset = dataset[0:10]

    matches = {}

    for publication in dataset:
        stcv_id = publication[0]
        matches[stcv_id] = []
        if verbose:
            print("STCV =", *publication)

        basic_matches = match(publication, mode="basic", verbose=verbose)
        if len(basic_matches) < 2:
            matches[stcv_id] = basic_matches
            continue

        advanced_matches = match(publication, mode="advanced", verbose=verbose)
        if len(advanced_matches) == 0:
            matches[stcv_id] = basic_matches
            continue

        matches[stcv_id] = [
            match for match in advanced_matches if match in basic_matches
        ]

    print(json.dumps(matches, indent=4))


# MAIN
if __name__ == "__main__":
    run(verbose=True, sample=True)


"""
result 11-12-2021

{
    "c:stcv:12854444": [
        "FR-751131015.CG.FRBNF363412140000008",
        "FR-751131015.CG.FRBNF304042620000006"
    ],
    "c:stcv:12854501": [
        "DE-604.VK.BV021245268",
        "FR-751131015.CG.FRBNF363412120000003",
        "FR-751131015.CG.FRBNF304042700000008"
    ],
    "c:stcv:12854549": [
        "BE-KBR00.CAT.1_1732080",
        "BE-KBR00.CAT.1_1604695",
        "BE-KBR00.CAT.1_1506014"
    ],
    "c:stcv:12854587": [],
    "c:stcv:12854599": [],
    "c:stcv:12857052": [],
    "c:stcv:12857069": [],
    "c:stcv:12857131": [],
    "c:stcv:12857158": [],
    "c:stcv:12857275": [
        "IT-ICCU.NAPE019587",
        "IT-ICCU.NAPE019586",
        "IT-ICCU.NAPE019581",
        "BE-KBR00.CAT.1_1604462",
        "FR-751131015.CG.FRBNF310695850000002"
    ],
    "c:stcv:12857374": [
        "NL-UtRU.01.001326315",
        "NL-0100030000.STCN.328581151"
    ],
    "c:stcv:12857912": [
        "PL-BJ.01.vtls000638405",
        "(OCoLC)169699620 "
    ],
    "c:stcv:12857923": [],
    "c:stcv:12858124": [],
    "c:stcv:12858392": [],
    "c:stcv:12858408": [],
    "c:stcv:12858413": [
        "PL-BJ.01.vtls000638397",
        "(OCoLC)168100284 "
    ],
    "c:stcv:12858468": [],
    "c:stcv:12858494": [],
    "c:stcv:12858622": [],
    "c:stcv:12858690": [],
    "c:stcv:12858729": [
        "CZ-PrNK.STT.stt20170188109",
        "(OCoLC)166959808",
        "(OCoLC)169421986 "
    ],
    "c:stcv:12858795": [],
    "c:stcv:12859250": [],
    "c:stcv:12859427": [
        "IT-ICCU.RLZE002043",
        "DE-604.VK.BV008787631",
        "NL-0100030000.EPE.284819875",
        "NL-UtRU.01.001327020",
        "DE-601.GVK.582272378",
        "DE-601.GVK.366456768",
        "DE-601.GVK.366456601",
        "DE-601.GVK.143740121",
        "PL-BJ.01.vtls000592024",
        "FR-341725201.SUDOC.065115295",
        "(OCoLC)169856512 "
    ],
    "c:stcv:12859712": [],
    "c:stcv:12859754": [
        "BE-AnVE.c:stcv:12922627",
        "BE-AnVE.c:stcv:12919908",
        "BE-AnVE.c:stcv:12915047",
        "BE-AnVE.c:stcv:12861606",
        "BE-AnVE.c:stcv:12860736",
        "BE-AnVE.c:stcv:12859754",
        "NL-0100030000.EPE.353584029"
    ],
    "c:stcv:12859820": [],
    "c:stcv:12859871": [
        "IT-ICCU.LIAE035738",
        "IT-ICCU.LIAE005802",
        "IT-ICCU.BA1E012026",
        "CZ-PrNK.STT.stt20180206257",
        "CZ-PrNK.STT.stt20120066666",
        "US-icn.01.518225",
        "CH-000003-X.003325169",
        "DE-604.VK.BV042261724",
        "DE-604.VK.BV041156848",
        "DE-604.VK.BV012674497",
        "DE-604.VK.BV012374925",
        "DE-604.VK.BV003538884",
        "NL-0100030000.EPE.331374919",
        "NL-0100030000.EPE.240558839",
        "(OCoLC)168948102",
        "GB-StEdNL.01.1969358",
        "NL-0100030000.STCN.30619614X",
        "FR-341725201.SUDOC.144969696",
        "FR-341725201.SUDOC.125454732",
        "FR-341725201.SUDOC.108787222",
        "FR-341725201.SUDOC.06767108X",
        "BE-KBR00.CAT.1_1674855",
        "BE-KBR00.CAT.1_1674846",
        "BE-KBR00.CAT.1_1671718",
        "BE-KBR00.CAT.1_1344768",
        "BE-KBR00.CAT.1_1335114",
        "FR-751131015.CG.FRBNF364358700000007",
        "FR-751131015.CG.FRBNF363082400000005",
        "FR-751131015.CG.FRBNF362998920000009",
        "FR-751131015.CG.FRBNF362998910000001",
        "FR-751131015.CG.FRBNF359879580000007",
        "FR-751131015.CG.FRBNF35987957000000X",
        "FR-751131015.CG.FRBNF359879560000002",
        "FR-751131015.CG.FRBNF359879550000005",
        "FR-751131015.CG.FRBNF340251890000002",
        "FR-751131015.CG.FRBNF308199440000003",
        "FR-751131015.CG.FRBNF308199430000006",
        "FR-751131015.CG.FRBNF308199420000009",
        "FR-751131015.CG.FRBNF308199410000001",
        "FR-751131015.CG.FRBNF308199400000004",
        "(OCoLC)168640641 ",
        "(OCoLC)167943925 ",
        "(OCoLC)169569253 ",
        "EE-TLUAR.OC.b23670654",
        "RuSpRNB.A2V16.54204",
        "(OCoLC)814597235 ",
        "(OCoLC)814597234 ",
        "(OCoLC)168325570 ",
        "(OCoLC)169025799 ",
        "(OCoLC)169025797 ",
        "(OCoLC)168133856 "
    ],
    "c:stcv:12859905": [],
    "c:stcv:12859931": [],
    "c:stcv:12860028": [
        "DE-604.VK.BV040096480",
        "DE-604.VK.BV019856498",
        "NL-0100030000.EPE.239899156",
        "NL-UtRU.01.001245503",
        "NL-UtRU.01.001245461",
        "FR-341725201.SUDOC.164520120",
        "FR-341725201.SUDOC.164519858",
        "BE-KBR00.CAT.1_811175",
        "BE-KBR00.CAT.1_1731045",
        "BE-KBR00.CAT.1_1505882"
    ],
    "c:stcv:12860136": [],
    "c:stcv:12860498": [],
    "c:stcv:12860697": [
        "BE-AnVE.c:stcv:12860697",
        "(OCoLC)166970269"
    ],
    "c:stcv:12860711": [
        "BE-AnVE.c:stcv:12861813",
        "BE-AnVE.c:stcv:12860711",
        "DE-604.VK.BV013602057",
        "(OCoLC)168933320"
    ],
    "c:stcv:12860736": [
        "BE-AnVE.c:stcv:12922627",
        "BE-AnVE.c:stcv:12919908",
        "BE-AnVE.c:stcv:12915047",
        "BE-AnVE.c:stcv:12861606",
        "BE-AnVE.c:stcv:12860736",
        "BE-AnVE.c:stcv:12859754",
        "NL-0100030000.EPE.353584029"
    ],
    "c:stcv:12861541": [],
    "c:stcv:12861606": [
        "BE-AnVE.c:stcv:12922627",
        "BE-AnVE.c:stcv:12919908",
        "BE-AnVE.c:stcv:12915047",
        "BE-AnVE.c:stcv:12861606",
        "BE-AnVE.c:stcv:12860736",
        "BE-AnVE.c:stcv:12859754",
        "NL-0100030000.EPE.353584029"
    ],
    "c:stcv:12861734": [
        "US-icn.01.813984",
        "DE-604.VK.BV040658704",
        "DE-604.VK.BV005872857"
    ],
    "c:stcv:12861760": [
        "US-icn.01.813984",
        "DE-604.VK.BV040658704",
        "DE-604.VK.BV005872857"
    ],
    "c:stcv:12861798": [],
    "c:stcv:12861813": [
        "BE-AnVE.c:stcv:12861813",
        "BE-AnVE.c:stcv:12860711",
        "DE-604.VK.BV013602057",
        "(OCoLC)168933320"
    ],
    "c:stcv:12862032": [],
    "c:stcv:12862035": [],
    "c:stcv:12862038": [
        "IT-ICCU.RMLE006002",
        "US-mdbj.01.1441206",
        "US-mdbj.01.1081990",
        "FR-341725201.SUDOC.044336217",
        "BE-KBR00.CAT.1_1195161",
        "FR-751131015.CG.FRBNF386531240000003",
        "FR-751131015.CG.FRBNF386531230000006"
    ],
    "c:stcv:12862053": [
        "IT-ICCU.RMLE009257",
        "IT-ICCU.MUS0020614",
        "CZ-PrNK.STT.stt20160154652",
        "DE-604.VK.BV035147754",
        "DE-604.VK.BV013869663",
        "DE-604.VK.BV004617550",
        "(OCoLC)168946516",
        "DE-601.GVK.211500437",
        "GB-UkOxU.01.019309930",
        "GB-UkOxU.01.012755670",
        "FR-341725201.SUDOC.150781520",
        "FR-341725201.SUDOC.099933942",
        "FR-341725201.SUDOC.044260202",
        "BE-KBR00.CAT.1_444793",
        "BE-KBR00.CAT.1_444786",
        "BE-KBR00.CAT.1_444749",
        "BE-KBR00.CAT.1_444746",
        "BE-KBR00.CAT.1_444744",
        "BE-KBR00.CAT.1_1848341",
        "FR-751131015.CG.FRBNF304224630000002",
        "FR-751131015.CG.FRBNF304224620000005",
        "SI-50001.RK.017100",
        "(OCoLC)169183514 "
    ],
    "c:stcv:12862058": [
        "BE-AnVE.c:stcv:12862058",
        "NL-0100030000.EPE.34568690X",
        "FR-341725201.SUDOC.099639262",
        "BE-KBR00.CAT.1_195550",
        "BE-KBR00.CAT.1_195554"
    ],
    "c:stcv:12862118": [
        "IT-ICCU.VIAE034877",
        "DE-604.VK.BV019895971",
        "DE-604.VK.BV010235799",
        "DE-604.VK.BV001348256",
        "US-mdbj.01.1023203",
        "(OCoLC)169701856",
        "(OCoLC)169657020",
        "DE-601.GVK.456731563",
        "(OCoLC)166961709",
        "(OCoLC)167279880",
        "(OCoLC)167279870",
        "GB-UkOxU.01.012291021",
        "GB-UkOxU.01.012291020",
        "FR-341725201.SUDOC.066602262",
        "FR-341725201.SUDOC.064778460",
        "FR-341725201.SUDOC.051849267",
        "FR-751131015.CG.FRBNF300726650000005",
        "(OCoLC)169231685 ",
        "(OCoLC)814530431 "
    ],
    "c:stcv:12862125": [],
    "c:stcv:12862153": [
        "IT-ICCU.UTOE674646",
        "IT-ICCU.TO0E086381",
        "IT-ICCU.LO1E012628",
        "IT-ICCU.LO1E012626",
        "CZ-PrNK.STT.stt20150142155",
        "DE-604.VK.BV003548519",
        "NL-0100030000.EPE.241851386",
        "US-mdbj.01.1188944",
        "(OCoLC)168912543",
        "(OCoLC)168167924",
        "(OCoLC)166954204",
        "GB-UkOxU.01.012289476",
        "(OCoLC)167279722",
        "FR-341725201.SUDOC.144746743",
        "FR-341725201.SUDOC.103476199",
        "BE-KBR00.CAT.1_1315237",
        "BE-KBR00.CAT.1_1062719",
        "FR-751131015.CG.FRBNF386532480000000",
        "FR-751131015.CG.FRBNF386532470000003",
        "FR-751131015.CG.FRBNF317683760000007",
        "FR-751131015.CG.FRBNF31768375000000X",
        "FR-751131015.CG.FRBNF300613150000009",
        "FR-751131015.CG.FRBNF300613140000001",
        "(OCoLC)168547796 ",
        "(OCoLC)814707436 ",
        "(OCoLC)169135830 "
    ],
    "c:stcv:12862168": [
        "BE-AnVE.c:stcv:12862168",
        "FR-341725201.SUDOC.162015100"
    ],
    "c:stcv:12863004": [
        "US-icn.01.862275",
        "DE-604.VK.BV039555824",
        "NL-0100030000.EPE.135774543",
        "NL-0100030000.EPE.135774470",
        "NL-0100030000.EPE.135774403",
        "(OCoLC)168848277",
        "FR-751131015.CG.FRBNF314252650000001",
        "FR-751131015.CG.FRBNF314252600000005",
        "FR-751131015.CG.FRBNF314252530000000"
    ],
    "c:stcv:12865436": [
        "DE-604.VK.BV019750776",
        "FR-751131015.CG.FRBNF314252460000006",
        "US-icn.01.861176"
    ],
    "c:stcv:12865677": [],
    "c:stcv:12865828": [
        "IT-ICCU.TSAE023943",
        "US-icn.01.613683",
        "NL-0100030000.EPE.149828985",
        "NL-UtRU.01.002047723",
        "BE-KBR00.CAT.1_1604136",
        "BE-KBR00.CAT.1_1504354"
    ],
    "c:stcv:12866841": [
        "IT-ICCU.UTOE674537",
        "DE-604.VK.BV010235692",
        "US-mdbj.01.1084260",
        "DE-601.GVK.456675019",
        "(OCoLC)167279837",
        "FR-341725201.SUDOC.116309326",
        "BE-KBR00.CAT.1_1393325",
        "FR-751131015.CG.FRBNF300693550000000"
    ],
    "c:stcv:12866854": [
        "CZ-PrNK.STT.stt20170189867",
        "DE-601.GVK.677750048",
        "BE-KBR00.CAT.1_437545",
        "BE-KBR00.CAT.1_437544",
        "BE-KBR00.CAT.1_397571",
        "FR-693836101.CG.0000297117"
    ],
    "c:stcv:12866862": [],
    "c:stcv:12866867": [],
    "c:stcv:12866905": [
        "US-icn.01.724762",
        "(OCoLC)169689766",
        "FR-341725201.SUDOC.150779208",
        "FR-341725201.SUDOC.099933470",
        "BE-KBR00.CAT.1_1848336",
        "FR-751131015.CG.FRBNF315998260000002",
        "FR-751131015.CG.FRBNF304222400000007",
        "(OCoLC)169844561 "
    ],
    "c:stcv:12866912": [
        "IT-ICCU.VEAE035318",
        "IT-ICCU.TO0E086509",
        "IT-ICCU.RMLE009370",
        "NL-0100030000.EPE.289032512",
        "US-mdbj.01.1949049",
        "DE-601.GVK.742721795",
        "FR-341725201.SUDOC.08752113X",
        "BE-KBR00.CAT.1_1314879",
        "FR-751131015.CG.FRBNF386933520000003",
        "FR-751131015.CG.FRBNF386933510000006",
        "FR-751131015.CG.FRBNF386933500000009"
    ],
    "c:stcv:12866920": [
        "DE-604.VK.BV015020001",
        "DE-601.GVK.566547155",
        "GB-UkOxU.01.015705205",
        "(OCoLC)166932578",
        "FR-341725201.SUDOC.150778120",
        "BE-KBR00.CAT.1_194735",
        "BE-KBR00.CAT.1_194734",
        "FR-751131015.CG.FRBNF307415740000002",
        "FR-751131015.CG.FRBNF307415730000005",
        "(OCoLC)169208715 "
    ],
    "c:stcv:12866939": [],
    "c:stcv:12867300": [],
    "c:stcv:12867792": [],
    "c:stcv:12867804": [],
    "c:stcv:12867845": [
        "BE-KBR00.CAT.1_1485772",
        "(OCoLC)167965765 "
    ],
    "c:stcv:12867878": [],
    "c:stcv:12867885": [],
    "c:stcv:12867907": [
        "IT-ICCU.VEAE122602",
        "CZ-PrNK.STT.stt20150135479",
        "US-icn.01.671636",
        "(OCoLC)814657469 ",
        "GB-UkCyUK.CLC.CLC09280",
        "SpMaBN.01.BNE20041046449",
        "(OCoLC)169083948 "
    ],
    "c:stcv:12867929": [
        "FR-341725201.SUDOC.100067409",
        "FR-341725201.SUDOC.044361696",
        "SpMaUC.BH.b20437663"
    ],
    "c:stcv:12867974": [],
    "c:stcv:12868566": [],
    "c:stcv:12868625": [],
    "c:stcv:12868640": [],
    "c:stcv:12868663": [],
    "c:stcv:12868736": [],
    "c:stcv:12868749": [],
    "c:stcv:12868755": [],
    "c:stcv:12868758": [],
    "c:stcv:12868994": [],
    "c:stcv:12869036": [
        "FR-751131015.CG.FRBNF304288820000007",
        "(OCoLC)169520746 ",
        "SpMaBN.01.BNE19949035029"
    ],
    "c:stcv:12869148": [],
    "c:stcv:12869229": [],
    "c:stcv:12869264": [],
    "c:stcv:12869479": [
        "IT-ICCU.RMRE005065",
        "IT-ICCU.PARE063904",
        "IT-ICCU.NAPE008659",
        "CZ-PrNK.STT.stt20160154694",
        "US-icn.01.365208",
        "NL-0100030000.EPE.284882615",
        "(OCoLC)169669054",
        "(OCoLC)753040131",
        "(OCoLC)168172652",
        "NL-0100030000.STCN.343164760",
        "DE-601.GVK.226136337",
        "DE-601.GVK.215055519",
        "(OCoLC)166932808",
        "FR-341725201.SUDOC.145496767",
        "FR-341725201.SUDOC.130837768",
        "FR-341725201.SUDOC.103303375",
        "FR-341725201.SUDOC.099933578",
        "FR-341725201.SUDOC.09993342X",
        "FR-341725201.SUDOC.075687372",
        "FR-341725201.SUDOC.054448956",
        "BE-KBR00.CAT.1_1390865",
        "BE-KBR00.CAT.1_1300651",
        "BE-KBR00.CAT.1_1050097",
        "FR-751131015.CG.FRBNF386542850000009",
        "FR-751131015.CG.FRBNF339915420000008",
        "FR-751131015.CG.FRBNF304222830000004",
        "FR-751131015.CG.FRBNF304222820000007",
        "FR-751131015.CG.FRBNF30422281000000X",
        "FR-751131015.CG.FRBNF304222800000002",
        "FR-751131015.CG.FRBNF304222790000001",
        "FR-751131015.CG.FRBNF304222780000004",
        "FR-751131015.CG.FRBNF304222770000007",
        "(OCoLC)169844809 "
    ],
    "c:stcv:12869497": [],
    "c:stcv:12869500": [],
    "c:stcv:12869588": [
        "GB-StGlU.01.b21207112",
        "US-icn.01.555822",
        "DE-604.VK.BV035262785",
        "NL-UtRU.01.002681177",
        "NL-UtRU.01.001661035",
        "(OCoLC)753021386",
        "DE-601.GVK.648010252",
        "DE-601.GVK.233962182",
        "DE-601.GVK.216961610",
        "GB-UkOxU.01.015705756",
        "(OCoLC)166937853",
        "FR-341725201.SUDOC.148111378",
        "FR-341725201.SUDOC.054448719",
        "FR-341725201.SUDOC.054448700",
        "BE-KBR00.CAT.1_444199",
        "BE-KBR00.CAT.1_444197",
        "BE-KBR00.CAT.1_444077",
        "BE-KBR00.CAT.1_1391709",
        "FR-751131015.CG.FRBNF386559270000008",
        "FR-751131015.CG.FRBNF386559260000000",
        "FR-751131015.CG.FRBNF340035850000009",
        "FR-751131015.CG.FRBNF335922560000000",
        "FR-751131015.CG.FRBNF313437310000006",
        "FR-751131015.CG.FRBNF313437300000009",
        "FR-751131015.CG.FRBNF313437290000008",
        "FR-751131015.CG.FRBNF313437280000000",
        "FR-751131015.CG.FRBNF313437270000003"
    ],
    "c:stcv:12869609": [
        "DE-604.VK.BV035258901",
        "BE-KBR00.CAT.1_1311671",
        "FR-751131015.CG.FRBNF387300720000007"
    ],
    "c:stcv:12869812": [
        "DE-604.VK.BV022510403",
        "DE-601.GVK.489072526",
        "(OCoLC)168304256 "
    ],
    "c:stcv:12869845": [],
    "c:stcv:12869872": [],
    "c:stcv:12869899": [
        "DE-604.VK.BV039537502",
        "(OCoLC)168804038 ",
        "GB-StEdNL.01.2330757"
    ],
    "c:stcv:12869970": [],
    "c:stcv:12869997": [],
    "c:stcv:12870045": [],
    "c:stcv:12870054": [],
    "c:stcv:12870121": [
        "BE-KBR00.CAT.1_1486308",
        "BE-KBR00.CAT.1_1483999",
        "(OCoLC)167965750 "
    ]
}
"""
