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
        self.add_argument('id', type=str, help='wikidata elements id')
        self.add_argument('method', type=str, help='method of generation (all: all related characters, desc: direct '
                                                   'descendants, asc: direct ascendants, linear: desc + asc)',
                          choices=['all', 'desc', 'asc', 'linear'])
        self.add_argument('output', type=str, help='output file')
        self.add_argument('--max-depth', type=int, default=10, help='maximum number of generation differences')
        self.add_argument('--allow-women', type=str2bool, default=True, help='allow women to be on gedcom')
        self.add_argument('--allow-men', type=str2bool, default=True, help='allow men to be on gedcom')
        self.add_argument('--men-descendant', type=str2bool, default=True, help='load men descendants')
        self.add_argument('--men-ascendant', type=str2bool, default=True, help='load men ascendants')
        self.add_argument('--women-descendant', type=str2bool, default=True, help='load women descendants')
        self.add_argument('--women-ascendant', type=str2bool, default=True, help='load women ascendants')
        self.add_argument('--enable-correction', type=str2bool, default=True, help='add missing paternity links in one way')
        self.add_argument('--load-children', type=str2bool, default=False, help='load every character children')
        self.add_argument('--load-parents', type=str2bool, default=False, help='load every character parents')
        self.args = self.parse_args()

    def create_wikidata(self):
        wikidata = WikidataWrapper(self.args.id, self.args.max_depth)
        wikidata.allow_women = self.args.allow_women
        print('{}={}'.format('allow_women', wikidata.allow_women))
        wikidata.allow_men = self.args.allow_men
        print('{}={}'.format('allow_men', wikidata.allow_men))
        wikidata.men_descendant = self.args.men_descendant and wikidata.allow_men
        print('{}={}'.format('men_descendant', wikidata.men_descendant))
        wikidata.men_ascendant = self.args.men_ascendant and wikidata.allow_men
        print('{}={}'.format('men_ascendant', wikidata.men_ascendant))
        wikidata.women_descendant = self.args.women_descendant and wikidata.allow_women
        print('{}={}'.format('women_descendant', wikidata.women_descendant))
        wikidata.women_ascendant = self.args.women_ascendant and wikidata.allow_women
        print('{}={}'.format('women_ascendant', wikidata.women_ascendant))
        wikidata.load_children = self.args.load_children
        print('{}={}'.format('load_children', wikidata.load_children))
        wikidata.load_parents = self.args.load_parents
        print('{}={}'.format('load_parents', wikidata.load_parents))
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
