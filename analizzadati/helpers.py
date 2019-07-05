import csv
import io
from math import ceil
from collections import OrderedDict
from django.core.files.uploadedfile import InMemoryUploadedFile as DjangoFile
from datetime import datetime, timedelta
# si lavora su file del tipo {"Data"->[data1,data2,..]}
# PRECONDIZIONI: LISTE ORDINATE

# usato per debug ritorna listadizionari,header


def create_dataset():
    file = open("C:/Users/Giorgio/Desktop/incidenticosenza/incidenti 2013 dal 1 gen al 30 giugno.csv", "r")

    myfile = DjangoFile(file=file, field_name="myfile", name="incidenti 2013 dal 1 gen al 30 giugno.csv", content_type="application/vnd.ms-excel", size=15503, charset=None)

    myfile.seek(0)
    data = csv.DictReader(io.StringIO(myfile.read()), delimiter=';')

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

    return lista, header


# data -> numero incidenti
def data_numincidenti(dataset):

    # estrai date senza ripetizioni
    lista_date = list(OrderedDict.fromkeys(dataset['Data']))
    diz = {"Data": lista_date,
           "Num": []}
    # print("##########")
    # print(dataset)

    for data in lista_date:
        diz["Num"].append(dataset['Data'].count(data))

    # print(diz)
    return diz


# mese_numincidentI
def mese_numincidenti(dataset):

    lista_mesi = ["Gennaio", "Febbraio"]
    diz = {"Mese": lista_mesi,
           "Num": [0, 0]}

    lista_date = dataset["Data"]

    for data in lista_date:
        token = data.split("/")

        if token[1] == "01":
            diz["Num"][0] += 1
        elif token[1] == "02":
            diz["Num"][1] += 1

    print(diz)
    return diz


def week_of_month(dt):
    first_day = dt.replace(day=1)

    dom = dt.day
    adjusted_dom = dom + first_day.weekday()

    return int(ceil(adjusted_dom / 7.0))


# restituisce
# settimana-> numincidenti
def settimana_numincidenti(dataset):
    diz = {
    }
    lista_date = list(OrderedDict.fromkeys(dataset["Data"]))
    num = 0
    iMese = 0
    iSettimana = 1

    for data in lista_date:
        dt = datetime.strptime(data, '%d/%m/%Y')
        iSettimana = week_of_month(dt)
        sSettimana = "Settimana{}".format(iSettimana)
        # print(dt, sSettimana, "weekday ", dt.weekday())

        if sSettimana not in diz:
            diz[sSettimana] = []
            diz[sSettimana].append(0)
        else:
            # print(diz)
            # print(dt.month)
            if len(diz[sSettimana]) != dt.month:
                diz[sSettimana].append(0)

            diz[sSettimana][dt.month - 1] += 1

        # delta_giorni = (last_day_of_month(dt) - dt).days
        # if delta_giorni == 0:
        #     iMese += 1

        # stringa = "{} settimana".format()
    # print(diz)

    return diz
