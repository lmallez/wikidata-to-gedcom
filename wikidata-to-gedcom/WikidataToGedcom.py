#!/usr/bin/env python3

import argparse

from GedcomWritter import write_gedcom
from export.Gedcom import GedcomExporter
from wrapper.Wikidata import WikidataWrapper

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
        self.add_argument('id', type=str, help='wikidata id of the entity choose')
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
        self.add_argument('--load-parents', type=str2bool, default=False, help='add the parents of each character')
        self.add_argument('--load-children', type=str2bool, default=False, help='add the children of each character')
        self.add_argument('--enable-correction', type=str2bool, default=True, help='add missing wikidata links')
        self.args = self.parse_args()

    def create_wikidata(self):
        wikidata = WikidataWrapper(self.args.id, self.args.max_depth)
        wikidata.allow_men = self.args.allow_men
        print('{}={}'.format('allow_men', wikidata.allow_men))
        wikidata.men_descendants = self.args.men_descendants and wikidata.allow_men
        print('{}={}'.format('men_descendants', wikidata.men_descendants))
        wikidata.men_ascendants = self.args.men_ascendants and wikidata.allow_men
        print('{}={}'.format('men_ascendants', wikidata.men_ascendants))
        wikidata.allow_women = self.args.allow_women
        print('{}={}'.format('allow_women', wikidata.allow_women))
        wikidata.women_descendants = self.args.women_descendants and wikidata.allow_women
        print('{}={}'.format('women_descendants', wikidata.women_descendants))
        wikidata.women_ascendants = self.args.women_ascendants and wikidata.allow_women
        print('{}={}'.format('women_ascendants', wikidata.women_ascendants))
        wikidata.load_parents = self.args.load_parents
        print('{}={}'.format('load_parents', wikidata.load_parents))
        wikidata.load_children = self.args.load_children
        print('{}={}'.format('load_children', wikidata.load_children))
        return wikidata

    def get_method(self):
        return {
            'all': WikidataWrapper.load_all,
            'asc': WikidataWrapper.load_ascendants,
            'desc': WikidataWrapper.load_descendants,
            'linear': WikidataWrapper.load_linear
        }[self.args.method]


if __name__ == "__main__":
    parser = ArgParse()

    print("==== START SETUP ====")
    wikidata = parser.create_wikidata()

    print("==== START LOAD =====")
    wikidata.load_root()
    parser.get_method()(wikidata)

    if parser.args.enable_correction:
        print("==== START CORRECT =====")
        wikidata.correct_family_links()

    print("==== START EXPORT =====")
    gedcom_export = GedcomExporter(wikidata.entity_cache)
    write_gedcom(parser.args.output, gedcom_export.collect_elements())
