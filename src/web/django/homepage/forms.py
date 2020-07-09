from django import forms
from .models import Search
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit
from django_range_slider.fields import RangeSliderField

def default_searchForm():
    """Fill the defaults values of the Search Form

    Returns:
        SearchForm: SearchForm with initial values
    """
    formSearch = SearchForm()
    formSearch.fields['departement'].initial = 75001
    formSearch.fields['price'].initial = 50000
    return formSearch


class SearchForm(forms.Form):
    """SearchForm class is the class that holds all the data of the Form with performing a researh on the Index.

    Args:
        forms (Form): Form
    """
    CHOICES = [('1', 'Maison'), ('2', 'Appartement')]
    departement = forms.IntegerField(label='Département', min_value=75001, max_value=75020)
    type_local = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES, required=True)
    superficie = RangeSliderField(label="Superficie(m²):", minimum=5, maximum=1000)
    nb_pieces = RangeSliderField(label="Nombre de pieces:", minimum=1, maximum=10)

    price = forms.IntegerField(label='Prix', min_value=0, max_value=3000000)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.form_method = 'post'
        self.helper.form_tag = False

        self.helper.layout = Layout(
            'departement',
            'type_local',
            'superficie',
            'nb_pieces',
            'price',

            Submit('submit', 'Submit', css_class='btn-success1')
        )


class AnnonceForm(forms.Form):
    """AnnonceForm  is the class that holds all the data of the Form with performing a researh on the Annonces

    Args:
        forms (Form): Form
    """
    CHOICES = [('1', 'Maison'), ('2', 'Appartement')]
    code_postal = forms.IntegerField(widget=forms.TextInput(attrs={'placeholder': 'Code Postal'}))
    adresse = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Adresse'}))
    type_local = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES)
    surface_reelle_bati = forms.IntegerField(widget=forms.TextInput(attrs={'placeholder': 'Surface du bien(m²)'}))
    nombre_pieces_principales = forms.IntegerField(widget=forms.TextInput(attrs={'placeholder': 'Nombre de pieces'}))
    surface_terrain = forms.IntegerField(widget=forms.TextInput(attrs={'placeholder': 'Surface du terrain (m²)'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Description'}))
    price = forms.DecimalField(widget=forms.TextInput(attrs={'placeholder': 'Prix du bien(€)'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.form_method = 'post'
        self.helper.form_tag = False

        self.helper.layout = Layout(
            'code_postal',
            'adresse',
            'type_local',
            'surface_reelle_bati',
            'nombre_pieces_principales',
            'surface_terrain',
            'message',
            'price',

            Submit('submit', 'Submit', css_class='btn-success')

        )
def default_predictionForm():
    """Create the default prediction form

    Returns:
        PredictionForm: PredictionForm empty
    """
    formPrediction = PredictionForm()
    return formPrediction

class PredictionForm(forms.Form):
    """PredictionForm  is the class that holds all the data of the Form with performing a submit on the prediction

    Args:
        forms (Form): Form
    """
    CHOICES_TYPE = [('1', 'Maison'), ('2', 'Appartement')]
    CHOICES_TIME = [('1', 'Evolution Trimestrielle'), ('2', 'Evolution sur 1 an'), ('3', 'Evolution sur 3 ans')]

    type_local = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES_TYPE)
    evolution = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES_TIME)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.form_method = 'post'
        self.helper.form_tag = False

        self.helper.layout = Layout(
            'type_local',
            'evolution',

            Submit('submit_', 'Submit', css_class='btn-success3')

        )
