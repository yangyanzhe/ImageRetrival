/*
 * runImageRetrieval.h
 *
 *  Created on: Jun 5, 2014
 *      Author: paul
 */
#ifndef RUNIMAGERETRIEVAL_H_
#define RUNIMAGERETRIEVAL_H_
#include <fann.h>
#include "Feature.h"
using std::vector;
using std::string;

class FANN
{
public:
	FANN(){}
	~FANN();

public:
	Feature brain;
	fann* body;

public:
	void establishFANN();
	vector<string> SingleQuery(char* pictureFileName);

	vector<string> findImage(int index);
	vector<vector<string> > getTitle(string imageTitleListPath, string titleIndexPath);
	int getMaxIndex(fann_type* output, int outputNodeNum);
	void annTrain(char* annTrainFilePath, int inputNode, int hiddenNode, int outputNode, char* resultFilePath);
};

extern string IR_to_string(int index);

#endif 
