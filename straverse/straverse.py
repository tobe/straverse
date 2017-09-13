# -*- coding: utf-8 -*-
import mmap
import os
import multiprocessing
import json
from .parser import Parser


class STraverse(object):
    mmap = None
    fp = None
    signatures = [None]
    config = None

    def __init__(self, processes: int) -> None:
        """ Initializes STraverse """
        self.processes = processes

    def load_input_file(self, file) -> bool:
        """ Memory maps the file """
        self.fp = file
        try:
            if os.name == 'nt':
                self.mmap = mmap.mmap(file.fileno(), 0, access=mmap.ACCESS_READ)
            else:
                self.mmap = mmap.mmap(file.fileno(), 0, prot=mmap.PROT_READ)
            return True
        except:  # The documentation is really bad for this one.
            return False

    def load_config_file(self, file) -> bool:
        """ Loads and extracts useful information from the JSON configuration file. """
        try:
            self.config = json.load(file)
        except json.JSONDecodeError as e:
            print("Failed to load the config file: %s" % e.msg)
            return False

        # Check whether the signatures object is present
        if not self.config["signatures"]:
            return False

        # Verify the each signature contains a name and a pattern
        for sig in self.config["signatures"]:
            if "name" not in sig or "pattern" not in sig:
                return False
        
        # The test has passed
        return True

    def close_file(self) -> None:
        """ Closes the memory mapped file """
        self.mmap.close()

    def process(self) -> dict:
        """ Processes the file. """
        # Determine the file size and the number of threads needed
        file_size = os.fstat(self.fp.fileno()).st_size
        chunk_size = file_size / self.processes
        print("File size: %s. Chunk size: %s. Using %d threads..." %
              (self.sizeof_fmt(file_size), self.sizeof_fmt(chunk_size), self.processes))

        # Will hold the results from each thread
        queue = multiprocessing.Queue()

        # Construct a list of threads and fill it with thread objects
        threads = []
        for i in range(self.processes):
            thread = multiprocessing.Process(target=Parser, args=(
                int(chunk_size*i),
                int(chunk_size*(i+1)),
                self.mmap,
                self.config["signatures"],
                queue
            ))
            threads.append(thread)
            # break

        # Start all threads
        for t in threads:
            t.start()
        # Wait until all threads finish
        for t in threads:
            t.join()

        # Grab results from the queue and store them in a single resulting object
        results = {}
        while not queue.empty():
            current_sig = queue.get()
            if not current_sig["name"] in results:
                results[current_sig["name"]] = []

            results[current_sig["name"]] += current_sig["values"]

        return results

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