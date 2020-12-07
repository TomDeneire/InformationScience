"""
Exercise for database handling in Python
"""

database = b'''
            <database>
                <teachers>
                <teacher nr="1">
                    <name type="last">Deneire</name>
                    <name type="first">Tom</name>
                </teacher>
                <teacher nr="2">
                    <name type="last">Kestemont</name>
                    <name type="first">Mike</name>
                </teacher>
                <teacher nr="3">
                    <name type="last">Daelemans</name>
                    <name type="first">Walter</name>
                </teacher>
                </teachers>
                <students>
                <student nr="1" nationality="American">
                    <name type="last">Modrall Sperling</name>
                    <name type="first">Dorothy</name>
                </student>
                <student nr="2" nationality="Belgian">
                    <name type="last">Claes</name>
                    <name type="first">Pauline</name>
                </student>
                <student nr="3" nationality="[unknown]">
                    <name type="last">Nagels</name>
                    <name type="first">Emma-Sophia</name>
                </student>
                </students>
            </database>'''


def convert_xml_to_dict(XML: bytes) -> dict:
    """
    Parse XML database and convert it to a Python dictionary
    """
    dictionary = {}
    # your code
    return dictionary


def convert_dict_to_JSON(dictionary: dict) -> str:
    """
    Convert Python dictionary to JSON string
    """
    JSON = ""
    # your code
    return JSON


if __name__ == "__main__":
    intermediary_dict = convert_xml_to_dict(database)
    JSON = convert_dict_to_JSON(intermediary_dict)
    print(JSON)
