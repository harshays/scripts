from __future__ import print_function
import pandas as pd
import re

class GPACalc(object):

    cols  = ['name', 'course', 'hours', 'letterGrade', 'semester']
    major = ['CS', 'MATH', 'STAT']

    @classmethod
    def grades(cls):
        letters = sum([[g+s for s in ['+','','-']] for g in 'ABCD'], []) + ['F']
        numbers = [4.0, 4.0, 3.67, 3.33, 3.0, 2.67, 2.33, 2.0, 1.67, 1.33, 1.0, 0.67, 0.0]
        return dict(zip(letters, numbers))

    @staticmethod
    def _calc(df):
        return (sum(df.hours*df.grade)/sum(df.hours))

    def __init__(self, csv_file, groupby=['semester', 'dept']):
        self.path = csv_file
        self.groupby_cols = groupby
        self.df = pd.read_csv(self.path).dropna()
        assert self.df.columns.tolist() == self.cols, "Invalid columns"
        self.munge()

    def munge(self):
        grades = self.grades()
        get_dept = lambda c: re.split('\d+', c)[0]
        ch_dept  = lambda d: d if d in self.major else 'MISC'
        self.df['grade'] = self.df.letterGrade.apply(lambda l: grades[l])
        self.df['dept'] = self.df.course.apply(get_dept).apply(ch_dept)
        self.df['semester'] = 'sem ' + self.df.semester.astype(str)

    def calc(self, groupby=None, df=None):
        f  = lambda df: df.groupby(groupby).apply(self._calc) if groupby else self._calc(df)
        df = df if df is not None else self.df
        if groupby: assert groupby in df.columns, "groupby columns invalid"
        return f(df)

    def __str__(self):
        info,fmt = [], "Grouped by {}:\n\n{}"
        major_df = self.df[self.df.dept.isin(self.major)] 
        info.append("Total GPA: {}".format(self.calc().round(3)))
        info.append("Major GPA: {}".format(self.calc(df=major_df).round(3)))
        for gb in self.groupby_cols:
            info.append(fmt.format(gb, self.calc(gb).round(3).to_string(header=False)))
        return ("\n"*2).join(info)

if __name__ == '__main__':
    rel_path = raw_input("Enter CSV file path: ")
    print (GPACalc(rel_path))
