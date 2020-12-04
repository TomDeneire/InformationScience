"""
Assignment chapter 04

"""

import json
import urllib.parse
import urllib.request
import urllib.error

"""
Note:
    Alternatively to urllib.request you can also you the `requests` module,
    This has the benefit of being able to use the .json() method
    on the resulting HTTP response object, more info at
    https://www.geeksforgeeks.org/response-json-python-requests/
    Also requests.get(string) does not require you to first url encode `string`.
    The downside is that `requests` is not in the standard library.
"""

# CONSTANTS

# Europeana API error codes https://pro.europeana.eu/page/entity
CODES = {}
CODES[401] = "Authentication credentials were missing or authentication failed."
CODES[404] = "The requested entity was not found."
CODES[429] = "The request could be served because the application has reached its usage limit."
CODES[500] = "Internal Server Error. Something has gone wrong, which we will correct."

# Europeana API prefix
EUROPEANA_ENTITIES = "https://www.europeana.eu/api/entities/suggest?wskey=apidemo&text="

# FUNCTIONS


def clean(string: str) -> str:
    """
    Clean input string and URL encode (e.g. Léon Degrelle)
    """
    string = string.strip()
    string = string.casefold()
    string = urllib.parse.quote(string)
    return string


def query_Europeana(search: str) -> bytes:
    """
    Query Europeana Entities API, return response or exit with errorcode
    """
    search = clean(search)
    url = EUROPEANA_ENTITIES + search
    try:
        with urllib.request.urlopen(url) as query:
            return query.read()
    except urllib.error.HTTPError as HTTPerr:
        exit(CODES.get(HTTPerr.code))
    except urllib.error.URLError as URLerr:
        exit(URLerr)

# MAIN


if __name__ == "__main__":
    search = input("Please input your search: ")
    result = query_Europeana(search)
    parsed_result = json.loads(result)
    if not parsed_result["total"] == 0:
        for item in parsed_result["items"]:
            print("\n")
            for key, value in item.items():
                print(key, ":", value)
    else:
        print("No results")

"""
Some points to take away from this assignment:

    1. Write code that is fail safe: i.e. think about what happens in 'edge
    cases' when the API server cannot be reached, when no results are found,
    when the user inputs gibberish, ... (monkeyuser concept)

    2. Some sources on programming will advise against using `if...elif...else`
    flow. Of course, this is nonsense as a general rule of thumb, but this
    assignment does show that you're sometimes better off using a data type
    such as a dictionary to test for multiple conditions.

    3. Constructing URLs is something that can easily be generalized into forms
    of webscraping. You can easily imagine a piece of code that would go from 1
    to 100000 and construct URLS like: "https://mywebsite.com/page1", etc.
    Web scraping can be very handy to collect data (e.g. collections of texts),
    but be careful as it is not always allowed or your IP can get banned
    because it looks like a so-called DOS-attack. It is often good to put some
    artificial time delay (time.sleep in Python) in between your webrequests.

    4. This is a real-world example, which is part of an application I wrote for
    Brocade, which harvests identifiers for named entities from multiple sources
    such as Europeana, VIAF, DBPedia, ...

    5. Things I saw in your code:
        - Place your imports at the top of your Python file, not within functions.
        - Beware of bare Excepts, they will obscure all errors. "There is one
        thing worse than software that crashes, and that's software that doesn't
        crash when it's supposed to".
"""
