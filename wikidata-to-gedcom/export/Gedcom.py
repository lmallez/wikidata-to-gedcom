#!/usr/bin/env python3

from gedcom.element.element import Element

from models.Character import Character


class Family:
    def __init__(self, family_id):
        self.id = family_id
        self.children_ids = []
        self.father_id = None
        self.mother_id = None


class GedcomExporter:
    def __init__(self, character_list: dict):
        self.characters = character_list
        self.families: dict = {}
        self.elements: dict = {}

    def create_character_element(self, character: Character):
        element = Element(0, '@{}@'.format(character.id), 'INDI', '')
        name_element = element.new_child_element('NAME', '', str(character.label))
        if character.data.given_name and character.data.family_name:
            name_element.new_child_element('GIVN', '', character.data.given_name)
            name_element.new_child_element('SURN', '', character.data.family_name)
        if character.data.birth_date:
            birth_element = element.new_child_element('BIRT')
            birth_element.new_child_element('DATE', '', str(character.data.birth_date))
        if character.data.birth_date:
            death_element = element.new_child_element('DEAT')
            death_element.new_child_element('DATE', '', str(character.data.birth_date))
        if character.sex:
            element.new_child_element('SEX', '', character.sex)
        self.create_family(character)
        self.elements[character.id] = element

    def create_family(self, character: Character):
        family_id = '{}//{}'.format(character.lineage.mother_id, character.lineage.father_id)
        if family_id in self.families.keys():
            self.families[family_id].children_ids.append(character.id)
        else:
            family = Family('FAM{}'.format(len(self.families.keys())))
            if character.lineage.mother_id in self.characters.keys():
                family.mother_id = character.lineage.mother_id
            if character.lineage.father_id in self.characters.keys():
                family.father_id = character.lineage.father_id
            if family.mother_id is None and family.father_id is None:
                return
            family.children_ids.append(character.id)
            self.families[family_id] = family

    def create_family_element(self, family: Family):
        if family.mother_id == 'Q271506':
            print('Q271506')
        element = Element(0, '@{}@'.format(family.id), 'FAM', '')
        if family.father_id and family.father_id in self.elements.keys():
            element.new_child_element('HUSB', '', '@{}@'.format(family.father_id))
            self.elements[family.father_id].new_child_element('FAMS', '', '@{}@'.format(family.id))
        if family.mother_id and family.mother_id in self.elements.keys():
            element.new_child_element('WIFE', '', '@{}@'.format(family.mother_id))
            self.elements[family.mother_id].new_child_element('FAMS', '', '@{}@'.format(family.id))
        for child_id in family.children_ids:
            if child_id in self.characters.keys():
                element.new_child_element('CHIL', '', '@{}@'.format(child_id))
                self.elements[child_id].new_child_element('FAMC', '', '@{}@'.format(family.id))
        self.elements[family.id] = element

    def collect_elements(self):
        for character in self.characters.values():
            self.create_character_element(character)
        for family in self.families.values():
            self.create_family_element(family)
        return self.elements.values()
