'''
Created on May 31, 2014

@author: paul
'''
import os
import preprocessing, dataAnalysis, imageRetrieval

def runTitleProcessing(titlePosition):
    originalTitleFile = titlePosition + r"/imagelist.txt"
    sortedTitleFile = titlePosition + r"/sortedimagelist.txt"
    preprocessing.sortFileName(originalTitleFile, sortedTitleFile)
    imagelistCountFile = titlePosition + r"/imagelistcount.txt"
    preprocessing.countFileClass(originalTitleFile, imagelistCountFile)
    titleCountFile = titlePosition + r"/imagelistcount.txt"
    classifiedImagelistFile = titlePosition + r"/imagelistclassify.txt"
    preprocessing.classifyFiles(sortedTitleFile, titleCountFile, classifiedImagelistFile)
    trainImageTitleFile = titlePosition + r"/train.txt"
    testImageTitleFile = titlePosition + r"/test.txt"
    preprocessing.classifyFiles2(classifiedImagelistFile, trainImageTitleFile, testImageTitleFile)

dataRootPosition = r"data"
titleKind = "titleOfData1"
titlePosition = dataRootPosition + r"/" + titleKind
dataPosition = dataRootPosition + r"/" + titleKind
hiddenLayerNode = 40
maxIteration = 1000

def mergeData(mergeName, featureToMerge, hasTitles):
    #mergeData
    #the third term means result0001 to result0009
    featureDataPosition = dataPosition + r"/" + mergeName
    if not os.path.exists(featureDataPosition):
        os.makedirs(featureDataPosition)
    #FeatureToMerge = ["pHashFeature"] + ["color_feature"] + ["result000" + str(x) for x in range(1,10)]
    #hasTitles = [False] + [False] + [False] * 9
    
    DataToMerge = [dataPosition + r"/" + x + r"/" + x + "NewOrder" for x in featureToMerge]
    mergeFeatureFile = featureDataPosition + r"/" + mergeName + "NewOrder"    
    preprocessing.mergeFiles(mergeFeatureFile, *zip(DataToMerge, hasTitles))
    with open(featureDataPosition + r"/mergeInfo", "w+") as mergeInfoWriter:
        mergeInfoWriter.write(" ".join(featureToMerge) + "\n")

def runImageFeatureProcessing(featureKind, doesScale = False):

    oldFileOrder = titlePosition + r"/imagelist.txt"
    newFileOrder = titlePosition + r"/sortedimagelist.txt"
    classifiedTitleFile = titlePosition + r"/imagelistclassify.txt"
    trainTitleFile = titlePosition + r"/train.txt"
    testTitleFile = titlePosition + r"/test.txt"
    titleIndexFile = titlePosition + r"/titleIndex"
    
    featureDataPosition = dataPosition + r"/" + featureKind
    featureDataFile = featureDataPosition + r"/" + featureKind + "NewOrder"
    
    if doesScale:
        preprocessing.scaleDataForEveryDim(featureDataFile, doesDividedByDim = True)
    
    #process data
    #data have been sorted in the order of sortedimagelist
    dataFile = featureDataPosition + r"/" + featureKind + "NewOrder"
    #separate data to train data and test data by classifiedTitleFile
    preprocessing.separateData(newFileOrder, trainTitleFile, testTitleFile, dataFile, hasTitle = False)
    
    #process train data and test data for use in fann and so on
    trainDataFile = featureDataPosition + r"/" + featureKind + "NewOrderTrain"
    testDataFile = featureDataPosition + r"/" + featureKind + "NewOrderTest"
    
    trainFileTitle = preprocessing.getTrainFileTitle(trainDataFile, titleIndexFile)
    preprocessing.trainDataProcessing(trainDataFile, titleIndexFile, trainFileTitle, doesShuffle = True)
    preprocessing.testDataProcessing(testDataFile, titleIndexFile)

def mergeAndRun(doesScale = False):
    featureKind = "mergeFeature5"
    featureToMerge = ["color_feature"] + ["result0004"] + ["siftFeature2"] + ["result0001"]
    hasTitles = [False] * 4
    mergeData(featureKind, featureToMerge, hasTitles)
    runImageFeatureProcessing(featureKind, doesScale)

def runTrain(featureKind):
    dataFileFolder = dataPosition + r"/" + featureKind    
    dataFile = dataFileFolder + r"/" + featureKind + "NewOrderTrain2"
    
    with open(dataFile) as tempDataFileReader:
        firstLine = tempDataFileReader.readline()
        inputNode = int(firstLine.split()[1])
        outputNode = int(firstLine.split()[2])
    imageRetrieval.train(dataFile, 3, [inputNode, hiddenLayerNode, outputNode], maxIteration)
    #neural network has been saved in file

def recordTestResult(record):
    with open("resultRecord", "a") as resultRecordWriter:
        resultRecordWriter.write(record + "\n")

def runtest(featureKind):
    dataFileFolder = dataPosition + r"/" + featureKind
    annFile = dataFileFolder + r"/" + featureKind + "NewOrderTrain2.net"
    testFile = dataFileFolder + r"/" + featureKind + "NewOrderTest2"
    
    imageRetrieval.test(annFile, testFile)
    resultFile = dataFileFolder + r"/" + featureKind + "NewOrderTest2result"
    expectFile = dataFileFolder + r"/" + featureKind + "NewOrderTestExpected"
    result = dataAnalysis.resultCount(resultFile, expectFile)
    print(result)
    #record
    recordTestResult(" ".join([featureKind] + [titleKind] + [str(hiddenLayerNode)] + [str(maxIteration)] + [str(x) for x in result]))

featureKind = "mergeFeatureFinal1"

#featureToMerge = ["color_feature", "surfFeature", "result0003", "result0002", "result0006", "siftFeature2", "pHashFeature"]
featureToMerge = ["hsv1", "hsv2", "hsv3", "surfFeature", "wavelet2"]
hasTitles = [False] * 30

processingState = True
doesMerge = True
#only scale when new file is created
doesScale = doesMerge and False
if processingState:
    if doesMerge:
        mergeData(featureKind, featureToMerge, hasTitles)
    runImageFeatureProcessing(featureKind, doesScale)
else:
    runTrain(featureKind)
    runtest(featureKind)


