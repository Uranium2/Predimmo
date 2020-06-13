import pymysql
import csv
import os
import datetime
import requests
import gzip
import csv
import pandas as pd

conn = pymysql.connect(
  host='predimodbinstance.cbiog1ld7y5x.eu-west-1.rds.amazonaws.com',
  user='admin',
  password='N8XR3u#m9[5Mk6UK',
  port=3306)

cursor = conn.cursor()

currentDirectory = os.path.dirname(os.path.realpath(__file__))
now = datetime.datetime.now()


url_cadastre = "https://cadastre.data.gouv.fr/data/etalab-dvf/latest/csv/{}/departements/".format(now.year - 1)
print(url_cadastre)

filename = "75.csv.gz"
r = requests.get(url_cadastre + filename, allow_redirects=True)

local_csv = os.path.join(currentDirectory, filename)
open(local_csv, 'wb').write(r.content)

with gzip.open(local_csv, mode="rt", encoding='utf-8') as f:
    df = pd.read_csv(f)
    
    df = df[["date_mutation", "valeur_fonciere", "code_type_local", "type_local", "surface_reelle_bati", "nombre_pieces_principales", "surface_terrain", "longitude", "latitude"]]
    df = df.fillna(0)

    args = []
    cols = ",".join([str(i) for i in df.columns.tolist()])
    for i, row in df.iterrows():
        sql = "INSERT INTO predimmo.data(" +cols + ") VALUES (" + "%s,"*(len(row)-1) + "%s)"


        cursor.execute(sql, tuple(row))

        # the connection is not autocommitted by default, so we must commit to save our changes
        if i % 100 == 0:
            print("Running... at line " + str(i))
        conn.commit()















#     sql = """INSERT INTO predimmo.predimmo(date_mutation, valeur_fonciere, code_postal, code_commune, type_local, surface_reelle_bati, nombre_pieces_principales, surface_terrain) VALUES("%s",%s,%s,%s,"%s",%s,%s,%s);\n"""
#     next(f)
#     for i, line in enumerate(f):
#       line = line[0].split(";")
#       line = [0 if x == '' else x for x in line]
#       args.append(line)

#       if i % 1000 == 0:
#         print("Running... At line " + str(i))
#         cursor.executemany(sql, args)
#         conn.commit()
#         args = []
#     cursor.executemany(sql, args)
#     conn.commit()



#     cursor.execute("select * from predimmo.predimmo")
#     res = cursor.fetchall()
#     print(res)

# cursor.close()