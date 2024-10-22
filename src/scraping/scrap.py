import pandas as pd
from bs4 import BeautifulSoup
import requests
from csv import writer
import os
from datetime import datetime

# !pip install fake-useragent

url_ref = "https://www.leboncoin.fr"
url = "https://www.leboncoin.fr/_immobilier_/offres/ile_de_france/"
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

url_page = "https://www.leboncoin.fr/_immobilier_/offres/ile_de_france/p-{}/"



def append_list_as_row(file_path, l):
    """ Appends a list in a file

    Args:
        file_path (String): File path 
        l (String): List of data to appends
    """
    script_dir = os.path.dirname(__file__)
    abs_file_path = os.path.join(script_dir, file_path)
    with open(abs_file_path, 'a+', newline='', encoding='utf-8') as write_obj:
        csv_writer = writer(write_obj)
        csv_writer.writerow(l)

def scrap_page(url, date):
    """Scrap the URL to get all the values of posts inside it. It will travel to all links to find all values.

    Args:
        url (String): http URL
        date (String): Todays day to happend in the data: "%d/%m/%Y"
    """
    response = requests.get(url, headers=headers)
    if (response.status_code != 200):
        return
    soup = BeautifulSoup(response.text, 'html.parser')

    list_immo = []
    for a in soup.find_all('a', href=True):
        list_immo.append(a['href'])


    list_immo = [x for x in list_immo if "ventes_immobilieres" in x]
    list_immo = [x for x in list_immo if not "offres" in x]
    
    for elm in list_immo:
        # store all info inside values_col and append to file
        values_col = []
        values_col.append(date)

        build_url = url_ref + elm

        response_immo = requests.get(build_url, headers=headers)
        soup_immo = BeautifulSoup(response_immo.text, 'html.parser')

        # Description
        description = soup_immo.find("span", class_="_1fFkI").text
        # print(description)
        # Price
        try:
            price = int(soup_immo.find("span", class_="_3Ce01 _3gP8T _25LNb _35DXM").text.replace("€", "").replace(" ", ""))
            # print(price)
        except:
            print(build_url + " => No price")
            continue

        
        # Localisation city + zip code
        localisation_all = soup_immo.find_all("h2", class_="Roh2X _3c6yv _25dUs _21rqc _3QJkO _1hnil _1-TTU _35DXM")[2]

        city = localisation_all.text.split("(")[0]
        # print(city)
        zip_code = localisation_all.text.split("(")[-1].split(")")[0]
        # print(zip_code)


        values_col.append(build_url)
        values_col.append(description)
        values_col.append(price)
        values_col.append(city)
        values_col.append(zip_code)

        div_key_value = soup_immo.find_all("p", class_="_2k43C _1pHkp _137P- P4PEa _3j0OU")

        for div in div_key_value:
            if (div.text == "Type de bien"):
                values_col.append(div.findNext("p").text)
            if (div.text == "Surface"):
                values_col.append(div.findNext("p").text.split(" ")[0])
            if (div.text == "Pièces"):
                values_col.append(div.findNext("p").text)

        # Writte to csv
        append_list_as_row("..\\datasets\\run_14_05_2020.csv", values_col)




        
date = datetime.now().strftime("%d/%m/%Y")
size = 100
for i in range(2, size):
    scrap_page(url_page.format(i), date)
    print(str(i) + " / " + str(size))









