import csv
import sys
from argparse import ArgumentError
import deepl

n_traductor = 0


class Ubersetzungsprogramm:
    def __init__(self, operador="deepl"):
        with open("api.key", 'r') as datei:
            self.lizenzschlussel = datei.readline()[:-1]

        if   operador == "deepl":
            self.traductor = self.__deepl
        else:
            raise ArgumentError

    def traductor(self, text: str) -> str:
        pass

    def __deepl(self, text: str) -> str:
        global n_traductor
        zielsprache = sys.argv[2]
        global n_traductor
        traduccion = "Traducido{0}: {1}".format(zielsprache, n_traductor)
        print("Traducido{0} {1}: {2}".format(zielsprache, n_traductor, text))
        n_traductor += 1
        return traduccion

        ubersetzungsprogramm = deepl.Translator(self.lizenzschlussel)
        # ergebnis = ubersetzungsprogramm.translate_text(
        #     text,
        #     target_lang=zielsprache,
        #     source_lang="DE",
        #     tag_handling="html"
        # )
        # return ergebnis.text