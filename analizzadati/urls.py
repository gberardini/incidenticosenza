from django.urls import path

from . import views


from .forms import ContactForm2, ContactForm1

from .views import ContactWizard


urlpatterns = [
    path('home', views.home, name='home'),
    path('prova', ContactWizard.as_view([ContactForm1, ContactForm2], condition_dict={'1': True}), name='prova')

]
