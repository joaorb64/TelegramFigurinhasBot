#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import sys

TOTAL = str(list(range(0,681)))[1:-1]

def getStickers(text):
    mine = text.splitlines()[1].strip()
    print("getStickers got: " + str(mine))
    return(mine)

def getStickersComplement(text):
    remaining = text.splitlines()[1].strip()
    return compareStickers(TOTAL, remaining)

def compareStickers(faltam, tenho):
    separator = ","
    faltamNum = [int(i) for i in faltam.split(",")]
    tenhoNum = [int(i) for i in tenho.split(",")]
    diff = sorted(list(set(faltamNum).difference(tenhoNum)))
    print(u"Diferença: " + str(diff))
    return separator.join(str(x) for x in diff)