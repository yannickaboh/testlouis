from django.shortcuts import get_object_or_404, render, redirect, render_to_response
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.views import generic
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.http import JsonResponse
from django.http import HttpResponse
from django.views.generic import TemplateView,ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView


from django.core.urlresolvers import reverse_lazy


from django.http import HttpResponseRedirect
from .models import Gprovince, Medicament, Fournisseur, Commande, FicheStock, Message,  Depot,Pharmacie, Pays, Province, Profile, Ordonnance, Photo, Employe
from django.forms import ModelForm
from .forms import MedicamentForm, FournisseurForm, FicheStockForm, ProfileForm, DepotForm, PharmacieForm, UserForm, OrdonnanceForm, PhotoForm, EmployeForm, MedocForm
from .serializers import PaysSerializer, ProvinceSerializer
import re
from django.db.models import Q
from django.template.loader import render_to_string
from .filters import FournisseurFilter, PharmacieFilter, MedicamentFilter, GprovinceFilter
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.
# Module de recherche

############################################################################

def profile_list(request):
    profiles = Profile.objects.all()
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm()
    return render(request, 'geststock/profile_list.html', {'form': form, 'profiles': profiles})

def search(request):
	fournisseur_list = Fournisseur.objects.all()
	fournisseur_filter = FournisseurFilter(request.GET, queryset=fournisseur_list)
	return render(request, 'geststock/fournisseur_search.html', {'filter': fournisseur_filter})

# Medoc CRUD
def medoc_list(request):
    medocs = Medicament.objects.all()
    page = request.GET.get('page', 1)
    paginator = Paginator(medocs, 10)
    try:
    	medicaments = paginator.page(page)
    except PageNotAnInteger:
    	medicaments = page(1)
    except:
    	medicaments = paginator.page(paginator.num_pages)
    	
    return render(request, 'geststock/medoc_list.html', {'medocs': medocs})


