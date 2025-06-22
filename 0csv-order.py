import csv
import sys

ursprung = sys.argv[1]
cabeceras = [
    "Worthäufigkeit",
    "Lemma",
    "Wortart",
    "Artikel",
    "Aussprache",
    "IPA",
    "Grammatik",
    "Worttrennung",
    "Wortzerlegung",
    "Bedeutungen"
]

with (open(ursprung, newline='') as datei):
    csvdatei = csv.DictReader(datei)
    lista = sorted(csvdatei, key= lambda linia: int(linia.items().mapping["Worthäufigkeit"]), reverse=True)
    # print(lista)
    # lista = []
    # for reihe in csvdatei:
    #     lista.append(reihe.items())

    # lista = sorted(lista, key= lambda valor: valor.mapping["Worthäufigkeit"])
    with open(ursprung + "-ordenado", 'w', newline='') as buch:
        worterbuch = csv.DictWriter(buch, fieldnames=cabeceras)
        i = 0
        for reihe in lista:
            i += 1
            worterbuch.writerow(
                {
                    "Worthäufigkeit": "B2"+str(i).zfill(4),
                    "Lemma": reihe["Lemma"],
                    "Wortart": reihe["Wortart"],
                    "Artikel": reihe["Artikel"],
                    "Aussprache": reihe["Aussprache"],
                    "IPA": reihe["IPA"],
                    "Grammatik": reihe["Grammatik"],
                    "Worttrennung": reihe["Worttrennung"],
                    "Wortzerlegung": reihe["Wortzerlegung"],
                    "Bedeutungen": reihe["Bedeutungen"]
                }
            )
