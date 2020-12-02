#!/usr/bin/env python

import os
import sys
import getopt
import json
import pandas as pd


def help_exit(error):
    print("Usage: analyze.py <input file>")
    exit(error)


def filter_p(df, p):
    return df.loc[(df["predicate"] == p)]


def filter_po(df, p, o):
    return df.loc[(df["predicate"] == p) & (df["object"] == o)]["subject"]


def filter_sp(df, s, p):
    return df.loc[(df["subject"] == s) & (df["predicate"] == p)]["object"]


def get_label(df, id):
    labels = filter_sp(df, id, "http://www.w3.org/2000/01/rdf-schema#label")
    if labels.empty:
        return id

    return labels.iloc[0]


context = {
    "http://www.w3.org/1999/02/22-rdf-syntax-ns#": "rdf",
    "http://www.w3.org/2000/01/rdf-schema#": "rdfs",
    "http://www.w3.org/2002/07/owl#": "owl",
    "http://purl.org/dc/elements/1.1/": "dc",
    "http://xmlns.com/foaf/0.1/": "foaf",
    "http://www.w3.org/2004/02/skos/core#": "skos",
    "http://purl.org/dc/dcam/": "dcam",
    "http://purl.org/dc/terms/": "dcterms",
    "http://purl.org/dc/dcmitype/": "dcmitype",
    "http://www.w3.org/2006/time#": "time",
    "http://www.w3.org/ns/time/gregorian/": "greg",
    "http://www.w3.org/2003/06/sw-vocab-status/ns#": "vs",
    "http://xmlns.com/wot/0.1/": "wot",
    "http://purl.org/vocab/vann/": "vann",
    "http://web.resource.org/cc/": "cc",
    "http://www.w3.org/2003/01/geo/wgs84_pos#": "geo"
}


def prefix_iri(iri):
    for key, value in context.items():
        if iri.startswith(key):
            rest = iri[len(key):]
            if len(rest) == 0:
                return iri
            prefix = value
            if rest[0].isupper():
                prefix = prefix[0].upper() + prefix[1:]
            else:
                rest = rest[0].upper() + rest[1:]
            return prefix + rest
    return iri


def main(argv):

    # Process arguments and options
    try:
        opts, args = getopt.getopt(argv, 'h', [])

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
    type_stmts = df.loc[df["predicate"] == "http://www.w3.org/1999/02/22-rdf-syntax-ns#type"]
    types = type_stmts["object"].unique()

    # Build a dictionary of the different types and their properties
    type_dict = {}
    for typ in types:
        # Find the instances of this type
        inst_dict = {}
        inst_stmts = df.loc[
            (df["predicate"] == "http://www.w3.org/1999/02/22-rdf-syntax-ns#type") &
            (df["object"] == typ)
        ]
        insts = inst_stmts["subject"]
        for inst in insts:
            # Find the properties of this type (=domain)
            prop_dict = {}
            prop_stmts = df.loc[
                (df["predicate"] == "http://www.w3.org/2000/01/rdf-schema#domain") &
                (df["object"] == inst)
            ]
            props = prop_stmts["subject"]
            for prop in props:
                # Find the type (range) of this property
                rng_stmts = df.loc[
                    (df["predicate"] == "http://www.w3.org/2000/01/rdf-schema#range") &
                    (df["subject"] == prop)
                ]
                rngs = rng_stmts["object"]
                for rng in rngs:
                    prop_dict[prefix_iri(prop)] = prefix_iri(rng)
            inst_dict[prefix_iri(inst)] = prop_dict

        type_dict[prefix_iri(typ)] = inst_dict

    output = {
        "context": context,
        "schema": type_dict
    }
    with open(output_file, 'w') as f:
        json.dump(output, f)


if __name__ == "__main__":
    main(sys.argv[1:])
