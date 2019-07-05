from django.urls import path

from . import views


from .forms import ContactForm2, ContactForm1


urlpatterns = [
    path('home', views.home, name='home'),
    path('selezionaColonne', views.selezionaColonne, name='selezionaColonne'),
    path('dashboard', views.dashboard, name='analisi-dashboard'),
    path('dashboard-data', views.dashboard_data, name='dashboard-data'),
    path('dashboard-conducenti', views.dashboard_conducenti, name='dashboard-conducenti'),
    path('ajax/dashboard-data', views.dashboard_data_ajax),
    path('ajax/dashboard-conducenti', views.dashboard_conducenti_ajax)
]
