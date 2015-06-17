import utils

class GPACalc(object):

    csv_fieldnames = ['name', 'course', 'hours', 'letterGrade', 'semester']

    def __init__(self, args):
        self.gradesfile = args.grades
        self.outputfile = args.output
        self.dictreader, self.grades = utils.parse_csv(self.gradesfile)

        self.__check()
        self.__update_csv()

    def __check(self):
        if self.dictreader.fieldnames != GPACalc.csv_fieldnames:
            print ("CSV header is incorrect. Quitting.")
            sys.exit(0)

    def __update_csv(self):
        ''' updates course properties for gpa calc '''
        for course in self.grades:
            course['numberGrade'] = utils.grades[course['letterGrade']]
            course['hours'] = int(course['hours'])
            course['semester'] = int(course['semester'])
            course['points'] = course['hours'] * course['numberGrade']
            course['dept'] = utils.get_dept(course['course'])

    @staticmethod
    def __calc_gpa(grades_list):
        ''' main gpa calc function '''
        hours = reduce(lambda acc, course: acc + course["hours"], grades_list, 0)
        points = reduce(lambda acc, course: acc + course["points"], grades_list, 0)
        return points, hours, points/float(hours)

    def __grouped_gpa(self, key):
        ''' calculates grouped gpa '''
        group_dct = utils.group_dict_by_key(self.grades, key)
        gpa = {grp: self.__calc_gpa(courses) for grp, courses in group_dct.items()}
        return gpa, key

    def __write_gpa(self, group_array, cumulative):
        ''' writes gpa stuff in output file '''

        def result(gname, gpa):  
            return '\t {}: {:.3f}, {} credits \n'.format(gname, gpa[-1], gpa[1])

        with open(self.outputfile, 'w') as f:
            for gdata, gname in group_array:
                f.write("GPA w.r.t. {}: \n".format(gname))
                for group, gpa in gdata.items():
                    group_name = "{} {}".format(gname, group)
                    res = result(group_name, gpa)
                    f.write(res)
                f.write('\n')
            f.write(result("\rTotal GPA", cumulative))

    def calc_gpa(self):
        ''' gets cumulative and grouped gpa '''
        gpa = self.__calc_gpa(self.grades)
        dept_gpa = self.__grouped_gpa('dept')
        semester_gpa = self.__grouped_gpa('semester')
        return gpa, dept_gpa, semester_gpa

    def run(self):
        gpa, dept, sem = self.calc_gpa()
        self.__write_gpa([sem, dept], gpa)


def main():
    args = utils.get_args()
    gpa = GPACalc(args)
    gpa.run()

