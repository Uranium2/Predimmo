from django import forms
from .models import Search
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit
from django_range_slider.fields import RangeSliderField

class SearchForm(forms.Form):

    CHOICES = [('1', 'Maison'), ('2', 'Appartement')]
    departement = forms.IntegerField(label='Département', min_value=75001, max_value=75020)
    type_local = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES)
    superficie = RangeSliderField(label="Superficie(m²):",minimum=5,maximum=1000)
    nb_pieces = RangeSliderField(label="Nombre de pieces:",minimum=1,maximum=10)

    price = forms.IntegerField(label='Prix', min_value=0, max_value=1000000)



    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper
        self.helper.form_method = 'post'

        self.helper.layout = Layout(
            'departement',
            'type_local',
            'superficie',
            'nb_pieces',
            'price',

            Submit('submit', 'Submit', css_class='btn-success')

        )