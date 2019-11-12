#!/usr/bin/env python3
from wikidata.client import Client
from wikidata.entity import EntityId, Entity

from EntityToCharacter import entity_to_character
from models.Character import Character


class WikidataWrapper:
    def __init__(self, root_id, max_depth=10):
        self.client = Client()
        self.entity_cache = {}
        self.max_depth = max_depth
        self.root_id = root_id
        self.root = None

    allow_women = True
    allow_men = True
    load_children = True
    load_parents = True
    men_descendants = True
    men_ascendant = True
    women_descendants = True
    women_ascendant = True

    def __get_entity(self, character_id) -> Entity:
        entity = self.client.get(EntityId(character_id), load=True)
        if entity.data is None:
            raise Exception("Entity not found")
        return entity

    def __build_character(self, entity) -> Character:
        return entity_to_character(entity, self.entity_cache)

    def get_character(self, character_id: str, depth=0) -> Character:
        if character_id in self.entity_cache:
            return self.entity_cache[character_id]
        entity = self.__get_entity(character_id)
        if entity is None:
            raise
        print("{} {} {}".format(len(self.entity_cache), depth, entity.label))
        character = self.__build_character(entity)
        self.entity_cache[character_id] = character
        return character

    __descendant_cache = []
    __ascendant_cache = []

    def __get_parents(self, character: Character, depth=0):
        if self.allow_men and character.father_id:
            self.get_character(character.father_id, depth=depth - 1)
        if self.allow_women and character.mother_id:
            self.get_character(character.mother_id, depth=depth - 1)

    def __get_children(self, character: Character, depth):
        if character.child_ids:
            for child_id in character.child_ids:
                child = self.get_character(child_id, depth=depth + 1)
                if child and self.__remove_by_sex(child):
                    del self.entity_cache[child_id]

    def __load_parents(self, character: Character, recursive_call, depth):
        if not -self.max_depth <= depth <= self.max_depth:
            return
        if character.id in self.__ascendant_cache:
            return
        self.__ascendant_cache.append(character.id)
        if self.allow_men and character.father_id:
            father = self.get_character(character.father_id, depth=depth - 1)
            if father and self.men_ascendant:
                recursive_call(father, depth - 1)
        if self.allow_women and character.mother_id:
            mother = self.get_character(character.mother_id, depth=depth - 1)
            if mother and self.women_ascendant:
                recursive_call(mother, depth - 1)

    def __descendants_by_sex(self, character):
        return ((not self.men_descendants and character.sex is 'M')
                or (not self.women_descendants and character.sex is 'F')) \
               and character.id != self.root.id

    def __remove_by_sex(self, character):
        return ((not self.allow_men and character.sex is 'M')
                or (not self.allow_women and character.sex is 'F')) \
               and character.id != self.root.id

    def __load_children(self, character: Character, recursive_call, depth):
        if not -self.max_depth <= depth <= self.max_depth:
            return
        if character.id in self.__descendant_cache:
            return
        self.__descendant_cache.append(character.id)
        if character.child_ids:
            for child_id in character.child_ids:
                child = self.get_character(child_id, depth=depth + 1)
                if child and self.__remove_by_sex(child):
                    del self.entity_cache[child_id]
                elif child and not self.__descendants_by_sex(child):
                    recursive_call(child, depth + 1)

    def __load_all(self, character: Character, depth=0):
        self.__load_parents(character, self.__load_all, depth)
        self.__load_children(character, self.__load_all, depth)

    def __load_ascendants(self, character: Character, depth=0):
        self.__load_parents(character, self.__load_ascendants, depth)
        if self.load_children:
            self.__get_children(character, depth)

    def __load_descendants(self, character: Character, depth=0):
        if self.load_parents:
            self.__get_parents(character, depth)
        self.__load_children(character, self.__load_descendants, depth)

    def load_root(self):
        self.root = self.get_character(self.root_id)

    def load_all(self):
        if not self.root:
            raise
        self.__load_all(self.root, 0)

    def load_ascendants(self):
        if not self.root:
            raise
        self.__load_ascendants(self.root, 0)

    def load_descendants(self):
        if not self.root:
            raise
        self.__load_descendants(self.root, 0)

    def load_linear(self):
        if not self.root:
            raise
        self.__load_ascendants(self.root, 0)
        self.__load_descendants(self.root, 0)

    def __correct_parent(self, character, parent_id):
        if not parent_id in self.entity_cache:
            return
        parent = self.entity_cache[parent_id]
        if parent and not character.id in parent.child_ids:
            print('correct link "{}" <- "{}"'.format(character.id, parent_id))
            parent.child_ids.append(character.id)

    def __correct_child(self, character, child_id):
        if not child_id in self.entity_cache:
            return
        child = self.entity_cache[child_id]
        if character.sex == 'M' and not child.father_id:
            print('correct link "{}" -> "{}"'.format(character.id, child_id))
            child.father_id = character.id
        if character.sex == 'F' and not child.mother_id:
            print('correct link "{}" -> "{}"'.format(character.id, child_id))
            child.mother_id = character.id

    def correct_family_links(self):
        for entity_id, character in self.entity_cache.items():
            if character.father_id:
                self.__correct_parent(character, character.father_id)
            if character.mother_id:
                self.__correct_parent(character, character.mother_id)
            if character.sex and character.child_ids:
                for child_id in character.child_ids:
                    self.__correct_child(character, child_id)
