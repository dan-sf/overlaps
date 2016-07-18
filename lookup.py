import sys
import argparse

def print_data(row):
    """
    Write data to stdout
    """
    row = '\t'.join(str(i) for i in row)
    sys.stdout.write(row + '\n')

def lookup_set(lookup_file):
    """
    Create a set from the lookup_file
    """
    return { line.rstrip('\n') for line in open(lookup_file) }

def filter_data(stream, args):
    """
    Include or disallow records that match data in lookup_file
    """
    join_set = lookup_set(args.file)
    for line in stream:
        line = line.rstrip('\n').split('\t')
        if not args.remove and line[args.column] in join_set:
            print_data(line)
        elif args.remove and line[args.column] not in join_set:
            print_data(line)

def cmd_line_parser(args):
    """
    Parse cmd line args
    """
    parser = argparse.ArgumentParser()

    parser.add_argument("-f", "--file", action="store",
                        help="One column file to lookup against", dest="file")
    parser.add_argument("-c", "--column", action="store", type=int,
                        help="Zero based column number to lookup against", dest="column")
    parser.add_argument("-r", "--remove", action="store_true", default=False,
                        help="Disallow values from the lookup file", dest="remove")
    return parser.parse_args(args)

def main():
    """
    Run the main task
    """
    args = cmd_line_parser(sys.argv[1:])
    filter_data(sys.stdin, args)

if __name__ == '__main__':
    main()

