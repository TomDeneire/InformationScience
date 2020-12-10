"""
Exercise for urllib in Python
"""

import time


def fetch_insult() -> str:
    """
    Fetch random insult from Evil Insult Generator
    https://evilinsult.com/generate_insult.php?lang=en&type=json
    Using delay for safety.
    """
    insult = ""
    time.sleep(2)
    # your code here
    return insult


if __name__ == "__main__":
    insults = []
    for example in range(0, 100):
        insults.append(fetch_insult())
    print(insults)
