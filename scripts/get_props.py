#!/usr/bin/env python

import sys
import getopt
import pandas as pd

pd.set_option('display.max_colwidth', 80)
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('expand_frame_repr', False)


def help_exit(error):
    print("Usage: get_props.py -p <prefix> [-n onto_name] <input file>")
    exit(error)


def main(argv):
    onto_name = ''
    prefix = ''

    # Process arguments and options
    try:
        opts, args = getopt.getopt(argv, "hp:n:", ["prefix=", "onto_name="])

        # Handle missing argument(s)
        if len(args) != 1:
            help_exit(1)

        # Get arguments
        input_file = args[0]
    except getopt.GetoptError:
        help_exit(1)
    for opt, arg in opts:
        if opt == '-h':
            help_exit(0)
        elif opt in ("-p", "--prefix"):
            prefix = arg
        elif opt in ("-n", "--onto_name"):
            onto_name = arg

    if prefix == '':
        print("Please specify a prefix to use when forming property names.\n")
        help_exit(1)

    # Read input file into a dataframe
    df = pd.read_csv(input_file)

    # Configure the dataframe
    df = df.set_index('id')
    df = df.sort_values(by='subject')

    # print(df)

    # Determine the ontology name to use
    if (onto_name == ''):
        # Find the ontology entry, if one exists
        onto_df = df.loc[
            (df['predicate'] == 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type') &
            (df['object'] == 'http://www.w3.org/2002/07/owl#Ontology')
        ]
        if (onto_df.empty):
            print("No ontology metadata found in ontology.  Please provide an ontology name.\n")
            help_exit(1)

        onto_name = onto_df.iloc[0]['subject']

    onto_name_len = len(onto_name)

    # print("Ontology:", onto_name)
    # print("Prefix:", prefix)

    # Find all properties
    props = df.loc[
        (df['predicate'] == 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type') &
        (df['object'] == 'http://www.w3.org/1999/02/22-rdf-syntax-ns#Property')
    ]

    for subject in props['subject']:
        if not subject.startswith(onto_name):
            print("WARNING: subject does not start with the ontology name:", subject)
            continue
        prop_name = subject[onto_name_len:]
        if prop_name[0] == '#' or prop_name[0] == '/':
            prop_name = prop_name[1:]
        prop_name = prefix + prop_name[0].upper() + prop_name[1:]
        print(prop_name)


if __name__ == "__main__":
    main(sys.argv[1:])
