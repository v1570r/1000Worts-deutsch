import json, urllib.parse, os
import time
from urllib.request import urlopen, urlretrieve
from _1html import eliminar_etiqueta, recortador, sustitucion, listar


def llamarURL(url):
    while True:
        try:
            return urlopen(url)
        except urllib.error.HTTPError or urllib.error.URLError as msg_error:
            print("Fallo HTTP con '" + url + "', esperando 10 segundos", msg_error)
            if 422 == msg_error.code:
                return None
            time.sleep(10)


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
    salida_mp3 = ".mp3"
    entrada_ipa = "["
    salida_ipa = "]"
    inicio = web.find(cabecera_bloque + "Aussprache")
    if 0 == inicio:
        return None

    fin = inicio + web[inicio:].find(fin_bloque) + len(fin_bloque)
    aussprache = web[inicio:fin]

    inicio_mp3 = aussprache.find(entrada_mp3)
    fin_mp3 = aussprache.find(salida_mp3) + len(salida_mp3)
    url_mp3 = aussprache[inicio_mp3:fin_mp3]
    posicion_inicial_nombre_mp3 = url_mp3.find("audio")
    if -1 == posicion_inicial_nombre_mp3:
        return None

    camino_relativo = url_mp3[posicion_inicial_nombre_mp3:]
    nombre_mp3 = camino_relativo.split("/")[2][:-len(salida_mp3)] + "-" + camino_relativo.split("/")[1] + salida_mp3
    ubicacion_mp3 = camino_relativo.split("/")[0]+ "/" + nombre_mp3
    mp3_paths = camino_relativo.split("/")[0]
    if not os.path.exists(mp3_paths):
        os.makedirs(mp3_paths)
    if not os.path.exists(ubicacion_mp3):
        urlretrieve(
            url_mp3,
            ubicacion_mp3
        )
    return "[sound:" + nombre_mp3 +"]"


def repeticiones(lemma):#https://www.dwds.de/api/frequency/?q=Haus
    url = "https://www.dwds.de/api/frequency/?q=" + urllib.parse.quote(lemma)
    apiseite = llamarURL(url)
    apibytes = apiseite.read()
    veces_usadas = json.loads(apibytes.decode("utf-8"))
    return veces_usadas["hits"]


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