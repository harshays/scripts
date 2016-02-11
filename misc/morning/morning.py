from __future__  import print_function
from blessings   import Terminal
from argparse    import ArgumentParser
from collections import defaultdict
import webbrowser
import csv
import os

FILE_DIR = os.path.dirname(os.path.realpath(__file__))
terminal = Terminal()

def get_parser():
    parser = ArgumentParser()
    arguments = ['less', 'more', 'update', 'num']
    parser.add_argument('--less', '-l', action='store_true', help='open fewer websites')
    parser.add_argument('--more', '-m', action='store_true', help='open more websites')
    parser.add_argument('--update', '-u', action='store_true', help='update websites list')
    parser.add_argument('--num', '-n', nargs=1, help='open first N websites')
    return parser, arguments

def parse_args():
    parser, all_args = get_parser()
    args_ns = parser.parse_args()
    args_tuple = [(arg, getattr(args_ns, arg)) for arg in all_args]
    args_true  = list(filter(lambda t: bool(t[-1]), args_tuple))
    if len(args_true) > 1: print (terminal.bold+"0 or 1 argument only"+terminal.normal); return
    # open_all is called when no argument is passed
    return args_true[0] if args_true else ('all', True)

def _read_websites_csv():
    website_dir = os.path.join(FILE_DIR, 'websites.csv')
    with open(website_dir, 'rb') as web_csv:
        web_list = list(csv.reader(web_csv))
    websites = defaultdict(list)
    for w, pr in web_list: websites[int(pr.strip())].append(w if w.startswith('http') else 'http://'+w)
    return websites

def get_websites(percent, num):
    d  = _read_websites_csv()
    dl = sum([d[k] for k in sorted(d)], [])
    percent = percent if 0 <= percent <= 1 else 1
    n = min(round(percent*len(dl)), len(dl)) if not num else (num[0] if isinstance(num, list) else num)
    return dl[:int(n)]

def call_fn(arg, val):
    fn_name = 'open_'+arg.lower()
    fn = globals().get(fn_name, None)
    if not fn: print (term.bold+'No such function: {}'.format(fn_name)); return
    return fn(val)

open_       = lambda p, n: map(webbrowser.open, get_websites(p, n))
open_all    = lambda _: open_(1, None)
open_less   = lambda _: open_(0.4, None)
open_more   = lambda _: open_(0.8, None)
open_num    = lambda n: open_(1, n)
open_update = lambda _: os.system('vim {}'.format(os.path.join(FILE_DIR, 'websites.csv')))

run = lambda: call_fn(*(parse_args()))

if __name__ == '__main__':
    run()
