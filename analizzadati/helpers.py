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


# ritorna numero sinistri
def sinistri_moda(dataset):
    return len(dataset['Data'])


def data_moda(dataset):
    freq = {}  # data->n
    for data in dataset["Data"]:
        if data not in freq:
            freq[data] = 1
        else:
            freq[data] += 1
   # lista = [(k, v) for k, v in dict.items()]
    #numeriOrdinati = sorted(freq.items())
    lista = freq.items()
    #n = max(lista[1])
    massimo = max(lista, key=lambda item: item[1])[1]
    date = []
    for data, frequenza in lista:
        if(frequenza == massimo):
            date.append(data)

    # print(date)
    # print(lista)
    # print(massimo)
    return date


def giorno_moda(dataset):
    freq = {}  # giorno->n
    giorno = {
        0: "Lunedì",
        1: "Martedì",
        2: "Mercoledì",
        3: "Giovedì",
        4: "Venerdì",
        5: "Sabato",
        6: "Domenica"}
    for data in dataset["Data"]:
        dt = datetime.strptime(data, '%d/%m/%Y')
        # print(dt)
        # print(dt.day)
        g = giorno[dt.weekday()]
        # print(g)
        if g not in freq:
            freq[g] = 1
        else:
            freq[g] += 1

    # print(freq)
    lista = freq.items()
    massimo = max(lista, key=lambda item: item[1])[1]
    giorni = []
    for data, frequenza in lista:
        if(frequenza == massimo):
            giorni.append(data)
    # print(giorni)
    return giorni

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

    # print(diz)
    return diz


def week_of_month(dt):
    first_day = dt.replace(day=1)

    dom = dt.day
    adjusted_dom = dom + first_day.weekday()

    return int(ceil(adjusted_dom / 7.0))


# settimana-> [numincidentimese1,numincidentimese2]
def settimana_numincidenti(dataset):
    diz = {}
    #lista_date = list(OrderedDict.fromkeys(dataset["Data"]))

    lista_date = dataset["Data"]

    #num = 0
    iMese = 0
    iSettimana = 1

    for data in lista_date:
        # print(data)
        dt = datetime.strptime(data, '%d/%m/%Y')
        iSettimana = week_of_month(dt)
        #print("Con week of m: ", iSettimana)
        sSettimana = "Settimana{}".format(iSettimana)
        # print(dt, sSettimana, "weekday ", dt.weekday())

        if sSettimana not in diz:
            diz[sSettimana] = []
            diz[sSettimana].append(1)
        else:
            # print(diz)
            # print(dt.month)
            # se non hai iniz numincidenti del mese
            if len(diz[sSettimana]) < dt.month:
                diz[sSettimana].append(0)

            diz[sSettimana][dt.month - 1] += 1
            # print(diz)

        # delta_giorni = (last_day_of_month(dt) - dt).days
        # if delta_giorni == 0:
        #     iMese += 1

        # stringa = "{} settimana".format()

    # print("#########")
    # print(diz)

    return diz


### BASATI SU CONDUCENTE #####


def fasciaeta_freq(dataset):
    diz = {"Fasciaeta": [],
           "numincidenti": []}

    # lista

    pass


def tuple_analizzate_conducente(dataset):
    count = 0
    for cond in dataset['Fascia di Età Conducente Veicolo (A)']:
        if cond != "":
            count += 1

    return count


def tuple_errore_conducente(dataset):
    count = 0
    for cond in dataset['Fascia di Età Conducente Veicolo (A)']:
        if cond == "":
            count += 1

    return count


def tuple_fasce_eta(dataset):
    lista_fasce = []

    for fascia in dataset['Fascia di Età Conducente Veicolo (A)']:
        if fascia not in lista_fasce and fascia != "":
            lista_fasce.append(fascia)

    return lista_fasce


# fascia ->{ tipocoll -> freq }
def fasciaeta_tipo_numero(dataset):

    lista_fasce = tuple_fasce_eta(dataset)

    diz_fasce = {}

    indice = 0
    for fascia in dataset['Fascia di Età Conducente Veicolo (A)']:

        if fascia == "":
            continue

        if fascia not in diz_fasce:
            diz_fasce[fascia] = {}

        tipo_collisione = dataset['Tipo collisione'][indice]

        # print("dizFAsce")
        # print(diz_fasce)

        # print("TipoCollisione")
        # print(tipo_collisione)

        # print("Indice")
        # print(indice)

        assert tipo_collisione != ""

        if tipo_collisione not in diz_fasce[fascia]:
            diz_fasce[fascia][tipo_collisione] = 1
        else:
            diz_fasce[fascia][tipo_collisione] += 1

        indice += 1

    print(diz_fasce)

    return diz_fasce
