from django.shortcuts import render, redirect
import csv
import io
import os
import re

from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.core.files.storage import FileSystemStorage


from .forms import ContactForm2, ContactForm1
from incidenticosenza import settings
from analizzadati import helpers
from django.contrib import messages
from .uploadfileform import CheckBox, MyForm, Box, DataSet, Setting


DEBUG_MODE = False

# Dati richiesti per ogni tab
COLUMNS_ICONS = {

    "Basato su Data": "nc-icon nc-tag-content",
    "Basato su Cond. Meteo": "nc-icon nc-icon nc-umbrella-13",
    "Basato su Conducenti": "nc-icon nc-circle-09",
    "Basato su Cond. Traffico": "nc-icon nc-bus-front-12"
}


COLUMNS_URLS = {

    "Basato su Data": "dashboard-data",
    "Basato su Cond. Meteo": "dashboard-meteo",
    "Basato su Conducenti": "dashboard-conducenti",
    "Basato su Cond. Traffico": "dashboard-traffico"

}

COLUMNS_DASHBOARD = {

    "Basato su Data": ['Data', 'Fascia oraria'],
    "Basato su Conducenti": ['Fascia di Età Conducente Veicolo (A)', 'Tipo collisione'],
    "Basato su Cond. Meteo": ['Stato fondo stradale', 'Tipo collisione'],
    "Basato su Cond. Traffico": ['Entità del Traffico', 'Fascia oraria']
}


def home(request):

    if request.method == 'GET':
        request.session.clear()

        # print(c.field)
        return render(request, "analizzadati/home.html", )

    if request.method == 'POST' and request.FILES['myfile']:

        myfile = request.FILES['myfile']

        # myfile = FileSystemStorage(location= )
        print("TIPO DI MYFILE")
        print(type(myfile))
        print(myfile.field_name)
        print(myfile.name)
        print(myfile.content_type)
        print(myfile.size)
        print(myfile.charset)

        myfile.seek(0)
        data = csv.DictReader(io.StringIO(myfile.read().decode('ISO-8859-1')), delimiter=';')
        print(type(data))

        lista = []
        header = []
        i = 0

        for line in data:
            if i == 0:

                for s in line:

                    header.append(s)
            else:
                lista.append(line)
            i = i + 1

        print(header)

        request.session['dati'] = lista

        d = DataSet(lista, header)

        request.session['dataset'] = d.dataset

        # DataSet(lista, header)
        request.session['header'] = header

        return redirect("selezionaColonne")


def selezionaColonne(request):

    if request.method == 'GET':

        # data = request.session['data']
        # count = 0
        # for d in data:
        #  count+=1

        n = 10
        # form = CheckBox(2)
        box = Box(request.session['header'])

        # form = CheckBox()
       # print(form)

        print("CREAZIONE FORM2")

        return render(request, "analizzadati/selezionaColonne.html", {"box": box})
    else:

        settings = {}

        header = request.session['header']

        for field in header:
            if field in request.POST:
                settings[field] = True
            else:
                settings[field] = False

        toView = []
        for dashboard in COLUMNS_DASHBOARD.keys():
            toView.append(dashboard)

        print("##COLUMNS_DASHBOARD##")
        print(COLUMNS_DASHBOARD)
        for dashboard in COLUMNS_DASHBOARD:
            for field in COLUMNS_DASHBOARD[dashboard]:
                # print("#field#")
                # print(field)
                if not settings[field]:
                    if dashboard in toView:
                        toView.remove(dashboard)

        # s = Setting(toView)

        request.session['settings'] = settings

        links = []
        icons = []

        for item in toView:
            icons.append(COLUMNS_ICONS[item])
            links.append(COLUMNS_URLS[item])

        context = {"toView": toView, "links": links, "icons": icons}
        request.session["base"] = context

        data = {"unak": "altrak"}
        for key in context:
            data[key] = context[key]

        # print("#####data#######")
        # print(data)

        # nextPage = "analizzadati/{}.html".format(links[0])
        # return render(request, nextPage, data)
        if len(links) == 0:
            messages.info(request, 'Your password has been changed successfully!')
            box = Box(request.session['header'])
            # return render(request, "analizzadati/selezionaColonne.html", {"box": box})
            return redirect("selezionaColonne")
        else:
            return redirect(links[0])


def dashboard(request):

    if request.method == 'GET':

        if DEBUG_MODE:

            lista_dizionari, header = helpers.create_dataset()

            d = DataSet(lista_dizionari, header)

            request.session['dataset'] = d.dataset

            request.session['header'] = header

        ##DEBUG##
        context = request.session["base"]
        data = {"unak": "altrak"}
        for key in context:
            data[key] = context[key]

        print("#####data#######")
        print(data)

        return render(request, "analizzadati/dashboard.html", data)


