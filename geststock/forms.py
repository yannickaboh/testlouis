from django import forms
from .models import Medicament, Fournisseur, Pharmacie, Ordonnance, Photo, Employe, Depot, FicheStock
from crispy_forms.helper import FormHelper
from crispy_forms.bootstrap import StrictButton
from crispy_forms.layout import Layout
from crispy_forms.bootstrap import TabHolder, Tab
from django.contrib.auth.models import User

from django.core.files import File

from .models import Profile

class ProfileForm(forms.ModelForm):
    x = forms.FloatField(widget=forms.HiddenInput())
    y = forms.FloatField(widget=forms.HiddenInput())
    width = forms.FloatField(widget=forms.HiddenInput())
    height = forms.FloatField(widget=forms.HiddenInput())

    class Meta:
        model = Profile
        fields = ('bio', 'telephone', 'photo', 'ville', 'quartier', 'x', 'y', 'width', 'height', )
        widgets = {
            'file': forms.FileInput(attrs={
                'accept': 'image/*'  # this is not an actual validation! don't rely on that!
            })
        }

    def save(self):
        profile = super(ProfileForm, self).save()

        x = self.cleaned_data.get('x')
        y = self.cleaned_data.get('y')
        w = self.cleaned_data.get('width')
        h = self.cleaned_data.get('height')

        image = Image.open(profile.photo)
        cropped_image = image.crop((x, y, w+x, h+y))
        resized_image = cropped_image.resize((200, 200), Image.ANTIALIAS)
        resized_image.save(profile.photo.path)

        return profile

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

class PhotoForm(forms.ModelForm):

    class Meta:
        model = Photo
        fields = ['file', ]

class EmployeForm(forms.ModelForm):

    class Meta:
        model = Employe
        fields = ['nom', 'prenom', 'dateofbirth', 'status', 'poste', 'direction', ]

class MedocForm(forms.ModelForm):
    class Meta:
        model = Medicament
        fields = ('genre', 'famille', 'nom_generique', 'forme', 'code', 
            'conditionnement', 'description', 'prix_achat', 'prix_vente')


class MedicamentForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        """
        Surcharge de l'initialisation du formulaire
        """
        super().__init__(*args, **kwargs)
        # Tu utilises FormHelper pour customiser ton formulaire
        self.helper = FormHelper()
        # Tu définis l'id et la classe bootstrap de ton formulaire
        self.helper.form_class = 'form-horizontal'
        self.helper.form_id = 'medicament-form'
        # Tu définis la taille des labels et des champs sur la grille
        self.helper.label_class = 'col-md-2'
        self.helper.field_class = 'col-md-8'
        # Tu crées l'affichage de ton formulaire
        self.helper.layout = Layout(
            # Le formulaire va contenir 3 onglets
            TabHolder(
                # Premier onglet
                Tab(
                    # Label de l'onglet
                    'Étape 1',
                    # Liste des champs du modèle à afficher dans l'onglet
                    'genre',
                    'famille',
                    'nom_generique',
                    'forme',
                    # Tu rajoutes un bouton "Suivant"
                    StrictButton(
                        '<span class="glyphicon glyphicon-arrow-right" \
                        aria-hidden="true"></span> %s' % "Suivant",
                        type='button',
                        css_class='btn-warning col-md-offset-9 btnNext',
                    )

                ),
                # Deuxième onglet
                Tab(
                    # Label de l'onglet
                    'Étape 2',
                    # Liste des champs à afficher
                    'code',
                    'conditionnement',
                    'description',
                    # Tu rajoutes des boutons "Précédent" et "Suivant"
                    StrictButton(
                        '<span class="glyphicon glyphicon-arrow-left" \
                        aria-hidden="true"></span> %s' % 'Précédent',
                        type='button',
                        css_class='btn-primary btnPrevious',
                    ),
                    StrictButton(
                        '<span class="glyphicon glyphicon-arrow-right" \
                        aria-hidden="true"></span> %s' % 'Suivant',
                        type='button',
                        css_class='btn-warning col-md-offset-8 btnNext',
                    )
                ),
                # Troisième onglet
                Tab(
                    # Label de l'onglet
                    'Étape 3',
                    # Liste des champs à afficher dont les champs supplémentaires
                    'prix_achat',
                    'prix_vente',
                    # Tu rajoutes des boutons "Précédent" et "Valider"
                    StrictButton(
                        '<span class="glyphicon glyphicon-arrow-left" \
                        aria-hidden="true"></span> %s' % "Précédent",
                        type='button',
                        css_class='btn-warning btnPrevious',
                    ),
                    StrictButton(
                        '<span class="glyphicon glyphicon-ok" \
                        aria-hidden="true"></span> %s' % "Valider",
                        type='submit',
                        css_class='btn-success col-md-offset-8'
                    )
                ),
            ),
        )

    class Meta:
        # Tu définis le modèle utilisé
        model = Medicament
        exclude = ['visibilite', 'created_at', 'updated_at', 'ajoute_par']


class DepotForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        """
        Surcharge de l'initialisation du formulaire
        """
        super().__init__(*args, **kwargs)
        # Tu utilises FormHelper pour customiser ton formulaire
        self.helper = FormHelper()
        # Tu définis l'id et la classe bootstrap de ton formulaire
        self.helper.form_class = 'form-horizontal'
        self.helper.form_id = 'depot-form'
        # Tu définis la taille des labels et des champs sur la grille
        self.helper.label_class = 'col-md-2'
        self.helper.field_class = 'col-md-8'
        # Tu crées l'affichage de ton formulaire
        self.helper.layout = Layout(
            # Le formulaire va contenir 3 onglets
            TabHolder(
                # Premier onglet
                Tab(
                    # Label de l'onglet
                    'Étape 1',
                    # Liste des champs à afficher dont les champs supplémentaires
                    'code',
                    'libelle',
                    # Tu rajoutes des boutons "Précédent" et "Valider"
                    StrictButton(
                        '<span class="glyphicon glyphicon-ok" \
                        aria-hidden="true"></span> %s' % "Valider",
                        type='submit',
                        css_class='btn-success col-md-offset-8'
                    )
                ),
            ),
        )

    class Meta:
        # Tu définis le modèle utilisé
        model = Depot
        exclude = ['date_ajout', 'ajoute_par']


class OrdonnanceForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        """
        Surcharge de l'initialisation du formulaire
        """
        super().__init__(*args, **kwargs)
        # Tu utilises FormHelper pour customiser ton formulaire
        self.helper = FormHelper()
        # Tu définis l'id et la classe bootstrap de ton formulaire
        self.helper.form_class = 'form-horizontal'
        self.helper.form_id = 'ordonnance-form'
        # Tu définis la taille des labels et des champs sur la grille
        self.helper.label_class = 'col-md-2'
        self.helper.field_class = 'col-md-8'
        # Tu crées l'affichage de ton formulaire
        self.helper.layout = Layout(
            # Le formulaire va contenir 3 onglets
            TabHolder(
                # Premier onglet
                Tab(
                    # Label de l'onglet
                    'Étape 1',
                    # Liste des champs du modèle à afficher dans l'onglet
                    'telephone',
                    'note',
                    # Tu rajoutes un bouton "Suivant"
                    StrictButton(
                        '<span class="glyphicon glyphicon-arrow-right" \
                        aria-hidden="true"></span> %s' % "Suivant",
                        type='button',
                        css_class='btn-warning col-md-offset-9 btnNext',
                    )

                ),
                # Deuxième onglet
                Tab(
                    # Label de l'onglet
                    'Étape 2',
                    # Liste des champs à afficher
                    'ordonance',
                    'pharmacie',
                    'quartier',
                    # Tu rajoutes des boutons "Précédent" et "Suivant"
                    StrictButton(
                        '<span class="glyphicon glyphicon-arrow-left" \
                        aria-hidden="true"></span> %s' % 'Précédent',
                        type='button',
                        css_class='btn-primary btnPrevious',
                    ),
                    StrictButton(
                        '<span class="glyphicon glyphicon-arrow-right" \
                        aria-hidden="true"></span> %s' % 'Suivant',
                        type='button',
                        css_class='btn-warning col-md-offset-8 btnNext',
                    )
                ),
                # Troisième onglet
                Tab(
                    # Label de l'onglet
                    'Étape 3',
                    # Liste des champs à afficher dont les champs supplémentaires
                    'visibilite',
                    'created_at',
                    'envoye_par',
                    # Tu rajoutes des boutons "Précédent" et "Valider"
                    StrictButton(
                        '<span class="glyphicon glyphicon-arrow-left" \
                        aria-hidden="true"></span> %s' % "Précédent",
                        type='button',
                        css_class='btn-warning btnPrevious',
                    ),
                    StrictButton(
                        '<span class="glyphicon glyphicon-ok" \
                        aria-hidden="true"></span> %s' % "Valider",
                        type='submit',
                        css_class='btn-success col-md-offset-8'
                    )
                ),
            ),
        )

    class Meta:
        # Tu définis le modèle utilisé
        model = Ordonnance
        exclude = []


class FournisseurForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        """
        Surcharge de l'initialisation du formulaire
        """
        super().__init__(*args, **kwargs)
        # Tu utilises FormHelper pour customiser ton formulaire
        self.helper = FormHelper()
        # Tu définis l'id et la classe bootstrap de ton formulaire
        self.helper.form_class = 'form-horizontal'
        self.helper.form_id = 'fournisseur-form'
        # Tu définis la taille des labels et des champs sur la grille
        self.helper.label_class = 'col-md-2'
        self.helper.field_class = 'col-md-8'
        # Tu crées l'affichage de ton formulaire
        self.helper.layout = Layout(
            # Le formulaire va contenir 3 onglets
            TabHolder(
                # Premier onglet
                Tab(
                    # Label de l'onglet
                    'Étape 1',
                    # Liste des champs du modèle à afficher dans l'onglet
                    'nom',
                    'site_web',
                    # Tu rajoutes un bouton "Suivant"
                    StrictButton(
                        '<span class="glyphicon glyphicon-arrow-right" \
                        aria-hidden="true"></span> %s' % "Suivant",
                        type='button',
                        css_class='btn-warning col-md-offset-9 btnNext',
                    )

                ),
                # Deuxième onglet
                Tab(
                    # Label de l'onglet
                    'Étape 2',
                    # Liste des champs à afficher
                    'email',
                    'boite_postale',
                    'telephone',
                    # Tu rajoutes des boutons "Précédent" et "Suivant"
                    StrictButton(
                        '<span class="glyphicon glyphicon-arrow-left" \
                        aria-hidden="true"></span> %s' % 'Précédent',
                        type='button',
                        css_class='btn-primary btnPrevious',
                    ),
                    StrictButton(
                        '<span class="glyphicon glyphicon-arrow-right" \
                        aria-hidden="true"></span> %s' % 'Suivant',
                        type='button',
                        css_class='btn-warning col-md-offset-8 btnNext',
                    )
                ),
                # Troisième onglet
                Tab(
                    # Label de l'onglet
                    'Étape 3',
                    # Liste des champs à afficher dont les champs supplémentaires
                    'quartier',
                    'ville',
                    # Tu rajoutes des boutons "Précédent" et "Valider"
                    StrictButton(
                        '<span class="glyphicon glyphicon-arrow-left" \
                        aria-hidden="true"></span> %s' % "Précédent",
                        type='button',
                        css_class='btn-warning btnPrevious',
                    ),
                    StrictButton(
                        '<span class="glyphicon glyphicon-ok" \
                        aria-hidden="true"></span> %s' % "Valider",
                        type='submit',
                        css_class='btn-success col-md-offset-8'
                    )
                ),
            ),
        )

    class Meta:
        # Tu définis le modèle utilisé
        model = Fournisseur
        exclude = ['created_at', 'updated_at', 'ajoute_par']


class PharmacieForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        """
        Surcharge de l'initialisation du formulaire
        """
        super().__init__(*args, **kwargs)
        # Tu utilises FormHelper pour customiser ton formulaire
        self.helper = FormHelper()
        # Tu définis l'id et la classe bootstrap de ton formulaire
        self.helper.form_class = 'form-horizontal'
        self.helper.form_id = 'pharmacie-form'
        # Tu définis la taille des labels et des champs sur la grille
        self.helper.label_class = 'col-md-2'
        self.helper.field_class = 'col-md-8'
        # Tu crées l'affichage de ton formulaire
        self.helper.layout = Layout(
            # Le formulaire va contenir 3 onglets
            TabHolder(
                # Premier onglet
                Tab(
                    # Label de l'onglet
                    'Étape 1 - Identité',
                    # Liste des champs du modèle à afficher dans l'onglet
                    'nom',
                    'libelle',
                    'slogan',
                    'horaires',
                    'statut',
                    
                    # Tu rajoutes un bouton "Suivant"
                    StrictButton(
                        '<span class="glyphicon glyphicon-arrow-right" \
                        aria-hidden="true"></span> %s' % "Suivant",
                        type='button',
                        css_class='btn-warning col-md-offset-9 btnNext',
                    )

                ),
                # Deuxième onglet
                Tab(
                    # Label de l'onglet
                    'Étape 2 - Coordonnées',
                    # Liste des champs à afficher
                    'agrement',
                    'nom_gerant',
                    'site_web',
                    'email',
                    'boite_postale',
                    # Tu rajoutes des boutons "Précédent" et "Suivant"
                    StrictButton(
                        '<span class="glyphicon glyphicon-arrow-left" \
                        aria-hidden="true"></span> %s' % 'Précédent',
                        type='button',
                        css_class='btn-primary btnPrevious',
                    ),
                    StrictButton(
                        '<span class="glyphicon glyphicon-arrow-right" \
                        aria-hidden="true"></span> %s' % 'Suivant',
                        type='button',
                        css_class='btn-warning col-md-offset-8 btnNext',
                    )
                ),
                # Troisième onglet
                Tab(
                    # Label de l'onglet
                    'Étape 3 - Localisation',
                    # Liste des champs à afficher dont les champs supplémentaires
                    'telephone',
                    'repere',
                    'ville',
                    'quartier',
                    'logo',
                    # Tu rajoutes des boutons "Précédent" et "Valider"
                    StrictButton(
                        '<span class="glyphicon glyphicon-arrow-left" \
                        aria-hidden="true"></span> %s' % "Précédent",
                        type='button',
                        css_class='btn-warning btnPrevious',
                    ),
                    StrictButton(
                        '<span class="glyphicon glyphicon-ok" \
                        aria-hidden="true"></span> %s' % "Valider",
                        type='submit',
                        css_class='btn-success col-md-offset-8'
                    )
                ),
            ),
        )

    class Meta:
        # Tu définis le modèle utilisé
        model = Pharmacie
        exclude = ['visibilite', 'created_at', 'updated_at', 'ajoute_par']


class FicheStockForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        """
        Surcharge de l'initialisation du formulaire
        """
        super().__init__(*args, **kwargs)
        # Tu utilises FormHelper pour customiser ton formulaire
        self.helper = FormHelper()
        # Tu définis l'id et la classe bootstrap de ton formulaire
        self.helper.form_class = 'form-horizontal'
        self.helper.form_id = 'fichestock-form'
        # Tu définis la taille des labels et des champs sur la grille
        self.helper.label_class = 'col-md-2'
        self.helper.field_class = 'col-md-8'
        # Tu crées l'affichage de ton formulaire
        self.helper.layout = Layout(
            # Le formulaire va contenir 3 onglets
            TabHolder(
                # Premier onglet
                Tab(
                    # Label de l'onglet
                    'Étape 1 - ',
                    # Liste des champs du modèle à afficher dans l'onglet
                    'pharmacie',
                    'dci',
                    'forme',
                    'cmm',
                    'dosage',
                    
                    # Tu rajoutes un bouton "Suivant"
                    StrictButton(
                        '<span class="glyphicon glyphicon-arrow-right" \
                        aria-hidden="true"></span> %s' % "Suivant",
                        type='button',
                        css_class='btn-warning col-md-offset-9 btnNext',
                    )

                ),
                # Deuxième onglet
                Tab(
                    # Label de l'onglet
                    'Étape 2 - ',
                    # Liste des champs à afficher
                    'stockMin',
                    'stockMax',
                    'conditionnement',
                    'zone_stockage',
                    
                    # Tu rajoutes des boutons "Précédent" et "Suivant"
                    StrictButton(
                        '<span class="glyphicon glyphicon-arrow-left" \
                        aria-hidden="true"></span> %s' % 'Précédent',
                        type='button',
                        css_class='btn-primary btnPrevious',
                    ),
                    StrictButton(
                        '<span class="glyphicon glyphicon-arrow-right" \
                        aria-hidden="true"></span> %s' % 'Suivant',
                        type='button',
                        css_class='btn-warning col-md-offset-8 btnNext',
                    )
                ),
                # Troisième onglet
                Tab(
                    # Label de l'onglet
                    'Étape 3 - ',
                    # Liste des champs à afficher dont les champs supplémentaires
                    
                    'entree',
                    'sortie',
                    'stock',
                    'peremption_observation',
                    # Tu rajoutes des boutons "Précédent" et "Valider"
                    StrictButton(
                        '<span class="glyphicon glyphicon-arrow-left" \
                        aria-hidden="true"></span> %s' % "Précédent",
                        type='button',
                        css_class='btn-warning btnPrevious',
                    ),
                    StrictButton(
                        '<span class="glyphicon glyphicon-ok" \
                        aria-hidden="true"></span> %s' % "Valider",
                        type='submit',
                        css_class='btn-success col-md-offset-8'
                    )
                ),
            ),
        )

    class Meta:
        # Tu définis le modèle utilisé
        model = FicheStock
        exclude = ['provenance', 'date_ajout',]