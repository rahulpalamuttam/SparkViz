import os
import sys

from pyspark import SparkContext
from Utilities import Reader, Sampling
from dateutil.parser import parse
# Path for spark source folder
os.environ['SPARK_HOME']="/home/rpalamut/spark-1.5.1"
#os.environ['SPARK_HOME']="/Users/nitesh/Developer/spark/spark-1.4.1"

# Append pyspark  to Python Path
sys.path.append("/home/rpalamut/spark-1.5.1/python")
#sys.path.append("/Users/nitesh/Developer/spark/spark-1.4.1/python")

DEFAULT_CACHE_SIZE = 10000
SAMPLE_SIZE = 1000
sc = SparkContext('local')
Point_RDD = None
coordinate_cache = None
flag_limit_reached = False


def __init__():
    global Point_RDD
    global coordinate_cache
    global SAMPLE_SIZE
    Point_RDD = sc.parallelize(Reader.twitterData(), 1)
    coordinate_cache = Point_RDD.takeSample(True, DEFAULT_CACHE_SIZE)


def __init__(sample_size):
    global Point_RDD
    global coordinate_cache
    global SAMPLE_SIZE
    Point_RDD = sc.parallelize(Reader.twitterData(), 1)
    coordinate_cache = Point_RDD.takeSample(True, DEFAULT_CACHE_SIZE)
    SAMPLE_SIZE = sample_size
    print coordinate_cache


def get_current():
    sample_array = Sampling.sample_unzip(coordinate_cache, SAMPLE_SIZE)
    return sample_array


def area(x_beg, x_end, y_beg, y_end):
    if y_beg is None or y_end is None:
        return 0
    return (x_end - x_beg) * (y_end - y_beg)

# def min_time():
#     Time_RDD = Point_RDD.map(lambda x, y, z, t: parse(t))
#     return Time_RDD.min()
#
# def max_time():
#     Time_RDD = Point_RDD.map(lambda x, y, z, t: parse(t))
#     return Time_RDD.max()

def sample_area(points):
    if len(points) == 0:
        return 0

    var_x = [x for x, y, z, t in points]
    var_y = [y for x, y, z, t in points]
    minx, maxx = min(var_x), max(var_x)
    miny, maxy = min(var_y), max(var_y)
    return area(minx, maxx, miny, maxy)


def fetch(x_beg, x_end, y_beg, y_end):
    global Point_RDD
    global coordinate_cache
    global DEFAULT_CACHE_SIZE

    filtered = filter(lambda pr: x_end > pr[0] > x_beg and y_end > pr[1] > y_beg, coordinate_cache)
    visible_area = area(x_beg, x_end, y_beg, y_end)
    s_area = sample_area(filtered)
    if s_area < visible_area/20:
        print "zooming out"

    print len(filtered)
    if len(filtered) < SAMPLE_SIZE or s_area <= visible_area/20:
        filtered_RDD = Point_RDD.filter(lambda pr: x_end > pr[0] > x_beg and y_end > pr[1] > y_beg)
        coordinate_cache = filtered_RDD.takeSample(False, DEFAULT_CACHE_SIZE)
        if len(coordinate_cache) < DEFAULT_CACHE_SIZE:
            flag_limit_reached = True
    filtered = filter(lambda pr: x_end > pr[0] > x_beg and y_end > pr[1] > y_beg, coordinate_cache)
    print len(filtered)
    return Sampling.sample_unzip(filtered, SAMPLE_SIZE)

