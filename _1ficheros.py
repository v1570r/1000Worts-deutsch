import csv
import sys

from _2externos import Ubersetzungsprogramm

zielsprache = sys.argv[2]
glossarinhaltsverzeichnis = ["key", "value"]
glossarname = "Glossar-" + zielsprache + ".txt"
diccionario_traductor = dict()
try:
    with open(glossarname, 'r', newline='') as buch:
        worterbuch = csv.DictReader(buch)
        for key in worterbuch:
            diccionario_traductor[key[glossarinhaltsverzeichnis[0]]] = key[glossarinhaltsverzeichnis[1]]
except FileNotFoundError:
    with open(glossarname, 'w', newline='') as buch:
        worterbuch = csv.DictWriter(buch, fieldnames=glossarinhaltsverzeichnis)
        worterbuch.writeheader()


def traducir(text: str) -> str:
    if text in diccionario_traductor:
        return diccionario_traductor[text]
    try:
        float(text)
        traduccion = text
    except ValueError:
        ubersetzungsprogramm = Ubersetzungsprogramm()
        traduccion = ubersetzungsprogramm.traductor(text)

    diccionario_traductor[text] = traduccion
    with open(glossarname, 'a', newline='') as buch:
        worterbuch = csv.DictWriter(buch, fieldnames=glossarinhaltsverzeichnis)
        worterbuch.writerow(
            {
                "key" : text,
                "value": traduccion
            }
        )
    return traduccion