# -*- coding: utf-8 -*-


class KMP(object):
    """ Modified Knuth-Morris-Pratt substring search algorithm """

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
