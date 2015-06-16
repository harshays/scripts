from utils import parse_grades, group_by, write_gpa

csvlist = parse_grades()

def computeGPA(csvlist = csvlist):
    hours = reduce(lambda acc, course: acc + course["Hours"], csvlist, 0)
    points = reduce(lambda acc, course: acc + course["Points"], csvlist, 0)
    return points, hours, points/float(hours)

def get_grouped_gpa(group):
    group_dct = group_by(csvlist, group)
    gpa = {grp: computeGPA(courses) for grp, courses in group_dct.items()}
    return gpa, group

def run():
    semester = get_grouped_gpa("Semester")
    dept = get_grouped_gpa("Dept")
    total = computeGPA()
    write_gpa([semester, dept], computeGPA())

if __name__ == '__main__':
    run()

