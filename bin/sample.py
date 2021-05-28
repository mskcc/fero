import sys
import os
from .attr.request import RequestAttr


class SampleObj:
    def __init__(self):
       self.request = RequestAttr()

    def set_request(self, header, data):
        self.request.set_attr(header, data)


