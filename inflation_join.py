import sys
import argparse

def join_data(stream, column, join_dict, printall=None):
    """
    Loop through stdin appending/inflating with join file data
    """
    for row in stream:
        row_list = row.rstrip('\n').split('\t')
        join_key = row_list[column]
        if join_key in join_dict:
            for appended_columns in join_dict[join_key]:
                print_list(row_list + appended_columns)
        elif printall != None:
            row_list.append(printall)
            print_list(row_list)

def print_list(row):
    """
    List printing helper function
    """
    output = '\t'.join(row) + '\n'
    sys.stdout.write(output)

def remove_join_key(row, key):
    """
    Remove key from list and return updated list
    """
    row.remove(key)
    return row

def create_join(join_file, column):
    """
    Create dict of lists for each key in the join file
    """
    join_dict = {}
    for row in open(join_file):
        row_list = row.rstrip('\n').split('\t')
        key = row_list[column]
        if key in join_dict:
            join_dict[key].append(remove_join_key(row_list, key))
        else:
            join_dict[key] = [ remove_join_key(row_list, key) ]
    return join_dict

def cmd_line_parser(args):
    """
    Parse cmd line args
    """
    parser = argparse.ArgumentParser()

    parser.add_argument("-1", "--file1", action="store", type=int,
                        help="Stdin column number to join on", dest="column_1")
    parser.add_argument("-2", "--file2", action="store", type=int,
                        help="File two column number to join on", dest="column_2")
    parser.add_argument("-j", "--joinfile", action="store",
                        help="File to join on", dest="joinfile")
    parser.add_argument("-p", "--printall", action="store", default=None,
                        help="Print non-matching values with input string", dest="printall")

    return parser.parse_args(args)

def main():
    """
    Run the main task
    """
    args = cmd_line_parser(sys.argv[1:])
    join_dict = create_join(args.joinfile, args.column_2)
    join_data(sys.stdin, args.column_1, join_dict, args.printall)

if __name__ == '__main__':
    main()

