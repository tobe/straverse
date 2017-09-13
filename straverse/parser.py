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
        self.thread_id = self.get_thread_id()

        print("[%d] start: %d, end: %d" % (self.thread_id, start, end))
        # print(self.signatures)
        self.parse()

    @staticmethod
    def build_table(word: bytes) -> list:
        """ Builds the Knuth-Morris-Pratt partial match table
        :param word: input word
        :return: partial match table as a list
        """
        table = [-1, 0]
        wpos = 0
        while len(table) < len(word):
            if word[len(table) - 1] == word[wpos]:
                wpos += 1
                table.append(wpos)
            elif wpos > 0:
                wpos = table[wpos]
            else:
                table.append(0)
        return table

    @staticmethod
    def search(needle: bytes, haystack: bytes, table: list) -> list:
        # table = build_table(word)
        ti, wi = 0, 0
        results = []
        while ti <= len(haystack) - len(needle):
            c = haystack[ti + wi]
            if needle[wi] == ord("?") or c == needle[wi]:
                if wi + 1 == len(needle):
                    results.append(ti)
                    ti += wi - table[wi]
                    if wi:
                        wi = table[wi]
                    continue

                wi += 1
            else:
                ti += wi - table[wi]
                if wi:
                    wi = table[wi]
        return results

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
        # Set-up the algorithm
        chunk = self.data[self.start:self.end]
        chunk_table = self.build_table(chunk)

        # Initialize the result list
        self.results[self.thread_id] = []

        # Run a search for every signature
        for signature_index, signature in enumerate(self.signatures):
            byte_signature = self.fix_signature(signature)
            res = self.search(byte_signature, chunk, chunk_table)

            # Save the results into the results list
            self.results[self.thread_id].append({
                "name": signature["name"],
                "values": []
            })

            # Offset the addresses
            res = [address + self.start for address in res]

            # Store
            self.results[self.thread_id][signature_index]["values"] = res

    @staticmethod
    def get_thread_id() -> int:
        return int(threading.current_thread().name[-1:]) - 1