def save_medoc_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            medocs = Medicament.objects.all()
            data['html_medoc_list'] = render_to_string('geststock/partial/partial_medoc_list.html', {
                'medocs': medocs
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def medoc_create(request):
    if request.method == 'POST':
        form = MedocForm(request.POST)
    else:
        form = MedocForm()
    return save_medoc_form(request, form, 'geststock/partial/partial_medoc_create.html')


def medoc_update(request, pk):
    medoc = get_object_or_404(Medicament, pk=pk)
    if request.method == 'POST':
        form = MedocForm(request.POST, instance=medoc)
    else:
        form = MedocForm(instance=medoc)
    return save_medoc_form(request, form, 'geststock/partial/partial_medoc_update.html')


def medoc_delete(request, pk):
    medoc = get_object_or_404(Medicament, pk=pk)
    data = dict()
    if request.method == 'POST':
        medoc.delete()
        data['form_is_valid'] = True
        medocs = medoc.objects.all()
        data['html_medoc_list'] = render_to_string('geststock/partial/partial_medoc_list.html', {
            'medocs': medocs
        })
    else:
        context = {'medoc': medoc}
        data['html_form'] = render_to_string('geststock/partial/partial_medoc_delete.html', context, request=request)
    return JsonResponse(data)

######################################################################################################################""




def django(request):
	employes = Employe.objects.all()
	return render(request, 'geststock/django.html', {'employes' : employes })


def Employe_list(request):
	employes = Employe.objects.all()
	return render(request, 'geststock/Employe_list.html', {'employes' : employes })

def save_employe_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            employes = Employe.objects.all()
            data['html_employe_list'] = render_to_string('geststock/Employe_list.html', {
                'employes': employes
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def Employe_create(request):
    if request.method == 'POST':
        form = EmployeForm(request.POST)
    else:
        form = EmployeForm()
    return save_employe_form(request, form, 'geststock/includes/partial_employe_create.html')





# Serialization
class PaysList(APIView):

	def get(self, request):
		pays = Pays.objects.all()
		serializer = PaysSerializer(pays, many=True)
		return Response(serializer.data)

	def post(self):
		pass


class ProvinceList(APIView):

	def get(self, request):
		provinces = Province.objects.all()
		serializer = PaysSerializer(provinces, many=True)
		return Response(serializer.data)

	def post(self):
		pass




def index(request):
	#p_list = Pharmacie.objects.all()
	#p_filter = PharmacieFilter(request.GET, queryset=p_list)
	p_list = Gprovince.objects.all()
	p_filter = GprovinceFilter(request.GET, queryset=p_list)
	return render(request, 'geststock/index.html', {'filter':p_filter})

def miss(request):
	return render(request, 'geststock/miss.html', {})

def search_garde(request):
	p_list = Pharmacie.objects.all()
	p_filter = PharmacieFilter(request.GET, queryset=p_list)
	return render(request, 'geststock/search_garde.html', {'filter':p_filter})

def mentions_legales(request):
	return render(request, 'geststock/mentions.html', {})


def faq(request):
	return render(request, 'geststock/faq.html', {})

def contact(request):
	return render(request, 'geststock/contact.html', {})

def kit_communication(request):
	return render(request, 'geststock/kit_communication.html', {})

def itineraire(request):
	return render(request, 'geststock/itineraire.html', {})



def disponible(request):
	pharmacies = Pharmacie.objects.all()
	query = request.GET.get("q")
	if query:
		medicaments = Medicament.objects.filter(Q(nom_generique__icontains=query))
		p = Medicament.objects.filter(Q(nom_generique__icontains=query))
		m = p.count()

		h = Pharmacie.objects.filter(medicament__nom_generique__icontains=query)
		k = h.all()
		t = h.count()
		return render(request, 'geststock/disponibilite.html', {'h' : h, 't' : t,
			'pharmacies' : pharmacies, 'medicaments' : medicaments, 
			'm' : m, 'p' : p, 'k': k })
	else:
		return render(request, 'geststock/disponibilite.html', {'pharmacies' : pharmacies, })


def login_user(request):
	if request.method == "POST":
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username, password=password)
		if user is not None:
			if user.is_active:
				login(request, user)
				return redirect('geststock:accueil')
			else:
				return render(request, 'geststock/login.html', {'error_message': 'Votre compte a été désactivé'})
		else:
			return render(request, 'geststock/login.html', {'error_message': 'Paramètres Invalides'})
	return render(request, 'geststock/login.html')

def logout_user(request):
    logout(request)
    form = UserForm(request.POST or None)
    context = {
        "form": form,
    }
    return redirect('geststock:login_user')

def register(request):
	return render(request, 'geststock/register.html')

def reset(request):
	return render(request, 'geststock/reset.html')

def teste(request):
	return render(request, 'geststock/teste.html')


def accueil(request):
	profiles = Profile.objects.filter(user=request.user)
	m = Medicament.objects.filter(genre__startswith='Medi')
	q = Medicament.objects.filter(genre__startswith='Mat')
	medicaments = m.count()
	medicamentss = q.count()
	fournisseurs = Fournisseur.objects.count()
	commandes = Commande.objects.count()
	messages = Message.objects.count()
	depots = Depot.objects.count()
	return render(request, 'geststock/pages/accueil.html', {
		'medicaments' : medicaments,
		'medicamentss' : medicamentss,
		'fournisseurs' : fournisseurs,
		'commandes' : commandes,
		'messages' : messages,
		'profiles' : profiles,
		'depots' : depots		})

def list_medoc(request):
	m = Medicament.objects.filter(genre__startswith='Medi')
	q = Medicament.objects.filter(genre__startswith='Mat')
	medocs = m.all()
	medicaments = m.count()
	medicamentss = q.count()
	fournisseurs = Fournisseur.objects.count()
	commandes = Commande.objects.count()
	messages = Message.objects.count()
	return render(request, 'geststock/pages/tables/liste_medoc.html', {
		'medicaments' : medicaments,
		'medicamentss' : medicamentss,
		'medocs' : medocs,
		'fournisseurs' : fournisseurs,
		'commandes' : commandes,
		'messages' : messages,
		})

def list_mat(request):
	m = Medicament.objects.filter(genre__startswith='Medi')
	q = Medicament.objects.filter(genre__startswith='Mat')
	medocs = q.all()
	medicaments = m.count()
	medicamentss = q.count()
	fournisseurs = Fournisseur.objects.count()
	commandes = Commande.objects.count()
	messages = Message.objects.count()
	return render(request, 'geststock/pages/tables/liste_medoc.html', {
		'medicaments' : medicaments,
		'medicamentss' : medicamentss,
		'medocs' : medocs,
		'fournisseurs' : fournisseurs,
		'commandes' : commandes,
		'messages' : messages,
		})


# Medicament CRUD
class MedicamentList(ListView):
	model = Medicament

class MedicamentCreate(CreateView):
	model = Medicament
	form_class = MedicamentForm
	success_url = reverse_lazy('geststock:medicament_list')

class MedicamentUpdate(UpdateView):
	model = Medicament
	form_class = MedicamentForm
	success_url = reverse_lazy('geststock:medicament_list')

class MedicamentDelete(DeleteView):
	model = Medicament
	success_url = reverse_lazy('geststock:medicament_list')

# Depot CRUD
class DepotList(ListView):
	model = Depot

class DepotCreate(CreateView):
	model = Depot
	form_class = DepotForm
	success_url = reverse_lazy('geststock:depot_list')

class DepotUpdate(UpdateView):
	model = Depot
	form_class = DepotForm
	success_url = reverse_lazy('geststock:depot_list')

class DepotDelete(DeleteView):
	model = Depot
	success_url = reverse_lazy('geststock:depot_list')


# Fiche de Stock CRUD
class FicheStockList(ListView):
	model = FicheStock

class FicheStockCreate(CreateView):
	model = FicheStock
	form_class = FicheStockForm
	success_url = reverse_lazy('geststock:fichestock_list')

class FicheStockUpdate(UpdateView):
	model = FicheStock
	form_class = FicheStockForm
	success_url = reverse_lazy('geststock:fichestock_list')

class FicheStockDelete(DeleteView):
	model = FicheStock
	success_url = reverse_lazy('geststock:fichestock_list')




	

# Ordonnance CRUD
class OrdonnanceList(ListView):
	model = Ordonnance

class OrdonnanceCreate(CreateView):
	model = Ordonnance
	form_class = OrdonnanceForm
	success_url = reverse_lazy('geststock:ordonnance_list')

#class OrdonnanceDetail(request):
	#model = Ordonnance
	#success_url = reverse_lazy('geststock:ordonnance_list')

class OrdonnanceUpdate(UpdateView):
	model = Ordonnance
	form_class = OrdonnanceForm
	success_url = reverse_lazy('geststock:ordonnance_list')

class OrdonnanceDelete(DeleteView):
	model = Ordonnance
	success_url = reverse_lazy('geststock:ordonnance_list')


# Fournisseur CRUD
class FournisseurList(ListView):
	model = Fournisseur

class FournisseurCreate(CreateView):
	model = Fournisseur
	form_class = FournisseurForm
	success_url = reverse_lazy('geststock:fournisseur_list')

class FournisseurUpdate(UpdateView):
	model = Fournisseur
	form_class = FournisseurForm
	success_url = reverse_lazy('geststock:fournisseur_list')

class FournisseurDelete(DeleteView):
	model = Fournisseur
	success_url = reverse_lazy('geststock:fournisseur_list')


# Pharmacie Inscription
class PharmacieCreate(CreateView):
	model = Pharmacie
	form_class = PharmacieForm
	success_url = reverse_lazy('geststock:index')



