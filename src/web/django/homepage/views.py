from django.http import HttpResponse
from django.shortcuts import render
from .forms import AnnonceForm
from .forms import SearchForm, PredictionForm, default_predictionForm, default_searchForm
import requests
import json
from mysqlcon import get_conn, create_query_search, make_request
import os
from django.shortcuts import redirect
from datetime import date
from random import uniform
import collections
import decimal


def template_color(stroke_color, fill_color=None):
    """Creates a Javascript ol.style.Style statement that will describe a Layer in OpenLayers

    Args:
        stroke_color (String): HTML color code
        fill_color (String): HTML color code

    Returns:
        String: JS statement that holds a new ol.style.Style 
    """
    if fill_color == None:
        return """new ol.style.Style({{
            stroke: new ol.style.Stroke({{
                color: '{}',
                width: 5
            }})
        }})""".format(stroke_color, fill_color)


    return """new ol.style.Style({{
            stroke: new ol.style.Stroke({{
                color: '{}',
                width: 3
            }}),
            fill: new ol.style.Fill({{
                color: 'rgba({}, 0.1)'
            }})
        }})""".format(stroke_color, fill_color)

def make_map(departement=None):
    """Generate a JS statement with the Layer and Style for the map
    Args:
        departement (String): City code to make a specific focus with openlayers after a search

    Returns:
        coords (List[String]): List of coords from quartier_paris.geojson
        styles (List[String]): List of styles with respect of coords
    """
    module_dir = os.path.dirname(__file__)
    file_path = os.path.join(module_dir, 'data', 'quartier_paris.geojson')
    coords = []
    styles = []

    with open(file_path, mode='r') as fp:
        for line in fp:
            coords.append(line)
    
    for i in range(80):
        # change me according to results
        if i % 2 == 0:
            strike_color = "red"
            rgba = "{}, {}, 0".format(255, 0)
        else:
            strike_color = "green"
            rgba = "{}, {}, 0".format(0, 255)
        styles.append(template_color(strike_color, rgba))

    if departement != None:
        file_path = os.path.join(module_dir, 'data', 'arrond.geojson')
        coords_dep = []
        with open(file_path, mode='r') as fp:
            for line in fp:
                coords_dep.append(line)
        index = int(departement) - 75000
        print(index)
        coords_dep = coords_dep[index - 1]
        coords.append(coords_dep)
        styles.append(template_color("black"))

    return coords, styles

def get_coord_from_address(code_postal, adresse=None):
    """Get coordinate from an address

    Args:
        code_postal (Int): Postal code of a city
        adresse (String, optional): The adresse of a house. Defaults to None.

    Returns:
        pos (List(Int, Int)): Give a list that holds X and Y coordinates of the given adress, else the adresse of Paris
    """
    headers = {"Content-Type": "application/json"}
    if adresse != None:
        url = str(("http://api-adresse.data.gouv.fr/search/?q=" + str(adresse) + "&postcode=" + str(code_postal)))
    else:
        url = str(("http://api-adresse.data.gouv.fr/search/?q=" + str(code_postal)))
    print(url)
    r = requests.get(url, headers=headers, data="")
    js = json.loads(r.text)
    if code_postal == 75001:
        x = js['features'][1]['geometry']['coordinates']
    else:
        	x = js['features'][0]['geometry']['coordinates']
    longitude = x[0]
    latitude = x[1]
    pos = []
    pos.append(longitude)
    pos.append(latitude)
    print(pos)
    return pos

def get_colors():
    """Get list of colors for the Recommandations color helper

    Returns:
        list(String): List of HTML colors
    """
    colors = []
    colors.append("#ff8000")
    colors.append("#eeff00")
    colors.append("#5eff00")
    colors.append("#00e1ff")
    colors.append("#2600ff")
    return colors

def get_colors_pred(list_pred):
    """Get the color with respect of a pediction list

    Args:
        list_pred (List(Int)): List of Predictions (Int => categories of predictions)

    Returns:
        List(String, String): List of color HTML and instruction for the displayed arrow Up or Down for the HTML
    """
    l = []
    img_dir = []
    i = 0
    for pred in list_pred:
        if pred < 5:
            l.append("#ff8000")
            img_dir.append("down" + str(i))
        elif pred < 0:
            l.append("#eeff00")
            img_dir.append("stay" + str(i))
        elif pred > 5:
            l.append("#ee5eff")   
            img_dir.append("up"  + str(i))
        i = i + 1
    return l, img_dir

