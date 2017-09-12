# -*- coding: utf-8 -*-
import mmap
import os


class STraverse(object):
    mmap = None
    fp = None

    """ Initializes STraverse """
    def __init__(self, threads: int) -> None:
        self.threads = threads

    """ Memory maps the file """
    def load_file(self, file) -> None:
        self.fp = file
        if os.name == 'nt':
            self.mmap = mmap.mmap(file.fileno(), 0, access=mmap.ACCESS_READ)
        else:
            self.mmap = mmap.mmap(file.fileno(), 0, prot=mmap.PROT_READ)

    def close_file(self) -> None:
        """ Closes the memory mapped file """
        self.mmap.close()

    def process(self) -> None:
        """ Processes the file. """
        # Determine the file size and the number of threads needed
        file_size = os.fstat(self.fp.fileno()).st_size
        chunk_size = file_size / self.threads
        print("File size: %s. Chunk size: %s. Using %d threads..." %
              (self.sizeof_fmt(file_size), self.sizeof_fmt(chunk_size), self.threads))

        for i in range(self.threads):
            print("%d. From %d to %d" % (i, chunk_size*i, chunk_size*(i+1)))

    @staticmethod
    def sizeof_fmt(num: int, suffix: str = 'B') -> str:
        """ https://stackoverflow.com/a/1094933
        :param num: number to transform
        :param suffix: the suffix to show
        :return: human readable string
        """
        for unit in ['', 'K', 'M', 'G', 'T', 'P', 'E', 'Z']:
            if abs(num) < 1024.0:
                return "%3.1f%s%s" % (num, unit, suffix)
            num /= 1024.0
        return "%.1f%s%s" % (num, 'Yi', suffix)