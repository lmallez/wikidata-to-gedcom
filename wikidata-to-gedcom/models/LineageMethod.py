#!/usr/bin/env python3
from enum import IntEnum


class LineageMethod(IntEnum):
    NOTHING = -1
    NONE = 0
    ASC = 1
    DESC = 2
    BOTH = 4
