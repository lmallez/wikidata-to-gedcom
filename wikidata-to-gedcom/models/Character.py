#!/usr/bin/env python3
from typing import Union

from wikidata.entity import EntityId

from models.Date import Date


class CharacterLineage:
    def __init__(self):
        self.father_id = None
        self.mother_id = None
        self.child_ids: [str] = []


class CharacterData:
    def __init__(self):
        self.given_name = None
        self.family_name = None
        self.birth_date: Union[Date, None] = None
        self.death_date: Union[Date, None] = None


class Character:
    def __init__(self, character_id: EntityId):
        self.id = character_id
        self.label = None
        self.sex: chr = None
        self.data = None
        self.lineage = None


