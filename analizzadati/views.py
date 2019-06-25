from django.shortcuts import render
import csv
import io
import os
from django.http import HttpResponse, HttpResponseRedirect
from django.core.files.storage import FileSystemStorage

from .forms import ContactForm2, ContactForm1
from incidenticosenza import settings
from formtools.wizard.views import SessionWizardView

<<<<<<< HEAD
from .uploadfileform import CheckBox, MyForm

=======
>>>>>>> parent of 3d5f281... Lavoro di Lunedì 24

def home(request):

    if request.method == 'GET':
        print("call")

        form2 = ContactForm2()
        form1 = ContactForm1()
        w = ContactWizard()

      #  print(w.form.forms)

        # w.done()

       # return render(request, "analizzadati/home2.html", {'form1': form1, 'form2': form2, 'wizard': w})
        return render(request, "analizzadati/home3.html", {'wizard': w})
    # if request.method == 'POST' and request.FILES['myfile']:
    #     myfile = request.FILES['myfile']

    #     myfile.seek(0)
    #     data = csv.DictReader(io.StringIO(myfile.read().decode('ISO-8859-1')), delimiter=';')

    #     request.session['data'] = data

    #     return HttpResponse("ciao")

    # if request.method=='POST':


<<<<<<< HEAD
def selezionaColonne(request):

    if request.method == 'GET':

        #data = request.session['data']
        # count = 0
        # for d in data:
        #  count+=1

        n = 10
        #form = CheckBox(2)
        form = MyForm()
       # print(form)

        print("CREAZIONE FORM2")
        # print(form)
        # print(form.is_valid())
        print("VALIDO")
        return render(request, "analizzadati/selezionaColonne.html", {"form": form})
    else:

        # f = CheckBox(request.POST)
        # print("###########")
        # # print(request.POST.items())
        # #prova = request.POST['CheckBoxk']
        # # print()

        # if(f.is_valid()):
        #     print("FORM VALIDO")
        #     print(f.cleaned_data)

        # diz = f.get_f()

        # for key, val in diz:
        #     print(key)
        #     print(val)
        # print("Dizionario")
        # # print(diz["ProvaNumero_1"])

        # print(f.is_bound)
        return HttpResponse("ciao")


=======
>>>>>>> parent of 3d5f281... Lavoro di Lunedì 24
class ContactWizard(SessionWizardView):
    template_name = "analizzadati/home3.html"
    #form_list = []

    file_storage = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'photos'))

    # def setForm(form_list):
    #         self.form_list= form_list
    condition_dict = {'1': ""}

    def done(self, form_list, **kwargs):

        return HttpResponseRedirect("OKKKK")
