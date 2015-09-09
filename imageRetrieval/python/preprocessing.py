'''
Created on May 29, 2014

@author: paul
'''

import itertools, os, random, shutil
from sets import Set
def sortFileName(filePath, resultPath):
    with open(filePath) as title, open(resultPath,'w+') as sortedTitle:
        content = title.readlines()
        #content contains the \n symbol
        content.sort()
        sortedTitle.writelines([x.strip() + "\r\n" for x in content if len(x.strip()) > 0])
        
def countFileClass(filePath, resultPath):
    with open(filePath) as title, open(resultPath,'w+') as titleCount:
        count = {}
        for line in title:
            if len(line.strip()) > 0:
                count.setdefault(line[:9],0)
                count[line[:9]] += 1
        for key in sorted(count.iterkeys()):
            titleCount.write(key + " " + str(count[key]) + "\n")
            
def classifyFiles(filePath, countPath, resultPath):

    
    titleCount = {}
    for line in open(countPath):
        if len(line.strip()) > 0:
            print(line.strip())
            key, value = tuple(line.split())
            titleCount[key] = int(value)
    markUpperCount = {}
    markLowerCount = {}
    for key in titleCount.keys():
        markUpperCount[key] = titleCount[key] / 10 * 10 + 10
        markLowerCount[key] = titleCount[key] / 10 * 9
    with open(filePath) as title, open(resultPath, 'w+') as titleClassify:
        tempMarkCount = {}
        for key in titleCount.keys():
            tempMarkCount[key] = 0
        for line in title:
            tempTitle = line[:9]
            if(markLowerCount[tempTitle] <= tempMarkCount[tempTitle] < markUpperCount[tempTitle]):
                titleClassify.write("tests " + line)                
            else:
                titleClassify.write("train " + line)
            tempMarkCount[tempTitle] += 1

def classifyFiles2(filePath, trainFiles, testFiles):

    with open(filePath) as titles, open(trainFiles,'w+') as trains, open(testFiles,"w+") as tests:
        for line in titles:
            if(line[:5] == "train"):
                trains.write(line[6:])
            else:
                tests.write(line[6:])

def resortData(oldOrderFile, newOrderFile, dataFile, hasTitle = False):
    newDataFile = dataFile + "NewOrder"
    dataMap = {}
    with open(oldOrderFile) as oldFileTitleReader, open(dataFile) as dataReader:
        if hasTitle:
            dataReader.readline()
        for title, data in itertools.izip(oldFileTitleReader, dataReader):
           dataMap[title] = data
    with open(newOrderFile) as newFileTitleReader, open(newDataFile, 'w+') as newDataWriter:
        for title in newFileTitleReader:
            newDataWriter.write(dataMap[title].strip() + "\n")

#data in dataFile should be sorted by resortData
def separateData(titleListFile, trainTitleFile, testTitleFile, dataFile, hasTitle = False):
    trainDataFile = dataFile + "Train"
    testDataFile = dataFile + "Test"
    #get the set of train data and test data
    with open(trainTitleFile) as trainTitleFileReader, open(testTitleFile) as testTitleFileReader:
        trainTitle = Set([x.strip() for x in trainTitleFileReader if len(x.strip()) > 0])
        testTitle = Set([x.strip() for x in testTitleFileReader if len(x.strip()) > 0])
    
    with open(titleListFile) as titleFileReader, open(dataFile) as dataFileReader:
        with open(trainDataFile, "w+") as trainDataWriter, open(testDataFile, "w+") as testDataWriter:
            for title, data in itertools.izip(titleFileReader, dataFileReader):
                if title.strip() in trainTitle:
                    trainDataWriter.write(title.strip() + " " + data)
                if title.strip() in testTitle:
                    testDataWriter.write(title.strip() + " " + data)

#parse file name and data into two different file
#trainTitle is the number of input, sensory, output neuron and so on in FANN data file
def trainDataProcessing(trainDataFile, titleIndexFile, trainTitle, doesShuffle = False):
    #read index of different title class
    titleIndexDictionary = {}
    with open(titleIndexFile) as titleIndexReader:
        for line in titleIndexReader:
            if len(line.strip()) > 0:
                titleIndexDictionary[line.split()[0]] = int(line.split()[1])
    
    #separate title and data to file that can be identified by FANN program
    trainDataFile2 = trainDataFile + "2"
    #trainData
    with open(trainDataFile) as trainDataFileReader, open(trainDataFile2, "w+") as trainDataFile2Writer:
        #the number of sensory, output, layer and so on
        trainDataFile2Writer.write(" ".join([str(x) for x in trainTitle]) + '\n')
        for line in trainDataFileReader:
            if not len(line.strip()) > 0:
                continue;
            indexOfUnderscore = line.find('_')
            indexOfSpace = line.find(' ')
            titleIndex = int(titleIndexDictionary[line[:indexOfUnderscore]])
            #output in FANN data has this format:
            networkOutput = [0] * len(titleIndexDictionary)
            networkOutput[titleIndex] = 1
            networkOutput = " ".join([str(x) for x in networkOutput]) + "\n"
            
            temp = line[indexOfSpace + 1:]
            temp2 = temp[:]
            trainDataFile2Writer.write(temp2.strip() + "\n")
            trainDataFile2Writer.write(networkOutput)
    if doesShuffle:
        with open(trainDataFile2) as trainDataFile2Reader:
            annTitle = trainDataFile2Reader.readline()
            trainDataFile2Content = trainDataFile2Reader.readlines()
        trainDataFile2Content = [x.strip() for x in trainDataFile2Content if len(x.strip()) > 0]
        trainDataFile2Content = list(zip(trainDataFile2Content[::2], trainDataFile2Content[1::2]))
        random.shuffle(trainDataFile2Content)
        #unzip zipped list to single list and add \n
        trainDataFile2Content = [x + "\n" for y in trainDataFile2Content for x in y]
        with open(trainDataFile2, "w+") as trainDataFile2Writer:
            trainDataFile2Writer.write(annTitle)
            trainDataFile2Writer.writelines(trainDataFile2Content)
        

