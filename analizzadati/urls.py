from django.urls import path

from . import views


from .forms import ContactForm2, ContactForm1




urlpatterns = [
    path('home', views.home, name='home'),
    path('selezionaColonne', views.selezionaColonne , name='selezionaColonne')

]
