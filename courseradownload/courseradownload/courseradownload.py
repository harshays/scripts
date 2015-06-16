import os, sys
import requests
import urllib
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from .utils import get_options, get_parser

# DONE: use properties instead of helpers
# DONE: example links json file


class CourseraDownloader(object):
    '''  Utility to download coursera videos

        @params course     link to course's preview page
        @params path       path where videos should be installed

        @info  Python 3 required
        @info  Drawback - only works for courses with
                          preview lectures option
        @info links.json links for reference
    '''

    def __init__(self, options):
        self.course = options.link
        self.path = options.path

        self.link = urlparse(self.course)

        try:
            self.request = requests.get(self.course, verify = False)
        except requests.exceptions.MissingSchema as e:
            print (e)
            exit(0)

        self.raw = self.request.text.encode('ascii','ignore')
        self.soup = BeautifulSoup(self.raw)

        self._check()

    def _check(self):
        err = lambda prop : "{} is invalid. Try again".format(prop)

        try:
            assert self.link.netloc == 'class.coursera.org', err('netloc')
        except AssertionError as e:
            print (e)
            exit(0)

    @property
    def coursename(self):
        return self.link.path[1:].split('/')[0]

    def _parse_soup(self):
        # get section
        weeks_section = self.soup.findAll('ul',
                             {'class' : 'course-item-list-section-list'})

        # get children in each section
        week_lectures = [w.children for w in weeks_section]

        # get lecture li elements
        lectures = [lecture for week in week_lectures for lecture in week]

        # parse lecture information
        parsed_info = []
        for lecture in lectures:
            tag = lecture.find('a', {
                          'class' : 'lecture-link'})
            title = tag.text.split('(')[0].replace(' ', '').replace('/','')
            content = tag['href'].split('/')
            body, tail = content[:-1], content[-1]
            link = '{}/download.mp4?lecture_id={}'.format('/'.join(body), tail)

            parsed_info.append([title, link])

        return parsed_info

    def _download_video(self, info_tuple, directory):
        # check if already downloaded
        if not os.path.exists(directory):
            urllib.request.urlretrieve(info_tuple[1], directory)

    def download(self):
        coursename = self.coursename
        directory = os.path.join(self.path, coursename)

        if not os.path.exists(directory):
            os.makedirs(directory)

        info = self._parse_soup()
        for idx, (name, downloadlink) in enumerate(info):
            name = name[1:]
            title = "%03i-%s" % (idx + 1, name)
            filename = "{}/{}.mp4".format(directory, title)
            print (filename)
            self._download_video((name, downloadlink), filename)

def main():
    requests.packages.urllib3.disable_warnings()
    options = get_options()
    downloader = CourseraDownloader(options)
    downloader.download()

def help():
    print ("use coursera.download <link> <fullpath> to download coursera videos")
    print ("checkout links.json for a few examplesl")

if __name__ == '__main__':
    main()