def testDataProcessing(testDataFile, titleIndexFile):
    #read index of different title class
    titleIndexDictionary = {}
    with open(titleIndexFile) as titleIndexReader:
        for line in titleIndexReader:
            if len(line.strip()) > 0:
                titleIndexDictionary[line.split()[0]] = int(line.split()[1])
    
    #separate expected result and data to separated file
    testDataFile2 = testDataFile + "2"
    testDataResult = testDataFile + "Expected"
    with open(testDataFile) as testDataFileReader:
        with open(testDataResult, "w+") as testDataResultWriter, open(testDataFile2, "w+") as testDataFile2Writer:
            for line in testDataFileReader:
                indexOfUnderscore = line.find('_')
                indexOfSpace = line.find(' ')
                
                titleIndex = int(titleIndexDictionary[line[:indexOfUnderscore]])                
                networkOutput = str(titleIndex) + '\n'
                
                testDataFile2Writer.write(line[indexOfSpace + 1:])
                testDataResultWriter.write(networkOutput)

def getTrainFileTitle(trainDataFile, titleIndexFile, hasTitle = False):
    result = [None] * 3
    with open(titleIndexFile) as titleIndexFileReader:
        titleIndexFileContent = titleIndexFileReader.readlines()
        #number of output neuron
        result[2] = len([x for x in titleIndexFileContent if len(x.strip()) > 0])
    with open(trainDataFile) as trainDataFileReader:
        if hasTitle:
            trainDataFileReader.readline()
        #every element is element number in non-empty line
        trainDataFileStatistics = [len(x.split()) - 1 for x in trainDataFileReader if len(x.strip()) > 0]
        result[0] = len(trainDataFileStatistics) 
        result[1] = trainDataFileStatistics[0]
    return result

def _mergeTwoFile(dataFile1, dataFile2, resultFile, hasTitle1 = False, hasTitle2 = False):
    with open(dataFile1) as dataFile1Reader, open(dataFile2) as dataFile2Reader:
        with open(resultFile, "w+") as resultFileWriter:
            if hasTitle1:
                dataFile1Reader.readline()
            if hasTitle2:
                dataFile2Reader.readline()
            for line1, line2 in itertools.izip(dataFile1Reader, dataFile2Reader):
                if len(line1.strip()) > 0 and len(line2.strip()) > 0:
                    resultFileWriter.write(line1.strip() + " " + line2.strip() + "\n")

#every element in dataFile is a tuple (fileName, hasTitle)
def mergeFiles(resultFile, *dataFileTupleList):
    try:
        dataFileTupleList[0]
    except:
        raise
    else:
        dataFiles, hasTitles = tuple(zip(*dataFileTupleList))
        #create result file and copy first file into it
        with open(dataFiles[0]) as dataFiles0Reader, open(resultFile, "w+") as resultFileWriter:
            if hasTitles[0]:
                dataFiles0Reader.readline()
            resultFileWriter.writelines(dataFiles0Reader.readlines())
        #We need a temp file
        tempFile = resultFile + "_temp_"
        for i in range(1, len(dataFiles)):
            _mergeTwoFile(resultFile, dataFiles[i], tempFile, hasTitle1 = False, hasTitle2 = hasTitles[i])
            shutil.copy(tempFile, resultFile)

def scaleDataForEveryDim(dataFile, doesDividedByDim = False):
    with open(dataFile) as dataFileReader:
        data = dataFileReader.readlines()
    data = [x.split() for x in data if len(x.strip()) > 0]
    for i in range(len(data)):
        data[i][:] = [float(x) for x in data[i]]
    dim = len(data[0])
    maxNumber = [0] * dim
    for i in range(dim):
        maxNumber[i] = max([x[i] for x in data])
    for i in range(dim):
        for dataElement in data:
            dataElement[i] = dataElement[i] / maxNumber[i]
    if doesDividedByDim:
        for i in range(dim):
            for dataElement in data:
                dataElement[i] = dataElement[i] / dim * 3
    with open(dataFile, "w+") as dataFileWriter:
        for dataLine in data:
            dataFileWriter.write(" ".join([str(x) for x in dataLine]) + "\n")
def scaleDataForEveryDim2(dataFile):
    maxForEveryDim = getMaxForEveryDim(dataFile)
    pass
            
def getMaxForEveryDim(dataFile):
    with open(dataFile) as dataFileReader:
        data = dataFileReader.readlines()
    data = [x.split() for x in data if len(x.strip()) > 0]
    for i in range(len(data)):
        data[i][:] = [float(x) for x in data[i]]
    dim = len(data[0])
    maxNumber = [0] * dim
    for i in range(dim):
        maxNumber[i] = max([x[i] for x in data])
    print(maxNumber)
if __name__ == '__main__':
    dataFile = r"/home/paul/myProgram/homework/dataStructureAndAlgorithms2/project2/myImageRetrieval/myImageRetrieval/data/titleOfData1/result0005/result0005NewOrder"
    getMaxForEveryDim(dataFile)
        