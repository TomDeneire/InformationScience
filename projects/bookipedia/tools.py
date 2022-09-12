"""
Tools module for Bookipedia
"""

import sys
import urllib.parse
import urllib.request
import urllib.error


def clean(string: str, type: str) -> str:
    """
    Clean input string (if necessary) and URL encode
    """
    string = urllib.parse.quote(string)
    if type == "search":
        string = string.strip()
        string = string.casefold()
    return string


def url_reader(url: str) -> bytes:
    """
    Read url request and return bytes or error
    """
    try:
        with urllib.request.urlopen(url) as response:
            return response.read()
    except (urllib.error.HTTPError, urllib.error.URLError) as err:
        sys.exit(err)


def template(result: dict) -> str:
    """
    Return result as HTML template
    """
    if "No further information" in result["label"]:
        html = f'<div>{result["label"]}</div>'
        return html
    title = template_title(result)
    author = template_author(result)
    html = f'''
    <div>
    <h1>{result["label"]}</h1>
    {title}
    {author}
    <h3>More information</h3>
    <p><a href="{result["externallinks"]}">{result["externallinks"]}</p>
    </div>
    '''
    return html


def template_title(result: dict) -> str:
    book_image = ""
    book_image_link = result.get("wikidataimage")
    if book_image_link is not None:
        book_image = f'<p><img src="{book_image_link}" style="width:150px;"></p>'
    template = f'''
    <h3>About this book</h3>
    {book_image}
    <p>{result["abstract"]}</p>'''
    return template


def template_author(result: dict) -> str:
    author_image = ""
    author_image_link = result.get("authorwikidataimage")
    if author_image_link is not None:
        author_image = f'<p><img src="{author_image_link}" style="width:150px;"></p>'
    author_abstract_text = "No information about this author"
    author_abstract = result.get("authorabstract")
    if author_abstract is not None:
        author_abstract_text = f'<p>{result["authorabstract"]}</p>'''
    template = f'''
    <h3>About the author</h3>
    {author_image}
    {author_abstract_text}'''
    return template
