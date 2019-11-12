#!/usr/bin/env python3
from typing import Dict

from wikidata.entity import Entity

from models.Character import Character


class WikidataKey:
    HUMAN = 'Q5'
    MALE = 'Q6581097'
    FEMALE = 'Q6581072'
    ADOPTED = 'Q20746725'
    SEX = 'P21'
    FATHER = 'P22'
    MOTHER = 'P25'
    INSTANCE_OF = 'P31'
    CHILD = 'P40'
    GIVEN_NAME = 'P735'
    FAMILY_NAME = 'P734'
    DATE_OF_BIRTH = 'P569'
    DATE_OF_DEATH = 'P570'
    TYPE_OF_KINSHIP = 'P1039'


def is_human(entity):
    if WikidataKey.INSTANCE_OF in entity.data['claims']:
        for instance in entity.data['claims'][WikidataKey.INSTANCE_OF]:
            if instance['mainsnak']['datavalue']['value']['id'] == WikidataKey.HUMAN:
                return True
    return False


def entity_to_character(entity: Entity, entity_cache: Dict) -> Character:
    # if not is_human(entity):
    #     raise Exception("entity is not an human")
    character = Character(str(entity.id))
    character.label = entity.label
    if WikidataKey.SEX in entity.data['claims'] and len(entity.data['claims'][WikidataKey.SEX]) > 0:
        sex_id = entity.data['claims'][WikidataKey.SEX][0]['mainsnak']['datavalue']['value']['id']
        if sex_id == WikidataKey.MALE:
            character.sex = 'M'
        elif sex_id == WikidataKey.FEMALE:
            character.sex = 'F'
        # TODO : rework this
    if WikidataKey.FATHER in entity.data['claims']:
        father_ids = []
        for father in entity.data['claims'][WikidataKey.FATHER]:
            if 'datavalue' in father['mainsnak']:
                father_ids.append(father['mainsnak']['datavalue']['value']['id'])
        if len(father_ids) > 0:
            loads_fathers = list(set(father_ids).intersection(entity_cache.keys()))
            character.father_id = loads_fathers[0] if len(loads_fathers) > 0 else father_ids[0]
    # TODO : rework this
    if WikidataKey.MOTHER in entity.data['claims']:
        mother_ids = []
        for mother in entity.data['claims'][WikidataKey.MOTHER]:
            if 'datavalue' in mother['mainsnak']:
                mother_ids.append(mother['mainsnak']['datavalue']['value']['id'])
        if len(mother_ids) > 0:
            loads_mothers = list(set(mother_ids).intersection(entity_cache.keys()))
            character.mother_id = loads_mothers[0] if len(loads_mothers) > 0 else mother_ids[0]
    # TODO: rework this
    if WikidataKey.CHILD in entity.data['claims']:
        for child in entity.data['claims'][WikidataKey.CHILD]:
            if 'qualifiers' in child and WikidataKey.TYPE_OF_KINSHIP in child['qualifiers']:
                if sum([1 if kinship['datavalue']['value']['id'] in [WikidataKey.ADOPTED] else 0 for kinship in child['qualifiers'][WikidataKey.TYPE_OF_KINSHIP]]) > 0:
                    continue
            if 'datavalue' in child['mainsnak']:
                character.child_ids.append(child['mainsnak']['datavalue']['value']['id'])
    return character
