import csv
import sys

from _1traduccion import ubersetzen

if 2 >= len(sys.argv):
    print("Requiere un fichero CSV e idioma de destino: https://developers.deepl.com/docs/resources/supported-languages#target-languages ")
    exit(2)
dateiname = sys.argv[1]
zielsprache = sys.argv[2]
cabeceras = [
    "Lemma",
    "Wortart",
    "Genus",
    "Artikel",
    "nur_im_Plural",
    "MP3",
    "IPA",
    "Grammatik",
    "Worttrennung",
    "Wortzerlegung",
    "Bedeutungsuebersicht"
]
with open(dateiname, newline='') as datei:
    csvdatei = csv.DictReader(datei)
    with open(zielsprache + "-" + dateiname, 'w', newline='') as buch:
        worterbuch = csv.DictWriter(buch, fieldnames=cabeceras)
        worterbuch.writeheader()
        for reihe in csvdatei:
            print("LEMMA:", reihe["Lemma"])
            worterbuch.writerow(
                {
                    "Worthäufigkeit": reihe["Worthäufigkeit"],
                    "Lemma": reihe["Lemma"],
                    "Wortart": reihe["Wortart"],
                    "Genus": reihe["Genus"],
                    "Artikel": reihe["Artikel"],
                    "nur_im_Plural": reihe["nur_im_Plural"],
                    "Aussprache": reihe["Aussprache"],
                    "IPA": reihe["IPA"],
                    "Grammatik": reihe["Grammatik"],
                    "Worttrennung": reihe["Worttrennung"],
                    "Wortzerlegung": reihe["Wortzerlegung"],
                    "Bedeutungen": ubersetzen(reihe["Bedeutungen"])
                }
            )

