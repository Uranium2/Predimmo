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
    def importToDb(self, fileName, indexDbName, YOUR_ACCESS_KEY, YOUR_SECRET_KEY, indexType="default"):
        host = 'search-predimmo-vzmz45q4vkntbsg5r2t7mlvlwm.eu-west-1.es.amazonaws.com'
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
        list = []
        headers = []
        index = 0

        f = open(dataFilePath+fileName, 'rt')
        reader = csv.reader(f)

        try:
            for i, row in enumerate(reader):
                print(row)
                try:
                    if(index == 0):
                        headers = row
                    else:
                        obj = {}
                        for i, val in enumerate(row):
                            obj[headers[i]] = val
                        es.index(index=indexDbName, doc_type=indexType, body=obj)

                except Exception as e:
                    print(index)
                    print(e)
            
                index = index + 1
        except:
            print ('error')
        
        if not f.closed:
            f.close()

importer = ElasticSearchImporter()
YOUR_ACCESS_KEY = "AKIAJWJKHI6WVWPQKSMA"
YOUR_SECRET_KEY = "S6W4yaPSXU6bzLI5fU6jrUQILUgUPqYYhh9Bk/5e"
importer.importToDb("idf.csv", "logements", YOUR_ACCESS_KEY, YOUR_SECRET_KEY, indexType="default")
