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


def now():
    return datetime.now()


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
    # numeriOrdinati = sorted(freq.items())
    lista = freq.items()
    # n = max(lista[1])
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
        # print(dt.weekday())
        # print(dt)

        g = giorno[dt.weekday()]
        # print(g)

        if g not in freq:
            freq[g] = 1
        else:
            freq[g] += 1

    # print(freq)

    lista = freq.items()

    # print(lista)
    massimo = max(lista, key=lambda item: item[1])[1]
    giorni = []
    for data, frequenza in lista:
        if(frequenza == massimo):
            giorni.append(data)
            # print("######data####")
            # print(data)

    # print(giorni)
    return giorni

# data -> numero incidenti


def data_errori(dataset):
    err = 0
    for data in dataset["Data"]:
        if data == "":
            err += 1

    return err


def global_dates(lista_date):
    f = '%d %m %Y'
    first = datetime.strptime(lista_date[0].replace("/", " "), f).replace(day=1)
    last = datetime.strptime(lista_date[len(lista_date) - 1].replace("/", " "), f).replace(day=28)
    global_date = []

    while(first <= last):
        global_date.append(first.strftime('%d/%m/%Y'))
        first += timedelta(days=1)

    # print("####global_date###")
    # print(global_date)
    return global_date


def data_numincidenti(dataset):

    # estrai date senza ripetizioni
    lista_date = list(OrderedDict.fromkeys(dataset['Data']))

    lista_date_globale = global_dates(lista_date)

    diz = {"Data": lista_date_globale,
           "Num": []}

    # print("##########")
    # print(dataset)

    for data in lista_date_globale:
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
    # lista_date = list(OrderedDict.fromkeys(dataset["Data"]))

    lista_date = dataset["Data"]

    # num = 0
    iMese = 0
    iSettimana = 1

    for data in lista_date:
        # print(data)
        dt = datetime.strptime(data, '%d/%m/%Y')
        iSettimana = week_of_month(dt)
        # print("Con week of m: ", iSettimana)
        sSettimana = "{} Settimana".format(iSettimana)
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


def data_ora_freq(dataset):

    diz = {}

    date_csv = list(OrderedDict.fromkeys(dataset['Data']))

    lista_date = global_dates(date_csv)

    for data in lista_date:
        if data not in diz:
            diz[data] = {}
        indice = 0
        for d in dataset['Data']:
            if d == data:
                fascia = dataset['Fascia oraria'][indice]
                if fascia not in diz[d]:
                    diz[d][fascia] = 1
                else:
                    diz[d][fascia] += 1

            indice += 1
    print("###Funzione data_fascia_freq###")
    print(diz)

    return diz


### BASATI SU CONDUCENTE #####


# def moda_generica(lista):

#     freq = {}

#     for cond in dataset['Fascia di Età Conducente Veicolo (A)']:
#         if cond not in freq:
#             freq[cond] = 1
#         else:
#             freq[cond] += 1

#     fascia_freq = freq.items()

#     massimaFreq = max(fascia_freq, key=lambda item: item[1])[1]
#     lista_fasce = []

#     for fascia, frequenza in fascia_freq:
#         if(frequenza == massimaFreq):
#             lista_fasce.append(fascia)
#     print("Funzione: fasciaeta_moda")
#     print(lista_fasce)
#     return lista_fasce


def tipologiainc_moda(dataset):
    freq = {}

    for cond in dataset["Tipo collisione"]:
        if cond not in freq:
            freq[cond] = 1
        else:
            freq[cond] += 1

    fascia_freq = freq.items()

    massimaFreq = max(fascia_freq, key=lambda item: item[1])[1]
    lista_fasce = []

    for fascia, frequenza in fascia_freq:
        if(frequenza == massimaFreq):
            lista_fasce.append(fascia)
    # print("Funzione: fasciaeta_moda")
    # print(lista_fasce)
    return lista_fasce


