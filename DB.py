import os
import sys
import random

# Path for spark source folder
os.environ['SPARK_HOME']="/home/rpalamut/spark-1.5.1"

# Append pyspark  to Python Path
sys.path.append("/home/rpalamut/spark-1.5.1/python")

from pyspark import SparkContext

import Reader
import Sampling

DEFAULT_CACHE_SIZE = 10000
sc = SparkContext('local')
Point_RDD = None
coordinate_cache = None

def __init__():
    global Point_RDD
    global coordinate_cache
    Point_RDD = sc.parallelize(Reader.coordinates(), 1)
    coordinate_cache = Point_RDD.takeSample(True, DEFAULT_CACHE_SIZE)

def getCurrent(sample_size):
    var_sampleArray = Sampling.sample_unzip(coordinate_cache, sample_size)
    return var_sampleArray

def fetch(xbeg, xend, ybeg, yend, sample_size):
    global Point_RDD
    global coordinate_cache

    filtered = filter(lambda pr: xend > pr[0] > xbeg and yend > pr[1] > ybeg, coordinate_cache)
    print len(filtered)
    if len(filtered) < sample_size:
        coordinate_cache = Point_RDD.filter(lambda pr: xend > pr[0] > xbeg and yend > pr[1] > ybeg).takeSample(False, DEFAULT_CACHE_SIZE)
    filtered = filter(lambda pr: xend > pr[0] > xbeg and yend > pr[1] > ybeg, coordinate_cache)
    print len(filtered)
    return Sampling.sample_unzip(filtered, sample_size)

