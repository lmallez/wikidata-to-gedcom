#!/usr/bin/env python3
from datetime import datetime
from typing import List

from gedcom.element.element import Element

HEADER = '0 HEAD\n1 SOUR Wikidata to Gedcom\n2 VERS 5.1.1\n2 NAME Wikidata to Gedcom\n1 DATE {}\n2 TIME {}\n1 SUBM @SUBM@\n1 FILE {}\n1 GEDC\n2 VERS 5.5.1\n2 FORM LINEAGE-LINKED\n1 CHAR UTF-8\n1 LANG English\n0 @SUBM@ SUBM\n1 NAME\n1 ADDR\n'

FOOTER = '0 TRLR\n'


def print_element(file, element: Element, depth=0):
    file.write(element.to_gedcom_string())
    for child in element.get_child_elements():
        print_element(file, child, depth=depth+1)


def write_gedcom(output_file, elements: List[Element]):
    f = open(output_file, "w+")
    dt = datetime.now()
    f.write(HEADER.format(
        dt.strftime("%d %b %Y"),
        dt.strftime("%H:%M:%S"),
        output_file
    ))
    for element in elements:
        print_element(f, element)
    f.write(FOOTER)
    f.close()
