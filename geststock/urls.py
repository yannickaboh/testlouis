from django.conf.urls import url, include
from django.contrib import admin
from . import views
from .views import disponible
from .filters import FournisseurFilter
from django_filters.views import FilterView

app_name = 'geststock'

urlpatterns = [

    # Administration
    url(r'^admin/', admin.site.urls),

    # Geststock
    url(r'^accueil/$', views.accueil, name='accueil'),
    url(r'^miss/$', views.miss, name='miss'),
    url(r'^$', views.index, name='index'),
    url(r'^mentions_legales/$', views.mentions_legales, name='mentions_legales'),
    url(r'^contact/$', views.contact, name='contact'),
    url(r'^kit_communication/$', views.kit_communication, name='kit_communication'),
    url(r'^FAQ/$', views.faq, name='faq'),
    url(r'^pharmacie/medicament/$', views.disponible, name='disponible'),

    #url(r'^recherche/$',  search,  name='recherche' ),
    url(r'^login_user/$', views.login_user, name='login_user'),
    url(r'^logout_user/$', views.logout_user, name='logout_user'),
    url(r'^register$', views.PharmacieCreate.as_view(), name='register'),
    url(r'^reset$', views.reset, name='reset'),

    # Mes Tests
    url(r'^teste$', views.teste, name='teste'),
    url(r'^search_garde/$', views.search_garde, name='search_garde'),
    url(r'^itineraire/(?P<pk>\d+)/$', views.itineraire, name='itineraire'),
    url(r'^employe_list/$', views.Employe_list, name='employe_list'),
    url(r'^employe_create/$', views.Employe_create, name='employe_create'),
    url(r'^django/$', views.django, name='django'),
    url(r'^profile/$', views.profile_list, name='profile'),
    
    # Medicament URLS
    url(r'^list_medoc/$', views.list_medoc, name='list_medoc'),
    url(r'^list_mat/$', views.list_mat, name='list_mat'),

    # Add, Update, Delete Medicament URLS
    url(r'^medicament_list/$', views.MedicamentList.as_view(), name='medicament_list'),
    url(r'^medicament_create/$', views.MedicamentCreate.as_view(), name='medicament_create'),
    url(r'^medicament_update/(?P<pk>\d+)/$', views.MedicamentUpdate.as_view(), name='medicament_update'),
    url(r'^medicament_delete/(?P<pk>\d+)/$', views.MedicamentDelete.as_view(), name='medicament_delete'),

    # Add, Update, Delete Depot URLS
    url(r'^depot_list/$', views.DepotList.as_view(), name='depot_list'),
    url(r'^depot_create/$', views.DepotCreate.as_view(), name='depot_create'),
    url(r'^depot_update/(?P<pk>\d+)/$', views.DepotUpdate.as_view(), name='depot_update'),
    url(r'^depot_delete/(?P<pk>\d+)/$', views.DepotDelete.as_view(), name='depot_delete'),

    # Add, Update, Delete FicheStock URLS
    url(r'^fichestock_list/$', views.FicheStockList.as_view(), name='fichestock_list'),
    url(r'^fichestock_create/$', views.FicheStockCreate.as_view(), name='fichestock_create'),
    url(r'^fichestock_update/(?P<pk>\d+)/$', views.FicheStockUpdate.as_view(), name='fichestock_update'),
    url(r'^fichestock_delete/(?P<pk>\d+)/$', views.FicheStockDelete.as_view(), name='fichestock_delete'),

    # Add, Update, Delete Ordonnance URLS
    url(r'^ordonnance_list/$', views.OrdonnanceList.as_view(), name='ordonnance_list'),
    url(r'^ordonnance_create/$', views.OrdonnanceCreate.as_view(), name='ordonnance_create'),
    #url(r'^ordonnance_detail/(?P<pk>\d+)/$', views.OrdonnanceDetail.as_view(), name='ordonnance_detail'),
    url(r'^ordonnance_update/(?P<pk>\d+)/$', views.OrdonnanceUpdate.as_view(), name='ordonnance_update'),
    url(r'^ordonnance_delete/(?P<pk>\d+)/$', views.OrdonnanceDelete.as_view(), name='ordonnance_delete'),

    # Add, Update, Delete Fournisseur URLS
    url(r'^fournisseur_list/$', views.FournisseurList.as_view(), name='fournisseur_list'),
    url(r'^fournisseur_create/$', views.FournisseurCreate.as_view(), name='fournisseur_create'),
    url(r'^fournisseur_update/(?P<pk>\d+)/$', views.FournisseurUpdate.as_view(), name='fournisseur_update'),
    url(r'^fournisseur_delete/(?P<pk>\d+)/$', views.FournisseurDelete.as_view(), name='fournisseur_delete'),
    url(r'^fournisseur_search/$', FilterView.as_view(filterset_class=FournisseurFilter, 
        template_name='geststock/fournisseur_search.html'), name='fournisseur_search'),


    # Add, Update, Delete Medoc URLS
    url(r'^medoc_list/$', views.medoc_list, name='medoc_list'),
    url(r'^medoc_create/$', views.medoc_create, name='medoc_create'),
    url(r'^medoc_update/(?P<pk>\d+)/$', views.medoc_update, name='medoc_update'),
    url(r'^medoc_delete/(?P<pk>\d+)/$', views.medoc_delete, name='medoc_delete'),
]