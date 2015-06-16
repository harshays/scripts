import os
from argparse import ArgumentParser
import urllib

def get_parser():
    parser = ArgumentParser(description='coursera downloader')
    parser.add_argument('link', help = "link to course's preview page")
    parser.add_argument('path', help = 'full path to dir where videos \
                                        should be installed')
    return parser

def get_options():
    parser = get_parser()
    options = parser.parse_args()
    return options

