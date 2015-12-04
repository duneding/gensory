__author__ = 'root'
import unicodedata

def normalizeText(text):
    unicodedata.normalize('NFKD', text).encode('ascii','ignore')