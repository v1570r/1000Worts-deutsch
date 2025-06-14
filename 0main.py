import sys, csv

from _1complemento import llamarURL, repeticiones, ipa, aussprache, BlockCaracteristicas, Bedeutung, Bedeutungy
from _1html import sustitucion, listar, ordenar
from _1traduccion import ubersetzen
from src.dwds_scraping import zuschneiden

##TODO faltan audios
##TODO arreglar problemas de nombres audios ficheros y donde se almacenan
##TODO ¿se seleccionan correctamente los audios en  función de la página?
##TODO solucionad WDG o semejante que aparece al final
##TODO algunas palabras tienen más de una pronunicación

dateiname = sys.argv[1]
zielsprache = sys.argv[2]
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
with (open(dateiname, newline='') as datei):
    csvdatei = csv.DictReader(datei)
    with open(zielsprache + "-DWDS-" + dateiname, 'w', newline='') as buch:
        worterbuch = csv.DictWriter(buch, fieldnames=cabeceras)
        worterbuch.writeheader()
        for reihe in csvdatei:
            print("##$$$$", reihe["Lemma"])

            webseite = llamarURL(reihe["URL"])
            webbytes = webseite.read()
            web = webbytes.decode("utf-8")

            posicion_pagina = reihe["URL"].rfind("#")
            if -1 != posicion_pagina:
                if "Bewegung" == reihe["Lemma"]:
                    print("------PAGINA:", reihe["URL"][posicion_pagina + 1:], "\n\r\tHTML:", web)
                cuadro_definicion = '<div role="tabpanel" class="tab-pane"'
                id_definicion = 'id="' + reihe["URL"][posicion_pagina + 1:] + '"'

                existe = -1
                fin_div = 0
                while -1 == existe:
                    if "Bewegung" == reihe["Lemma"]:
                        print("inicio_div:", inicio_div, "\tfin_div:", fin_div, "\tlen(web):", len(web))
                    inicio_div = web.find(cuadro_definicion, fin_div)
                    if -1 == inicio_div:
                        break
                    fin_div = web.find(">", inicio_div)
                    existe = web[inicio_div:fin_div].find(id_definicion)

                # inicio_div = web.find(cuadro_definicion)
                # fin_div = web.find(">", inicio_div)
                # existe = web[inicio_div:fin_div].find(id_definicion)
                # while -1 == existe:
                #     fin_div = web.find(">", inicio_div) + 1
                #     existe = web[inicio_div:fin_div].find(id_definicion)
                #     print("EJEMPLOS:", cuadro_definicion + id_definicion)
                #     print("TROCITOS:",web[inicio_div:fin_div])
                #     print("EXISTE:", existe, "INICIO:", inicio_div, "FIN:", fin_div)
                #     input("jooooo")
                #     if -1 == existe:
                #         inicio_div = web.find(cuadro_definicion, fin_div)

                # print("WEB:", zuschneiden(web[inicio_div:], "div")
                if -1 != inicio_div:
                    web = zuschneiden(web[inicio_div:], "div")

            bedeutung = Bedeutung(web, "dwdswb-lesarten")
            if bedeutung is not None:
                bedeutung = sustitucion(bedeutung)
                bedeutung = listar(bedeutung)
                bedeutung = ordenar(bedeutung)

            worterbuch.writerow(
                {
                    "Worthäufigkeit": repeticiones(reihe["Lemma"]),
                    "Lemma": reihe["Lemma"],
                    "Wortart": reihe["Wortart"],
                    "Artikel": reihe["Artikel"],
                    "Aussprache": aussprache(web),
                    "IPA": ipa(reihe["Lemma"]),
                    "Grammatik": BlockCaracteristicas(web, "Grammatik"),
                    "Worttrennung": BlockCaracteristicas(web, "Worttrennung"),
                    "Wortzerlegung": BlockCaracteristicas(web, "Wortzerlegung"),
                    "Bedeutungen": ubersetzen(bedeutung)
                }
            )

