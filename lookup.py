#!/usr/bin/python

import sys
import argparse

def lookup_set(lookup_file):
    """
    Create a set from the lookup_file
    """
    return { line.rstrip('\n') for line in open(lookup_file) }

def filter_data(stream, column, include, lookup_file):
    """
    Include or disallow records that match data in lookup_file
    """
    join_set = lookup_set(lookup_file)
    for line in stream:
        line = line.rstrip('\n').split('\t')
        if include and line[column] in join_set:
            print '\t'.join(str(x) for x in line)
        elif not include and line[column] not in join_set:
            print '\t'.join(str(x) for x in line)

def cmd_line_parser(args):
    """
    Parse cmd line args
    """
    parser = argparse.ArgumentParser()

    parser.add_argument("-f", "--file", action="store",
                        help="One column file to lookup against", dest="file")
    parser.add_argument("-c", "--column", action="store", type=int,
                        help="Zero based column number to lookup against", dest="column")
    parser.add_argument("-i", "--include", action="store_true",
                        help="One or zero to include or disallow values from the lookup file", dest="include")
    return parser.parse_args(args)

def main():
    """
    Run the main task
    """
    args = cmd_line_parser(sys.argv[1:])
    filter_data(sys.stdin, args.column, args.include, args.file)

if __name__ == '__main__':
    main()

