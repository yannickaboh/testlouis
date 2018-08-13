from django.contrib.auth.models import User
import django_filters
from .models import Fournisseur, Pharmacie, Medicament, Gprovince
from django import forms


class FournisseurFilter(django_filters.FilterSet):
	nom = django_filters.CharFilter(lookup_expr='icontains')


	class Meta:
		model = Fournisseur
		fields = ['nom', 'site_web', 'email', 'boite_postale', 'telephone', 'ville', 'quartier', ]


class GprovinceFilter(django_filters.FilterSet):
	nom = django_filters.CharFilter(lookup_expr='icontains')


	class Meta:
		model = Gprovince
		fields = ['nom', 'latitude', 'longitude',  ]


class PharmacieFilter(django_filters.FilterSet):
	ville__libelle = django_filters.CharFilter(lookup_expr='icontains')
	garde = django_filters.BooleanFilter(widget=forms.CheckboxInput, )


	class Meta:
		model = Pharmacie
		fields = ['ville__libelle', 'garde', ]


class MedicamentFilter(django_filters.FilterSet):
	nom_generique = django_filters.CharFilter(lookup_expr='icontains')


	class Meta:
		model = Pharmacie
		fields = ['nom_generique', ]





