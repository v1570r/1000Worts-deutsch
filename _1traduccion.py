from _1ficheros import traducir
from _1html import sustitucion, posiciones, eliminar_etiqueta


def traductor(text: str) -> str:#ubersetzen
    text = text.strip()
    text = " ".join(text.split())

    if 0 != len(text) and "●" == text[0]:
        text = text[1:].strip()

    if 0 == len(text) or "[" != text[0]:
        return traducir(text)

    posicion_aclaracion = text.find("]") + 1
    aclaraciones = text[:posicion_aclaracion].strip()
    lista_aclaraciones = aclaraciones[1:-1].split(",")
    traduccion = "["
    for aclaracion in lista_aclaraciones:
        if 1 < len(traduccion):
            traduccion += ", "
        traduccion += traducir(
            aclaracion.strip()
        )

    traduccion += "] " + traducir(
        text[posicion_aclaracion:].strip()
    )
    return traduccion


def comprobar_vinyeta(texto):
    punto = texto[:4].find(".")
    parentesis = texto[:3].find(")")
    vinyeta    = ""
    if -1 == punto and -1 == parentesis:
        traduccion = traductor(texto)
    if -1 != punto:
        punto      += 1
        vinyeta    = texto[:punto]
        traduccion = traductor(texto[punto:])
    if -1 != parentesis:
        parentesis += 1
        vinyeta    = texto[:parentesis]
        traduccion = traductor(texto[parentesis:])
    return vinyeta + traduccion


def traducirBedeutungsuebersicht(bedeutungsuebersicht):
    etiqueta_inicial_li = "<li>"
    etiqueta_final_li  = "</li>"
    # bedeutungsuebersicht = eliminar_etiqueta(bedeutungsuebersicht, "i")
    bedeutungsuebersicht = eliminar_etiqueta(bedeutungsuebersicht, "span")
    bedeutungsuebersicht = eliminar_etiqueta(bedeutungsuebersicht, "/span")
    posicion_inicial_li, posicion_final_li = posiciones(
        bedeutungsuebersicht,
        "li",
        ""
    )
    posicion_inicial_li_relativa = posicion_inicial_li
    while -1 != posicion_inicial_li_relativa:
        posicion_inicial_ol, posicion_final_ol = posiciones(
            bedeutungsuebersicht[posicion_inicial_li:posicion_final_li],
            "ol",
            ""
        )
        posicion_inicial_a_traducir = posicion_inicial_li + len(etiqueta_inicial_li)
        if -1 == posicion_inicial_ol:
            posicion_final_a_traducir = posicion_final_li - len(etiqueta_final_li)
        else:
            posicion_inicial_ol += posicion_inicial_li
            posicion_final_ol += posicion_final_li
            posicion_final_a_traducir = posicion_inicial_ol
        traduccion = comprobar_vinyeta(
            bedeutungsuebersicht[posicion_inicial_a_traducir : posicion_final_a_traducir]
        )
        bedeutungsuebersicht = (bedeutungsuebersicht[:posicion_inicial_a_traducir]
                                + traduccion
                                + bedeutungsuebersicht[posicion_final_a_traducir:])
        posicion_inicial_li_relativa, posicion_final_li_relativa = posiciones(
            bedeutungsuebersicht[posicion_inicial_a_traducir:],
            "li",
            ""
        )
        posicion_inicial_li = posicion_inicial_a_traducir + posicion_inicial_li_relativa
        posicion_final_li   = posicion_inicial_a_traducir + posicion_final_li_relativa
    return bedeutungsuebersicht


def traducirBedeutung(bedeutung, etiqueta, opciones_etiqueta):
    # if 0 != len(opciones_etiqueta):
    #     etiqueta_inicial = "<" + etiqueta + ">"
    # else:
    #     etiqueta_inicial = "<" + etiqueta + " " + opciones_etiqueta + ">"
    # etiqueta_final = "</" + etiqueta + ">"
    posicion_inicial, posicion_final = posiciones(
        bedeutung,
        etiqueta,
        opciones_etiqueta
    )
    while -1 != posicion_inicial:
        aclaracion = eliminar_etiqueta(
            bedeutung[posicion_inicial : posicion_final],
            "span"
        )
        aclaracion = eliminar_etiqueta(
            aclaracion,
            "/span"
        )
        aclaracion = comprobar_vinyeta(aclaracion)

        bedeutung = (bedeutung[:posicion_inicial]
                     + aclaracion
                     + bedeutung[posicion_final:])
        posicion_inicial_relativa, posicion_final_relativa = posiciones(
            bedeutung,#[posicion_inicial + len(aclaracion):],
            etiqueta,
            opciones_etiqueta
        )
        posicion_inicial = posicion_inicial_relativa #+ posicion_final
        posicion_final   = posicion_final_relativa#+ posicion_final
    return bedeutung


def ubersetzen(bedeutungsuebersicht):
    if bedeutungsuebersicht is None:
        return None
    bedeutungsuebersicht = sustitucion(bedeutungsuebersicht)
    if -1 != bedeutungsuebersicht.find('class="bedeutungsuebersicht"'):
        return traducirBedeutungsuebersicht(bedeutungsuebersicht)
    # bedeutungsuebersicht = traducirBedeutung(
    #     bedeutungsuebersicht,
    #     "span",
    #     'class="dwdswb-diasystematik"'
    # )
    bedeutungsuebersicht = traducirBedeutung(
        bedeutungsuebersicht,
        "span",
        'class="dwdswb-definitionen"'
    )
    return bedeutungsuebersicht
