'''
Created on May 31, 2014

@author: paul
'''

import pyfann.libfann as libfann
import dataAnalysis

def train(trainFile, layerNumber, neuronNumber, maxIteration):
    desiredError = 1e-2
    #maxIteration = 1000
    iterationBetweenReports = 100
    ann = libfann.neural_net()
    ann.create_standard_array(tuple(neuronNumber))
    ann.set_learning_rate(0.7)
    ann.set_activation_function_output(libfann.SIGMOID_SYMMETRIC_STEPWISE)
    ann.set_activation_function_hidden(libfann.SIGMOID_SYMMETRIC_STEPWISE)
    ann.train_on_file(trainFile, maxIteration, iterationBetweenReports, desiredError)
    ann.save(trainFile + ".net")

def test(annFile, testFile):
    ann = libfann.neural_net()
    ann.create_from_file(annFile)
    resultFile = testFile + "result"
    with open(testFile) as testFileReader, open(resultFile, "w+") as resultFileWriter:
        for line in testFileReader:
            if len(line.strip()) > 0:
                tempResult = ann.run([float(x) for x in line.split()])
                tempImageClass = tempResult.index(max(tempResult))
#                resultFileWriter.write(str(tempImageClass) + "\n")
                resultFileWriter.write(" ".join([str(x) for x in tempResult]) + " " + str(tempImageClass) + "\n")


