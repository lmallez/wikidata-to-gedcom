#!/usr/bin/env python3
from typing import Dict

from wikidata.entity import EntityId

from models.Character import Character


class DataCorrecter:
    def __init__(self, characters: Dict[EntityId, Character]):
        self.characters = characters

    def __correct_parent(self, character, parent_id):
        if not parent_id in self.characters:
            return
        parent = self.characters[parent_id]
        if parent and not character.id in parent.lineage.child_ids:
            print('correct link "{}" <- "{}"'.format(character.id, parent_id))
            parent.lineage.child_ids.append(character.id)

    def __correct_child(self, character, child_id):
        if not child_id in self.characters:
            return
        child = self.characters[child_id]
        if character.sex == 'M' and not child.lineage.father_id:
            print('correct link "{}" -> "{}"'.format(character.id, child_id))
            child.lineage.father_id = character.id
        if character.sex == 'F' and not child.lineage.mother_id:
            print('correct link "{}" -> "{}"'.format(character.id, child_id))
            child.lineage.mother_id = character.id

    def correct_family_links(self):
        for entity_id, character in self.characters.items():
            if character.lineage.father_id:
                self.__correct_parent(character, character.lineage.father_id)
            if character.lineage.mother_id:
                self.__correct_parent(character, character.lineage.mother_id)
            if character.sex and character.lineage.child_ids:
                for child_id in character.lineage.child_ids:
                    self.__correct_child(character, child_id)
