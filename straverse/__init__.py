# -*- coding: utf-8 -*-
import argparse
import sys
import os
import straverse.straverse as straverse


def main():
    parser = argparse.ArgumentParser(
        description="Cross-platform static file signature scanner")
    parser.add_argument("-i", "--input", help="Configuration file",
                        type=argparse.FileType('r'), default="config.json")
    parser.add_argument("-o", "--output", help="Output file",
                        type=argparse.FileType('w'), default=sys.stdout)
    parser.add_argument("-q", "--quiet", help="Do not display any output", action="store_true")
    parser.add_argument("-v", "--verify", help="Verify against a single signature", type=str)
    parser.add_argument("-c", "--convert",
                        help="Converts a signature into straverse compatible signature")
    parser.add_argument("-t", "--threads", help="Number of threads to run", type=int, default=4)
    parser.add_argument("file", nargs="?", type=argparse.FileType('rb'))
    args = parser.parse_args()

    if not args:
        parser.print_help()
        sys.exit(1)

    # If -v or -t aren't present and file isn't as well, error
    if not (args.verify or args.convert) and not args.file:
        parser.print_help()
        sys.exit(1)

    # Set quietness
    if args.quiet:
        sys.stdout = open(os.devnull, "a")
        sys.stderr = open(os.devnull, "a")

    # Instantiate STraverse
    s = straverse.STraverse(args.threads)

    if args.verify:
        # s.load_file(...)
        pass
        return
    if args.convert:
        pass
        return

    s.load_file(args.file)
    s.process()
    s.close_file()
