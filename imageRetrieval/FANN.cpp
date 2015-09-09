/*
 * runImageRetrieval.cpp
 *
 *  Created on: Jun 5, 2014
 *      Author: paul
 */

#include <fann.h>
#include <string>
#include <vector>
#include <fstream>
#include <iostream>
#include <map>
#include <string.h>
#include <stdlib.h>
#include "FANN.h"
using std::vector;
using std::string;
using std::ifstream;
using std::map;


FANN::~FANN()
{
	//delete[] brain.fHSV1;			//(H, S, V) = (8, 8, 0)
	//delete[] brain.fHSV2;			//(H, S, V) = (6, 6, 6)
	//delete[] brain.fHSV3;			//(H, S, V) = (18, 12, 6)
	//delete[] brain.fSurf;			//dim of SurfFeature is 24
	//delete[] brain.fWaveLet;		//dim of fWaveLet is 64
	//delete[] brain.fPixel;     
}

void FANN::establishFANN()
{
	brain.Initial();
	char annFileName[] = "ann.net";

	body = fann_create_from_file(annFileName);
}

vector<string> FANN::SingleQuery(char* pictureFileName)
{
	fann_type* output;
	fann_type* data = new fann_type[brain.totalDim];

	brain.runFeature(pictureFileName);

	for (int i = 0; i < brain.totalDim; i++)
		data[i] = brain.fTotal[i];

	output = fann_run(body, data);

	int resultIndex = getMaxIndex(output, fann_get_num_output(body));
	vector<string> result = findImage(resultIndex);

	return result;
}

vector<string> FANN::findImage(int index)
{
	ifstream dimReader("dataForSorting/dimension");
	//The title index is integer. change this if use string title to search
	//read index and dimension at the same time
	int tempIndex, tempDimension, tempElementNumber;
	while(!dimReader.eof())
	{
		dimReader>>tempIndex>>tempDimension>>tempElementNumber;
		if(tempIndex == index)
			break;
	}
	int dimension = tempDimension;
	int elementNumber = tempElementNumber;

	map<double, string> dataMap;
	string titleFile = string("dataForSorting/titleClass") + IR_to_string(index);
	string dataFile = string("dataForSorting/dataClass") + IR_to_string(index);
	ifstream titleReader(titleFile.c_str()), dataReader(dataFile.c_str());
	for(int i = 0 ; i < elementNumber ; i++)
	{
		string tempTitle;
		titleReader>>tempTitle;
		vector<double> tempData = vector<double>(dimension, 0);
		for(int j = 0 ; j < dimension ; j++)
			dataReader>>tempData[j];
		double distance = 0;
		for(int j = 0 ; j < dimension ; j++)
			distance += (brain.fHSV1[j] - tempData[j]) * (brain.fHSV1[j] - tempData[j]);
		dataMap[distance] = tempTitle;
	}

	vector<string> result(10, string());
	map<double, string>::iterator it;
	int j = 0;
	for(it = dataMap.begin() ; j < 10 ; j++, it++)
		result[j] = it->second;

	return result;
}

int FANN::getMaxIndex(fann_type* output, int outputNodeNum)
{
	fann_type max = -1e20;
	int maxIndex = -1;
	for(int i = 0 ; i < outputNodeNum ; i++)
		if(output[i] > max)
		{
			max = output[i];
			maxIndex = i;
		}
	return maxIndex;
}

void FANN::annTrain(char* annTrainFilePath, int inputNode, int hiddenNode, int outputNode, char* resultFilePath)
{
	fann* ann;
	fann_type desiredError = 1e-2;
	int maxIteration = 1000;
	int iterationBetweenReports = 10;
	const unsigned int layerArray[3] = {inputNode,hiddenNode,outputNode};
	ann = fann_create_standard_array(3, layerArray);
	fann_set_learning_rate(ann, 0.7);
	fann_set_activation_function_output(ann, FANN_SIGMOID_SYMMETRIC_STEPWISE);
	fann_set_activation_function_hidden(ann, FANN_SIGMOID_SYMMETRIC_STEPWISE);
	fann_train_on_file(ann, annTrainFilePath, maxIteration, iterationBetweenReports, desiredError);
	fann_save(ann, resultFilePath);
}

string IR_to_string(int index)
{//could only handle 0 to 9
	string result = string(1, '\0');
	result[0] = index + '0';
	return result;
}

