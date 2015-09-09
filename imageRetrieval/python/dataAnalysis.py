'''
Created on Jun 1, 2014

@author: paul
'''

import numpy as np
import scipy.linalg
import matplotlib as mpb
import itertools
import random
import pyfann.libfann
def svdPlot(DataFile):
    pass

def resultCount(resultFile, expectFile):
    trueResult, falseResult = 0, 0
    analysisDebug = resultFile + "analysisDebug"
    with open(resultFile) as resultFileReader, open(expectFile) as expectFileReader:
        with open(analysisDebug, "w+") as analysisDebug:
            for line1, line2 in itertools.izip(resultFileReader, expectFileReader):
                #output file has more than one format in this program, this could hand them all
                temp = line1.split()
                if temp[len(temp) - 1] == line2.strip():
                    trueResult += 1
                    analysisDebug.write("hit" + "\n")
                else:
                    falseResult += 1
                    analysisDebug.write("miss" + "\n")
    return (trueResult, falseResult, float(trueResult) / float(trueResult + falseResult))

def getRandomData(filePath, dim, totalNumber):
    with open(filePath, "w+") as filePathWriter:
        for i in range(totalNumber):
            randomData = [None] * dim
            for i in range(dim):
                randomData[i] = random.uniform(0, 10**(i / 4))
            filePathWriter.write(" ".join([str(x) for x in randomData]) + "\n")
def scaleData(DataPath):
    trainData = pyfann.libfann.training_data()
    trainData.read_train_from_file(DataPath)
    trainData.scale_train_data(0,100)
    trainData.save_train(DataPath + "scale")
def isDataMatrix(filePath, row, column):
    with open(filePath) as dataFileReader:
        content = dataFileReader.readlines()
    content = [x.split() for x in content if len(x.strip()) > 0]
    for i in range(len(content)):
        content[i] = [float(x) for x in content[i]]
    if len(content) == row:
        for row in content:
            if len(row) == column:
                pass
            else:
                print(row)
                return False
    else:
        return False

if __name__ == '__main__':
    resultFile = r"../runImageRetrieval/result"
    expectFile = r"data/titleOfData1/test/testNewOrderTestExpected"
    resultRecord2 = r"resultRecord2"
    result = resultCount(resultFile, expectFile)
    with open(resultRecord2, "a+") as resultRecordWriter:
        resultRecordWriter.write(" ".join([str(x) for x in result]) + "\n")
    print(result)

#===============================================================================
#  dataFilePath = r"/home/paul/myProgram/homework/dataStructureAndAlgorithms2/project2/myImageRetrieval/myImageRetrieval/data/titleOfData1/mergeFeatureFinal1/mergeFeatureFinal1NewOrder"
# print(isDataMatrix(dataFilePath, 5613, 146))
#===============================================================================
