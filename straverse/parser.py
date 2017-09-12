# -*- coding: utf-8 -*-
import threading
import binascii

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

    def search(self, haystack: str, needle: str) -> list:
        haystack_length = len(haystack)
        needle_length = len(needle)
        results = []

        if needle_length > haystack_length:
            return results

        # Preprocess
        skip = []
        for i in range(256):
            skip.append(haystack_length)
        for i in range(haystack_length - 1):
            pass

    def fix_signature(self, signature: str) -> str:
        """ Converts an IDA style signature into a bytestring """
        bytestring = b""
        for byte in signature["pattern"].split():
            if byte != "?":
                byte_int = int(byte, 16)
                byte_hex = byte_int.to_bytes(1, byteorder="big")
                bytestring += byte_hex
            else:
                bytestring += b"?"
        return bytestring

    def parse(self) -> None:
        """self.results[self.get_thread_id()] = {
            "name": threading.current_thread().name,
            "value": self.data[self.start:self.start+10]
        }"""

        for signature in self.signatures:
            signature = self.fix_signature(signature)
            print(signature)

        # self.testing = self.data[self.start:self.start+10]
        # print(self.data[self.start:self.start+10])

    @staticmethod
    def get_thread_id() -> int:
        return int(threading.current_thread().name[-1:]) - 1
