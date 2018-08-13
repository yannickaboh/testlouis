from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from . import models
from .models import Profile
from django.conf import settings

# Register your models here.

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = True
    verbose_name_plural = 'Profil'
    fk_name = 'user'

class CustomerUserAdmin(UserAdmin):
    inlines = (ProfileInline, )

    def get_telephone(self, instance):
        return instance.profil.telephone
    get_telephone.short_description = 'Telephone'

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomerUserAdmin, self).get_inline_instances(request, obj)

class OrdonnanceAdmin(admin.ModelAdmin):
    list_display   = ('telephone', 'infos', 'ordonance', 'quartier', 'created_at', 'visibilite', 'envoye_par')
    list_filter    = ('telephone', 'infos', 'ordonance', 'quartier', 'created_at', 'visibilite', 'envoye_par')
    date_hierarchy = 'created_at'
    ordering       = ('created_at', 'visibilite')
    search_fields  = ('telephone', 'infos', 'ordonance', 'quartier', 'created_at', 'visibilite', 'envoye_par')

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'envoye_par', None) is None:
            obj.envoye_par = request.user
        obj.save()


class FamilleAdmin(admin.ModelAdmin):
    list_display   = ('libelle', 'code', 'description', 'created_at', 'ajoute_par')
    list_filter    = ('libelle', 'code', 'description', 'created_at', )
    date_hierarchy = 'updated_at'
    ordering       = ('created_at', )
    search_fields  = ('libelle', 'code', 'description', 'created_at', 'ajoute_par', 'updated_at')

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'ajoute_par', None) is None:
            obj.envoye_par = request.user
        obj.save()

class DepotAdmin(admin.ModelAdmin):
    list_display   = ('libelle', 'code', 'date_ajout', 'ajoute_par',)
    list_filter    = ('libelle', 'code', 'date_ajout', 'ajoute_par', )
    date_hierarchy = 'date_ajout'
    ordering       = ('date_ajout', )
    search_fields  = ('libelle', 'code', 'date_ajout', 'ajoute_par', )

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'ajoute_par', None) is None:
            obj.envoye_par = request.user
        obj.save()


class MedicamentAdmin(admin.ModelAdmin):
    list_display   = ('genre' ,'famille', 'nom_generique', 'code', 'prix_achat', 'prix_vente', 'created_at', 'ajoute_par')
    list_filter    = ('genre' ,'famille', 'nom_generique', 'code', 'prix_achat', 'prix_vente', 'created_at', 'ajoute_par')
    date_hierarchy = 'updated_at'
    ordering       = ('created_at', )
    search_fields  = ('genre' ,'famille', 'nom_generique', 'code', 'prix_achat', 'prix_vente', 'created_at', 'ajoute_par')

    #def save_model(self, request, obj, form, change):
        #if getattr(obj, 'ajoute_par', None) is None:
            #obj.ajoute_par = request.user
        #obj.save()

class FournisseurAdmin(admin.ModelAdmin):
    list_display   = ('nom', 'site_web', 'email', 'boite_postale', 'telephone', 'created_at', 'ajoute_par')
    list_filter    = ('nom', 'site_web', 'email', 'boite_postale', 'telephone', 'created_at', 'ajoute_par')
    date_hierarchy = 'updated_at'
    ordering       = ('created_at', )
    search_fields  = ('nom', 'site_web', 'email', 'boite_postale', 'telephone', 'created_at', 'ajoute_par')

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'ajoute_par', None) is None:
            obj.ajoute_par = request.user
        obj.save()


class FicheStockAdmin(admin.ModelAdmin):
    list_display   = ('dci', 'forme', 'cmm', 'dosage', 'stockMin', 'stockMax', 'conditionnement', 'entree', 'sortie', 'stock')
    list_filter    = ('dci', 'forme', 'cmm', 'dosage', 'stockMin', 'stockMax', 'conditionnement', 'entree', 'sortie', 'stock')
    date_hierarchy = 'date_ajout'
    ordering       = ('date_ajout', )
    search_fields  = ('dci', 'forme', 'cmm', 'dosage', 'stockMin', 'stockMax', 'conditionnement', 'entree', 'sortie', 'stock')

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'ajoute_par', None) is None:
            obj.ajoute_par = request.user
        obj.save()

    def set_stock(self, request, obj):
        if getattr(obj, 'stock', None) is None:
            obj.stock = request.entree - request.sortie
        obj.save()



