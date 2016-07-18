import sys
import argparse

def print_data(row):
    """
    Write data to stdout
    """
    row = '\t'.join(str(i) for i in row)
    sys.stdout.write(row + '\n')

def create_lookup(lookup_file):
    """
    Create lookup dictionary of values from the input file
    """
    lookup_dict = {}
    for line in open(lookup_file):
            line_list = line.rstrip('\n').split('\t')
            lookup_dict[line_list[0]] = line_list[1]
    return lookup_dict

def join_data(stream, args):
    """
    Join the data, either appending or replacing values
    """
    join_dict = create_lookup(args.file)
    for row in stream:
        row = row.rstrip('\n').split('\t')
        if args.replace and row[ args.column ] in join_dict:
            row[ args.column ] = join_dict[row[ args.column ]]
            print_data(row)
        elif not args.replace and row[ args.column ] in join_dict:
            row.append(join_dict[row[ args.column ]])
            print_data(row)
        elif row[ args.column ] not in join_dict and args.printall != None:
            row.append(args.printall)
            print_data(row)

def cmd_line_parser(args):
    """
    Parse cmd line args
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", action="store",
                        help="Two column file to lookup against", dest="file")
    parser.add_argument("-c", "--column", action="store", type=int,
                        help="Zero based column number to lookup against", dest="column")
    parser.add_argument("-r", "--replace", action="store_true", default=False,
                        help="Option to replace the field you are matching on", dest="replace")
    parser.add_argument("-p", "--printall", action="store",
                        help="Print non-matching values with input string", dest="printall")

    return parser.parse_args(args)

def main():
    """
    Run the main task
    """
    args = cmd_line_parser(sys.argv[1:])
    join_data(sys.stdin, args)

if __name__ == '__main__':
    main()

