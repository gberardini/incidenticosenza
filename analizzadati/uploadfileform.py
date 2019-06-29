from django import forms
from collections import OrderedDict


class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()


class CheckBox(forms.Form):

    # your_name = forms.CharField(label='Your name', max_length=100)
    # self.fiels
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     # for key, n in kwargs:

    #     try:
    #         n = int(args[0])
    #     except:
    #         return
    #     print("CREAZIONE FORM1")
    #     print(n)
    #     for i in range(0, n):
    #         field_name = 'provaNumero_%s' % (i,)
    #         self.fields[field_name] = forms.BooleanField(required=False, widget=forms.CheckboxInput(

    #             attrs={
    #                 "class": "form-check-input",

    #             }))
    #     print("Creato: ", self.fields)
    #     for x in self.fields:
    #         print(x)

    choices = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple())

    # print("OKKKKKKKKKKKKKKKK")

   # c = forms.BooleanField(label="Ciao", required=False,

    # def clean(self):
    #     cleaned_data = super().clean()
    #     print("FIELDS")
    #     print(self.fields)
    #     #print(self.fields[' provaNumero_0'])

    #     for field_name in self.fields:
    #         print("nel for: ", field_name)
    #         cleaned_data[field_name] = self.fields[field_name]

    #     print("da clean()")
    #     print(cleaned_data)
    #     return cleaned_data

    # ritorna lista campi
    def get_field(self):
        lista = []
        for f in self.fields:
            lista.append(f)
        return lista


class Box():

    #fields = []

    def __init__(self, fields):

        # lista = args[0]

        # # print("\n \n \n ")
        # # print(args)

        # for field in lista:
        #     # print("append campo", field)
        #     self.fields.append(field)

        self.fields = fields

        print('CAMPI CREATI \n')
        print(self.fields)


class DataSet():

    # fields = []
    # dataset = []

    def __init__(self):
        pass

    # costruisci su un dizionario OrderDict
    def __init__(self, diz={}, header=[]):
        self.fields = []
        self.dataset = {}

        if not header:
            return

        for f in header:
            self.fields.append(f)
            if f not in self.dataset:
                self.dataset[f] = []

        for od in diz:
            for f in self.fields:
                self.dataset[f].append(od[f])
                lung = len(self.dataset[f])

        print(self.dataset)

    def data_numincidenti(self, dati):

        # estrai date senza ripetizioni
        lista_date = list(OrderedDict.fromkeys(dati['Data']))
        diz = {"Data": lista_date,
               "Num": []}
        print("##########")
        print(dati)

        for data in lista_date:
            diz["Num"].append(dati['Data'].count(data))

        print(diz)
        return diz


class MyForm(forms.Form):

    my_object = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        choices=["ciao", "ciao2"]
    )
