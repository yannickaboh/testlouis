from django.db import models
from django.contrib.auth.models import User, Permission
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.urlresolvers import reverse

# Create your models here.

class Profile(models.Model):
	user = models.OneToOneField(User, related_name='user', null=True, blank=True)
	bio = models.TextField(max_length=150, null=True, blank=True, verbose_name="Biographie")
	telephone = models.CharField(max_length=100, unique=True, null=True, blank=True,)
	photo = models.FileField(upload_to='media/photos', verbose_name="Photo de profil", null=True, blank=True, )
	ville = models.ForeignKey('Ville', verbose_name="Ville", null=True, blank=True,)
	quartier = models.ForeignKey('Quartier', verbose_name="Quartier", null=True, blank=True,)
	created_at = models.DateTimeField(auto_now_add=True)


	def __str__(self):
		return self.user.username

	def create_profile(sender, **kwargs):
	    if kwargs['created']:
	    	profile = Profile.objects.create(user=kwargs['instance'])
	    post_save.connect.save(create_profile, sender=User)


class Image(models.Model):
	name = models.CharField(max_length=255, blank=True)
	file = models.FileField(upload_to='media/photos')
	url = models.URLField(max_length=255, null=True, blank=True)
	uploaded_at = models.DateTimeField(auto_now_add=True)


class Photo(models.Model):
	title = models.CharField(max_length=255, blank=True)
	file = models.FileField(upload_to='media/photos')
	url = models.URLField(max_length=255, null=True, blank=True)
	uploaded_at = models.DateTimeField(auto_now_add=True)


class Sms(models.Model):
	code_type = models.CharField(max_length=255, blank=True)
	texte = models.TextField(max_length=250, null=False, blank=False, verbose_name="Contenu")
	lu = models.BooleanField(default=False)
	date_envoi = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.code_type
	class Meta:
		verbose_name_plural = 'Sms'

class TypeSms(models.Model):
	code = models.CharField(max_length=255, blank=True)
	libelle = models.CharField(max_length=255, blank=True)
	date_ajout = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.libelle
	class Meta:
		verbose_name_plural = 'TypeSms'

class Depot(models.Model):
	code = models.CharField(max_length=255, blank=True)
	libelle = models.CharField(max_length=255, blank=True)
	date_ajout = models.DateTimeField(auto_now_add=True)
	ajoute_par = models.ForeignKey(User, null=True, blank=True, editable=False)

	def __str__(self):
		return self.libelle
	class Meta:
		verbose_name_plural = 'Depots'


class Ordonnance(models.Model):
	telephone = models.CharField(max_length=50, unique=True, null=True, blank=True, verbose_name="Numero de telephone")
	infos = models.TextField(max_length=250, null=True, blank=True, verbose_name="Infos Supplémentaires")
	ordonance = models.FileField(upload_to='media/ordonnances', verbose_name="Ordonnance numerisée", null=True, blank=True, )
	pharmacie = models.ForeignKey('Pharmacie', verbose_name="Pharmacie", null=True, blank=True, editable=True)
	quartier = models.ForeignKey('Quartier', verbose_name="Quartier", null=True, blank=True,)
	created_at = models.DateTimeField(auto_now_add=True)
	visibilite = models.BooleanField(default=True)
	envoye_par = models.ForeignKey(User, null=True, blank=True, editable=False)


	def __str__(self):
		return self.telephone + ' - ' + self.envoye_par
	class Meta:
		verbose_name_plural = 'Ordonnances'


