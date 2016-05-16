#!/usr/bin/python

#-----------------------
# Overlap inflation join
#-----------------------

import sys
import argparse

# Parse the args
parser = argparse.ArgumentParser()
parser.add_argument("-1", "--file1", action="store", help="Stdin column number to join on", dest="filecol1")
parser.add_argument("-2", "--file2", action="store", help="File two column number to join on", dest="filecol2")
parser.add_argument("-j", "--joinfile", action="store", help="File to join on", dest="joinfile")
parser.add_argument("-p", "--printall", action="store", help="Print non-matching values with input string", dest="printall")
args = vars(parser.parse_args())

def rem(l,item):
	l.remove(item)
	return l

# # Create lookup dictionary of values from the input file
lookup_dic = {}
for row in open(args['joinfile']):
	row_list = row.strip().split('\t')
	key = row_list[int(args['filecol2'])]
	if key not in lookup_dic:
		lookup_dic[key] = [ rem(row_list,key) ]
	else:
		lookup_dic[key].append(rem(row_list,key))

# Loop through stdin looking up against the input values replacing or appending matching records
for row in sys.stdin:
	row_list = list(row.strip().split('\t'))
	if row_list[int(args['filecol1'])] in lookup_dic:
		s = ""
		for l in lookup_dic[row_list[int(args['filecol1'])]]:
			s = '\t'.join(str(x) for x in row_list)
			for i in l:
				s = s + "\t" + i
			print s
	elif args['printall'] != None:
		row_list.append(args['printall'])
		print '\t'.join(str(x) for x in row_list)

