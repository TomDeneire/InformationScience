"""
Exercise for urllib in Python
"""

import time
from urllib import request
import urllib.error

EVIL = "https://evilinsult.com/generate_insult.php?lang=en&type=json"


def fetch_insult() -> str:
    """
    Fetch random insult from Evil Insult Generator
    https://evilinsult.com/generate_insult.php?lang=en&type=json
    Using delay for safety.
    """
    insult = ""
    time.sleep(2)
    # your code here
    try:
        with urllib.request.urlopen(EVIL) as query:
            insult = str(query.read())
            return insult
    except (urllib.error.HTTPError, urllib.error.URLError) as err:
        exit(err)


if __name__ == "__main__":
    insults = []
    for example in range(0, 100):
        insults.append(fetch_insult())
    print(insults)
