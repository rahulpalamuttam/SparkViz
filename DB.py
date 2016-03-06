import os
import sys
import random

# Path for spark source folder
os.environ['SPARK_HOME']="/home/rpalamut/spark-1.5.1"
#os.environ['SPARK_HOME']="/Users/nitesh/Developer/spark/spark-1.4.1"



# Append pyspark  to Python Path
sys.path.append("/home/rpalamut/spark-1.5.1/python")

#sys.path.append("/Users/nitesh/Developer/spark/spark-1.4.1/python")

from pyspark import SparkContext

import Reader
import Sampling

DEFAULT_CACHE_SIZE = 10000
sc = SparkContext('local')
Point_RDD = None
coordinate_cache = None

flag_limit_reached = False

def __init__():
    global Point_RDD
    global coordinate_cache
    Point_RDD = sc.parallelize(Reader.twitterData(), 1)
    coordinate_cache = Point_RDD.takeSample(True, DEFAULT_CACHE_SIZE)
    print coordinate_cache

def getCurrent(sample_size):
    var_sampleArray = Sampling.sample_unzip(coordinate_cache, sample_size)
    return var_sampleArray

def area(xbeg, xend, ybeg, yend):
    if(ybeg == None or yend == None):
        return 0

    return (xend - xbeg) * (yend - ybeg)

def sample_area(points):
    if(len(points) == 0):
        return 0

    var_x = [x for x,y,z in points]
    var_y = [y for x,y,z in points]
    minx, maxx = min(var_x), max(var_x)
    miny, maxy = min(var_y), max(var_y)
    return area(minx, maxx, miny, maxy)

def fetch(xbeg, xend, ybeg, yend, sample_size):
    global Point_RDD
    global coordinate_cache
    global flag_limit_reached

    filtered = filter(lambda pr: xend > pr[0] > xbeg and yend > pr[1] > ybeg, coordinate_cache)
    visible_area = area(xbeg, xend, ybeg, yend)
    s_area = sample_area(filtered)
    t = coordinate_cache
    if s_area < visible_area/100:
        print "zooming out"

    print len(filtered)
    if len(filtered) < sample_size or s_area <= visible_area/100:
        coordinate_cache = Point_RDD.filter(lambda pr: xend > pr[0] > xbeg and yend > pr[1] > ybeg).takeSample(False, DEFAULT_CACHE_SIZE)
        if len(coordinate_cache) < DEFAULT_CACHE_SIZE:
            flag_limit_reached = True
    filtered = filter(lambda pr: xend > pr[0] > xbeg and yend > pr[1] > ybeg, coordinate_cache)
    print len(filtered)
    return Sampling.sample_unzip(filtered, sample_size)

