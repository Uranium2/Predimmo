import pymysql
import csv
import os

conn = pymysql.connect(
  host='predimodbinstance.cbiog1ld7y5x.eu-west-1.rds.amazonaws.com',
  user='admin',
  password='N8XR3u#m9[5Mk6UK',
  port=3306)
print(conn)
cursor = conn.cursor()

cursor.execute('CREATE DATABASE IF NOT EXISTS predimmo;')

#date_mutation    valeur_fonciere    code_type_local    type_local    surface_reelle_bati    nombre_pieces_principales    surface_terrain    longitude    latitude
# cursor.execute("drop table if exists predimmo.data")
# cursor.execute("drop table if exists predimmo.data_django")
# cursor.execute("drop table if exists predimmo.prediction")

DATABASE_BODY = """
CREATE TABLE IF NOT EXISTS predimmo.data(
    date_mutation varchar(30),
    valeur_fonciere int(11) DEFAULT NULL,
    code_type_local int(11) DEFAULT NULL,
    type_local varchar(30),
    surface_reelle_bati int(11) DEFAULT NULL,
    nombre_pieces_principales int(5) DEFAULT NULL,
    surface_terrain int(11) DEFAULT NULL,
    longitude Decimal(9,6) DEFAULT NULL,
    latitude Decimal(9,6) DEFAULT NULL
)
"""

cursor.execute(DATABASE_BODY)
cursor.execute("ALTER TABLE predimmo.data ADD UNIQUE `unique_index`(date_mutation, valeur_fonciere, code_type_local, type_local, surface_reelle_bati, nombre_pieces_principales, surface_terrain, longitude, latitude)")

DATABASE_BODY = """
CREATE TABLE IF NOT EXISTS predimmo.data_django(
    date_mutation varchar(30),
    valeur_fonciere int(11) DEFAULT NULL,
    code_type_local int(11) DEFAULT NULL,
    type_local varchar(30),
    surface_reelle_bati int(11) DEFAULT NULL,
    nombre_pieces_principales int(5) DEFAULT NULL,
    surface_terrain int(11) DEFAULT NULL,
    longitude Decimal(9,6) DEFAULT NULL,
    latitude Decimal(9,6) DEFAULT NULL,
    message varchar(255)
)
"""

cursor.execute(DATABASE_BODY)
cursor.execute("ALTER TABLE predimmo.data_django ADD UNIQUE `unique_index`(date_mutation, valeur_fonciere, code_type_local, type_local, surface_reelle_bati, nombre_pieces_principales, surface_terrain, longitude, latitude)")


DATABASE_BODY = """
CREATE TABLE IF NOT EXISTS predimmo.prediction(
    code_postal int(11),
    prediction int(11) DEFAULT NULL
)
"""

cursor.execute(DATABASE_BODY)
cursor.close()