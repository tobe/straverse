# -*- coding: utf-8 -*-
import argparse
import sys
import os
from straverse import straverse, output


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
                        help="Converts a signature into straverse compatible signature")
    parser.add_argument("-p", "--processes", help="Number of processes to run", type=int, default=4)
    parser.add_argument("--no-colors", help="Disable the use of colors", action="store_true")
    parser.add_argument("file", nargs="?", type=argparse.FileType('rb'))
    args = parser.parse_args()

    if not args:
        parser.print_help()
        sys.exit(1)

    # If -v or -t aren't present and file isn't as well, error
    if not (args.verify or args.transform) and not args.file:
        parser.print_help()
        sys.exit(1)

    # Set quietness
    """if args.quiet:
        sys.stdout = open(os.devnull, "a")
        sys.stderr = open(os.devnull, "a")"""

    # Instantiate STraverse
    s = straverse.STraverse(args.processes, args.quiet)

    if args.verify:
        # s.load_file(...)
        pass
        return
    if args.transform:
        pass
        return

    # Load the input file
    if not s.load_input_file(args.file):
        print("Failed to load the input file.")
        return

    # Load the config file
    if not s.load_config_file(args.config):
        print("The JSON configuration file is erroneous.")
        return

    # Process the input file
    result = s.process()
    # Close it when we're done
    s.close_file()

    # Call the Output class to generate some output if needed
    o = output.Output(result, args.no_colors)
    if not args.quiet:
        # Output to stdout
        o.output_results()
    if args.output:
        # output to file
        o.save_results(s.config["options"]["output"], args.output)
