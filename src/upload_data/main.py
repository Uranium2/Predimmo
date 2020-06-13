import csv
import sys
import os
import re
import json
import requests
from elasticsearch import Elasticsearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth

currentDirectory = os.path.dirname(os.path.realpath(__file__))
dataFilePath = currentDirectory + '\\..\\datasets\\'

    

class ElasticSearchImporter(object):

    def __init__(self, YOUR_ACCESS_KEY, YOUR_SECRET_KEY): 
        host = 'search-predimmo-watswwwfxpozxbfaaasxu7ksym.eu-west-1.es.amazonaws.com'
        print(host)
        awsauth = AWS4Auth(YOUR_ACCESS_KEY, YOUR_SECRET_KEY, "eu-west-1", 'es')
        print(awsauth)
        es = Elasticsearch(
            hosts=[{'host': host, 'port': 443}],
            http_auth=awsauth,
            use_ssl=True,
            verify_certs=True,
            connection_class=RequestsHttpConnection
        )
        self.es = es

    def importToDb(self, fileName, indexDbName, indexType="default"):

        list = []
        headers = []
        index = 0

        f = open(dataFilePath+fileName, 'rt')
        reader = csv.reader(f)

        try:
            for i, row in enumerate(reader):
                try:
                    if(index == 0):
                        headers = row
                    else:
                        obj = {}
                        for j, val in enumerate(row):
                            obj[headers[j]] = val
                        print(headers)
                        self.es.index(index=indexDbName, body=obj, headers=headers)
                        
                        exit()
                        if i % 100 == 0:
                            print("Running... at ligne " + str(i))

                except Exception as e:
                    print(index)
                    print(e)
                    exit()
            
                index = index + 1
        except:
            print ('error')
        
        if not f.closed:
            f.close()

# date_mutation;valeur_fonciere;code_postal;code_commune;type_local;surface_reelle_bati;nombre_pieces_principales;surface_terrain

request_body = {
    "settings" : {
        "number_of_shards": 5,
        "number_of_replicas": 1
    },

    "mappings": {
        "properties": {
            "date_mutation": {"type": "keyword"},
            "valeur_fonciere": {"type": "integer"},
            "code_postal": {"type": "integer"},
            "code_commune": {"type": "integer"},
            "type_local": {"type": "keyword"},
            "surface_reelle_bati": {"type": "integer"},
            "nombre_pieces_principales": {"type": "integer"},
            "surface_terrain": {"type": "integer"}
        }
    }
}
index="logements"

ACCESS_KEY = "AKIAJWJKHI6WVWPQKSMA"
SECRET_KEY = "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"

importer = ElasticSearchImporter(ACCESS_KEY, SECRET_KEY)

importer.es.indices.delete(index=index, ignore=[400, 404])

importer.es.indices.create(index=index, body=request_body)

importer.importToDb("vente_paris_2019.csv", "logements", indexType="_doc")



# admin N8XR3u#m9[5Mk6UK
