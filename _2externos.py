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

        # global n_traductor
        # traduccion = "Traducido{0}: {1}".format(zielsprache, n_traductor)
        # print("Traducido{0} {1}: {2}".format(zielsprache, n_traductor, text))
        # n_traductor += 1
        # return traduccion

        """
Traceback (most recent call last):
  File "/home/usuario/programacion/1000Worts-deutsch/_1ficheros.py", line 25, in traducir
    float(text)
ValueError: could not convert string to float: 'ständige Aufsicht, Überwachung'

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/home/usuario/programacion/1000Worts-deutsch/_2externos.py", line 30, in __deepl
    ergebnis = ubersetzungsprogramm.translate_text(
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/usuario/programacion/DWDS-worterbuch/.venv/lib/python3.11/site-packages/deepl/translator.py", line 455, in translate_text
    self._raise_for_status(status, content, json)
  File "/home/usuario/programacion/DWDS-worterbuch/.venv/lib/python3.11/site-packages/deepl/translator.py", line 184, in _raise_for_status
    raise AuthorizationException(
deepl.exceptions.AuthorizationException: Authorization failure, check auth_key, message: Wrong endpoint. Use https://api-free.deepl.com

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/home/usuario/programacion/1000Worts-deutsch/0main.py", line 92, in <module>
    "Bedeutungen": ubersetzen(bedeutung)
                   ^^^^^^^^^^^^^^^^^^^^^
  File "/home/usuario/programacion/1000Worts-deutsch/_1traduccion.py", line 136, in ubersetzen
    bedeutungsuebersicht = traducirBedeutung(
                           ^^^^^^^^^^^^^^^^^^
  File "/home/usuario/programacion/1000Worts-deutsch/_1traduccion.py", line 110, in traducirBedeutung
    aclaracion = comprobar_vinyeta(aclaracion)
                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/usuario/programacion/1000Worts-deutsch/_1traduccion.py", line 37, in comprobar_vinyeta
    traduccion = traductor(texto)
                 ^^^^^^^^^^^^^^^^
  File "/home/usuario/programacion/1000Worts-deutsch/_1traduccion.py", line 13, in traductor
    return traducir(text)
           ^^^^^^^^^^^^^^
  File "/home/usuario/programacion/1000Worts-deutsch/_1ficheros.py", line 29, in traducir
    traduccion = ubersetzungsprogramm.traductor(text)
                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/usuario/programacion/1000Worts-deutsch/_2externos.py", line 41, in __deepl
    ergebnis = ubersetzungsprogramm.translate_text(
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/usuario/programacion/DWDS-worterbuch/.venv/lib/python3.11/site-packages/deepl/translator.py", line 455, in translate_text
    self._raise_for_status(status, content, json)
  File "/home/usuario/programacion/DWDS-worterbuch/.venv/lib/python3.11/site-packages/deepl/translator.py", line 189, in _raise_for_status
    raise QuotaExceededException(
deepl.exceptions.QuotaExceededException: Quota for this billing period has been exceeded, message: Quota Exceeded

Process finished with exit code 1
"""

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
