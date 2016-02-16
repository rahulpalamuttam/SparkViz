import pandas as pd
import DictionaryReader
CONST_PATH_TO_FILE = 'resources/ghcnd-stations.txt'
CONST_PATH_TO_TWITTER= 'resources/dataless.text'

colspecs = [(0, 11), (11, 21), (21, 31), (31, 38),(39,41),(41,72),(72,76),(76,80),(80,86)]
stations = pd.read_fwf(CONST_PATH_TO_FILE, colspecs=colspecs, header=None, index_col=0,
                       names=['latitude','longitude','elevation','state','name','GSNFLAG','HCNFLAG','WMOID'])

def lats():
    return [i for i in stations['latitude']]


def lons():
    return [i for i in stations['longitude']]


def coordinates():
    subset = stations[['longitude', 'latitude']]
    return [tuple(i) for i in subset.values]

def twitterData():
    tupleList = DictionaryReader.tuplize(CONST_PATH_TO_TWITTER)
    return tupleList

twitterData()