class StockAdmin(admin.ModelAdmin):
    list_display   = ('libelle', 'stock_min', 'stock_max', 'created_at', 'ajoute_par')
    list_filter    = ('stock_min', 'stock_max', 'created_at', 'ajoute_par')
    date_hierarchy = 'updated_at'
    ordering       = ('created_at', )
    search_fields  = ('libelle', 'stock_min', 'stock_max', 'created_at', 'ajoute_par')

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'ajoute_par', None) is None:
            obj.ajoute_par = request.user
        obj.save()

class StockMedicamentAdmin(admin.ModelAdmin):
    list_display   = ('qte_stock', 'alerte_qte', 'created_at', 'ajoute_par')
    list_filter    = ('qte_stock', 'alerte_qte', 'created_at', 'ajoute_par')
    date_hierarchy = 'updated_at'
    ordering       = ('created_at', )
    search_fields  = ('qte_stock', 'alerte_qte', 'created_at', 'ajoute_par')

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'ajoute_par', None) is None:
            obj.ajoute_par = request.user
        obj.save()



class PharmacieAdmin(admin.ModelAdmin):
    list_display   = ('nom' ,'libelle', 'horaires', 'garde', 'agrement', 'nom_gerant', 'site_web', 'email', 'boite_postale', 'telephone', 'created_at', 'ajoute_par')
    list_filter    = ('nom' ,'libelle', 'horaires', 'garde', 'agrement', 'nom_gerant', 'site_web', 'email', 'boite_postale', 'telephone', 'created_at', 'ajoute_par')
    date_hierarchy = 'updated_at'
    ordering       = ('created_at', )
    search_fields  = ('nom' ,'libelle', 'horaires', 'garde', 'agrement', 'nom_gerant', 'site_web', 'email', 'boite_postale', 'telephone', 'created_at', 'ajoute_par')

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'ajoute_par', None) is None:
            obj.ajoute_par = request.user
        obj.save()

    fieldsets = (
        (None, {
            'fields': ('nom' ,'libelle', 'horaires', 'garde', 'agrement', 'nom_gerant', 
                'site_web', 'email', 'boite_postale', 
                'telephone', 'ville', 'quartier', 'longitude', 'latitude',)
        }),
    )

    class Media:
        if hasattr(settings, 'GOOGLE_MAPS_API_KEY') and settings.GOOGLE_MAPS_API_KEY:
            css = {
                'all': ('geststock/css/admin/location_picker.css',),
            }
            js = (
                'https://maps.googleapis.com/maps/api/js?key={}'.format(settings.GOOGLE_MAPS_API_KEY),
                'geststock/js/admin/location_picker.js',
            )

class CommandeAdmin(admin.ModelAdmin):
    list_display   = ('num_commande', 'created_at', 'ajoute_par')
    list_filter    = ('num_commande', 'created_at', 'ajoute_par')
    date_hierarchy = 'updated_at'
    ordering       = ('created_at', )
    search_fields  = ('num_commande', 'created_at', 'ajoute_par')

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'ajoute_par', None) is None:
            obj.ajoute_par = request.user
        obj.save()


class LigneCommandeAdmin(admin.ModelAdmin):
    list_display   = ('qte_commande', 'created_at', 'ajoute_par')
    list_filter    = ('qte_commande', 'created_at', 'ajoute_par')
    date_hierarchy = 'updated_at'
    ordering       = ('created_at', )
    search_fields  = ('medicament', 'commande','qte_commande', 'created_at', 'ajoute_par')

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'ajoute_par', None) is None:
            obj.ajoute_par = request.user
        obj.save()
        

class VenteAdmin(admin.ModelAdmin):
    list_display   = ('created_at', 'ajoute_par')
    list_filter    = ('created_at', 'ajoute_par')
    date_hierarchy = 'updated_at'
    ordering       = ('created_at', )
    search_fields  = ('created_at', 'ajoute_par')

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'ajoute_par', None) is None:
            obj.ajoute_par = request.user
        obj.save()

