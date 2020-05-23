from django.http import HttpResponse
from django.shortcuts import render

from .forms import SearchForm
from .query import my_query

def index(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            ville = form.cleaned_data['departement']
            res = my_query()
            # traiter res, et render ?
            print(res)
    else:
        # Valeurs par défaut
        form = SearchForm()
        form.fields['departement'].initial = 75001
    return render(request, 'index.html', {'form': form})
