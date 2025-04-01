import json, urllib.parse, os
import time
from random import randint
from urllib.request import urlopen, urlretrieve
from _1html import eliminar_etiqueta, recortador, sustitucion, listar
from src.konstant import AUSSPRACHE_FORMAT, VORHERIG_AUSSPRACHE, ROOT_FOLDER


def llamarURL(url):
    sekunden = 5
    while True:
        try:
            return urlopen(url)
        except urllib.error.HTTPError as msg_error:
            print("HTTP-Fehler '" , url,  "'.", sekunden, "Sekunden warten.", msg_error)
            if 422 == msg_error.code:
                return None
            time.sleep(sekunden)
        except urllib.error.URLError as msg_error:
            print("Vorübergehender Fehler bei der Namensauflösung:'" , url,  "'.", sekunden, "Sekunden warten.", msg_error)
            time.sleep(sekunden)


def ipa(lemma):
    url = "https://www.dwds.de/api/ipa/?q=" + urllib.parse.quote(lemma)

    apiseite = llamarURL(url)
    if apiseite is None:
        return None
    apibytes = apiseite.read()
    ipaseite = json.loads(apibytes.decode("utf-8"))
    for ipa in ipaseite:
        return '[' + ipa["ipa"] + ']'
    return None


def aussprache(web):
    cabecera_bloque = '<div class="dwdswb-ft-block"><span class="dwdswb-ft-blocklabel serif italic">'
    # cabecera_bloque = '<span class="dwdswb-ft-blocklabel serif italic">'
    inicio_bloque = "<div "
    fin_bloque = '</div>'
    entrada_mp3 = "https"
    entrada_ipa = "["
    salida_ipa = "]"
    inicio = web.find(cabecera_bloque + "Aussprache")
    if 0 == inicio:
        return None

    fin = inicio + web[inicio:].find(fin_bloque) + len(fin_bloque)
    aussprache = web[inicio:fin]

    inicio_mp3 = aussprache.find(entrada_mp3)
    fin_mp3 = aussprache.find(AUSSPRACHE_FORMAT) + len(AUSSPRACHE_FORMAT)
    url_mp3 = aussprache[inicio_mp3:fin_mp3]
    posicion_inicial_nombre_mp3 = url_mp3.find(VORHERIG_AUSSPRACHE)
    if -1 == posicion_inicial_nombre_mp3:
        return None

    camino_relativo = url_mp3[posicion_inicial_nombre_mp3:]
    nombre_mp3 = (VORHERIG_AUSSPRACHE + "-" +
                  camino_relativo.split("/")[2][:-len(AUSSPRACHE_FORMAT)] + "-" +
                  camino_relativo.split("/")[1] + AUSSPRACHE_FORMAT)
    ubicacion_mp3 = ROOT_FOLDER + "/" + nombre_mp3
    if not os.path.exists(ROOT_FOLDER):
        os.makedirs(ROOT_FOLDER)
    if not os.path.exists(ubicacion_mp3):
        urlretrieve(
            url_mp3,
            ubicacion_mp3
        )
    return "[sound:" + nombre_mp3 +"]"


def repeticiones(lemma):#https://www.dwds.de/api/frequency/?q=Haus
    MAXIM = 1108780648
    url = "https://www.dwds.de/api/frequency/?q=" + urllib.parse.quote(lemma)
    apiseite = llamarURL(url)
    apibytes = apiseite.read()
    veces_usadas = json.loads(apibytes.decode("utf-8"))
    if veces_usadas["hits"] is None or veces_usadas["hits"] == 0:
        return randint(MAXIM, 2*MAXIM)
    return MAXIM - veces_usadas["hits"]


def BlockCaracteristicas(web, atributo):
    cabecera_bloque = '<div class="dwdswb-ft-block"><span class="dwdswb-ft-blocklabel serif italic">'
    fin_bloque = '</div>'
    inicio = web.find(cabecera_bloque + atributo)
    if 0 == inicio:
        return None

    fin = inicio + web[inicio:].find(fin_bloque) + len(fin_bloque)
    block = web[inicio:fin]
    block = eliminar_etiqueta(block, "a")
    block = eliminar_etiqueta(block, "/a")
    return block


def Bedeutung(web, divclass):
    inicio = web.find('<div class="' + divclass + '"')
    if -1 == inicio:
        return None
    html = recortador(web[inicio:], "div")
    html = eliminar_etiqueta(html, "a")
    html = eliminar_etiqueta(html, "/a")
    return html

def Bedeutungy(web):
    bedeutung = Bedeutung(web, "bedeutungsuebersicht")
    if bedeutung is None:
        bedeutung = Bedeutung(web, "dwdswb-lesarten")
        if bedeutung is not None:
            bedeutung = sustitucion(bedeutung)
            bedeutung = listar(bedeutung)
    return bedeutung