from django.urls import path

from . import views


from .forms import ContactForm2, ContactForm1


urlpatterns = [
    path('home', views.home, name='home'),
    path('selezionaColonne', views.selezionaColonne, name='selezionaColonne'),
    path('dashboard', views.dashboard, name='analisi-dashboard'),
    path('dashboard-data', views.dashboard_data, name='dashboard-data'),
    path('dashboard-conducenti', views.dashboard_conducenti, name='dashboard-conducenti'),
    path('dashboard-meteo', views.dashboard_meteo, name='dashboard-meteo'),
    path('dashboard-traffico', views.dashboard_traffico, name='dashboard-traffico'),
    path('ajax/dashboard-data', views.dashboard_data_ajax),
    path('ajax/dashboard-conducenti', views.dashboard_conducenti_ajax),
    path('ajax/dashboard-meteo', views.dashboard_meteo_ajax),
    path('ajax/dashboard-traffico', views.dashboard_traffico_ajax)

]
