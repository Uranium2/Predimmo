import pandas as pd
from bs4 import BeautifulSoup
import requests
from csv import writer
# !pip install fake-useragent

url_ref = "https://www.leboncoin.fr"
url = "https://www.leboncoin.fr/_immobilier_/offres/ile_de_france/"
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

url_page = "https://www.leboncoin.fr/_immobilier_/offres/ile_de_france/p-{}/"



def append_list_as_row(file_path, l):
    with open(file_path, 'a+', newline='', encoding='utf-8') as write_obj:
        csv_writer = writer(write_obj)
        csv_writer.writerow(l)

def scrap_page(url):
    response = requests.get(url, headers=headers)

    soup = BeautifulSoup(response.text, 'html.parser')

    list_immo = []
    for a in soup.find_all('a', href=True):
        list_immo.append(a['href'])


    list_immo = [x for x in list_immo if "ventes_immobilieres" in x]
    list_immo = [x for x in list_immo if not "offres" in x]

    for elm in list_immo:
        # store all info inside values_col and append to file
        values_col = []

        build_url = url_ref + elm

        response_immo = requests.get(build_url, headers=headers)
        soup_immo = BeautifulSoup(response_immo.text, 'html.parser')
        div_key_value = soup_immo.find_all("div", class_="_2B0Bw _1nLtd")

        # Description
        description = soup_immo.find("span", class_="content-CxPmi").text
        # Price
        try:
            price = int(soup_immo.find("span", class_="_1F5u3").text.replace("€", "").replace(" ", ""))
        except:
            print(build_url + " => No price")
            continue
        

        # Localisation city + zip code
        localisation_all = soup_immo.find("div", class_="_1aCZv").contents[0].text
        city = " ".join(localisation_all.split(" ")[:-1])
        zip_code = localisation_all.split(" ")[-1]


        values_col.append(build_url)
        values_col.append(description)
        values_col.append(price)
        values_col.append(city)
        values_col.append(zip_code)

        for t in div_key_value:
            list_key = [""] * 7

            key = t.find("div", class_="_3-hZF").text
            value = t.find("div", class_="_3Jxf3").text

            if (key == "Type de bien"):
                list_key[0] = value
            if (key == "Surface"):
                list_key[1] = value
            if (key == "Pièces"):
                list_key[2] = value
            if (key == "Classe énergie"):
                list_key[3] = value
            if (key == "GES"):
                list_key[4] = value
            if (key == "Référence"):
                list_key[5] = value
            if (key == "Honoraires"):
                list_key[6] = value

        # Concat lists
        values_col = values_col + list_key
        # Writte to csv
        append_list_as_row("C:\\Users\\taver\\Desktop\\test.csv", values_col)




        

size = 100000
for i in range(2, size):
    scrap_page(url_page.format(i))
    print(str(i) + " / " + str(size))









