#!/usr/bin/env python3
from wikidata.entity import Entity

from models.Character import Character


class WikidataKey:
    HUMAN = 'Q5'
    MALE = 'Q6581097'
    FEMALE = 'Q6581072'
    SEX = 'P21'
    FATHER = 'P22'
    MOTHER = 'P25'
    INSTANCE_OF = 'P31'
    CHILD = 'P40'
    GIVEN_NAME = 'P735'
    FAMILY_NAME = 'P734'
    DATE_OF_BIRTH = 'P569'
    DATE_OF_DEATH = 'P570'


def is_human(entity):
    if WikidataKey.INSTANCE_OF in entity.data['claims']:
        for instance in entity.data['claims'][WikidataKey.INSTANCE_OF]:
            if instance['mainsnak']['datavalue']['value']['id'] == WikidataKey.HUMAN:
                return True
    return False


def entity_to_character(entity: Entity) -> Character:
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
    if WikidataKey.FATHER in entity.data['claims']:
        for father in entity.data['claims'][WikidataKey.FATHER]:
            if 'datavalue' in father['mainsnak']:
                character.father_id = father['mainsnak']['datavalue']['value']['id']
    if WikidataKey.MOTHER in entity.data['claims']:
        for mother in entity.data['claims'][WikidataKey.MOTHER]:
            if 'datavalue' in mother['mainsnak']:
                character.mother_id = mother['mainsnak']['datavalue']['value']['id']
    if WikidataKey.CHILD in entity.data['claims']:
        for child in entity.data['claims'][WikidataKey.CHILD]:
            if 'datavalue' in child['mainsnak']:
                character.child_ids.append(child['mainsnak']['datavalue']['value']['id'])
    return character