class VenteMedicamentAdmin(admin.ModelAdmin):
    list_display   = ('medicament', 'vente', 'qte_vendu', 'created_at', 'ajoute_par')
    list_filter    = ('medicament', 'vente', 'qte_vendu', 'created_at', 'ajoute_par')
    date_hierarchy = 'updated_at'
    ordering       = ('created_at', )
    search_fields  = ('medicament', 'vente', 'qte_vendu', 'created_at', 'ajoute_par')

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'ajoute_par', None) is None:
            obj.ajoute_par = request.user
        obj.save()


class PaysAdmin(admin.ModelAdmin):
    list_display   = ('libelle', 'code', 'longitude', 'latitude', 'created_at', 'ajoute_par')
    list_filter    = ('libelle', 'code', 'longitude', 'latitude', 'created_at',)
    date_hierarchy = 'updated_at'
    ordering       = ('created_at', )
    search_fields  = ('libelle', 'code', 'longitude', 'latitude', 'created_at')

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'ajoute_par', None) is None:
            obj.ajoute_par = request.user
        obj.save()

    fieldsets = (
        (None, {
            'fields': ('libelle', 'code', 'longitude', 'latitude',)
        }),
    )

    class Media:
        if hasattr(settings, 'GOOGLE_MAPS_API_KEY') and settings.GOOGLE_MAPS_API_KEY:
            css = {
                'all': ('geststock/css/admin/location_picker.css',),
            }
            js = (
                'https://maps.googleapis.com/maps/api/js?key={}'.format(settings.GOOGLE_MAPS_API_KEY),
                'geststock/js/admin/location_picker.js',
            )


class ProvinceAdmin(admin.ModelAdmin):
    list_display   = ('libelle', 'code', 'longitude', 'latitude', 'created_at', 'ajoute_par')
    list_filter    = ('libelle', 'code', 'longitude', 'latitude', 'created_at',)
    date_hierarchy = 'updated_at'
    ordering       = ('created_at', )
    search_fields  = ('libelle', 'code', 'longitude', 'latitude', 'created_at')

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'ajoute_par', None) is None:
            obj.ajoute_par = request.user
        obj.save()

class VilleAdmin(admin.ModelAdmin):
    list_display   = ('libelle', 'code_ville', 'longitude', 'latitude', 'created_at', 'ajoute_par')
    list_filter    = ('libelle', 'code_ville', 'longitude', 'latitude', 'created_at',)
    date_hierarchy = 'updated_at'
    ordering       = ('created_at', )
    search_fields  = ('libelle', 'code_ville', 'longitude', 'latitude', 'created_at')

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'ajoute_par', None) is None:
            obj.ajoute_par = request.user
        obj.save()

    fieldsets = (
        (None, {
            'fields': ('libelle', 'code_ville', 'longitude', 'latitude',)
        }),
    )

    class Media:
        if hasattr(settings, 'GOOGLE_MAPS_API_KEY') and settings.GOOGLE_MAPS_API_KEY:
            css = {
                'all': ('geststock/css/admin/location_picker.css',),
            }
            js = (
                'https://maps.googleapis.com/maps/api/js?key={}'.format(settings.GOOGLE_MAPS_API_KEY),
                'geststock/js/admin/location_picker.js',
            )

class DepartementAdmin(admin.ModelAdmin):
    list_display   = ('libelle', 'code', 'longitude', 'latitude', 'created_at', 'ajoute_par')
    list_filter    = ('libelle', 'code', 'longitude', 'latitude', 'created_at',)
    date_hierarchy = 'updated_at'
    ordering       = ('created_at', )
    search_fields  = ('libelle', 'code', 'longitude', 'latitude', 'created_at')

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'ajoute_par', None) is None:
            obj.ajoute_par = request.user
        obj.save()

class CommuneAdmin(admin.ModelAdmin):
    list_display   = ('libelle', 'code', 'longitude', 'latitude', 'created_at', 'ajoute_par')
    list_filter    = ('libelle', 'code', 'longitude', 'latitude', 'created_at',)
    date_hierarchy = 'updated_at'
    ordering       = ('created_at', )
    search_fields  = ('libelle', 'code', 'longitude', 'latitude', 'created_at')

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'ajoute_par', None) is None:
            obj.ajoute_par = request.user
        obj.save()

