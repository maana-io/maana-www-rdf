#!/usr/bin/env python

import sys
import getopt
import csv
import rdflib


def help_exit(error):
    print("Usage: rdfcsv.py -i <input file> -f <input format> -o <output file>")
    print("\nSupported input formats:")
    print("\tapplication/rdf+xml")
    print("\txml")
    print("\ttext/n3")
    print("\tn3")
    print("\ttext/turtle")
    print("\tturtle")
    print("\tttl")
    print("\tapplication/n-triples")
    print("\tntriples")
    print("\tnt")
    print("\tnt11")
    print("\tapplication/n-quads")
    print("\tnquads")
    print("\tapplication/trix")
    print("\ttrix")
    print("\ttrig")
    print("\tjson-ld")

    sys.exit(error)


def main(argv):
    input_file = ''
    input_format = ''
    output_file = ''
    try:
        opts, args = getopt.getopt(argv, "hi:f:o:", ["ifile=", "iformat=", "ofile="])
    except getopt.GetoptError:
        help_exit(1)
    for opt, arg in opts:
        if opt == '-h':
            help_exit(0)
        elif opt in ("-i", "--ifile"):
            input_file = arg
        elif opt in ("-f", "--iformat"):
            input_format = arg
        elif opt in ("-o", "--ofile"):
            output_file = arg

    g = rdflib.Graph()
    g.parse(input_file, format=input_format)
    fields = ['id', 'subject', 'predicate', 'object', 'language', 'datatype']

    i = 0
    with open(output_file, 'w') as csvfile:
        csvwriter = csv.writer(csvfile, quoting=csv.QUOTE_NONNUMERIC)
        csvwriter.writerow(fields)

        for s, p, o in g:
            lang = ''
            dt = ''
            if isinstance(o, rdflib.Literal):
                lang = o.language
                dt = o.datatype
            row = ["{}".format(i), s, p, o, lang, dt]
            i = i+1
            csvwriter.writerow(row)
    print("Wrote {} statements".format(i))


if __name__ == "__main__":
    main(sys.argv[1:])
