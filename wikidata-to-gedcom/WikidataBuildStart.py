#!/usr/bin/env python3
from WikidataBuilder import WikidataBuilder
from models.LineageMethod import LineageMethod


class WikidataBuilderStart(WikidataBuilder):
    def __init__(self, root_id, max_depth):
        super().__init__(root_id, max_depth)

    def start_all(self):
        self.init_character(self.root_id, LineageMethod.BOTH)

    def start_ascendants(self):
        self.init_character(self.root_id, LineageMethod.ASC)

    def start_descendants(self):
        self.init_character(self.root_id, LineageMethod.DESC)

    def start_linear(self):
        self.init_character(self.root_id, LineageMethod.ASC)
        self.init_character(self.root_id, LineageMethod.DESC)
