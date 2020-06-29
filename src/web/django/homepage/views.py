from django.http import HttpResponse
from django.shortcuts import render
from .forms import AnnonceForm
from .forms import SearchForm, PredictionForm, default_predictionForm, default_searchForm
import requests
import json
from mysqlcon import get_conn, create_query_search
import os
from django.shortcuts import redirect
from datetime import date


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

def make_map():
    module_dir = os.path.dirname(__file__)
    file_path = os.path.join(module_dir, 'data', 'quartier_paris.geojson')
    coords = []
    with open(file_path, mode='r') as fp:
        for line in fp:
            coords.append(line)
    styles = []
    for i in range(80):
        # change me according to results
        if i % 2 == 0:
            strike_color = "red"
            rgba = "{}, {}, 0".format(255, 0)
        else:
            strike_color = "green"
            rgba = "{}, {}, 0".format(0, 255)
        styles.append(template_color(strike_color, rgba))

    return coords, styles

def get_coord_from_address(code_postal, adresse=None):
    headers = {"Content-Type": "application/json"}
    if adresse != None:
        url = str(("http://api-adresse.data.gouv.fr/search/?q=" + str(adresse) + "&postcode=" + str(code_postal)))
    else:
        url = str(("http://api-adresse.data.gouv.fr/search/?q=" + str(code_postal)))
    print(url)
    r = requests.get(url, headers=headers, data="")
    js = json.loads(r.text)
    x = js['features'][0]['geometry']['coordinates']
    longitude = x[0]
    latitude = x[1]
    pos = []
    pos.append(longitude)
    pos.append(latitude)
    return pos

def get_colors():
    colors = []
    colors.append("#ff8000")
    colors.append("#eeff00")
    colors.append("#5eff00")
    colors.append("#00e1ff")
    colors.append("#2600ff")
    return colors

def index(request):
    result = ""
    annonces = list()
    if request.method == 'POST':
        formSearch = SearchForm(request.POST)
        formPrediction = PredictionForm(request.POST)

        if formSearch.is_valid():
            try:
                conn = get_conn()
                with conn.cursor() as cursor:
                    sql = create_query_search(formSearch)
                    print(sql)
                    cursor.execute(sql)
                    result = cursor.fetchall()
                    conn.commit()
                    print(result)
                    annonces = list(result)
            finally:
                conn.close()
            pos_map = get_coord_from_address(formSearch.cleaned_data['departement'])
            zoom = 14
            formPrediction = default_predictionForm()
        elif formPrediction.is_valid():
            print("prediction ok")
            formSearch = default_searchForm()
    else:
        # Valeurs par défaut
        pos_map = [2.333333, 48.866667] # CENTRE DE PARIS
        zoom = 12.5
        formSearch = default_searchForm()
        formPrediction = default_predictionForm()

    coords, styles = make_map()

    forms = [formSearch, formPrediction]

    print(pos_map)

    return render(request, 'index.html', {'forms': forms, 'coords': coords, 'styles': styles, 'annonces': build_annonce_result(annonces), 'pos_map': pos_map, 'zoom': zoom, 'colors': get_colors()})

def get_adress(x, y):
        url = str(("http://api-adresse.data.gouv.fr/reverse/?lon=" + str(x) + "&lat=" + str(y)))
        print(url)
        headers = {"Content-Type": "application/json"}
        r = requests.get(url, headers=headers, data="")
        js = json.loads(r.text)
        address = js['features'][0]['properties']['label']
        return address

def build_annonce_result(annonces):
    div = []
    for i, annonce in enumerate(annonces):
        div.append([])
        x = annonce[7]
        y = annonce[8]
        address = get_adress(x, y)
        print(annonce[3])
        if annonce[3] == 1:
            batiment = "Maison"
        else:
            batiment = "Appartement"
        
        div[i].append( address + "\n" + str(annonce[2]) + " €\n" + \
                    batiment + "\n" + \
                    str(annonce[4]) + "	㎡\n" + \
                    str(annonce[5]) + " pièces\n")
    return div

def annonce(request):
    coords, styles = make_map()

    if request.method == 'POST':
        form = AnnonceForm(request.POST)
        adresse = form.data['adresse']
        code_postal = form.data['code_postal']
        pos = get_coord_from_address(code_postal, adresse)
        longitude = pos[0]
        latitude = pos[1]
        if form.is_valid():
            conn = get_conn()
            try:
                with conn.cursor() as cursor:
                    # Create a new record
                    date_mutation = date.today().strftime("%y-%m-%d")
                    sql = "INSERT INTO data_django (`date_mutation`, `code_postal`, `valeur_fonciere`, `code_type_local`, `surface_reelle_bati`, `nombre_pieces_principales`,`surface_terrain`,`longitude`,`latitude`,`message`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                    cursor.execute(sql, (
                        date_mutation,
                        form.data['code_postal'],
                        form.data['price'],
                        form.data['type_local'],
                        form.data['surface_reelle_bati'],
                        form.data['nombre_pieces_principales'],
                        form.data['surface_terrain'],
                        longitude,
                        latitude,
                        form.data['message']))
                    conn.commit()
                    print("Inserted")
            finally:
                conn.close()
                return redirect('/index/')
    else:
        form = AnnonceForm()
    return render(request, "annonce.html", {'form': form, 'coords': coords, 'styles': styles})
