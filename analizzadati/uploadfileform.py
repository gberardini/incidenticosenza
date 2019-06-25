from django import forms


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

    fields = []

    def __init__(self, *args):

        lista = args[0]

        # print("\n \n \n ")
        # print(args)

        for field in lista:
            # print("append campo", field)
            self.fields.append(field)


class MyForm(forms.Form):

    my_object = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        choices=["ciao", "ciao2"]
    )
