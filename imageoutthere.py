################################################################################
# imageoutthere.py                                                             #
# by bender.rodriges                                                           #
#                                                                              #
# Returns images from shortened links.                                         #
#                                                                              #
# This code distributes under no license. Do whatever you want and be happy!   #
################################################################################

import requests

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
        # valid images types
        types = ['image/jpeg','image/pjpeg', 'image/png', 'image/gif']
        # performing request
        response = requests.get(link)
        # if request has been successful (e.g. HTTP 200)
        if response.status_code == requests.codes.ok:
            # matching target type against images types
            if response.headers['content-type'] in types:
                # filling predefined values
                self.link = response.url
                self.type = response.headers['content-type'],
                self.size = response.headers['content-length']
                self.is_image = True
        self.redirects = len(response.history)