def fascia_moda(dataset):

    freq = {}

    for cond in dataset['Fascia di Età Conducente Veicolo (A)']:
        if cond not in freq:
            freq[cond] = 1
        else:
            freq[cond] += 1

    fascia_freq = freq.items()

    massimaFreq = max(fascia_freq, key=lambda item: item[1])[1]
    lista_fasce = []

    for fascia, frequenza in fascia_freq:
        if(frequenza == massimaFreq):
            lista_fasce.append(fascia)
    # print("Funzione: fasciaeta_moda")
    # print(lista_fasce)
    return lista_fasce


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

    # print(diz_fasce)

    return diz_fasce


def fasciaeta_freq(dataset):

    freq = {}

    for fascia in dataset['Fascia di Età Conducente Veicolo (A)']:
        if fascia != "":
            if fascia not in freq:
                freq[fascia] = 1
            else:
                freq[fascia] += 1

    return freq


def tipocoll_freq(dataset):
    freq = {}

    for coll in dataset['Tipo collisione']:

        if coll not in freq:
            freq[coll] = 1
        else:
            freq[coll] += 1

    return freq


#{tipocoll - > { fascia -> freq }}
def tipocoll_fascia_freq(dataset):
    diz_coll = {}

    indice = 0
    for tipo_coll in dataset['Tipo collisione']:

        fascia = dataset['Fascia di Età Conducente Veicolo (A)'][indice]

        if fascia != "":
            if tipo_coll not in diz_coll:
                diz_coll[tipo_coll] = {}

            if fascia not in diz_coll[tipo_coll]:
                diz_coll[tipo_coll][fascia] = 1
            else:
                diz_coll[tipo_coll][fascia] += 1

        indice += 1

    # print("DIZIONARIO COLLISIONI")
    # print(diz_coll)
    return diz_coll


# fascia -> {tipocoll -> freq}
def fascia_tipocoll_freq(dataset):

    diz = {}

    indice = 0
    for fascia in dataset['Fascia di Età Conducente Veicolo (A)']:

        if fascia != "":

            if fascia not in diz:
                diz[fascia] = {}

            tipo_coll = dataset['Tipo collisione'][indice]

            if tipo_coll not in diz[fascia]:
                diz[fascia][tipo_coll] = 1
            else:
                diz[fascia][tipo_coll] += 1

        indice += 1

    # print("funzone fascia_tipocoll_freq")
    # print(diz)
    return diz


# fascia -> { fascia -> freq }
def fascia_fascia_freq(dataset):
    diz = {}
    indice = 0
    for condA in dataset['Fascia di Età Conducente Veicolo (A)']:
        condB = dataset['Fascia di Età Conducente Veicolo (B)'][indice]

        if condA != "" and condB != "":

            if (condA, condB) in diz:
                diz[(condA, condB)] += 1
            elif (condB, condA) in diz:
                diz[(condB, condA)] += 1
            else:
                # aggiungi prima volta
                diz[(condA, condB)] = 1

        indice += 1

    # print("####FASCIA FASCIA FREQ #####")

    # print(diz)

    return diz


# tipo coll -> { condstrada -> freq }
def tipocoll_strada_freq(dataset):

    diz = {}
    indice = 0
    for coll in dataset["Tipo collisione"]:

        strada = dataset["Stato fondo stradale"][indice]

        if strada != "":

            if coll not in diz:
                diz[coll] = {}

            if strada not in diz[coll]:
                diz[coll][strada] = 1
            else:
                diz[coll][strada] += 1

        indice += 1

    print("Funzione: tipocoll_strada_freq")
    print(diz)

    return diz


# tipocoll -> {tipostrda -> freq}
def tipocoll_tipostrada_freq(dataset):

    diz = {}
    indice = 0
    for coll in dataset["Tipo collisione"]:

        tipostrada = dataset["Caratteristiche della Strada"][indice]

        if tipostrada != "":

            if coll not in diz:
                diz[coll] = {}

            if tipostrada not in diz[coll]:
                diz[coll][tipostrada] = 1
            else:
                diz[coll][tipostrada] += 1

        indice += 1

    print("Funzione: tipocoll_tipostrada_freq")
    print(diz)
    return diz


