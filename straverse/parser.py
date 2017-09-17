# -*- coding: utf-8 -*-
import multiprocessing
from .kmp import KMP
import pefile

class Parser(object):
    def __init__(self, offsets: tuple, data: object,
                 signatures: list, queue: multiprocessing.Queue,
                 quiet: bool, options: dict) -> None:
        self.offsets = offsets
        self.data = data
        self.queue = queue
        self.signatures = signatures
        self.quiet = quiet
        self.options = options
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
                byte_hex = byte_int.to_bytes(1, byteorder="big")  # A single byte, byteorder doesn't matter.
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

        # Fix the addresses if it's a PE
        if self.options["fixpe"]:
            # https://stackoverflow.com/questions/20027990/how-can-i-get-text-section-from-pe-file-using-pefile
            pe_sections = self.process_pe()

        # Run a search for every signature
        for signature_index, signature in enumerate(self.signatures):
            if not self.quiet:
                self.print_message("Looking for %s" % signature["name"])

            # Grab a byte signature and perform the search
            byte_signature = self.fix_signature(signature)
            res = KMP.search(byte_signature, chunk, chunk_table)

            # Fix the address relative to the file
            res = [self.offsets[0] + address for address in res]

            # Now fix the offset, if required
            if "offset" in signature:
                res = [address + signature["offset"] for address in res]

            # Dereferencing: Instead of the address, take the value and convert it to an integer.
            # The length depends on the user-defined setting, whether it's a uint32_t or similar.
            if "dereference" in signature and signature["dereference"] is True:
                for index, address in enumerate(res):
                    bytes = self.data[address:address + signature["length"]]
                    bytes_int = int.from_bytes(bytes, self.options["endianness"])
                    res[index] = bytes_int

                    # TODO: Do this properly
                    if "fixpe" in signature:
                        res[index] = bytes_int + int(signature["fixpe"], 16)

            # Put the results into the queue
            self.queue.put({
                "name": signature["name"],
                "values": res
            })

            # Instantly print *found* signatures
            if not self.quiet:
                self.print_results(signature["name"], res)

    def process_pe(self) -> dict:
        pass

    def print_results(self, signature: str, results: list) -> None:
        """ Prints found results for a single process """
        if len(results) == 0:
            return

        results = list(set(results))

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
