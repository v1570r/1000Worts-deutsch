import os
from urllib.request import urlretrieve


def zuschneiden(unterwebsite, auszeichnung):
    endekennzeichnung = "</" + auszeichnung + ">"
    ausgangsposition_zeichnung = unterwebsite.find("<" + auszeichnung)
    if -1 == ausgangsposition_zeichnung:
        return ""
    unterwebsite = unterwebsite[ausgangsposition_zeichnung:]
    endposition_endekennzeichnung = unterwebsite.find(endekennzeichnung) + len(endekennzeichnung)
    website_verkurzt = unterwebsite[:endposition_endekennzeichnung]
    while website_verkurzt.count(endekennzeichnung) != website_verkurzt.count("<" + auszeichnung):
        endposition_endekennzeichnung += unterwebsite[endposition_endekennzeichnung:].find(endekennzeichnung) + len(endekennzeichnung)
        website_verkurzt = unterwebsite[:endposition_endekennzeichnung]
    return website_verkurzt


def aussprache(web):
    anfangsposition_zeichnung = web.find('<div class="dwdswb-ft-block"><span class="dwdswb-ft-blocklabel serif italic">Aussprache')
    if 0 == anfangsposition_zeichnung:
        print("aussprache:  0")
        return None
    if -1 == anfangsposition_zeichnung:
        print("aussprache: -1")
        return None

    aussprache_verkurzt = zuschneiden(web[anfangsposition_zeichnung:], "div")
    ausgangsposition_aussprache = aussprache_verkurzt.find("https")
    endposition_aussprache = aussprache_verkurzt.find(konstant.AUSSPRACHE_FORMAT) + len(konstant.AUSSPRACHE_FORMAT)
    url_aussprache = aussprache_verkurzt[ausgangsposition_aussprache:endposition_aussprache]
    anfangsposition_aussprachename = url_aussprache.find(konstant.VORHERIG_AUSSPRACHE)
    if -1 == anfangsposition_aussprachename:
        return None

    relative_aussprache = url_aussprache[anfangsposition_aussprachename:]
    aussprachename = (konstant.VORHERIG_AUSSPRACHE + "-" +
                  relative_aussprache.split("/")[2][:-len(konstant.AUSSPRACHE_FORMAT)] + "-" +
                  relative_aussprache.split("/")[1] + konstant.AUSSPRACHE_FORMAT)
    speicherort_aussprache = konstant.ROOT_FOLDER + "/" + aussprachename
    if not os.path.exists(konstant.ROOT_FOLDER):
        os.makedirs(konstant.ROOT_FOLDER)
    if not os.path.exists(speicherort_aussprache):
        urlretrieve(
            url_aussprache,
            speicherort_aussprache
        )
    return "[sound:" + aussprachename +"]"