def dashboard_data(request):
    if request.method == 'GET':
        # data = {"numsinistri":
        #         "giorno più incidenti":
        #         "mesepiùincidenti": }

        dataset = request.session['dataset']
        data = {
            # ccorreggere sin moda
            "incmoda": helpers.sinistri_moda(dataset),
            "datamoda": helpers.data_moda(dataset),
            "giornomoda": helpers.giorno_moda(dataset),
            "errori": helpers.data_errori(dataset)

        }

        # print(data)
        print("###############DATA PASSED!!################")
        context = request.session["base"]
        for key in context:
            data[key] = context[key]

        print("#####data#######")
        print(data)

        return render(request, "analizzadati/dashboard-data.html", data)


def dashboard_data_ajax(request):

    dataset = request.session['dataset']

    d = DataSet()

    data = {}
    # print(dataset)

    # diz = d.data_numincidenti(dataset)
    diz = helpers.data_numincidenti(dataset)
    data["datachart_day"] = {"labels": diz['Data'],
                             "values": diz['Num']}

    diz = helpers.settimana_numincidenti(dataset)

    data["datachart_month_labels"] = ["Gennaio", "Febbraio"]
    data["datachart_month_data"] = {}

    for settimana in diz:
        if settimana not in data["datachart_month_data"]:
            data["datachart_month_data"][settimana] = diz[settimana]

    # print(data)

    diz = helpers.mese_numincidenti(dataset)

    data["mesechart"] = {"labels": diz['Mese'],
                         "values": diz['Num']}

    data["now"] = helpers.now()
    # if request.method == 'GET':
    # data = {"labels": ["prova1", "prova2"],
    #             "values": [100, 200]}

    diz = helpers.data_ora_freq(dataset)

    data["data_ora_freq"] = diz

    return JsonResponse(data)


def dashboard_conducenti(request):

    if request.method == 'GET':
        dataset = request.session['dataset']
        data = {
            "num": helpers.tuple_analizzate_conducente(dataset),
            "err": helpers.tuple_errore_conducente(dataset),
            "fascia_moda": helpers.fascia_moda(dataset),
            "tipologiainc_moda": helpers.tipologiainc_moda(dataset)

        }
        # print(dataset)
        diz = helpers.fasciaeta_tipo_numero(dataset)

        ##DEBUG##
        context = request.session["base"]
        for key in context:
            data[key] = context[key]

        print("#####data#######")
        print(data)

        return render(request, "analizzadati/dashboard-conducenti.html", data)


def dashboard_conducenti_ajax(request):

    dataset = request.session['dataset']

    data = {}

    # print(dataset)

    diz = helpers.fasciaeta_tipo_numero(dataset)

    lista_fasce = helpers.tuple_fasce_eta(dataset)

    # continua qui
    for fascia in lista_fasce:
        query = "datachart_{}".format(fascia)
        tipi_coll = []
        num_inc = []
        # print("##################")
        # print(diz[fascia])
        for coll, num in diz[fascia].items():
            tipi_coll.append(coll)
            num_inc.append(num)

            # print("tipi coll")
            # print(tipi_coll)

            # print("num incd")
            # print(num_inc)

        data[query] = {"labels": tipi_coll,
                       "values": num_inc}

    # print("#######")
    # print(data)

    diz = helpers.fasciaeta_freq(dataset)

    fasce = []
    freq = []

    for x in diz.keys():
        fasce.append(x)
    for x in diz.values():
        freq.append(x)

    data["instogramma"] = {"labels": fasce,
                           "values": freq}
    # print("###### KEYS #####")
    # print(fasce)

    # print("###### ITEMS #####")
    # print(freq)

    # print("###### DIZ #####")
    # print(diz)

    # diz = helpers.tipocoll_fascia_freq(dataset)

    diz = helpers.tipocoll_freq(dataset)

    data["tipocoll_freq"] = {"labels": list(diz.keys()),
                             "values": list(diz.values())}

    # print("Diz tipocoll_freq")
    # print(diz)
    # print(list(diz.keys()))
    # print(list(diz.values()))

    diz = helpers.fascia_tipocoll_freq(dataset)

    for f in diz:
        data["fascia_{}".format(f)] = {}
        data["fascia_{}".format(f)]["labels"] = list(diz[f].keys())
        data["fascia_{}".format(f)]["values"] = list(diz[f].values())

    # print("###################")
    # print(data)

    diz = helpers.fascia_fascia_freq(dataset)

    data["fascia_fascia_freq"] = {}
    for fasciaA, fasciaB in diz:

        # fasciaAint = int(re.search(r'\d+', fasciaA).group())

        # fasciaBint = int(re.search(r'\d+', fasciaB).group())
        # print(fasciaA)
        # print(fasciaB)

        # if fasciaA not in data["fascia_fascia_freq"]:
        #     data["fascia_fascia_freq"] = {}
        if fasciaA not in data["fascia_fascia_freq"]:
            # data["fascia_fascia_freq"] = fasciaA
            data["fascia_fascia_freq"][fasciaA] = {}

        data["fascia_fascia_freq"][fasciaA][fasciaB] = diz[(fasciaA, fasciaB)]
        # print(data["fascia_fascia_freq"])

    # data["fascia_fascia_freq"] = diz

    # print("#####data#####")
    # print(data["fascia_fascia_freq"])

    # fasciaeta -> { tipoinc -> num }
    # data["datachart_fasciaeta"] =

    return JsonResponse(data)


