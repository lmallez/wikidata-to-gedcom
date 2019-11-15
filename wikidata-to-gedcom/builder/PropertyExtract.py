#!/usr/bin/env python3
from models.Date import Date
from mywikidata.WikidataKeys import WikidataKey


def is_human(entity):
    if WikidataKey.INSTANCE_OF in entity.data['claims']:
        for instance in entity.data['claims'][WikidataKey.INSTANCE_OF]:
            if instance['mainsnak']['datavalue']['value']['id'] == WikidataKey.HUMAN:
                return True
    return False


def get_parent_id(properties, entity_cache):
    parents_ids = []
    for parent in properties:
        if 'datavalue' in parent['mainsnak']:
            parents_ids.append(parent['mainsnak']['datavalue']['value']['id'])
    if len(parents_ids) > 0:
        loads_parents = list(set(parents_ids).intersection(entity_cache))
        return loads_parents[0] if len(loads_parents) > 0 else parents_ids[0]
    return None


def get_children_ids(properties):
    child_ids = []
    for child in properties:
        if 'qualifiers' in child and WikidataKey.TYPE_OF_KINSHIP in child['qualifiers']:
            if sum([1 if kinship['datavalue']['value']['id'] in [WikidataKey.ADOPTED] else 0 for kinship in
                    child['qualifiers'][WikidataKey.TYPE_OF_KINSHIP]]) > 0:
                continue
        if 'datavalue' in child['mainsnak']:
            child_ids.append(child['mainsnak']['datavalue']['value']['id'])
    return child_ids


def get_date(properties):  # TODO : refactor this
    if len(properties) == 0:
        return None
    data_property = properties[0]
    if not 'datavalue' in data_property['mainsnak']:
        return None
    precision = data_property['mainsnak']['datavalue']['value']['precision']
    time = data_property['mainsnak']['datavalue']['value']['time']
    if precision < 9:
        return None
    return Date(time[1:5])
