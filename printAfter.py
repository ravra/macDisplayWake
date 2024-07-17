"""

Print all lines after the occurrance of a regex is found

python3 printafter.py --search '^mystring' myfile
   or
cat myfile | python3 printafter.py --search '^mystring'

"""

import sys, re, argparse

def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--search", help="search string", type=str, required=True)
    parser.add_argument('infile', nargs='?', type=argparse.FileType('r'),
                        default=sys.stdin)
    args = parser.parse_args()

    if args.infile != sys.stdin:
        fptr = args.infile.readlines()
    else:
        fptr = args.infile

    print_on = False

    for line in fptr:
        if not print_on:
            if re.search(args.search, line):
                print_on = True
                print(line.strip())
        else:
            print(line.strip())

if __name__ == "__main__":
    main()
