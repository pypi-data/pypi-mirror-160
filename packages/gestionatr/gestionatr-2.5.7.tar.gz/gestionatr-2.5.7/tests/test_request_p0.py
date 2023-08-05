from gestionatr.cli import request_p0

P0_DEMO = {
    "Iberdrola": {
        'url': "https://www.i-de.es/cnmcws/agentes/sync?wsdl",
        'user': "EC980Y4",
        'password': "9UWyvGv39D",
        'cups': "ES0021000008103774WC0F",
        'emisora': "0373",
        'destino': "0021",
    },
    "Morella": {
        'url': "https://ov.maestrazgodistribucion.es/Sync?WSDL",
        'user': "0373",
        'password': "0373_aeQuee3F",
        'cups': "ES0189000038091476YE0F",
        'emisora': "0373",
        'destino': "0189",
    },
    "Dielsur": {
        'url': "http://wsp0dielesur.portalswitching.com/WSCurvas.asmx?wsdl",
        'user': "1440",
        'password': "Test1440",
        'cups': "ES0143000000203855EW0F",
        'emisora': "1440",
        'destino': "0143",
    },
    "CIDE": {
        'url': "https://switchingsync.sercide.com/SYNCService.svc?wsdl",
        'user': "0370_i1C6N",
        'password': "=mYow<umQV`aq",
        'cups': "ES0614000000000035ZJ0F",
        'emisora': "0706",
        'destino': "0614",
    },
    "Endesa": {
        'url': "http://trader-eapi.de-c1.eu1.cloudhub.io/api/P0?wsdl",
        'user': "ea1f02cb9ed04a1da80496255df63870",
        'password': "78415Cd1a3e44798A87d642EF0171517",
        'cups': "ES0031300002599001TX0F",
        'emisora': "0706",
        'destino': "0031",
    },
    "Fenosa": {
        'url': "https://sctd.gasnaturalfenosa.com/sctd/ws/Sync?wsdl",
        'user': "1664WSSAP",
        'password': "2022Mayo",
        'cups': "ES0022000006704409RB1P",
        'emisora': "1664",
        'destino': "0022",
    },
    "Viesgo": {
        'url': "https://viesgop0.app.viesgo.com/syncRequest.wsdl",
        'user': "0706",
        'password': "ENE190#06",
        'cups': "ES0027700037401002ZB0F",
        'emisora': "0706",
        'destino': "0282",
    },
}

import sys
for distri in P0_DEMO:
    sys.stdout.write(("Testing {}...".format(distri)))
    res = request_p0(url=P0_DEMO[distri]["url"], user=P0_DEMO[distri]["user"], password=P0_DEMO[distri]["password"], params=P0_DEMO[distri])
    if "CodigoDePaso>02" not in res:
        print "ERROR"
    else:
        print "OK"
