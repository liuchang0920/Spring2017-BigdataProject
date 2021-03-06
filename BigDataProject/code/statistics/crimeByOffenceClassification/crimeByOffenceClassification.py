import sys
import os
import sys
import os
from pyspark import SparkContext
from operator import add
import csv

def readfile(input):
    csvreader = csv.reader(input)
    next(csvreader)
    return csvreader

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print "usage: inputfile outputfile"
        exit(-1)

    sc = SparkContext()
    crime_data = sc.textFile(sys.argv[1]).mapPartitions(readfile)
    offence_classification = crime_data.map(lambda x: x[7] if x[7] != "" else "999").map(lambda x:(x, 1))
    offence_classification_count = offence_classification.reduceByKey(add).sortByKey().map(lambda x: "%s\t%s" % (x[0], x[1]))
    offence_classification_count.saveAsTextFile(sys.argv[2])
    sc.stop()
