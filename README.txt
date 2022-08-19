### Enumeration of family relationships in a relationships file.

A python script for the enumeration of different family relationships in a
family relations .txt or .nx file.

### Why should I use this project ?

This script allows you to quickly enumerate the number and types of relationships
found within any family relations .txt file.

### Setup

You need `python>3.8` to run this script.

The project depends on the `pandas`, `networkx`, `itertools`, `numpy`, and `argparse` modules, install them with pip:
`pip install pandas`
`pip install networkx`
etc...

### How to run?

You can run the Enumeration script from the command-line using
```
python Enumeration_Final.py -n -gd -me -t -o
```
Where:
-n --networkx is the whole name of the family relations .txt file.

-gd --generation is the integer of generation depth you want to search for.

-me --meioses is the integer of meioses events you want to search for.

-t --type is the type of relationships you want to search for. These include (half, full, direct, NA).
Where a direct relationsip is a direct descendant/ancestor and NA applies to exclusions such as comparing an individual against themselves.

-o --output is a string that will be the file name of the results output from the Enumeration scripts.

```
Enumeration.py is the main enumeration script. Input is a family relations .txt or .nx file. Output is a results .csv file with every relationship represented by each row. Relationships returned can also be output if the user searched for a specific type of relationshiup during the initial run - where the output files contians all individual pairs that match the queried relationship. Finally, Enumeration.py will output three separate files based on the relationship matrices: generation_depth.xlsx, meioses_event.xlsx, and half_full.xlsx for the final family listed within a family relations file (if multiple are present).

Relationship_Search.py is code that must be edited to take in a generation_depth.xlsx, meioses_event.xlsx, and half_full.xlsx excel files generation from Enumeration.py for an individual family. Relationship_Search.py can then be run to prompt the user for relationship metrics to searh for a specific relationship type in a family represented by the three excel files. Output is written to the console before starting another search.

Visualization is an R script that provides the code template for creating beeswarm plots out of the results .csv output from Enumeration.py.

### How to cite this project?

Please email `joaquinmmagana@gmail.com` to get instructions on how to properly cite this project.

### Contributing

Please contact `joaquinmmagana@gmail` or Joaquín Magaña via Slack for contributions.
