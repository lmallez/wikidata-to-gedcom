#!/usr/bin/env python3
from threading import Thread
from typing import List, Tuple

from wikidata.entity import EntityId

from builder.CharacterBuilder import CharacterBuilder
from models.Character import Character
from models.LineageMethod import LineageMethod
from mywikidata.WikidataWrapper import WikidataWrapper


class WikidataBuilder:
    def __init__(self, root_id, max_depth):
        self.max_depth = max_depth
        self.wikidata = WikidataWrapper()
        self.character_builder = CharacterBuilder()
        self.root_id = root_id
        self.character_cache = {}

    def init_character(self, entity_id: EntityId, lineage_method: LineageMethod, depth=0) -> Character:
        if entity_id in self.character_cache:
            character = self.character_cache[entity_id]
        else:
            entity = self.wikidata.get(entity_id, load=True)
            character = self.character_builder.build_base(entity)
            # TODO : set up threads when data will need to make another request to mywikidata
            character.lineage = self.character_builder.build_lineage(entity, self.character_cache.keys())
            character.data = self.character_builder.build_data(entity)
            if character and not self.__remove_by_sex(character):
                self.character_cache[character.id] = character
        print("{} {} {}\n".format(len(self.character_cache), depth, character.label), end='', flush=True)
        self.__load_character_lineage(character, lineage_method, depth)
        return character

    allow_men = True
    men_descendants = True
    men_ascendants = True

    allow_women = True
    women_descendants = True
    women_ascendants = True

    load_children = True
    load_parents = True

    __descendant_cache = []
    __ascendant_cache = []

    def __max_depth(self, depth):
        return -self.max_depth <= depth <= self.max_depth

    def __descendants_by_sex(self, character):
        return not ((not self.men_descendants and character.sex == 'M')
                    or (not self.women_descendants and character.sex == 'F')) \
               or character.id == self.root_id

    def __ascendants_by_sex(self, character):
        return not ((not self.men_ascendants and character.sex == 'M')
                    or (not self.women_ascendants and character.sex == 'F')) \
               or character.id == self.root_id

    def __remove_by_sex(self, character):
        return ((not self.allow_men and character.sex == 'M')
                or (not self.allow_women and character.sex == 'F')) \
               and character.id != self.root_id

    def __load_character_ascendants(self, character: Character, method: LineageMethod, depth):
        if not -self.max_depth <= depth <= self.max_depth:
            return
        if character.id in self.__ascendant_cache:
            return
        self.__ascendant_cache.append(character.id)
        father_id = character.lineage.father_id
        to_init = []
        if self.allow_men and father_id:
            to_init.append((father_id, method if self.men_ascendants else LineageMethod.NONE))
        mother_id = character.lineage.mother_id
        if self.allow_women and character.lineage.mother_id:
            to_init.append((mother_id, method if self.women_ascendants else LineageMethod.NONE))
        self.__init_characters(to_init, depth - 1)

    def __load_character_descendants(self, character: Character, method: LineageMethod, depth):
        if not self.__max_depth(depth) or character.id in self.__descendant_cache:
            return
        self.__descendant_cache.append(character.id)
        if character.lineage.child_ids:
            to_init = [(child_id, method) for child_id in character.lineage.child_ids]
            self.__init_characters(to_init, depth + 1)

    def __load_character_lineage(self, character: Character, method: LineageMethod, depth=0):
        if method == LineageMethod.NOTHING:
            return
        if method == LineageMethod.ASC or method == LineageMethod.BOTH and self.__ascendants_by_sex(character):
            self.__load_character_ascendants(character, method, depth=depth)
        elif self.load_parents:
            self.__load_character_ascendants(character, LineageMethod.NOTHING, depth=depth)
        if (method == LineageMethod.DESC or method == LineageMethod.BOTH) and self.__descendants_by_sex(character):
            self.__load_character_descendants(character, method, depth=depth)
        elif self.load_children:
            self.__load_character_descendants(character, LineageMethod.NOTHING, depth=depth)

    thread_max = 100
    __thread_nbr = 0

    def __init_characters(self, entities: List[Tuple[EntityId, LineageMethod]], depth=0):
        if len(entities) == 0:
            return
        if len(entities) == 1:
            self.init_character(entities[0][0], entities[0][1], depth)
            return
        threads = []
        other_entities = []
        for entity in entities:
            if self.__thread_nbr < self.thread_max:
                threads.append(Thread(target=self.init_character, args=(entity[0], entity[1], depth)))
                self.__thread_nbr += 1
            else:
                other_entities.append(entity)
        for thread in threads:
            thread.start()
        for entity in other_entities:
            self.init_character(entity[0], entity[1], depth)
        for thread in threads:
            thread.join()
        self.__thread_nbr -= len(threads)