class FicheStock(models.Model):
	pharmacie = models.ForeignKey('Pharmacie', null=True, blank=True, verbose_name="Pharmacie")
	dci = models.ForeignKey('Medicament', verbose_name="Nom generique")
	forme = models.CharField(max_length=150, blank=True, verbose_name="Forme")
	cmm = models.FloatField(blank=True, null=True, verbose_name="Conso. Moyenne Mensuelle")
	dosage = models.FloatField(blank=True, null=True, verbose_name="Dosage")
	stockMin = models.IntegerField(blank=True, null=True, verbose_name="Stock Minimal")
	stockMax = models.IntegerField(blank=True, null=True, verbose_name="Stock Maximal")
	conditionnement = models.CharField(max_length=150, blank=True, verbose_name="Conditionnement")
	zone_stockage = models.ForeignKey('Depot', verbose_name="Zone de Stockage")
	date_ajout = models.DateTimeField(auto_now_add=True, verbose_name="Date")
	provenance_destination = models.CharField(max_length=150, blank=True, verbose_name="Provenance/Destination")
	entree = models.IntegerField(blank=True, null=True, verbose_name="Entrées")
	sortie = models.IntegerField(blank=True, null=True, verbose_name="Sorties")
	stock = models.IntegerField(blank=True, null=True, verbose_name="Stock restant")
	peremption_observation = models.TextField(blank=True, verbose_name="Peremptions/Observations")
	ajoute_par = models.ForeignKey(User, null=True, blank=True, editable=False)


	def __unicode__(self):
		return self.dci

	class Meta:
		verbose_name_plural = 'Fiches de Stock'


class Inventaire(models.Model):
	dci = models.ForeignKey('Medicament', verbose_name="Nom generique")
	forme = models.CharField(max_length=150, blank=True, verbose_name="Forme")
	dosage = models.FloatField(blank=True, null=True, verbose_name="Dosage")
	quantite = models.IntegerField(blank=True, null=True, verbose_name="Quantité")
	prix_unitaire = models.IntegerField(blank=True, null=True, verbose_name="Prix Unitaire")
	prix_total = models.CharField(max_length=150, blank=True, verbose_name="Prix Total")
	date_ajout = models.DateTimeField(auto_now_add=True, verbose_name="Date")
	peremption = models.TextField(blank=True, verbose_name="Date Peremption")
	ajoute_par = models.ForeignKey(User, null=True, blank=True, editable=False)


	def __unicode__(self):
		return self.dci

	class Meta:
		verbose_name_plural = 'Inventaires'


class BonCommande(models.Model):
	centrale = models.CharField(max_length=150, blank=True, verbose_name="Centrale de Distribution")
	depot_repartiteur = models.CharField(max_length=150, blank=True, verbose_name="Dépôt Repartiteur")
	designation = models.CharField(max_length=250, blank=True, verbose_name="Désignation")
	stock = models.IntegerField(blank=True, null=True, verbose_name="Stock")
	cmm = models.FloatField(blank=True, null=True, verbose_name="Conso. Moyenne Mensuelle")
	quantite = models.IntegerField(blank=True, null=True, verbose_name="Quantité")
	date_ajout = models.DateTimeField(auto_now_add=True, verbose_name="Date")
	ajoute_par = models.ForeignKey(User, null=True, blank=True, editable=False)


	def __unicode__(self):
		return self.designation

	class Meta:
		verbose_name_plural = 'Bons de Commande'


class BonLivraison(models.Model):
	centrale = models.CharField(max_length=150, blank=True, verbose_name="Centrale de Distribution")
	depot_pharma = models.CharField(max_length=150, blank=True, verbose_name="Dépôt Pharmaceutique")
	dci = models.CharField(max_length=250, blank=True, verbose_name="Nom Générique")
	forme = models.CharField(max_length=250, blank=True, verbose_name="Forme")
	dosage = models.IntegerField(blank=True, null=True, verbose_name="Dosage")
	quantite = models.IntegerField(blank=True, null=True, verbose_name="Quantité")
	observations = models.CharField(max_length=250, blank=True, verbose_name="Observations")
	date_ajout = models.DateTimeField(auto_now_add=True, verbose_name="Date")
	ajoute_par = models.ForeignKey(User, null=True, blank=True, editable=False)


	def __unicode__(self):
		return self.dci

	class Meta:
		verbose_name_plural = 'Bons de Livraison'


