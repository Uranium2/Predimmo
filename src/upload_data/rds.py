import pymysql
import csv
import os

conn = pymysql.connect(
  host='predimmo.cbmo9oexrwuq.eu-west-1.rds.amazonaws.com',
  user='admin',
  password='N8XR3u#m9[5Mk6UK',
  port=3306)
print(conn)
cursor = conn.cursor()

cursor.execute('CREATE DATABASE IF NOT EXISTS predimmo;')

DATABASE_BODY = """
CREATE TABLE IF NOT EXISTS predimmo.predimmo(
    date_mutation varchar(30),
    valeur_fonciere int(11) DEFAULT NULL,
    code_postal int(11) DEFAULT NULL,
    code_commune int(11) DEFAULT NULL,
    type_local varchar(30),
    surface_reelle_bati int(11) DEFAULT NULL,
    nombre_pieces_principales int(11) DEFAULT NULL,
    surface_terrain int(11) DEFAULT NULL
)
"""
cursor.execute(DATABASE_BODY)
# cursor.execute("drop table predimmo.predimmo")

currentDirectory = os.path.dirname(os.path.realpath(__file__))
dataFilePath = currentDirectory + '\\..\\datasets\\'

f = csv.reader(open(dataFilePath + "vente_paris_2019.csv"))


args = []
sql = """INSERT INTO predimmo.predimmo(date_mutation, valeur_fonciere, code_postal, code_commune, type_local, surface_reelle_bati, nombre_pieces_principales, surface_terrain) VALUES("%s",%s,%s,%s,"%s",%s,%s,%s);\n"""
next(f)
for i, line in enumerate(f):
  line = line[0].split(";")
  line = [0 if x == '' else x for x in line]
  args.append(line)

  if i % 1000 == 0:
    print("Running... At line " + str(i))
    cursor.executemany(sql, args)
    conn.commit()
    args = []
cursor.executemany(sql, args)
conn.commit()



# cursor.execute("select * from predimmo.predimmo")
# res = cursor.fetchall()
# print(res)
cursor.close()