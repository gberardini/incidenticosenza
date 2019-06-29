from django import forms
from django.core.files.storage import FileSystemStorage


class ContactForm1(forms.Form):
    subject = forms.BooleanField()


class ContactForm2(forms.Form):
    subject = forms.CharField(

        widget=forms.TextInput(
            attrs={

                "class": "form-control",
                "type": "text",
                "name": "first_name",
                "placeholder": "ex: Mike"

            }

        ))