class ProduitHorsUsage(models.Model):
	MOIS  =  ( 
        ('Janvier', 'Janvier'),
        ('Fevrier', 'Fevrier'),
        ('Mars', 'Mars'),
        ('Avril', 'Avril'),
        ('Mai', 'Mai'),
        ('Juin', 'Juin'),
        ('Juillet', 'Juillet'),
        ('Aout', 'Aout'),
        ('Septembre', 'Septembre'),
        ('Octobre', 'Octobre'),
        ('Novembre', 'Novembre'),
        ('Decembre', 'Decembre'),
    )
	mois = models.CharField(max_length=30, verbose_name="Mois", choices=MOIS,)
	designation = models.CharField(max_length=250, blank=True, verbose_name="Designation")
	quantite = models.IntegerField(blank=True, null=True, verbose_name="Quantité")
	motif = models.TextField(max_length=250, blank=True, verbose_name="Motif")
	prix = models.IntegerField(blank=True, null=True, verbose_name="Prix")
	date_ajout = models.DateTimeField(auto_now_add=True, verbose_name="Date")
	ajoute_par = models.ForeignKey(User, null=True, blank=True, editable=False)


	def __unicode__(self):
		return self.designation

	class Meta:
		verbose_name_plural = 'Produits Hors Usage'


class ProcesVerbal(models.Model):
	centrale = models.CharField(max_length=150, blank=True, verbose_name="Centrale de Distribution")
	depot_pharma = models.CharField(max_length=150, blank=True, verbose_name="Dépôt Pharmaceutique")
	date_cmd = models.DateTimeField(auto_now_add=False, verbose_name="Date de la Commande")
	fournisseur = models.ForeignKey('Fournisseur', verbose_name="Fournisseur")
	num_cmde = models.ForeignKey('Commande', verbose_name="Numéro Commande")
	date_reception = models.DateTimeField(auto_now_add=True, verbose_name="Date Reception")
	dci = models.CharField(max_length=250, blank=True, verbose_name="Nom Générique")
	forme = models.CharField(max_length=250, blank=True, verbose_name="Forme")
	dosage = models.IntegerField(blank=True, null=True, verbose_name="Dosage")
	qte_cmdee = models.IntegerField(blank=True, null=True, verbose_name="Qté Cmdée")
	qte_recue = models.IntegerField(blank=True, null=True, verbose_name="Qté Reçue")
	observations = models.TextField(null=True, blank=True, verbose_name="Observations")
	date_ajout = models.DateTimeField(auto_now_add=True, verbose_name="Date")
	ajoute_par = models.ForeignKey(User, null=True, blank=True, editable=False)


	def __unicode__(self):
		return self.num_cmde

	class Meta:
		verbose_name_plural = 'Proces Verbaux'


class Reconditionnement(models.Model):
	designation = models.CharField(max_length=250, blank=True, verbose_name="Désignation")
	nbre_unite_by_cdt = models.IntegerField(blank=True, null=True, verbose_name="Nbre d'Unité par Conditionnement")
	nbre_unite_by_boite = models.IntegerField(blank=True, null=True, verbose_name="Nbre d'Unité par Boite")
	nbre_theorique_cdt = models.IntegerField(blank=True, null=True, verbose_name="Nbre théorique de cdt")
	nbre_reel_cdt = models.IntegerField(blank=True, null=True, verbose_name="Nbre Réel de cdt")
	perte_exces = models.CharField(max_length=250, blank=True, null=True, verbose_name="Perte ou Exces")
	date_ajout = models.DateTimeField(auto_now_add=True, verbose_name="Date")
	ajoute_par = models.ForeignKey(User, null=True, blank=True, editable=False)


	def __unicode__(self):
		return self.designation

	class Meta:
		verbose_name_plural = 'Cahier Reconditionnement'



class TypeEtat(models.Model):
	libelle = models.CharField(max_length=250, blank=False)
	description = models.CharField(max_length=250, blank=True)
	created_at = models.DateTimeField(auto_now_add=True)
	ajoute_par = models.ForeignKey(User, null=True, blank=True, editable=False)

	def __str__(self):
		return self.libelle
	class Meta:
		verbose_name_plural = 'Type_Etats'


