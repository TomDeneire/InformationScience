"""
Bookipedia wrapper
"""

import dbpedia
import tools


def run(search: str) -> str:
    if search == "":
        print("Please try again and enter a book title.")
        return ""
    query_result = dbpedia.query(search)
    hits = dbpedia.get_hits(query_result)
    if len(hits) == 0:
        print("No results found. Please try again.")
        return ""
    elif len(hits) == 1:
        choice = hits[1]["URI"]
    else:
        for nr, hit in hits.items():
            print(nr, ":", hit["Label"])
        selection = 0
        while selection not in hits:
            try:
                selection = int(input("Select a book from the list: "))
            except ValueError:
                selection = 0
        choice = hits[selection]["URI"]
    book = dbpedia.lookup_hit(choice, "dbpedia")
    result = dbpedia.process_hit(book, choice)
    template = tools.template(result)
    return template


if __name__ == "__main__":
    for test in ["",
                 "sdfsdfsdf",
                 "1",
                 "hobbit",
                 "for whom the bell tolls",
                 "the origin of species",
                 "mockingbird"]:
        print(run(test))
