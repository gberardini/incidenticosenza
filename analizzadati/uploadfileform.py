from django import forms


class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()
<<<<<<< HEAD


class CheckBox(forms.Form):
    # your_name = forms.CharField(label='Your name', max_length=100)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # for key, n in kwargs:

        try:
            n = int(args[0])
        except:
            return
        print("CREAZIONE FORM1")
        print(n)
        for i in range(0, n):
            field_name = 'provaNumero_%s' % (i,)
            self.fields[field_name] = forms.BooleanField(required=False, widget=forms.CheckboxSelectMultiple(



                attrs={
                    "class": "form-check-input",


                }))

        # print("OKKKKKKKKKKKKKKKK")

   # c = forms.BooleanField(label="Ciao", required=False,

    def clean(self):
        cleaned_data = super().clean()

        print(cleaned_data)
        return cleaned_data

    def get_f(self):
        return self.fields


class MyForm(forms.Form):

    my_object = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        choices=["ciao", "ciao2"]
    )
=======
>>>>>>> parent of 3d5f281... Lavoro di Lunedì 24