class Etat(models.Model):
	type_etat = models.ForeignKey(TypeEtat, on_delete=models.CASCADE)
	code = models.CharField(max_length=10, blank=True)
	libelle = models.CharField(max_length=250, blank=False, unique=True)
	description = models.TextField(max_length=250, blank=True)
	visibilite = models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now_add=True)
	ajoute_par = models.ForeignKey(User, null=True, blank=True, editable=False)

	def __str__(self):
		return self.libelle
	class Meta:
		verbose_name_plural = 'Etats'


class TypeMessage(models.Model):
	libelle = models.CharField(max_length=250, blank=False)
	description = models.CharField(max_length=250, blank=True)
	created_at = models.DateTimeField(auto_now_add=True)
	ajoute_par = models.ForeignKey(User, null=True, blank=True, editable=False)

	def __str__(self):
		return self.libelle
	class Meta:
		verbose_name_plural = 'Types_Messages'

class Message(models.Model):
	type_message = models.ForeignKey('TypeMessage', verbose_name="Type_Message")
	expediteur = models.ForeignKey(User, null=True, blank=True, editable=False)
	destinataire = models.ManyToManyField('Pharmacie', verbose_name="destinataires",)
	texte = models.CharField(max_length=300, blank=False)
	nom_ordon = models.CharField(max_length=300, blank=True)
	url = models.TextField( blank=True)
	lu = models.BooleanField(default=False)
	date_envoi = models.DateTimeField(auto_now_add=True)
	


	def __str__(self):
		return self.libelle

	class Meta:
		verbose_name_plural = 'Messages'


