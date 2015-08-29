from   datetime import datetime
from   argparse import ArgumentParser
import os
import sys

"""
Script to resume/open recently used files in a directory
"""

def get_recent_files(folder, file_filter, limit):
    files  = [os.path.join(folder, f) for f in os.listdir(folder)]
    if file_filter:
        files  = list(filter(lambda f: f.endswith(file_filter), files))
    recent = [(f, datetime.fromtimestamp(int(os.stat(f).st_ctime))) for f in files]
    recent.sort(key=lambda a: a[-1], reverse=True)
    for f, d in recent:
        if "'" in f:
            print (f)
    return recent[:limit]

def get_parser():
    parser = ArgumentParser(description="watch.py")
    parser.add_argument('-l', '--limit', default=3, help='get #limit recent files')
    parser.add_argument('-a', '--app', default=None, help='full path to specific app')
    parser.add_argument('-d', '--dir', default=os.getcwd(), help='full path to directory')
    parser.add_argument('-f', '--filter', default=None, help='filter file type e.g. mp4')
    return parser

def io(options):
    options.dir = os.path.expanduser(options.dir)
    files = get_recent_files(options.dir, options.filter, options.limit)

    for file, date in files:
        ui = None
        io_options = ['y', 'n', 'exit']

        while (not ui or ui not in io_options):
            ui = raw_input("Open {}? {}: ".format(file.rsplit('/')[-1], '/'.join(io_options)))

        if (ui == 'exit'): sys.exit()

        if (ui == 'y'):
            cmd = 'open \'{}\''.format(file)
            cmd = cmd if not options.app else '{} -a {}'.format(cmd, options.app)
            os.system(cmd)
            sys.exit()

if __name__ == '__main__':
    parser = get_parser()
    options = parser.parse_args()
    io(options)
