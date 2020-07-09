import pymysql
import csv
import os

def get_conn():
    """ Get a connection to the RDS database

    Returns:
        pymysql.connect: Connection to the RDS database
    """
    return pymysql.connect(
        host='predimodbinstance.cbiog1ld7y5x.eu-west-1.rds.amazonaws.com',
        db='predimmo',
        user='admin',
        password='N8XR3u#m9[5Mk6UK',
        port=3306)

conn = get_conn()
cursor = conn.cursor()

cursor.execute('CREATE DATABASE IF NOT EXISTS predimmo;')

#date_mutation    valeur_fonciere    code_type_local    type_local    surface_reelle_bati    nombre_pieces_principales    surface_terrain    longitude    latitude
# cursor.execute("drop table if exists predimmo.data")
# cursor.execute("drop table if exists predimmo.data_django")
# cursor.execute("drop table if exists predimmo.prediction")

DATABASE_BODY = """
CREATE TABLE IF NOT EXISTS predimmo.data(
    date_mutation varchar(30),
    code_postal int(11) DEFAULT NULL,
    valeur_fonciere int(11) DEFAULT NULL,
    code_type_local int(11) DEFAULT NULL,
    surface_reelle_bati int(11) DEFAULT NULL,
    nombre_pieces_principales int(5) DEFAULT NULL,
    surface_terrain int(11) DEFAULT NULL,
    longitude Decimal(9,6) DEFAULT NULL,
    latitude Decimal(9,6) DEFAULT NULL
)
"""

cursor.execute(DATABASE_BODY)
cursor.execute("ALTER TABLE data ADD UNIQUE `unique_index`(date_mutation, code_postal, valeur_fonciere, code_type_local, surface_reelle_bati, nombre_pieces_principales, surface_terrain, longitude, latitude)")

DATABASE_BODY = """
CREATE TABLE IF NOT EXISTS predimmo.data_django(
    date_mutation varchar(30),
    code_postal int(11) DEFAULT NULL,
    valeur_fonciere int(11) DEFAULT NULL,
    code_type_local int(11) DEFAULT NULL,
    surface_reelle_bati int(11) DEFAULT NULL,
    nombre_pieces_principales int(5) DEFAULT NULL,
    surface_terrain int(11) DEFAULT NULL,
    longitude Decimal(9,6) DEFAULT NULL,
    latitude Decimal(9,6) DEFAULT NULL,
    message varchar(255)
)
"""

cursor.execute(DATABASE_BODY)
cursor.execute("ALTER TABLE data_django ADD UNIQUE `unique_index`(code_postal, valeur_fonciere, code_type_local, surface_reelle_bati, nombre_pieces_principales, surface_terrain, longitude, latitude)")


DATABASE_BODY = """
CREATE TABLE IF NOT EXISTS predimmo.prediction(
    code_postal int(11),
    prediction_1 int(11) DEFAULT NULL,
    prediction_3 int(11) DEFAULT NULL,
    prix_m2_appart int(11) DEFAULT NULL,
   prix_m2_maison int(11) DEFAULT NULL
)
"""

cursor.execute(DATABASE_BODY)
cursor.close()
