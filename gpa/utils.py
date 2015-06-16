import csv
import pprint
from collections import defaultdict
import re

class colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

grades = {
    'A+':4.0, 
    'A':4.0, 
    'A-':3.67, 
    'B+':3.33, 
    'B':3.0, 
    'B-':2.67, 
    'C+': 2.33, 
    'C': 2.00, 
    'C-': 1.67
}

def cleancsv(course):
    course["NGrade"] = grades[course["LGrade"]]
    course["Hours"] = int(course["Hours"])
    course["Semester"] = int(course["Semester"])
    course["Points"] = course["Hours"] * course["NGrade"]
    course["Dept"] = get_dept(course["Course"]) if get_dept(course["Course"]) in ["MATH","CS","STAT"] else "MISC"

def miscdept(data):
    pass
def get_dept(cname):
    return re.split('\d+', cname)[0]

def parse_grades(fname = "grades.csv"):
    with open(fname, 'rb') as csvfile:
        csvreader = csv.DictReader(csvfile)
        csvlist = list(csvreader)
        map(cleancsv,csvlist)
        miscdept(csvlist)
        return csvlist

def group_by(data, key):
    # data is list of dictionaries
    group_dct = defaultdict(list)
    for dct in data:
        group_dct[dct[key]].append(dct)
    return dict(group_dct)


def cprint(s, color):
    print "{}{}{}".format(colors.__dict__[color], s, colors.ENDC),


def write_gpa(group_array, cumulative):
    def result(gname, gpa):  return "\t {}: {:.3f}, {} credits \n".format(gname, gpa[-1], gpa[1])
    def log(f,s): f.write(s); print s

    with open("gpa.txt","w") as f:
        for gdata, gname in group_array:
            log(f,"GPA w.r.t. {}: \n".format(gname))
            for group, gpa in gdata.items():
                group_name = "{} {}".format(gname, group)
                res = result(group_name, gpa)
                log(f,res)
            log(f,'\n')
        log(f,result("\rTotal GPA", cumulative))

if __name__ == '__main__':
    pass










