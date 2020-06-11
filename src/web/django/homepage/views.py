from django.http import HttpResponse
from django.shortcuts import render

from .forms import SearchForm
from .query import my_query

import os

def template_color(stroke_color, fille_color):
    return """new ol.style.Style({{
            stroke: new ol.style.Stroke({{
                color: '{}',
                width: 3
            }}),
            fill: new ol.style.Fill({{
                color: 'rgba({}, 0.1)'
            }})
        }})""".format(stroke_color, fille_color)


def index(request):
    module_dir = os.path.dirname(__file__) 
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            departement = form.cleaned_data['departement']
            price = form.cleaned_data['price']
            #res = my_query()
            # traiter res, et render ?
            #print(res)
    else:
        # Valeurs par défaut
        form = SearchForm()
        form.fields['departement'].initial = 75001
        form.fields['price'].initial = 50000
    
    file_path = os.path.join(module_dir, 'data', 'quartier_paris.geojson')
    coords = []
    with open(file_path, mode='r') as fp:
        for line in fp:
            coords.append(line)
    # print(coords[0])
    # coords = coords[0]
    styles = []
    for i in range(80):
        #change me according to results
        if i % 2 == 0:
            strike_color = "red"
            rgba = "{}, {}, 0".format(255, 0)
        else:
            strike_color = "green"
            rgba = "{}, {}, 0".format(0, 255)
        styles.append(template_color(strike_color, rgba))
        print(rgba)
    return render(request, 'index.html', {'form': form, 'coords': coords, 'styles' : styles})