import pandas as pd
import os
import numpy as np

script_dir = os.path.dirname(__file__)
csv_lbc = pd.read_csv(os.path.join(script_dir,"..\\datasets\\run_14_05_2020.csv"), header=None)

# supprimer col useless
del csv_lbc[1]
del csv_lbc[2]
del csv_lbc[4]

csv_lbc.columns = ["date_mutation", "valeur_fonciere", "code_postal", "type_local", "surface", "nombre_pieces_principales"]

# remove les data vide
csv_lbc['valeur_fonciere'] = csv_lbc['valeur_fonciere'].fillna(csv_lbc['valeur_fonciere'].mean())
csv_lbc = csv_lbc.fillna({'type_local':"Appartement"})
csv_lbc['nombre_pieces_principales'] = csv_lbc['nombre_pieces_principales'].fillna(csv_lbc['nombre_pieces_principales'].mean())
csv_lbc =  csv_lbc.fillna(0)
#garde les lignes avec une surface
csv_lbc = csv_lbc[csv_lbc['surface']>0]

csv_75 = pd.read_csv(os.path.join(script_dir,"..\\datasets\\vente_paris_2019.csv"), sep=";")
csv_75['surface_terrain'] = csv_75['surface_terrain'].fillna(csv_75['surface_terrain'].mean())
csv_75['valeur_fonciere'] = csv_75['valeur_fonciere'].fillna(csv_75['valeur_fonciere'].mean())
csv_75 =  csv_75.fillna(0)
# on garde la surface total en tant que surface
csv_75["surface"] = csv_75["surface_terrain"]

csv_75 = csv_75[csv_75['surface']>0]
csv_75 = csv_75[csv_75['valeur_fonciere']>100]

# del les truc uselss
del csv_75["code_commune"]
del csv_75["surface_reelle_bati"]
del csv_75["surface_terrain"]

#changement d'ordre des col pour un append
csv_75 = csv_75[["date_mutation", "valeur_fonciere", "code_postal", "type_local", "surface", "nombre_pieces_principales"]]

csv_append = csv_75.append(csv_lbc)
csv_append.reset_index()
csv_append = csv_append.astype({"valeur_fonciere": int, "code_postal": int, "surface": int, "nombre_pieces_principales": int})

# Changement de la date en colonnes
dates = csv_append["date_mutation"].str.split("/", n = 2, expand = True) 
dates.columns = ["day", "month", "year"]
del dates["day"]

#rajout a droite des cols de date et delete la date brute
csv_append = csv_append.join(dates)
del csv_append["date_mutation"]

# Type de bien en int
type_local = csv_append["type_local"].unique()
type_local_dict = dict(zip(type_local, range(len(type_local))))
csv_append = csv_append.replace(type_local_dict)

csv_append = csv_append.drop_duplicates()


csv_append.to_csv(os.path.join(script_dir,"..\\datasets\\lbc_75_append.csv"), index=False)

