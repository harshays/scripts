import os, sys
import csv
import re
from collections import defaultdict
from argparse import ArgumentParser

grades = { 
       'A+':4.0,  'A':4.0,  'A-':3.67, 
       'B+':3.33, 'B':3.0, 'B-':2.67, 
       'C+': 2.33, 'C': 2.00, 'C-': 1.67  
     }

colors = {
    'HEADER' : '\033[95m', 'OKBLUE' : '\033[94m',
    'OKGREEN' : '\033[92m', 'WARNING' : '\033[93m',
    'FAIL' : '\033[91m', 'ENDC' : '\033[0m',
    'BOLD' : '\033[1m', 'UNDERLINE' : '\033[4m'
    }
    
def get_parser():
    parser = ArgumentParser(description = 'GPA Calculator')
    parser.add_argument('grades', help = 'full path to grade csv file', default = None)
    parser.add_argument('output', help = 'full path to output txt file', default = None)
    return parser

def get_args():
    parser = get_parser()
    args = parser.parse_args()
    args.grades = os.path.expanduser(args.grades)
    args.output = os.path.expanduser(args.output)

    if not os.path.exists(args.grades):
        print "grades csv file does not exist"
        sys.exit(0)

    open(args.output, 'a').close()
    
    return args

def parse_csv(csvfilepath):
    with open(csvfilepath, 'r') as csvfile:
        csvreader = csv.DictReader(csvfile)
        csvlist = list(csvreader)
        return csvreader, csvlist

def group_dict_by_key(data, key):
    grp = defaultdict(list)
    for d in data:
        grp[d[key]].append(d)
    return grp

def cprint(s, color):
    print "{}{}{}".format(colors[color], s, colors.ENDC),

def get_dept(cname):
    dept = re.split('\d+', cname)[0]
    dept = dept if dept in ['MATH','STAT','CS'] else 'MISC'
    return dept

if __name__ == '__main__':
    print parse_csv('mygrades.csv')



























