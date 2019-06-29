from django.shortcuts import render, redirect
import csv
import io
import os
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.core.files.storage import FileSystemStorage


from .forms import ContactForm2, ContactForm1
from incidenticosenza import settings


from .uploadfileform import CheckBox, MyForm, Box, DataSet


def home(request):

    if request.method == 'GET':
        request.session.clear()

        # print(c.field)
        return render(request, "analizzadati/home.html", )

    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']

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

        print("Stampo ContactForm1")

        request.session['dati'] = lista

        d = DataSet(lista, header)

        request.session['dataset'] = d.dataset

        #DataSet(lista, header)
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
        return render(request, "analizzadati/dashboard.html")


def dashboard_data(request):
    if request.method == 'GET':
        #pr = {"prova": 1}
        return render(request, "analizzadati/dashboard-data.html")


def dashboard_data_ajax(request):

    dataset = request.session['dataset']

    d = DataSet()

    print(dataset)

    diz = d.data_numincidenti(dataset)

    data = {"labels": diz['Data'],
            "values": diz['Num']}
    # if request.method == 'GET':
    # data = {"labels": ["prova1", "prova2"],
    #             "values": [100, 200]}
    return JsonResponse(data)
