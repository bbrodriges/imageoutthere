################################################################################
# imageoutthere.py                                                             #
# by bender.rodriges                                                           #
#                                                                              #
# Returns images from shortened links.                                         #
#                                                                              #
# This code distributes under no license. Do whatever you want and be happy!   #
################################################################################

import requests
from urlparse import urlparse
from HTMLParser import HTMLParser

class ImageOutThere:

    def __init__(self, link):
        self._get_image(link)

    def _get_image(self, link):
        # predefined attributes
        self.is_image = False
        self.link = None
        self.type = None
        self.size = None
        self.redirects = None
        self.host = None
        # valid images types
        types = ['image/jpeg','image/pjpeg', 'image/png', 'image/gif']
        # performing request
        response = requests.get(link)
        # if request has been successful (e.g. HTTP 200)
        if response.status_code == requests.codes.ok:
            # matching target type against images types
            #if response.headers['content-type'] in types:
            data = response.content
            # filling predefined values
            self.link = self._extract_image(response.url, data)
            response = requests.get(self.link)
            if response.status_code == requests.codes.ok:
                self.type = response.headers['content-type']
                self.size = response.headers['content-length']
                # check if image out there
                if self.type in types:
                    self.is_image = True
        self.redirects = len(response.history)

    def _extract_image(self, url, data):
        # predefined pictures domains and URL needles to search
        domains = {
            'twitter.com': 'pbs.twimg.com',
            'instagram.com': 'distilleryimage'
        }
        self.host = urlparse(url).netloc
        if self.host in domains.keys():
            parser = imagehtmlparser(domains[self.host])
            parser.feed(data.decode('UTF-8'))
            url = parser.direct_link if parser.direct_link else None
        return url

class imagehtmlparser(HTMLParser):

    def __init__(self, needle):
        HTMLParser.__init__(self)
        self.needle = needle

    def handle_starttag(self, tag, attrs):
        for attr in attrs:
            if attr and (attr[0] == 'content' or attr[0] == 'src'):
                if self.needle in attr[1]:
                    self.direct_link = attr[1]

img = ImageOutThere('http://pic.twitter.com/Il9fojx4')
print(img.link, img.size, img.type)