# -*- coding: utf-8 -*-


class Output(object):
    """ Manages the output, either to the stdout or the file. """

    def __init__(self, results: dict):
        self.results = results

    def output_results(self):
        print("res->", self.results)

    def save_results(self):
        pass