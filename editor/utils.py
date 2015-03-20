# -*- coding: utf-8 -*-
from urlparse import urlparse

from HTMLParser import HTMLParser

import requests


class LinksParser(HTMLParser):
    """ Collects all links from given url. """

    def __init__(self, url, *args, **kwargs):
        self.links = []
        self.in_a = False
        self.url = url
        HTMLParser.__init__(self, *args, **kwargs)

    def handle_starttag(self, tag, attrs):
        """ Collects all attributes of the link, extends relative paths."""
        if tag == 'a':
            self.in_a = True
            link = {val: key for val, key in attrs}
            href = link.get('href', '')
            if href.startswith('/') and not href.startswith('//'):
                # relative path, convert to full
                link['href'] = urlparse(self.url)._replace(path=href).geturl()
            self.links.append(link)

    def handle_endtag(self, tag):
        if tag == 'a':
            self.in_a = False

    def handle_data(self, data):
        """ Updates last link found with `a` text. """
        if self.in_a:
            self.links[-1]['text'] = data


def get_links(url):
    """ Gets content from url, finds all links in the content and returns the list of dict.

    Args:
        url (str):

    Returns:
        list of dicts: for example [{'text': 'Yandex', 'href': 'http://ya.ru', 'title': 'Yandex'}]

    """
    resp = requests.get(url)
    assert resp.status_code == 200

    parser = LinksParser(url)
    parser.feed(resp.content)
    return parser.links
