import csv
import sys
import os
import re
import json
import requests
from elasticsearch import Elasticsearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth

def my_query():
    YOUR_ACCESS_KEY = "AKIAJWJKHI6WVWPQKSMA"
    YOUR_SECRET_KEY = "S6W4yaPSXU6bzLI5fU6jrUQILUgUPqYYhh9Bk/5e"

    host = 'search-predimmo-vzmz45q4vkntbsg5r2t7mlvlwm.eu-west-1.es.amazonaws.com'

    awsauth = AWS4Auth(YOUR_ACCESS_KEY, YOUR_SECRET_KEY, "eu-west-1", 'es')

    es = Elasticsearch(
        hosts=[{'host': host, 'port': 443}],
        http_auth=awsauth,
        use_ssl=True,
        verify_certs=True,
        connection_class=RequestsHttpConnection
    )

    res = es.search(index="logements", body={"query":{"match_all": {}}})

    return res
