import os, sys, time
import urllib
import workerpool 

def get_video_url(lect, part):
    vid_prefix = 'https://s3-us-west-2.amazonaws.com/classtranscribe/'
    vid_zero_suffix = 'lecture_{lect}/media_part{part}.webm'
    vid_suffix = 'lecture_{lect}/media_{lect}_part{part}.webm'

    if lect == 0:
        return vid_prefix + vid_zero_suffix.format(lect = lect, part = part)

    return vid_prefix + vid_suffix.format(lect = lect, part = part)

def get_filename(pth, lect, part):
    path = os.path.expanduser(pth)
    fname = 'lecture{}part{}.mov'.format(lect, part)
    return os.path.join(path, fname)

class VideoDownload(workerpool.Job):

    def __init__(self, pth, lect, part):
        self.lect = lect
        self.part = part 
        self.url = get_video_url(lect, part)
        self.path = get_filename(pth, lect, part)

    def run(self):
        urllib.urlretrieve(self.url, self.path)
        print u'\u2713',
        print " Downloaded lect {}, part {}".format(self.lect, self.part)


def run():
    worker = workerpool.WorkerPool(5)
    missing_lectures = set([12,16,20,25,28,33])
    path = os.path.expanduser(sys.argv[1])

    for lect in xrange(35):
        if lect in missing_lectures:
            continue
        for part in xrange(6):
            job = VideoDownload(path, lect, part)
            worker.put(job)

    worker.shutdown()
    worker.wait()

if __name__ == '__main__':
    run()