def get_preditions(departement=None):
    """Get the predictions on the RDS of each city code or of Paris

    Args:
        departement (Int, optional): City code. Defaults to None.

    Returns:
        String: List of predictions
    """
    conn = get_conn()
    
    if departement == None:
        #trouver la prediction de paris en total
        sql = "SELECT ROUND(AVG(prediction_1), 2), ROUND(AVG(prediction_3), 2), ROUND(AVG(prix_m2_appart), 2), ROUND(AVG(prix_m2_maison), 2) FROM prediction"
    else:
        #trouver la prediction en fonction du departement
        sql = "SELECT * FROM prediction WHERE code_postal = {}".format(departement)
    
    result = make_request(conn, sql)
    conn.close()
    print(result)
    result = list(result[0])
    if departement != None:
        result = result[1:]
        print(result)
        result = ["Ø" if x == -1 else x for x in result]
    return result

def index(request):
    """View for the index Page
        This will generate all the default forms, handle POST and GET request for the index page

    Args:
        request (request): The request sent by the user

    Returns:
        render: Send the render to the client to render the index.hmtl with multiples variables that will be used to display data
    """
    result = ""
    annonces = list()
    if request.method == 'POST':
        formSearch = SearchForm(request.POST)
        formPrediction = PredictionForm(request.POST)

        if formSearch.is_valid():
            try:
                conn = get_conn()
                sql = create_query_search(formSearch)
                result = make_request(conn, sql)
                annonces = list(result)
            finally:
                conn.close()
            departement = formSearch.cleaned_data['departement']
            pos_map = get_coord_from_address(departement)
            zoom = 14
            points = []
            percentages = get_preditions(departement)
            
            for annonce in annonces:
                x = float(annonce[7])
                y = float(annonce[8])
                x = x + uniform(0.001, 0.0001)
                y = y + uniform(0.001, 0.0001)
                points.append([x, y])
            formPrediction = default_predictionForm()
            coords, styles = make_map(departement)
            header = departement

    else:
        # Valeurs par défaut
        pos_map = [2.333333, 48.866667] # CENTRE DE PARIS
        zoom = 12.5
        formSearch = default_searchForm()
        percentages = get_preditions()
        header = "Paris"
        points = []
        coords, styles = make_map()

    forms = [formSearch]
    pred = format_predictions(percentages)

    percentages_1 = percentages[:2]
    pred_1 = pred[:2]
    pred_2 = pred[-2:]
    colors_pred, img_dir = get_colors_pred(percentages_1)

    return render(request, 'index.html', {'forms': forms, 'coords': coords, 'styles': styles, \
            'annonces': build_annonce_result(annonces), \
            'pos_map': pos_map, \
            'zoom': zoom, \
            'colors': get_colors(), \
            'points': points,
            'colors_pred': colors_pred,
            'pred': pred_1,
            'price': pred_2,
            'header': header,
            'img_dir': img_dir
            })

def format_predictions(pred):
    pred = pred.copy()
    pred[0] = "%0.2f" % pred[0] + "%"
    pred[1] = "%0.2f" % pred[1] + "%"
    pred[2] = str(int(pred[2])) + "€"
    if pred[3] != "Ø":
        pred[3] = str(int(pred[3])) + "€"
    return pred

def get_adress(x, y):
    """Get adresse from coordinates

    Args:
        x (Int): Long
        y (Int): Lat

    Returns:
        String: The street and city name in a String format
    """
    url = str(("http://api-adresse.data.gouv.fr/reverse/?lon=" + str(x) + "&lat=" + str(y)))
    headers = {"Content-Type": "application/json"}
    r = requests.get(url, headers=headers, data="")
    js = json.loads(r.text)
    address = js['features'][0]['properties']['label']
    return address

def build_annonce_result(annonces):
    """Builds the HTML code to display the Recommandations in the right bottom corner

    Args:
        annonces (List(String)): List of element describing the house

    Returns:
        String: Formated String with the needed information
    """
    div = []
    for i, annonce in enumerate(annonces):
        div.append([])
        x = annonce[7]
        y = annonce[8]
        address = get_adress(x, y)
        if annonce[3] == 1:
            batiment = "Maison"
        else:
            batiment = "Appartement"
        
        div[i].append( address + "\n" + str(annonce[2]) + " €\n" + \
                    batiment + "\n" + \
                    str(annonce[4]) + "	㎡\n" + \
                    str(annonce[5]) + " pièces\n" +\
                    str(annonce[9]))
    return div

def annonce(request):
    """View for the annonce Page
        This will generate all the default forms, handle POST and GET request for the annonce page.
        It will also send the data to the RDS.

    Args:
        request (request): The request sent by the user

    Returns:
        render: Send the render to the client to render the annonce.hmtl with multiples variables that will be used to display data. 
    """
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
                    date_mutation = date.today().strftime("%Y-%m-%d")
                    message = form.data['message'].replace('\n', ' ').replace('from', '').replace('select', '').replace('drop', '').replace('database', '').replace(';', ':').replace(',', ' ')
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
                        message))
                    conn.commit()
                    print("Inserted")
            finally:
                conn.close()
                return redirect('/index/')
    else:
        form = AnnonceForm()
    return render(request, "annonce.html", {'form': form, 'coords': coords, 'styles': styles})
