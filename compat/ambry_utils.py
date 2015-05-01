# -*- coding: utf-8 -*-
from logging import getLogger

from ambry.run import get_runconfig
from ambry.identity import NumberServer

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
