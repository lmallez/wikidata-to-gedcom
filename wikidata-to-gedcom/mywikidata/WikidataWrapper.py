#!/usr/bin/env python3
from wikidata.client import Client
from wikidata.entity import EntityId, Entity


class WikidataWrapper:
    class __WikidataWrapper(Client):
        def __init__(self):
            super().__init__()
            self.entity_cache = {}

        def get(self, entity_id: EntityId, load: bool = False) -> Entity:
            if entity_id in self.entity_cache:
                entity = self.entity_cache[entity_id]
            else:
                entity = super().get(entity_id, load)
                self.entity_cache[entity_id] = entity
            return entity

    instance: __WikidataWrapper = None

    def __init__(self):
        if not WikidataWrapper.instance:
            WikidataWrapper.instance = WikidataWrapper.__WikidataWrapper()

    def get(self, entity_id: EntityId, load: bool = False) -> Entity:
        return self.instance.get(entity_id, load)
