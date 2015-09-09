'''
Created on Jun 10, 2014

@author: paul
'''

import preprocessing

oldOrderFile = r"data/titleOfData1/imagelist.txt"
newOrderFile = r"data/titleOfData1/sortedimagelist.txt"
dataFile = r"data/titleOfData1/hsv3/hsv3"
preprocessing.resortData(oldOrderFile, newOrderFile, dataFile)