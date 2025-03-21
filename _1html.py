
def eliminar_etiqueta(subweb, etiqueta):
    etiqueta_apertura = "<" + etiqueta
    def posiciones_etiqueta(mensaje):
        posición_inicial_etiqueta_apertura = mensaje.find(etiqueta_apertura + " ")
        posición_inicial_etiqueta_apertura_cerrada = mensaje.find(etiqueta_apertura + ">")
        if -1 == posición_inicial_etiqueta_apertura or -1 != posición_inicial_etiqueta_apertura_cerrada and posición_inicial_etiqueta_apertura_cerrada < posición_inicial_etiqueta_apertura:
            posición_inicial_etiqueta_apertura = posición_inicial_etiqueta_apertura_cerrada
        primer_bloque_inicial = mensaje[posición_inicial_etiqueta_apertura:]
        posición_final_etiqueta_cierre = posición_inicial_etiqueta_apertura + primer_bloque_inicial.find(">") + 1
        return (posición_inicial_etiqueta_apertura, posición_final_etiqueta_cierre)

    nuevo_fin, nuevo_inicio = posiciones_etiqueta(subweb)
    while -1 != nuevo_fin:
        subweb = subweb[:nuevo_fin] + subweb[nuevo_inicio:]
        nuevo_fin, nuevo_inicio = posiciones_etiqueta(subweb)
    return subweb



def recortador(subweb, etiqueta):
    etiqueta_final = "</" + etiqueta + ">"
    posicion_ultima_etiqueta_final = subweb.find(etiqueta_final) + len(etiqueta_final)
    recorte = subweb[:posicion_ultima_etiqueta_final]
    while recorte.count(etiqueta_final) != recorte.count("<" + etiqueta):
        posicion_ultima_etiqueta_final += subweb[posicion_ultima_etiqueta_final:].find(etiqueta_final) + len(etiqueta_final)
        recorte = subweb[:posicion_ultima_etiqueta_final]
    return recorte


def posiciones(web, etiqueta, opciones_etiqueta):
    etiqueta_final = "</" + etiqueta + ">"
    if 0 != len(opciones_etiqueta):
        opciones_etiqueta = " " + opciones_etiqueta

    posición_inicial_recorte = web.find("<" + etiqueta + opciones_etiqueta)
    posicion_relativa_ultima_etiqueta_final = (
            posición_inicial_recorte
            + web[posición_inicial_recorte:].find(etiqueta_final)
            + len(etiqueta_final)
        )
    recorte = web[posición_inicial_recorte:posicion_relativa_ultima_etiqueta_final]
    while recorte.count(etiqueta_final) != recorte.count("<" + etiqueta):
        posicion_relativa_ultima_etiqueta_final = (
                posicion_relativa_ultima_etiqueta_final
                + web[posicion_relativa_ultima_etiqueta_final:].find(etiqueta_final)
                + len(etiqueta_final)
        )
        recorte = web[posición_inicial_recorte:posicion_relativa_ultima_etiqueta_final]
    return posición_inicial_recorte, posicion_relativa_ultima_etiqueta_final





def sustitucion(html):
    etiqueta_apertura = "<abbr "
    etiqueta_cierre  = "</abbr>"
    etiqueta_opcional = 'data-original-title="'
    titulo_inicial = 'title="'
    def posiciones_etiqueta(mensaje):
        posición_inicial_etiqueta_apertura = mensaje.find(etiqueta_apertura)
        primer_bloque_inicial = mensaje[posición_inicial_etiqueta_apertura:]
        posición_final_etiqueta_cierre = posición_inicial_etiqueta_apertura + primer_bloque_inicial.find(etiqueta_cierre) + len(etiqueta_cierre)
        return posición_inicial_etiqueta_apertura, posición_final_etiqueta_cierre
    nuevo_fin, nuevo_inicio = posiciones_etiqueta(html)
    while -1 != nuevo_fin:
        # print("INICIO:",html)
        a_sustituir = html[nuevo_fin:nuevo_inicio]
        inicio_etiqueta = a_sustituir.find(etiqueta_opcional)
        # print("inicio_etiqueta", inicio_etiqueta)
        if -1 == inicio_etiqueta:
            inicio_etiqueta = a_sustituir.find(titulo_inicial)
            if -1 == inicio_etiqueta:
                break
            else:
                inicio_texto = inicio_etiqueta + len(titulo_inicial)
        else:
            inicio_texto = inicio_etiqueta + len(etiqueta_opcional)
        fin_texto = a_sustituir[inicio_texto:].find('"') + inicio_texto
        # print("posiciones", inicio_texto, fin_texto)
        # print("html:", html[nuevo_fin:nuevo_inicio])
        html = html[:nuevo_fin] + a_sustituir[inicio_texto:fin_texto] + html[nuevo_inicio:]
        nuevo_fin, nuevo_inicio = posiciones_etiqueta(html)
        # print("\tFIN:",html)
    return html


