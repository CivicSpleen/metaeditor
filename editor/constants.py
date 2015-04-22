# -*- coding: utf-8 -*-

from geoid.civick import GVid
from geoid import summary_levels


def get_region_choices():
    ret = []
    for level in summary_levels:
        ret.append((str(GVid.get_class(level)().summarize()), level.title()))
    return sorted(ret, key=lambda x: x[1])

REGION_CHOICES = get_region_choices()
