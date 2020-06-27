from django.http import HttpResponse
from django.shortcuts import render
from .forms import AnnonceForm
from .forms import SearchForm
import requests
from .query import my_query
import pymysql

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
            # res = my_query()
            # traiter res, et render ?
            # print(res)
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
        # change me according to results
        if i % 2 == 0:
            strike_color = "red"
            rgba = "{}, {}, 0".format(255, 0)
        else:
            strike_color = "green"
            rgba = "{}, {}, 0".format(0, 255)
        styles.append(template_color(strike_color, rgba))
        print(rgba)
    return render(request, 'index.html', {'form': form, 'coords': coords, 'styles': styles})


def annonce(request):
    if request.method == 'POST':
        form = AnnonceForm(request.POST)
        headers = {"Content-Type": "application/json"}
        adresse = form.data[]
        code_postal = form[]
        #arrondir les coor
        url = str(("http://api-adresse.data.gouv.fr/search/?q=" + str(adresse) + "&postcode=" + str(code_postal)))
        #print(url)

        r = requests.get(url, headers=headers, data="")
        content = r.text
        print(content)

        if form.is_valid():
            conn = pymysql.connect(
                host='predimodbinstance.cbiog1ld7y5x.eu-west-1.rds.amazonaws.com',
                db='predimmo',
                user='admin',
                password='N8XR3u#m9[5Mk6UK',
                port=3306)
            print(conn)
            print("ca marche")
            try:
                with conn.cursor() as cursor:
                    # Create a new record

                    sql = "INSERT INTO `data_django` (`valeur_fonciere`, `code_type_local`,`type_local`, `surface_reelle_bati`, `nombre_pieces_principales`,`surface_terrain`,`message`) VALUES (%s, %s,%s, %s,%s, %s,%s)"
                    cursor.execute(sql, (
                    form.data['valeur_fonciere'], form.data['code_type_local'], form.data['type_local'],
                    form.data['surface_reelle_bati'],
                    form.data['nombre_pieces_principales'], form.data['surface_terrain'], form.data['message']))
                    conn.commit()
                    print("inséré")
            finally:
                conn.close()
    else:
        form = AnnonceForm()
    return render(request, 'annonce.html', {'form': form})
