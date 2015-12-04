__author__ = 'root'
#!/usr/bin/env python
# -*- coding: utf-8 -*-

from elasticsearch import Elasticsearch
import config

def host():
    return config.value(['elasticsearch', 'host'])

def port():
    return config.value(['elasticsearch', 'port'])

es = Elasticsearch([{'host': host(), 'port': port()}])

def index(index, type, id, object):
    res = es.index(index=index, doc_type=type, id=id, body=object)
    #log = 'Indexing Gensory - Type: ' + type + ' ID: ' + str(id)
    #print log
