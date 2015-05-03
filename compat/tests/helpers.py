# -*- coding: utf-8 -*-

import fudge


local_cache = {}


def patch_identifier_index(result):
    """ Patches ambry search identifier to return given result. """
    from ambry.library.search import Search

    # convert each dict in the result to the hit expected by searcher.
    class MyDict(dict):
        pass

    new_result = []
    for i, one in enumerate(result):
        my = MyDict()
        my.update(one)
        my.score = i
        new_result.append(my)

    class FakeSearcher(object):
        def search(self, query, limit=20):
            return new_result

        def __enter__(self, *args, **kwargs):
            return self

        def __exit__(self, *args, **kwargs):
            pass

    class FakeIdentifierIndex(object):
        schema = '?'

        def searcher(*args, **kwargs):
            return FakeSearcher()

    local_cache['patched_identifier_index'] = fudge.patch_object(
        Search, 'identifier_index', FakeIdentifierIndex())


def restore_patched():
    local_cache['patched_identifier_index'].restore()
