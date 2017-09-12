# -*- coding: utf-8 -*-
import threading


class Parser(object):
    testing = None

    def __init__(self, start: int, end: int, data: object,
                 signatures: list, results: list) -> None:
        self.start = start
        self.end = end
        self.data = data
        self.results = results
        self.signatures = signatures

        print("[%d] start: %d, end: %d" % (self.get_thread_id(), start, end))
        print(self.signatures)
        self.parse()

    def parse(self) -> None:
        self.results[self.get_thread_id()] = {
            "name": threading.current_thread().name,
            "value": self.data[self.start:self.start+10]
        }
        # self.testing = self.data[self.start:self.start+10]
        # print(self.data[self.start:self.start+10])

    @staticmethod
    def get_thread_id() -> int:
        return int(threading.current_thread().name[-1:]) - 1