def traffico_freq(dataset):

    freq = {}

    for entita in dataset["Entità del Traffico"]:
        if entita != "":
            if entita not in freq:
                freq[entita] = 1
            else:
                freq[entita] += 1

    # print("Funzione: traffico_freq")
    # print(freq)

    return freq


# fascia_oraria -> freq
def fascia_freq(dataset):
    freq = {}

    for fasciaoraria in dataset["Fascia oraria"]:
        if fasciaoraria != "":
            if fasciaoraria not in freq:
                freq[fasciaoraria] = 1
            else:
                freq[fasciaoraria] += 1

    # print("Funzione: fascia_freq")
    # print(freq)

    return freq


def entita_fascia_freq(dataset):
    diz = {}

    indice = 0

    for entita in dataset["Entità del Traffico"]:

        if entita != "":
            if entita not in diz:
                diz[entita] = {}

            fasciaoraria = dataset["Fascia oraria"][indice]

            if fasciaoraria not in diz[entita]:
                diz[entita][fasciaoraria] = 1
            else:
                diz[entita][fasciaoraria] += 1
        indice += 1

    print("Funzione: entita_fascia_freq")
    print(diz)

    return diz


def tuple_analizzate_meteo(dataset):
    count = 0
    for cond in dataset['Stato fondo stradale']:
        if cond != "":
            count += 1

    return count


def tuple_errore_meteo(dataset):
    count = 0
    for cond in dataset['Stato fondo stradale']:
        if cond == "":
            count += 1

    return count


def tuple_analizzate_traffico(dataset):
    count = 0
    for cond in dataset['Entità del Traffico']:
        if cond != "":
            count += 1

    return count


def tuple_errore_traffico(dataset):
    count = 0
    for cond in dataset['Entità del Traffico']:
        if cond == "":
            count += 1

    return count


def asfalto_moda(dataset):
    freq = {}

    for cond in dataset['Stato fondo stradale']:
        if cond not in freq:
            freq[cond] = 1
        else:
            freq[cond] += 1

    asfalto_freq = freq.items()

    massimaFreq = max(asfalto_freq, key=lambda item: item[1])[1]
    lista_asfalti = []

    for asfalto, frequenza in asfalto_freq:
        if(frequenza == massimaFreq):
            lista_asfalti.append(asfalto)
    # print("Funzione: fasciaeta_moda")
    # print(lista_fasce)
    return lista_asfalti


def tipostrada_moda(dataset):
    freq = {}

    for cond in dataset['Caratteristiche della Strada']:

        if cond not in freq:
            freq[cond] = 1
        else:
            freq[cond] += 1

    tipostrada_freq = freq.items()

    massimaFreq = max(tipostrada_freq, key=lambda item: item[1])[1]
    lista_tipistrada = []

    for tipostrada, frequenza in tipostrada_freq:
        if(frequenza == massimaFreq):
            lista_tipistrada.append(tipostrada)
    # print("Funzione: fasciaeta_moda")
    # print(lista_fasce)
    return lista_tipistrada


def orario_moda(dataset):
    freq = {}

    for cond in dataset['Fascia oraria']:

        if cond not in freq:
            freq[cond] = 1
        else:
            freq[cond] += 1

    tipostrada_freq = freq.items()

    massimaFreq = max(tipostrada_freq, key=lambda item: item[1])[1]
    lista_tipistrada = []

    for tipostrada, frequenza in tipostrada_freq:
        if(frequenza == massimaFreq):
            lista_tipistrada.append(tipostrada)
    # print("Funzione: fasciaeta_moda")
    # print(lista_fasce)
    return lista_tipistrada


def traffico_moda(dataset):
    freq = {}

    for cond in dataset['Entità del Traffico']:

        if cond not in freq:
            freq[cond] = 1
        else:
            freq[cond] += 1

    tipostrada_freq = freq.items()

    massimaFreq = max(tipostrada_freq, key=lambda item: item[1])[1]
    lista_tipistrada = []

    for tipostrada, frequenza in tipostrada_freq:
        if(frequenza == massimaFreq):
            lista_tipistrada.append(tipostrada)
    # print("Funzione: fasciaeta_moda")
    # print(lista_fasce)
    return lista_tipistrada
