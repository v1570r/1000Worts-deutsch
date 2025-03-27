import sys
import deepl
from argparse import ArgumentError


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
        zielsprache = sys.argv[2]

        ubersetzungsprogramm = deepl.Translator(self.lizenzschlussel)
        try:
            ergebnis = ubersetzungsprogramm.translate_text(
                text,
                target_lang=zielsprache,
                source_lang="DE",
                tag_handling="html"
            )
        except deepl.exceptions.AuthorizationException:
            ubersetzungsprogramm = deepl.Translator(
                self.lizenzschlussel,
                server_url="https://api-free.deepl.com"
            )
            ergebnis = ubersetzungsprogramm.translate_text(
                text,
                target_lang=zielsprache,
                source_lang="DE",
                tag_handling="html"
            )
        return ergebnis.text
