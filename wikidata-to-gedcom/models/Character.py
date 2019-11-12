#!/usr/bin/env python3
from typing import List


class Character:
    def __init__(self, character_id: str):
        self.id: str = character_id
        self.child_ids = []
        self.label = None
        self.given_name = None
        self.family_name = None
        self.father_id = None
        self.mother_id = None
        self.sex: chr = None
        self.child_ids: List[str]


