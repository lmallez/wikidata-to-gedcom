#!/usr/bin/env python3

import argparse

from DataCorrecter import DataCorrecter
from GedcomWritter import write_gedcom
from WikidataBuildStart import WikidataBuilderStart
from export.Gedcom import GedcomExporter


def str2bool(v):
    if isinstance(v, bool):
        return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')


class ArgParse(argparse.ArgumentParser):
    def __init__(self):
        super().__init__(description='Fetch Wikidata API to generate a gedcom file')
        self.add_argument('id', type=str, help='mywikidata id of the entity choose')
        self.add_argument('method', type=str, help='method of generation (all: all related characters, desc: direct '
                                                   'descendants, asc: direct ascendants, linear: desc + asc)',
                          choices=['all', 'desc', 'asc', 'linear'])
        self.add_argument('output', type=str, help='output file name')
        self.add_argument('--max-depth', type=int, default=10, help='maximum number of generation differences')
        self.add_argument('--allow-men', type=str2bool, default=True, help='add men in gedcom')
        self.add_argument('--men-descendants', type=str2bool, default=True, help='add men descendants (can\'t be activate if `allow-men` is false)')
        self.add_argument('--men-ascendants', type=str2bool, default=True, help='add men ascendants (can\'t be activate if `allow-men` is false)')
        self.add_argument('--allow-women', type=str2bool, default=True, help='add women in gedcom')
        self.add_argument('--women-descendants', type=str2bool, default=True, help='add women descendants (can\'t be activate if `allow-women` is false)')
        self.add_argument('--women-ascendants', type=str2bool, default=True, help='add women ascendants (can\'t be activate if `allow-women` is false)')
        self.add_argument('--load-parents', type=str2bool, default=False, help='add the parents of each builder')
        self.add_argument('--load-children', type=str2bool, default=False, help='add the children of each builder')
        self.add_argument('--enable-correction', type=str2bool, default=True, help='add missing mywikidata links')
        self.add_argument('--thread-max', type=int, default=100, help='maximum number of threads')
        self.args = self.parse_args()

    def create_wikidata(self):
        wikidata_builder = WikidataBuilderStart(self.args.id, self.args.max_depth)
        wikidata_builder.allow_men = self.args.allow_men
        print('{}={}'.format('allow_men', wikidata_builder.allow_men))
        wikidata_builder.men_descendants = self.args.men_descendants and wikidata_builder.allow_men
        print('{}={}'.format('men_descendants', wikidata_builder.men_descendants))
        wikidata_builder.men_ascendants = self.args.men_ascendants and wikidata_builder.allow_men
        print('{}={}'.format('men_ascendants', wikidata_builder.men_ascendants))
        wikidata_builder.allow_women = self.args.allow_women
        print('{}={}'.format('allow_women', wikidata_builder.allow_women))
        wikidata_builder.women_descendants = self.args.women_descendants and wikidata_builder.allow_women
        print('{}={}'.format('women_descendants', wikidata_builder.women_descendants))
        wikidata_builder.women_ascendants = self.args.women_ascendants and wikidata_builder.allow_women
        print('{}={}'.format('women_ascendants', wikidata_builder.women_ascendants))
        wikidata_builder.load_parents = self.args.load_parents
        print('{}={}'.format('load_parents', wikidata_builder.load_parents))
        wikidata_builder.load_children = self.args.load_children
        print('{}={}'.format('load_children', wikidata_builder.load_children))
        wikidata_builder.thread_max = self.args.thread_max
        return wikidata_builder

    def get_method(self):
        return {
            'all': WikidataBuilderStart.start_all,
            'asc': WikidataBuilderStart.start_ascendants,
            'desc': WikidataBuilderStart.start_descendants,
            'linear': WikidataBuilderStart.start_linear
        }[self.args.method]


if __name__ == "__main__":
    parser = ArgParse()

    print("==== START SETUP ====")
    wikidata = parser.create_wikidata()

    print("==== START LOAD =====")
    parser.get_method()(wikidata)

    characters = wikidata.character_cache

    if parser.args.enable_correction:
        print("==== START CORRECT =====")
        data_correcter = DataCorrecter(characters)
        data_correcter.correct_family_links()

    print("==== START EXPORT =====")
    gedcom_export = GedcomExporter(characters)
    write_gedcom(parser.args.output, gedcom_export.collect_elements())