def listar(html):
    etiqueta_apertura = '<div class="dwdswb-lesart" id="'
    segunda_etiqueta_apertura = '<div class="dwdswb-lesart-content"'
    etiqueta_cierre  = "</div>"

    def listado(bloque):
        orden_posicion_final = bloque.find('"', len(etiqueta_apertura))
        orden_lista = bloque[len(etiqueta_apertura):orden_posicion_final]
        # print("LISTADO-orden:", orden_lista)

        posicion_inicial_desde_borrar = bloque.find(segunda_etiqueta_apertura) + len(segunda_etiqueta_apertura)
        posicion_inicial_desde_borrar = bloque.find(">", posicion_inicial_desde_borrar) + 1

        # posicion_inicial, posicion_final = posiciones(
        #     bloque,
        #     "span",
        #     'class="dwdswb-definitionen"'
        # )
        #
        # if -1 != bloque.find(etiqueta_apertura, posicion_final):
        #     posicion_final = -2*len(etiqueta_cierre)
        # return '<li id="' + orden_lista + '">' + bloque[posicion_inicial:posicion_final] + "</li>"
        return '<li id="' + orden_lista + '">' + bloque[posicion_inicial_desde_borrar:-2*len(etiqueta_cierre)] + "</li>"

    posición_inicial_etiqueta_apertura = html.find(etiqueta_apertura)
    while -1 != posición_inicial_etiqueta_apertura:
        bloque = recortador(html[posición_inicial_etiqueta_apertura:], "div")
        posicion_inicial_bloque = html.find(bloque)
        posicion_final_bloque = posicion_inicial_bloque + len(bloque)

        bloque = listado(bloque)
        html = html[:posicion_inicial_bloque] + bloque + html[posicion_final_bloque:]

        posición_inicial_etiqueta_apertura = html.find(etiqueta_apertura)
    return html


def ordenar(html):
    etiqueta_inicial  = "li"
    etiqueta_apertura = '<' + etiqueta_inicial + ' id="'
    etiqueta_cierre   = '</' + etiqueta_inicial + '>'
    etiqueta_definicion_apertura = '<div class="dwdswb-lesart-def"'
    etiqueta_definicion_cierre   = '</div>'

    def listado(bloque):
        orden_posicion_final = bloque.find('"', len(etiqueta_apertura))
        orden_lista = bloque[len(etiqueta_apertura):orden_posicion_final]
        ol_type = "1"
        ol_count = orden_lista.count("-")
        if 3 == ol_count:
            ol_type = "a"
        if 4 == ol_count:
            ol_type = "A"
        if 5 == ol_count:
            ol_type = "i"

        # print("ORden:", orden_lista)

        posicion_div_inicial = bloque.find(etiqueta_definicion_apertura)
        posicion_definicion_inicial = bloque.find(">", posicion_div_inicial) + 1
        posicion_definicion_final   = bloque.find(etiqueta_definicion_cierre, posicion_definicion_inicial)
        posicion_div_final = posicion_definicion_final + len(etiqueta_definicion_cierre)
        definicion = bloque[posicion_definicion_inicial:posicion_definicion_final]

        posicion_inicial_hijo = bloque.find(etiqueta_apertura,orden_posicion_final)
        if -1 != posicion_inicial_hijo:
            bloque = (bloque[:posicion_div_inicial] + definicion +
                      '<ol type="' + ol_type + '">' + bloque[posicion_inicial_hijo:])
            bloque = bloque[:-len(etiqueta_cierre)]    + "</ol>" + bloque[-len(etiqueta_cierre):]
        else:
            bloque = bloque[:posicion_div_inicial] + definicion + bloque[-len(etiqueta_cierre):]
        return bloque

    posición_inicial_etiqueta_apertura = html.find(etiqueta_apertura)
    while -1 != posición_inicial_etiqueta_apertura:
        bloque = recortador(html[posición_inicial_etiqueta_apertura:], etiqueta_inicial)
        posicion_inicial_bloque = html.find(bloque)
        posicion_final_bloque = posicion_inicial_bloque + len(bloque)

        bloque = listado(bloque)
        html = html[:posicion_inicial_bloque] + bloque + html[posicion_final_bloque:]

        posición_inicial_etiqueta_apertura = html.find(etiqueta_apertura, posicion_inicial_bloque + len(etiqueta_apertura))
    return '<ol type="I">' + html + "</ol>"
