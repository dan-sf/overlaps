#!/usr/bin/python

#----------------
# Overlap replace
#----------------

import sys
import argparse

# Parse the args
parser = argparse.ArgumentParser()
parser.add_argument("-f", "--file", action="store", help="Two column file to lookup against", dest="file")
parser.add_argument("-c", "--column", action="store", help="Zero based column number to lookup against", dest="column")
parser.add_argument("-r", "--replace", action="store", help="One or zero to replace or append values from the lookup file (1: replace, 2: append)", dest="replace")
parser.add_argument("-p", "--printall", action="store", help="Print non-matching values with input string", dest="printall")
args = vars(parser.parse_args())

# # Create lookup dictionary of values from the input file
lookup_dic = {}
for line in open(args['file']):
	line_list = line.strip().split('\t')
	lookup_dic[line_list[0]] = line_list[1]

# Loop through stdin looking up against the input values replacing or appending matching records
for row in sys.stdin:
	row_list = list(row.strip().split('\t'))
	if int(args['replace']) == 1 and row_list[int(args['column'])] in lookup_dic:
		row_list[int(args['column'])] = lookup_dic[row_list[int(args['column'])]]
		print '\t'.join(str(x) for x in row_list)
	elif int(args['replace']) == 0 and row_list[int(args['column'])] in lookup_dic:
		row_list.append(lookup_dic[row_list[int(args['column'])]])
		print '\t'.join(str(x) for x in row_list)
	elif row_list[int(args['column'])] not in lookup_dic and args['printall'] != None:
		row_list.append(args['printall'])
		print '\t'.join(str(x) for x in row_list)

