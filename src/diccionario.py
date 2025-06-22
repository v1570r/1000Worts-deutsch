import csv
import json
import sys
import time

from src.LeoAccess import search

IDs_BEDEUTUNGEN = {
    "Affix"                   : "*",
    "Adjektiv"                : "adjadv",
    "Adverb"                  : "adjadv",
    "bestimmter Artikel"      : "praep",
    "Demonstrativpronomen"    : "praep",
    "Eigenname"               : "subst",
    "Expresion"               : "phrase",
    "Indefinitpronomen"       : "praep",
    "Interjektion"            : "phrase",
    "Interrogativpronomen"    : "praep",
    "Kardinalzahl"            : "praep",
    "Komparativ"              : "adjadv",
    "Konjunktion"             : "praep",
    "Mehrwortausdruck"        : "*",
    "Ordinalzahl"             : "praep",
    "Partikel"                : "adjadv",
    "partizipiales Adjektiv"  : "adjadv",
    "Präposition"             : "praep",
    "Präposition + Artikel"   : "praep",
    "Personalpronomen"        : "praep",
    "Pronomen"                : "praep",
    "Pronominaladverb"        : "adjadv",
    "Possessivpronomen"       : "praep",
    "Reflexivpronomen"        : "praep",
    "Substantiv"              : "subst",
    "Superlativ"              : "adjadv",
    "Symbol"                  : "abbrev",
    "Verb"                    : "verb"
}


zielsprache = sys.argv[2]
glossarinhaltsverzeichnis = ["key", "value"]
glossarname = "LEO_dict-" + zielsprache + ".txt"
diccionario_traductor = dict()
try:
    with open(glossarname, 'r', newline='') as buch:
        worterbuch = csv.DictReader(buch)
        for key in worterbuch:
            diccionario_traductor[key[glossarinhaltsverzeichnis[0]]] = json.loads(key[glossarinhaltsverzeichnis[1]])
except FileNotFoundError:
    with open(glossarname, 'w', newline='') as buch:
        worterbuch = csv.DictWriter(buch, fieldnames=glossarinhaltsverzeichnis)
        worterbuch.writeheader()

class LEODict:
    def __init__(self, lemma, wortart):
        self.lemma = lemma
        self.bedeutungens = self.__cargar_traducciones()
        self.type = self.__cargar_tipo(wortart)
        self.tabelle = self.__contruir_tabla()

    def __cargar_traducciones(self):
        if self.lemma in diccionario_traductor:
            diccionarior_leo = diccionario_traductor[self.lemma]
        else:
            diccionarior_leo = search(self.lemma)
            diccionario_traductor[self.lemma] = diccionarior_leo
            with open(glossarname, 'a', newline='') as buch:
                worterbuch = csv.DictWriter(buch, fieldnames=glossarinhaltsverzeichnis)
                worterbuch.writerow(
                    {
                        "key": self.lemma,
                        "value": json.dumps(diccionarior_leo)
                    }
                )
            time.sleep(5)
        return diccionarior_leo

    def __cargar_tipo(self, wortart):
        if wortart in IDs_BEDEUTUNGEN:
            return IDs_BEDEUTUNGEN[wortart]
        with open("wortart_por_definir.txt", 'a', newline='') as buch:
            buch.write("{} : {} tamaño: {} dict {} \n".format(self.lemma, wortart, len(self.bedeutungens), self.bedeutungens.keys()))
        return "praep"

    def __contruir_tabla(self):
        prefijo_tabla = '<table class="bedeuteng"><thead><tr><th>Deutsch</th><th>Spanisch</th></tr></thead><tbody>'
        plantilla     = '<tr><th>{0}</th><td>{1}</td></tr>'
        sufijo_tabla  = "</tbody></table>"
        if 0 == len(self.bedeutungens):
            listado_expresiones = list()
        else:
            try:
                if "*" == self.type:
                    listado_tipos = self.bedeutungens
                    listado_expresiones = []
                    for expresiones in listado_tipos.values():
                        listado_expresiones += expresiones
                else:
                    listado_expresiones = self.bedeutungens[self.type]
            except KeyError:
                listado_expresiones = self.bedeutungens[list(self.bedeutungens.keys())[0]]
        contenido = ''
        for elemento in listado_expresiones:
            contenido += plantilla.format(
                elemento["de"],
                elemento["es"]
            )
        return prefijo_tabla + contenido + sufijo_tabla

