'''
Created on Jun 8, 2014

@author: paul
'''

def separateData(dataFile, titleCount, resultFolder):
    with open(dataFile) as dataFileReader:
        content = dataFileReader.readlines()
    content = [x.strip() for x in content if len(x.strip()) > 0]
    
    count = []
    with open(titleCount) as titleCountReader:
        for line in titleCountReader:
            if len(line.strip()) > 0:
                count.append(int(line.split()[1]))
    print(count)
    countSum = [0] * (len(count) + 1)
    for i in range(len(count)):
        countSum[i] = sum(count[0:i])
    countSum[len(countSum) - 1] = 5613
    for i in range(len(countSum)):
        countSum[i] += 1
    print(countSum)
    for i in range(len(count)):
        tempContent = content[countSum[i]:countSum[i + 1]]
        print(tempContent)
        #=======================================================================
        # with open(resultFolder + r"/result000" + str(i), "a+") as resultFileWriter:
        #     tempContent2 = [x + "\n" for x in tempContent]
        #     resultFileWriter.writelines(tempContent2)
        #=======================================================================
    
dataFile = r"/home/paul/myProgram/homework/dataStructureAndAlgorithms2/project2/myImageRetrieval/result0003ScaleNewOrder"
titleCount = r"/home/paul/myProgram/homework/dataStructureAndAlgorithms2/project2/myImageRetrieval/myImageRetrieval/data/titleOfData1/imagelistcount.txt"
resultFolder = r"/home/paul/myProgram/homework/dataStructureAndAlgorithms2/project2/myImageRetrieval"
separateData(dataFile, titleCount, resultFolder)