class Famille(models.Model):
	libelle = models.CharField(max_length=250, blank=False, unique=True)
	code = models.CharField(max_length=250, blank=True, unique=True)
	description = models.CharField(max_length=250, blank=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	ajoute_par = models.ForeignKey(User, null=True, blank=True, editable=False)

	def __str__(self):
		return self.libelle
	class Meta:
		verbose_name_plural = 'Familles'

class Medicament(models.Model):
	pharmacie = models.ForeignKey('Pharmacie', null=True, blank=True)
	GENRE  =  ( 
        ('MaterielMedical', 'MaterielMedical'),
        ('Medicament', 'Medicament'),
    )
	genre = models.CharField(max_length=30, verbose_name="Type", choices=GENRE, default='Medicament')
	famille = models.ForeignKey('Famille', verbose_name="Famille")
	nom_generique = models.CharField(max_length=250, blank=False, unique=True)
	forme = models.CharField(max_length=150, blank=True)
	code = models.CharField(max_length=150, blank=True)
	conditionnement = models.CharField(max_length=250, blank=True)
	description = models.TextField(blank=True)
	prix_achat = models.IntegerField(blank=True)
	prix_vente = models.IntegerField(blank=True)
	visibilite = models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	ajoute_par = models.ForeignKey(User, null=True, blank=True, editable=False)


	def __str__(self):
		return self.nom_generique

	def get_absolute_url(self):
		return reverse('geststock:medicament_update', kwargs={'pk': self.pk})

	class Meta:
		verbose_name_plural = 'Medicaments'

class Pharmacie(models.Model):
	nom = models.CharField(max_length=250, blank=False, null=False)
	libelle = models.CharField(max_length=250, blank=True)
	slogan = models.CharField(max_length=100, blank=True, null=True)
	horaires = models.CharField(max_length=100, blank=True, null=True)
	garde = models.BooleanField(default=False)
	agrement = models.CharField(max_length=250, blank=True, null=True, unique=True)
	nom_gerant = models.CharField(max_length=200, blank=True, null=True)
	site_web = models.URLField(max_length=100, unique=True, blank=True)
	logo = models.FileField(upload_to='media/photos', verbose_name="Logo", null=True, blank=True, )
	email = models.EmailField(max_length=50, unique=True, blank=False)
	boite_postale = models.CharField(max_length=100, blank=True)
	telephone = models.CharField(max_length=50, unique=True, blank=False)
	repere = models.CharField(max_length=100, blank=True, null=True)
	ville = models.ForeignKey('Ville', verbose_name="Ville", blank=True, null=True)
	quartier = models.ForeignKey('Quartier', verbose_name="Quartier",blank=True, null=True)
	rue = models.ForeignKey('Rue', verbose_name="Rue", blank=True, null=True)
	longitude = models.CharField(max_length=100, blank=True, default='0.0')
	latitude = models.CharField(max_length=100, blank=True, default='0.0')
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	ajoute_par = models.ForeignKey(User, null=True, blank=True, editable=False)


	def __str__(self):
		return self.nom

	def get_absolute_url(self):
		return reverse('geststock:index')

	class Meta:
		verbose_name_plural = 'Pharmacies'

class Gprovince(models.Model):
	nom = models.CharField(max_length=250, blank=False, null=False)
	libelle = models.CharField(max_length=250, blank=True)
	slogan = models.CharField(max_length=100, blank=True, null=True)
	longitude = models.CharField(max_length=100, blank=True, default='0.0')
	latitude = models.CharField(max_length=100, blank=True, default='0.0')

	def __str__(self):
		return self.nom

	class Meta:
		verbose_name_plural = 'Gprovinces'



class Fournisseur(models.Model):
	nom = models.CharField(max_length=100, blank=False, unique=True)
	site_web = models.URLField(max_length=100, unique=True, blank=True)
	email = models.EmailField(max_length=50, unique=True, blank=False)
	boite_postale = models.CharField(max_length=100, blank=True)
	telephone = models.CharField(max_length=50, unique=True, blank=False)
	ville = models.ForeignKey('Ville', verbose_name="Ville")
	quartier = models.ForeignKey('Quartier', verbose_name="Quartier")
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	ajoute_par = models.ForeignKey(User, null=True, blank=True, editable=False)


	def __str__(self):
		return self.nom

	def get_absolute_url(self):
		return reverse('geststock:fournisseur_update', kwargs={'pk': self.pk})
		
	class Meta:
		verbose_name_plural = 'Fournisseurs'


class Stock(models.Model):
	medicament = models.ManyToManyField('Medicament', verbose_name="Medicament", through='StockMedicament')
	libelle = models.CharField(max_length=300, blank=False, default='')
	stock_min = models.IntegerField(blank=False)
	stock_max = models.IntegerField(blank=False)
	visibilite = models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	ajoute_par = models.ForeignKey(User, null=True, blank=True, editable=False)


	def __str__(self):
		return self.libelle
	class Meta:
		verbose_name_plural = 'Stocks'

class Entree(models.Model):
	medicament = models.ForeignKey('Medicament', null=True, blank=True)
	qte_cmdee = models.ForeignKey('LigneCommande', null=True, blank=True)
	qte_entree = models.IntegerField(null=True, blank=True)
	created_at = models.DateTimeField(auto_now_add=True)
	ajoute_par = models.ForeignKey(User, null=True, blank=True, editable=False)

	class Meta:
		verbose_name_plural = 'Entrees'

class Sortie(models.Model):
	medicament = models.ForeignKey('Medicament', null=True, blank=True)
	qte_vendu = models.ForeignKey('VenteMedicament', null=True, blank=True)
	qte_sortie = models.IntegerField(null=True, blank=True)
	created_at = models.DateTimeField(auto_now_add=True)
	ajoute_par = models.ForeignKey(User, null=True, blank=True, editable=False)

	class Meta:
		verbose_name_plural = 'Sorties'


class StockMedicament(models.Model):
	medicament = models.ForeignKey('Medicament', verbose_name="Medicament", null=True, blank=True)
	stock = models.ForeignKey('Stock', verbose_name="Stock", null=True, blank=True)
	entrees = models.ForeignKey('Entree', verbose_name="Entrees", null=True, blank=True)
	sorties = models.ForeignKey('Sortie', verbose_name="Sorties", null=True, blank=True)
	qte_stock = models.IntegerField(blank=False)
	alerte_qte = models.CharField(max_length=300, blank=False)
	disponible = models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	ajoute_par = models.ForeignKey(User, null=True, blank=True, editable=False)

	class Meta:
		verbose_name_plural = 'Stock_Pharmacies_Medicaments'


class Commande(models.Model):
	medicament = models.ManyToManyField('Medicament', verbose_name="Medicament", through='LigneCommande')
	fournisseur = models.ForeignKey('Fournisseur', verbose_name="Fournisseur")
	num_commande = models.CharField(max_length=30, null=True, blank=True, verbose_name="Numéro Commande")
	montant = models.IntegerField(blank=True, null=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	ajoute_par = models.ForeignKey(User, null=True, blank=True, editable=False)

	def __unicode__(self):
		return self.fournisseur

	def _get_num_commande(self):
		if self.pk==None:
			last = Commande.objects.all()
			newid=last.count()+1
			return 'GPM2017%s' % (newid)
		if len(str(self.pk))==1:
			return 'GPM20170000%s' % (self.pk)
		elif len(str(self.pk))==2:
			return 'GPM2017000%s' % (self.pk)
		elif len(str(self.pk))==3:
			return 'GPM201700%s' % (self.pk)
		elif len(str(self.pk))==4:
			return 'GPM20170%s' % (self.pk)
		else:
			return 'GPM2017%s' % (self.pk)

		num_commande = property(_get_num_commande)

	def save(self, *args, **kwargs):
		self.num_commande=self.num_commande
		super(Commande, self).save(*args, **kwargs) # Call the "real" save() method.

	class Meta:
		verbose_name_plural = 'Commandes'


class LigneCommande(models.Model):
	commande = models.ForeignKey('Commande', verbose_name="Commande")
	medicament = models.ForeignKey('Medicament', verbose_name="Medicament")
	qte_commande = models.IntegerField(blank=False,)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	ajoute_par = models.ForeignKey(User, null=True, blank=True, editable=False)

	class Meta:
		verbose_name_plural = 'Lignes_Commandes_Medicaments'

class Vente(models.Model):
	medicament = models.ManyToManyField('Medicament', verbose_name="Medicament", through='VenteMedicament')
	montant = models.IntegerField(blank=True, null=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	ajoute_par = models.ForeignKey(User, null=True, blank=True, editable=False)

	class Meta:
		verbose_name_plural = 'Ventes'


class VenteMedicament(models.Model):
	medicament = models.ForeignKey('Medicament', verbose_name="Medicament")
	vente = models.ForeignKey('Vente', verbose_name="Vente")
	qte_vendu = models.IntegerField(blank=True, null=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	ajoute_par = models.ForeignKey(User, null=True, blank=True, editable=False)

	class Meta:
		verbose_name_plural = 'Ventes_Medicaments'


class Pays(models.Model):
	libelle = models.CharField(max_length=50, blank=False, unique=True)
	code = models.CharField(max_length=10, blank=True)
	longitude = models.DecimalField(max_digits=10, decimal_places=9, null=True, blank=True)
	latitude = models.DecimalField(max_digits=10, decimal_places=9, null=True, blank=True)
	visibilite = models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	ajoute_par = models.ForeignKey(User, null=True, blank=True, editable=False)


	def __str__(self):
		return self.libelle
	class Meta:
		verbose_name_plural = 'Pays'


class Province(models.Model):
	pays = models.ForeignKey('Pays', verbose_name="Pays", related_name='provinces', on_delete=models.CASCADE)
	libelle = models.CharField(max_length=50, blank=False)
	code = models.CharField(max_length=10, blank=True)
	longitude = models.DecimalField(max_digits=10, decimal_places=9, null=True, blank=True)
	latitude = models.DecimalField(max_digits=10, decimal_places=9, null=True, blank=True)
	visibilite = models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	ajoute_par = models.ForeignKey(User, null=True, blank=True, editable=False)

	
	def __str__(self):
		return self.libelle
	class Meta:
		verbose_name_plural = 'Provinces'

class Ville(models.Model):
	pays = models.ForeignKey('Pays', verbose_name="Pays", null=True, blank=True)
	province = models.ForeignKey('Province', verbose_name="Province", null=True, blank=True)
	libelle = models.CharField(max_length=50, blank=True, null=True)
	code_ville = models.CharField(max_length=10, blank=True, null=True)
	longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
	latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
	visibilite = models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	ajoute_par = models.ForeignKey(User, null=True, blank=True, editable=False)


	def __str__(self):
		return self.libelle
	class Meta:
		verbose_name_plural = 'Villes'


class Departement(models.Model):
	pays = models.ForeignKey('Pays', verbose_name="Pays")
	province = models.ForeignKey('Province', verbose_name="Province")
	ville = models.ForeignKey('Ville', verbose_name="Ville")
	libelle = models.CharField(max_length=50, blank=False)
	code = models.CharField(max_length=10, blank=True)
	longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
	latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
	visibilite = models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	ajoute_par = models.ForeignKey(User, null=True, blank=True, editable=False)


	def __str__(self):
		return self.libelle
	class Meta:
		verbose_name_plural = 'Departements'


class Commune(models.Model):
	pays = models.ForeignKey('Pays', verbose_name="Pays")
	province = models.ForeignKey('Province', verbose_name="Province")
	ville = models.ForeignKey('Ville', verbose_name="Ville")
	departement = models.ForeignKey('Departement', verbose_name="Departement")
	libelle = models.CharField(max_length=50, blank=False)
	code = models.CharField(max_length=10, blank=True)
	longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
	latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
	visibilite = models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	ajoute_par = models.ForeignKey(User, null=True, blank=True, editable=False)


	def __str__(self):
		return self.libelle
	class Meta:
		verbose_name_plural = 'Communes'


class Quartier(models.Model):
	pays = models.ForeignKey('Pays', verbose_name="Pays", null=True, blank=True)
	province = models.ForeignKey('Province', verbose_name="Province", null=True, blank=True)
	ville = models.ForeignKey('Ville', verbose_name="Ville", null=True, blank=True)
	departement = models.ForeignKey('Departement', verbose_name="Departement", null=True, blank=True)
	commune = models.ForeignKey('Commune', verbose_name="Commune", null=True, blank=True)
	libelle = models.CharField(max_length=50, blank=False)
	code_quartier = models.CharField(max_length=100,blank=True)
	longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
	latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
	visibilite = models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	ajoute_par = models.ForeignKey(User, null=True, blank=True, editable=False)


	def __str__(self):
		return self.libelle
	class Meta:
		verbose_name_plural = 'Quartiers'


class Rue(models.Model):
	pays = models.ForeignKey('Pays', verbose_name="Pays")
	province = models.ForeignKey('Province', verbose_name="Province")
	ville = models.ForeignKey('Ville', verbose_name="Ville")
	departement = models.ForeignKey('Departement', verbose_name="Departement")
	commune = models.ForeignKey('Commune', verbose_name="Commune")
	quartier = models.ForeignKey('Quartier', verbose_name="Quartier")
	libelle = models.CharField(max_length=50, blank=False)
	code = models.CharField(max_length=10, blank=True)
	longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
	latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
	visibilite = models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	ajoute_par = models.ForeignKey(User, null=True, blank=True, editable=False)


	def __str__(self):
		return self.libelle
	class Meta:
		verbose_name_plural = 'Rues'


class Employe(models.Model):
	STATUT  =  ( 
        ('CELIBATAIRE', 'Celibataire'),
        ('MARIE', 'Marié'),
    )
	nom = models.CharField(max_length=255, blank=True, null=True, verbose_name="Nom")
	prenom = models.CharField(max_length=255, blank=True, null=True, verbose_name="Prénom")
	dateofbirth = models.DateField(blank=True, null=True, verbose_name="Date de Naissance")
	status = models.CharField(max_length=255, blank=True, null=True, choices=STATUT, verbose_name="Statut Matrimonial")
	poste = models.CharField(max_length=255, blank=True, null=True, verbose_name="Poste Occupé")
	direction = models.CharField(max_length=255, blank=True, null=True, verbose_name="Direction")


	def __str__(self):
		return self.nom
	class Meta:
		verbose_name_plural = 'Employees'