# -*- coding: utf-8 -*-
import multiprocessing
from .kmp import KMP

class Parser(object):
    def __init__(self, offsets: tuple, data: object,
                 signatures: list, queue: multiprocessing.Queue,
                 quiet: bool) -> None:
        self.offsets = offsets
        self.data = data
        self.queue = queue
        self.signatures = signatures
        self.quiet = quiet
        self.process_id = self.get_process_id()

        self.print_message("Searching from %s to %s" % (
            hex(offsets[0]), hex(offsets[1])
        ))
        self.parse()

    def fix_signature(self, signature: str) -> bytes:
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
        """ Runs a search for every signature and stores found
         signatures into a queue """

        if not self.quiet:
            self.print_message("Setting up the partial match table")

        # Set-up the algorithm for the chunk
        chunk = self.data[self.offsets[0]:self.offsets[1]]
        chunk_table = KMP.build_table(chunk)

        # Run a search for every signature
        for signature_index, signature in enumerate(self.signatures):
            if not self.quiet:
                self.print_message("Looking for %s" % signature["name"])

            # Grab a byte signature and perform the search
            byte_signature = self.fix_signature(signature)
            res = KMP.search(byte_signature, chunk, chunk_table)

            # Fix the address relative to the file
            res = [self.offsets[0] + address for address in res]

            # TODO: Handle dereferencing

            # Now fix the offset, if required
            if "offset" in signature:
                res = [address + signature["offset"] for address in res]

            # Put the results into the queue
            self.queue.put({
                "name": signature["name"],
                "values": res
            })

            # Instantly print *found* signatures
            if not self.quiet:
                self.print_results(signature["name"], res)

    def print_results(self, signature: str, results: list) -> None:
        """ Prints found results for a single process """
        if len(results) == 0:
            return

        self.print_message("Found %s at %s" % (
            signature,
            ', '.join(hex(r) for r in results)
        ))

    def print_message(self, message: str) -> None:
        """ Prints a message prefixed with a worker ID """
        print("[Worker #%d] %s" % (self.process_id, message))

    @staticmethod
    def get_process_id() -> int:
        """ Returns a process ID (number) """
        return int(multiprocessing.current_process().name.split("-")[-1])
