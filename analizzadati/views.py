from django.shortcuts import render, redirect
import csv
import io
import os


from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.core.files.storage import FileSystemStorage


from .forms import ContactForm2, ContactForm1
from incidenticosenza import settings
from analizzadati import helpers

from .uploadfileform import CheckBox, MyForm, Box, DataSet


DEBUG_MODE = True


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

        request.session['settings'] = settings

        return HttpResponse("ciao")


def dashboard(request):

    if request.method == 'GET':

        if DEBUG_MODE:

            lista_dizionari, header = helpers.create_dataset()

            d = DataSet(lista_dizionari, header)

            request.session['dataset'] = d.dataset

            request.session['header'] = header

        return render(request, "analizzadati/dashboard.html")


def dashboard_data(request):
    if request.method == 'GET':
        # data = {"numsinistri":
        #         "giorno più incidenti":
        #         "mesepiùincidenti": }
        return render(request, "analizzadati/dashboard-data.html")


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

    # if request.method == 'GET':
    # data = {"labels": ["prova1", "prova2"],
    #             "values": [100, 200]}
    return JsonResponse(data)
