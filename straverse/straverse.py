# -*- coding: utf-8 -*-
import mmap
import os


class STraverse(object):
    """ Initializes STraverse """
    def __init__(self, quiet):
        self.quiet = quiet

    """ Memory maps the file """
    def load_file(self, file):
        if os.name == 'nt':
            self.mmap = mmap.mmap(file.fileno(), 0, access=mmap.ACCESS_READ)
        else:
            self.mmap = mmap.mmap(file.fileno(), 0, prot=mmap.PROT_READ)

    def close_file(self):
        self.mmap.close()