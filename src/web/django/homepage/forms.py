from django import forms
from .models import Search
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit

class SearchForm(forms.Form):
    departement = forms.IntegerField(label='Département', min_value=75001, max_value=75020) 

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper
        self.helper.form_method = 'post'

        self.helper.layout = Layout(
            'departement',
            Submit('submit', 'Submit', css_class='btn-success')
        )