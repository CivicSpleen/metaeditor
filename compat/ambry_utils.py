# -*- coding: utf-8 -*-
from logging import getLogger

from ambry import library
from ambry.identity import NumberServer
from ambry.run import get_runconfig

logger = getLogger(__name__)


def get_vid():
    """ Retrieves unique number from ambry service and returns that number or None
        if retrieve failed. """
    try:
        rc = get_runconfig()
        nsconfig = rc.service('numbers')
        ns = NumberServer(**nsconfig)
        return str(ns.next())
    except Exception as exc:
        logger.error('`{}` error while retrieving vid from ambry.'.format(exc))


def search(term, limit=30):
    """ Searches names in the ambry library. Returns list of names. """
    l = library()
    try:
        search_result = l.search.search_identifiers(term, limit=limit)
        names = []
        if search_result is not None:
            for result in search_result:
                names.append(result[-1])
        return names
    except Exception as exc:
        logger.error(u'Search term failed with `%s` error.' % exc)
        return []
