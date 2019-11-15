#!/usr/bin/env python3

from wikidata.entity import Entity, EntityId

from builder.PropertyExtract import get_date, get_parent_id, get_children_ids
from models.Character import CharacterData, CharacterLineage, Character
from mywikidata.WikidataKeys import WikidataKey


class CharacterBuilder:
    @staticmethod
    def has_claims(key: str, entity: Entity):
        return key in entity.data['claims']

    # TODO reword
    @staticmethod
    def build_lineage(entity: Entity, character_cache: [EntityId]) -> CharacterLineage:
        lineage = CharacterLineage()
        if WikidataKey.FATHER in entity.data['claims']:
            lineage.father_id = get_parent_id(entity.data['claims'][WikidataKey.FATHER], character_cache)
        if WikidataKey.MOTHER in entity.data['claims']:
            lineage.mother_id = get_parent_id(entity.data['claims'][WikidataKey.MOTHER], character_cache)
        if WikidataKey.CHILD in entity.data['claims']:
            lineage.child_ids = get_children_ids(entity.data['claims'][WikidataKey.CHILD])
        return lineage

    @staticmethod
    def build_data(entity: Entity) -> CharacterData:
        data = CharacterData()
        if WikidataKey.DATE_OF_BIRTH in entity.data['claims']:
            data.birth_date = get_date(entity.data['claims'][WikidataKey.DATE_OF_BIRTH])
        if WikidataKey.DATE_OF_DEATH in entity.data['claims']:
            data.death_date = get_date(entity.data['claims'][WikidataKey.DATE_OF_DEATH])
        return data

    @staticmethod
    def build_base(entity: Entity) -> Character:
        character = Character(entity.id)
        character.label = entity.label
        if WikidataKey.SEX in entity.data['claims'] and len(entity.data['claims'][WikidataKey.SEX]) > 0:
            sex_id = entity.data['claims'][WikidataKey.SEX][0]['mainsnak']['datavalue']['value']['id']
            if sex_id == WikidataKey.MALE:
                character.sex = 'M'
            elif sex_id == WikidataKey.FEMALE:
                character.sex = 'F'
        return character
