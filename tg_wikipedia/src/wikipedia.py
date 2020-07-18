import re
import logging
from collections import namedtuple
from urllib.parse import urlencode
import requests


logger = logging.getLogger(__name__)
Suggestion = namedtuple('Suggestion', ['pageid', 'text'])
SearchResult = namedtuple('SearchResult', ['title', 'text', 'url'])
regexp = re.compile('<span.*?>(?P<term>.+?)</span>', re.IGNORECASE)


def search(term, lang='ru', suggestions_count=3):
    query_str = urlencode({
        'action': 'query',
        'format': 'json',
        'formatversion': '2',
        'list': 'search',
        'srlimit': suggestions_count + 1,
        'srsearch': term,
    })
    url = f'https://{lang}.wikipedia.org/w/api.php?{query_str}'
    r = requests.get(url)
    if not r.ok:
        print('not ok', r, r.content)
        return False, r.content
    variants = r.json().get('query', {}).get('search')
    if not variants:
        print('not variants', r, r.content)
        return False, r.content
    first = variants[0]
    first_title = first.get('title', term)
    first_text = regexp.sub('\g<term>', first.get('snippet', ''))
    first_url = f'https://{lang}.wikipedia.org/?curid={first["pageid"]}'
    suggestions = ((Suggestion(one['pageid'], one['title']))
                   for one in variants[1:suggestions_count+1])
    return SearchResult(first_title, first_text, first_url), suggestions


def get_page_data(pageid, lang='en', suggestions_count=3):
    query_str = urlencode({
        'action': 'query',
        'format': 'json',
        'formatversion': '2',
        'list': 'backlinks',
        'blpageid': pageid,
    })
    url = f'https://{lang}.wikipedia.org/w/api.php?{query_str}'
    r = requests.get(url)
    if not r.ok:
        return False
    variants = r.json().get('query', {}).get('search')
    if not variants:
        return False
    first = variants[0]
    first_title = first.get('title', term)
    first_text = regexp.sub('\g<term>', first.get('snippet', ''))
    first_url = f'https://{lang}.wikipedia.org/?curid={first["pageid"]}'
    suggestions = ((one['title'], one['pageid']) for one in variants[1:suggestions_count+1])
    return SearchResult(first_title, first_text, first_url), suggestions
