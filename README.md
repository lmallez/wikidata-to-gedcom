# wikidata-to-gedcom

use wikidata lineage to generate a gedcom file

### Usage

```
usage: WikidataToGedcom.py [-h] [--max-depth MAX_DEPTH]
                           [--allow-men ALLOW_MEN]
                           [--men-descendants MEN_DESCENDANTS]
                           [--men-ascendants MEN_ASCENDANTS]
                           [--allow-women ALLOW_WOMEN]
                           [--women-descendants WOMEN_DESCENDANTS]
                           [--women-ascendants WOMEN_ASCENDANTS]
                           [--load-parents LOAD_PARENTS]
                           [--load-children LOAD_CHILDREN]
                           [--enable-correction ENABLE_CORRECTION]
                           id {all,desc,asc,linear} output
```

| name              | type | default | description                                                        |
|-------------------|------|---------|--------------------------------------------------------------------|
| id                | str  |         | wikidata id of the entity choose                                   |
| method            | str  |         | {all, asc, desc, linear} method of gedcom generation (see bellow)  |
| output            | str  |         | output file name                                                   |
| max_depth         | int  | 10      | maximum number of generation differences                           |
| allow-mens        | bool | True    | add men in gedcom                                                  |
| men-descendants   | bool | True    | add men descendants (can't be activate if `allow-men` is false)    |
| men-ascendants    | bool | True    | add men ascendants (can't be activate if `allow-men` is false)     |
| allow-womens      | bool | True    | add women in gedcom                                                |
| women-descendants | bool | True    | add women descendants (can't be activate if `allow-women` is false)|
| women-ascendants  | bool | True    | add women ascendants (can't be activate if `allow-women` is false) |
| load-parents      | bool | False   | add the parents of each character                                  |
| load-children     | bool | False   | add the children of each character                                 |
| enable-correction | bool | True    | add missing wikidata links                                         |

| methods of gedcom generation | description                                              |
|-----------------------------|-----------------------------------------------------------|
| all                         | all the family members (can take a long time to complete) |
| desc                        | all the descendants of the root character                 |
| asc                         | all the ascendants of the root character                  |
| linear                      | combine desc and asc                                      |

_beware of the different options you choose, some characters have a very large number of ancestors on wikidata_

### Samples

*the generated images bellow are not created in this project, they are generated via the [gramps software](https://gramps-project.org/blog/) from the output gedcom*

* `WikidataToGedcom.py Q9696 linear ../samples/Q9696_1.ged`
![img](https://github.com/lmallez/wikidata-to-gedcom/blob/master/samples/Q9696_1.png)

* `WikidataToGedcom.py Q9696 linear ../samples/Q9696_2.ged --load-children 1 --load-parents 1`
![img](https://github.com/lmallez/wikidata-to-gedcom/blob/master/samples/Q9696_2.png)

* `WikidataToGedcom.py Q82339 desc ../sample Q82339 --allow-women 0`
![img](https://github.com/lmallez/wikidata-to-gedcom/blob/master/samples/Q82339.png)

* `Q2042 all ../samples/Q2042.ged`
![img](https://github.com/lmallez/wikidata-to-gedcom/blob/master/samples/Q2042.png)

### TODO

* parse the name and use GIVN and SURN tags
* use more properties of wikidata to fill gedcom (date of birth/death, weddings...)
* find an appropriate way to enter into transactions when a wikidata entity has more than one parent
