# -*- coding: utf-8 -*-
import multiprocessing
from .kmp import KMP

class Parser(object):
    testing = None

    def __init__(self, offsets: tuple, data: object,
                 signatures: list, queue: multiprocessing.Queue,
                 quiet: bool) -> None:
        self.offsets = offsets
        self.data = data
        self.queue = queue
        self.signatures = signatures
        self.quiet = quiet

        print("[Worker #%d] Searching from %s to %s" % (
            self.get_process_id(), hex(offsets[0]), hex(offsets[1])
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
        # Set-up the algorithm for the chunk
        chunk = self.data[self.offsets[0]:self.offsets[1]]
        chunk_table = KMP.build_table(chunk)

        # Run a search for every signature
        for signature_index, signature in enumerate(self.signatures):
            byte_signature = self.fix_signature(signature)
            res = KMP.search(byte_signature, chunk, chunk_table)

            # Fix the address relative to the file
            res = [self.offsets[0] + address for address in res]

            # Now fix the offset, if required
            if "offset" in signature:
                res = [address + signature["offset"] for address in res]

            # Put the results into the queue
            self.queue.put({
                "name": signature["name"],
                "values": res
            })

    @staticmethod
    def get_process_id() -> int:
        return int(multiprocessing.current_process().name.split("-")[-1]) - 1
