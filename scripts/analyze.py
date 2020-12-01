#!/usr/bin/env python

import os
import sys
import getopt
import json
import pandas as pd


def help_exit(error):
    print("Usage: analyze.py <input file>")
    exit(error)


def main(argv):

    # Process arguments and options
    try:
        opts, args = getopt.getopt(argv, "h", [])

        # Handle missing argument(s)
        if len(args) != 1:
            help_exit(1)

        # Get arguments
        input_file = args[0]
        output_file = os.path.splitext(input_file)[0] + ".json"
    except getopt.GetoptError:
        help_exit(1)

    # Read input file into a dataframe
    df = pd.read_csv(input_file)

    # Find all types
    type_stmts = df.loc[df['predicate'] == 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type']
    types = type_stmts['object'].unique()

    # Build a dictionary of the different types and their properties
    type_dict = {}
    for typ in types:
        # Find the instances of this type
        inst_dict = {}
        inst_stmts = df.loc[
            (df['predicate'] == 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type') &
            (df['object'] == typ)
        ]
        insts = inst_stmts['subject']
        for inst in insts:
            # Find the properties of this type (=domain)
            prop_dict = {}
            prop_stmts = df.loc[
                (df['predicate'] == 'http://www.w3.org/2000/01/rdf-schema#domain') &
                (df['object'] == inst)
            ]
            props = prop_stmts['subject']
            for prop in props:
                # Find the type (range) of this property
                rng_stmts = df.loc[
                    (df['predicate'] == 'http://www.w3.org/2000/01/rdf-schema#range') &
                    (df['subject'] == prop)
                ]
                rngs = rng_stmts['object']
                for rng in rngs:
                    prop_dict[prop] = rng
            inst_dict[inst] = prop_dict
        type_dict[typ] = inst_dict

    with open(output_file, 'w') as f:
        json.dump(type_dict, f)


if __name__ == "__main__":
    main(sys.argv[1:])
