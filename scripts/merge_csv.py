#!/usr/bin/env python

import sys
import getopt
import shutil
import glob


def help_exit(error):
    print("Usage: merge_csv.py -i <input path> -o <output file>")
    exit(error)


def main(argv):

    # Process arguments and options
    try:
        opts, args = getopt.getopt(argv, "hi:o:", ["ipath=", "oname="])

    except getopt.GetoptError:
        help_exit(1)

    input_path = ''
    output_name = ''

    for opt, arg in opts:
        if opt == '-h':
            help_exit(0)
        elif opt in ("-i", "--ipath"):
            input_path = arg
        elif opt in ("-o", "--oname"):
            output_name = arg

    if input_path == '' or output_name == '':
        help_exit(1)

    # import csv files from folder
    allFiles = glob.glob(input_path + "/*.csv")
    allFiles.sort()  # glob lacks reliable ordering, so impose your own if output order matters
    with open(output_name, 'wb') as outfile:
        for i, fname in enumerate(allFiles):
            with open(fname, 'rb') as infile:
                if i != 0:
                    infile.readline()  # Throw away header on all but first file
                # Block copy rest of file from input to output without parsing
                shutil.copyfileobj(infile, outfile)
                print(fname + " merged")


if __name__ == "__main__":
    main(sys.argv[1:])
