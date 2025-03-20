import sys, csv

from _1complemento import llamarURL, repeticiones, ipa, aussprache, BlockCaracteristicas, Bedeutung, Bedeutungy
from _1html import sustitucion, listar
from _1traduccion import ubersetzen

if 2 >= len(sys.argv):
    print("Requiere un fichero CSV e idioma de destino: https://developers.deepl.com/docs/resources/supported-languages#target-languages ")
    exit(2)
dateiname = sys.argv[1]
zielsprache = sys.argv[2]
cabeceras = [
    "Worthäufigkeit",
    "Lemma",
    "Wortart",
    "Genus",
    "Artikel",
    "nur_im_Plural",
    "Aussprache",
    "IPA",
    "Grammatik",
    "Worttrennung",
    "Wortzerlegung",
    "Bedeutungsuebersicht",
    "Bedeutungen"
]
with open(dateiname, newline='') as datei:
    csvdatei = csv.DictReader(datei)
    with open(zielsprache + "-DWDS-" + dateiname, 'w', newline='') as buch:
        worterbuch = csv.DictWriter(buch, fieldnames=cabeceras)
        worterbuch.writeheader()
        for reihe in csvdatei:
            print("##$$$$", reihe["Lemma"])

            webseite = llamarURL(reihe["URL"])
            webbytes = webseite.read()
            web = webbytes.decode("utf-8")

            bedeutung = Bedeutung(web, "dwdswb-lesarten")
            if bedeutung is not None:
                bedeutung = sustitucion(bedeutung)
                bedeutung = listar(bedeutung)

            worterbuch.writerow(
                {
                    "Worthäufigkeit": repeticiones(reihe["Lemma"]),
                    "Lemma": reihe["Lemma"],
                    "Wortart": reihe["Wortart"],
                    "Genus": reihe["Genus"],
                    "Artikel": reihe["Artikel"],
                    "nur_im_Plural": reihe["nur_im_Plural"],
                    "Aussprache": aussprache(web),
                    "IPA": ipa(reihe["Lemma"]),
                    "Grammatik": BlockCaracteristicas(web, "Grammatik"),
                    "Worttrennung": BlockCaracteristicas(web, "Worttrennung"),
                    "Wortzerlegung": BlockCaracteristicas(web, "Wortzerlegung"),
                    "Bedeutungsuebersicht": Bedeutungy(web),
                    "Bedeutungen": ubersetzen(bedeutung)
                }
            )

