# -*- coding: utf-8 -*-
import argparse
import sys
import straverse.straverse as straverse

def main():
    parser = argparse.ArgumentParser(
        description="Cross-platform static file signature scanner")
    parser.add_argument("-c", "--config", help="Configuration file",
                        type=argparse.FileType('r'), default="config.json")
    parser.add_argument("-o", "--output", help="Output file",
                        type=argparse.FileType('w'), default=sys.stdout)
    parser.add_argument("-q", "--quiet", help="Do not display any output", action="store_true")
    parser.add_argument("-v", "--verify", help="Verify against a single signature", type=str)
    parser.add_argument("-t", "--transform",
                        help="Transform a signature into straverse compatible signature")
    parser.add_argument("file", nargs="?", type=argparse.FileType('rb'))
    args = parser.parse_args()

    if not args:
        parser.print_help()
        sys.exit(1)

    # If -v or -t aren't present and file isn't as well, error
    if not (args.verify or args.transform) and not args.file:
        parser.print_help()
        sys.exit(1)

    if args.verify:
        pass
        return
    if args.transform:
        pass
        return

    s = straverse.STraverse(args.quiet)
    s.load_file(args.file)
    # Process file
    s.close_file()