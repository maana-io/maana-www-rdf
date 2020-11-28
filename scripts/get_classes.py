#!/usr/bin/env python

import sys
import getopt
import pandas as pd

pd.set_option('display.max_colwidth', 80)
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('expand_frame_repr', False)


def help_exit(error):
    print("Usage: get_classes.py <input file>")
    exit(error)


def filter_p(df, p):
    return df.loc[(df['predicate'] == p)]


def filter_po(df, p, o):
    return df.loc[(df['predicate'] == p) & (df['object'] == o)]['subject']


def filter_sp(df, s, p):
    return df.loc[(df['subject'] == s) & (df['predicate'] == p)]['object']


def get_label(df, id):
    labels = filter_sp(df, id, "http://www.w3.org/2000/01/rdf-schema#label")
    if labels.empty:
        return id

    return labels.iloc[0]


def main(argv):

    # Process arguments and options
    try:
        opts, args = getopt.getopt(argv, "h", [])

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

    # Read input file into a dataframe
    df = pd.read_csv(input_file)

    # Configure the dataframe
    df = df.set_index('id')
    df = df.sort_values(by='subject')

    # print(df)

    # Find all classes
    rdfs_classes_df = filter_po(
        df,
        "http://www.w3.org/1999/02/22-rdf-syntax-ns#type",
        "http://www.w3.org/2000/01/rdf-schema#Class")

    owl_classes_df = filter_po(
        df,
        "http://www.w3.org/1999/02/22-rdf-syntax-ns#type",
        "http://www.w3.org/2002/07/owl#Class")

    classes_df = pd.concat([rdfs_classes_df, owl_classes_df])

    # Get some class metadata (i.e., label and comment)
    classes = {}
    for class_id in classes_df:

        class_info = {'props': {}}

        class_info['label'] = get_label(df, class_id)

        class_comments = filter_sp(df, class_id, "http://www.w3.org/2000/01/rdf-schema#comment")
        if not class_comments.empty:
            class_info['comment'] = class_comments.iloc[0]

        classes[class_id] = class_info

    # For properties, drive things from 'domain' assertions.
    # Note: we'll also pick out properties for classes not defined
    #       in this ontology
    dom_stmts = filter_p(df, "http://www.w3.org/2000/01/rdf-schema#domain")
    for i, dom_stmt in dom_stmts.iterrows():
        prop_id = dom_stmt['subject']
        class_id = dom_stmt['object']
        ranges = filter_sp(df, prop_id, "http://www.w3.org/2000/01/rdf-schema#range")
        if ranges.empty:
            print("Property is missing range:", prop_id)
            continue
        range_id = ranges.iloc[0]
        if class_id not in classes:
            print("Property for class in different ontology: {} - {} : {}".format(class_id, prop_id, range_id))
            continue
        class_info = classes[class_id]
        props = class_info['props']
        prop_label = get_label(df, prop_id)
        range_label = get_label(df, range_id)
        props[prop_label] = range_label

    for cid in classes:
        print(classes[cid])


if __name__ == "__main__":
    main(sys.argv[1:])
