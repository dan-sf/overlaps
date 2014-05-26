#!/usr/bin/python

#------------------------------------------------
# Overlap lookup script: Maintained by Dan Fowler
# Website: dsfcode.com
# Version 1.0.0
#------------------------------------------------

import sys
import argparse

# Parse the args
parser = argparse.ArgumentParser()
parser.add_argument("-f", "--file", action="store", help="One column file to lookup against", dest="file")
parser.add_argument("-c", "--column", action="store", help="Zero based column number to lookup against", dest="column")
parser.add_argument("-i", "--include", action="store", help="One or zero to include or disallow values from the lookup file", dest="include")
args = vars(parser.parse_args())

# Create lookup set of values from the input file
lookup_set = set(line.strip() for line in open(args['file']))

# Loop through stdin looking up against the input values
for row in sys.stdin:
	row_list = list(row.strip().split('\t'))
	if int(args['include']) == 1 and row_list[int(args['column'])] in lookup_set:
		print '\t'.join(str(x) for x in row_list)
	elif int(args['include']) != 1 and row_list[int(args['column'])] not in lookup_set:
		print '\t'.join(str(x) for x in row_list)

