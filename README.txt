### Enumeration of family relationships in a relationships file.

A python script for the enumeration of different family relationships in a
family relations .txt file.

### Why should I use this project ?

This script allows you to quickly enumerate the number and types of relationships
found within any family relations .txt file.

### Setup

You need `python>3.8` to run this script.

The project depends on the `pandas`, `networkx`, `matplot`, `numpy`, `argparse`,
and `openpyxl` modules, install them with pip:
`pip install pandas`
`pip install networkx`
etc...

### How to run?

You can run the script from the command-line using
```
python Enumeration_Final.py -f -gd -me -t
```
Where:
-f --file is the whole name of the family relations .txt file.

-gd --generation is the integer of generation depth you want to search for.

-me --meioses is the integer of meioses events you want to search for.

-t --type is the type of relationships you want to search for. These include (half, full, direct, NA).
Where a direct relationsip is a direct descendant/ancestor and NA applies to exclusions such as 
comparing an individual against themselves.

```
After an initial run and search. The script will then prompt you once again for gd, me, and t to
search for another set of relationships after enumeration. You may continue to search until you quit
the script.

The script will also write out three separate dataframes to excel format for cross comparisons between all
individuals for gd, me, and type.

### How to cite this project?

Please email `joaquinmmagana@gmail.com` to get instructions on how to properly cite this project.

### Contributing

Please contact `joaquinmmagana@gmail` or Joaquín Magaña via Slack for contributions.