class GprovinceAdmin(admin.ModelAdmin):
    list_display   = ('nom', 'longitude', 'latitude',)
    list_filter    = ('nom', 'longitude', 'latitude',)

    fieldsets = (
        (None, {
            'fields': ('nom', 'longitude', 'latitude',)
        }),
    )

    class Media:
        if hasattr(settings, 'GOOGLE_MAPS_API_KEY') and settings.GOOGLE_MAPS_API_KEY:
            css = {
                'all': ('geststock/css/admin/location_picker.css',),
            }
            js = (
                'https://maps.googleapis.com/maps/api/js?key={}'.format(settings.GOOGLE_MAPS_API_KEY),
                'geststock/js/admin/location_picker.js',
            )


class QuartierAdmin(admin.ModelAdmin):
    list_display   = ('libelle', 'code_quartier', 'longitude', 'latitude', 'created_at', 'ajoute_par')
    list_filter    = ('libelle', 'code_quartier', 'longitude', 'latitude', 'created_at',)
    date_hierarchy = 'updated_at'
    ordering       = ('created_at', )
    search_fields  = ('libelle', 'code_quartier', 'longitude', 'latitude', 'created_at')

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'ajoute_par', None) is None:
            obj.ajoute_par = request.user
        obj.save()

    fieldsets = (
        (None, {
            'fields': ('libelle', 'code_quartier', 'longitude', 'latitude',)
        }),
    )

    class Media:
        if hasattr(settings, 'GOOGLE_MAPS_API_KEY') and settings.GOOGLE_MAPS_API_KEY:
            css = {
                'all': ('geststock/css/admin/location_picker.css',),
            }
            js = (
                'https://maps.googleapis.com/maps/api/js?key={}'.format(settings.GOOGLE_MAPS_API_KEY),
                'geststock/js/admin/location_picker.js',
            )

class RueAdmin(admin.ModelAdmin):
    list_display   = ('libelle', 'code', 'longitude', 'latitude', 'created_at', 'ajoute_par')
    list_filter    = ('libelle', 'code', 'longitude', 'latitude', 'created_at',)
    date_hierarchy = 'updated_at'
    ordering       = ('created_at', )
    search_fields  = ('libelle', 'code', 'longitude', 'latitude', 'created_at')

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'ajoute_par', None) is None:
            obj.ajoute_par = request.user
        obj.save()


admin.site.unregister(User)
admin.site.register(models.Gprovince, GprovinceAdmin)
admin.site.register(User, CustomerUserAdmin)
admin.site.register(models.Profile)
admin.site.register(models.FicheStock, FicheStockAdmin)
admin.site.register(models.Entree)
admin.site.register(models.Sortie)
admin.site.register(models.Depot, DepotAdmin)
admin.site.register(models.Ordonnance, OrdonnanceAdmin)
admin.site.register(models.Famille, FamilleAdmin)
admin.site.register(models.Medicament, MedicamentAdmin)
admin.site.register(models.Pharmacie, PharmacieAdmin)
admin.site.register(models.Fournisseur, FournisseurAdmin)
admin.site.register(models.Stock, StockAdmin)
admin.site.register(models.StockMedicament, StockMedicamentAdmin)
admin.site.register(models.Vente, VenteAdmin)
admin.site.register(models.VenteMedicament, VenteMedicamentAdmin)
admin.site.register(models.Commande, CommandeAdmin)
admin.site.register(models.LigneCommande, LigneCommandeAdmin)
admin.site.register(models.Pays, PaysAdmin)
admin.site.register(models.Province, ProvinceAdmin)
admin.site.register(models.Ville, VilleAdmin)
admin.site.register(models.Departement, DepartementAdmin)
admin.site.register(models.Commune, CommuneAdmin)
admin.site.register(models.Quartier, QuartierAdmin)
admin.site.register(models.Rue, RueAdmin)
admin.site.register(models.TypeEtat)
admin.site.register(models.Etat)
admin.site.register(models.TypeMessage)
admin.site.register(models.Message)