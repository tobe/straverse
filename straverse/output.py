# -*- coding: utf-8 -*-
import colorama


class Output(object):
    """ Manages the output, either to the stdout or the file. """

    def __init__(self, results: dict, no_colors: bool):
        self.results = results
        self.no_colors = no_colors

        if not no_colors:
            colorama.init()

    def output_results(self):
        for name, values in self.results.items():
            if len(values) == 0:
                self.print_message("[-] Did not find %s" % name, False)

            self.print_message("Found %s at %s" % (
                name,
                ', '.join(hex(r) for r in values)
            ), True)

    def print_message(self, message: str, severity=None) -> None:
        if severity:
            prefix = "[+] "
            color_code = colorama.Fore.LIGHTGREEN_EX
        if severity == False:
            prefix = "[-] "
            color_code = colorama.Fore.LIGHTRED_EX
        if severity == None or self.no_colors:
            prefix = ""
            color_code = ""

        print(color_code + "%s%s" % (prefix, message) + colorama.Style.RESET_ALL)


    def save_results(self):
        pass