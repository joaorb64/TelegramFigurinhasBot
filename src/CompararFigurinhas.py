#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import sys

def lerArquivo(filename):
    try:
        f = open(filename, "r")
        f.readline()
        
        mine = f.readline().strip().split(",")
        mine = [int(i) for i in mine]
        print("minhas: " + str(mine));

        f.close()

        return(mine);
    except IOError:
        print(IOError)

def comparaArquivos(faltam, tenho):
    print(u"Diferença: " + str(sorted(list(set(faltam).difference(tenho)))))

arquivo1 = raw_input("File1: ")
tenho = lerArquivo(arquivo1)

arquivo2 = raw_input("File2: ")
tem = lerArquivo(arquivo2)

comparaArquivos(tem, tenho)