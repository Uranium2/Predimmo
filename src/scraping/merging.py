import pandas as pd
import os

script_dir = os.path.dirname(__file__)
csv_lbc = pd.read_csv(os.path.join(script_dir,"..\\datasets\\run_14_05_2020.csv"), header=None)

del csv_lbc[1]
del csv_lbc[2]
del csv_lbc[4]

csv_lbc =  csv_lbc.fillna(0)
csv_lbc.columns = ["date_mutation", "valeur_fonciere", "code_postal", "type_local", "surface", "nombre_pieces_principales"]
csv_lbc = csv_lbc[csv_lbc['surface']>0]

csv_75 = pd.read_csv(os.path.join(script_dir,"..\\datasets\\vente_paris_2019.csv"), sep=";")
csv_75 =  csv_75.fillna(0)

csv_75["surface"] = csv_75["surface_reelle_bati"] + csv_75["surface_terrain"]

csv_75 = csv_75[csv_75['surface']>0]


del csv_75["code_commune"]
del csv_75["surface_reelle_bati"]
del csv_75["surface_terrain"]

csv_75 = csv_75[["date_mutation", "valeur_fonciere", "code_postal", "type_local", "surface", "nombre_pieces_principales"]]

csv_append = csv_75.append(csv_lbc)
csv_append.reset_index()
csv_append = csv_append.astype({"valeur_fonciere": int, "code_postal": int, "surface": int, "nombre_pieces_principales": int})
print(csv_append)
csv_append.to_csv(os.path.join(script_dir,"..\\datasets\\lbc_75_append.csv"), index=False)