def dashboard_meteo(request):

    dataset = request.session['dataset']
    data = {
        "num": helpers.tuple_analizzate_meteo(dataset),
        "err": helpers.tuple_errore_meteo(dataset),
        "asfalto_moda": helpers.asfalto_moda(dataset),
        "tipostrada_moda": helpers.tipostrada_moda(dataset)
    }

    ##DEBUG##
    context = request.session["base"]
    for key in context:
        data[key] = context[key]

    print("#####data#######")
    print(data)
    return render(request, "analizzadati/dashboard-meteo.html", data)


def dashboard_meteo_ajax(request):

    dataset = request.session['dataset']

    data = {}

    diz = helpers.tipocoll_strada_freq(dataset)

    lista_tipo_inc = list(diz.keys())

    print(lista_tipo_inc)

    data["tipocoll_strada_freq"] = {"labels": lista_tipo_inc,
                                    "datasets": {}}

    lista_cond_stradali = []

    for tipo in diz:
        for cond in diz[tipo]:
            if cond not in lista_cond_stradali:
                lista_cond_stradali.append(cond)

    print("###LISTA COND STRADALI####")
    print(lista_cond_stradali)

    # for coll in diz:
    #     for cond_strada in diz[coll]:

    #         if cond_strada not in data["tipocoll_strada_freq"]["datasets"]:
    #             data["tipocoll_strada_freq"]["datasets"][cond_strada] = []

    #         for c in list(diz.keys()):

    #             if c not in diz[coll]:
    #                 data["tipocoll_strada_freq"]["datasets"][cond_strada].append(0)
    #             else:
    #                 data["tipocoll_strada_freq"]["datasets"][cond_strada].append(diz[coll][cond_strada])

    for cond in lista_cond_stradali:
        if cond not in data["tipocoll_strada_freq"]["datasets"]:
            data["tipocoll_strada_freq"]["datasets"][cond] = []

        for coll in lista_tipo_inc:

            if cond not in diz[coll]:
                data["tipocoll_strada_freq"]["datasets"][cond].append(0)
            else:
                data["tipocoll_strada_freq"]["datasets"][cond].append(diz[coll][cond])

    # print("####DATA#######")
    # print(data)

    diz = helpers.tipocoll_tipostrada_freq(dataset)

    # for coll in diz:
    #     for tipo_strada in diz[coll]:
    #         if tipo_strada not in lista_tipi_strada:
    #             lista_tipi_strada.append(tipo_strada)

    # print(lista_tipi_strada)

    # for strada in lista_tipi_strada:
    #     if strada not in data["tipocoll_tipostrada_freq"]["datasets"]:
    #         data["tipocoll_tipostrada_freq"]["datasets"][tipostrada] = []

    #     for coll in lista_tipo_inc:

    # lista tipo inc sono le coll

    lista_coll = list(diz.keys())

    data["tipocoll_tipostrada_freq"] = {"labels": lista_coll,
                                        "datasets": {}}

    lista_tipo_strada = []  # asciutto/bagnato

    for coll in diz:
        for tipostrada in diz[coll]:
            if tipostrada not in lista_tipo_strada:
                lista_tipo_strada.append(tipostrada)
    print("####")
    print(lista_tipo_strada)

    for tipostrada in lista_tipo_strada:
        if tipostrada not in data["tipocoll_tipostrada_freq"]["datasets"]:
            data["tipocoll_tipostrada_freq"]["datasets"][tipostrada] = []

        for coll in lista_coll:
            if tipostrada not in diz[coll]:
                data["tipocoll_tipostrada_freq"]["datasets"][tipostrada].append(0)

            else:
                data["tipocoll_tipostrada_freq"]["datasets"][tipostrada].append(diz[coll][tipostrada])

    print("####DATA#######")
    print(data)

    return JsonResponse(data)


def dashboard_traffico(request):
    dataset = request.session['dataset']
    data = {
        "num": helpers.tuple_analizzate_traffico(dataset),
        "err": helpers.tuple_errore_traffico(dataset),
        "orario_moda": helpers.orario_moda(dataset),
        "traffico_moda": helpers.traffico_moda(dataset)



    }
    ##DEBUG##
    context = request.session["base"]
    for key in context:
        data[key] = context[key]

    print("#####data#######")
    print(data)
    return render(request, "analizzadati/dashboard-traffico.html", data)


def dashboard_traffico_ajax(request):

    dataset = request.session['dataset']

    data = {}

    diz = helpers.traffico_freq(dataset)

    data["traffico_freq"] = {"labels": list(diz.keys()),
                             "values": list(diz.values())}

    diz = helpers.fascia_freq(dataset)

    data["fascia_freq"] = {"labels": list(diz.keys()),
                           "values": list(diz.values())}

    diz = helpers.entita_fascia_freq(dataset)

    data["entita_fascia_freq"] = diz

    print("##########")
    print(data)

    return JsonResponse(data)
