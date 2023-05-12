"""
Exercise for database handling in Python
"""

from lxml import etree
import json

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
    dictionary = {"database": {"teachers": {}, "students": {}}}
    root = etree.fromstring(XML)
    # `student` element
    for student in root.iter("student"):
        nr = student.get("nr")
        nationality = student.get("nationality")
        dictionary["database"]["students"].update(
            {nr:
             {"nationality": nationality,
              "name": {}
              }
             })
        for name in student.iter("name"):
            dictionary["database"]["students"][nr]["name"].update(
                {name.get("type"): name.text})
    # `teacher` element
    for teacher in root.iter("teacher"):
        nr = teacher.get("nr")
        dictionary["database"]["teachers"].update(
            {nr:
             {"name": {}
              }
             })
        for name in teacher.iter("name"):
            dictionary["database"]["teachers"][nr]["name"].update(
                {name.get("type"): name.text})
    # You could iterate over `student` and `teacher` elements at the same time
    # but for didactic purposes this is more clear
    return dictionary


def convert_dict_to_JSON(dictionary: dict) -> str:
    """
    Convert Python dictionary to JSON string
    """
    JSON = ""
    # your code
    JSON = json.dumps(dictionary)
    return JSON


if __name__ == "__main__":
    intermediary_dict = convert_xml_to_dict(database)
    JSON = convert_dict_to_JSON(intermediary_dict)
    print(JSON)
