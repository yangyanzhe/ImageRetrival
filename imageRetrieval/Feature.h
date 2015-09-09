#ifndef FEATURE_H
#define FEATURE_H

#include <cv.h>
#include <highgui.h>
#include <highgui/highgui.hpp>
#include <features2d/features2d.hpp>
#include <nonfree/features2d.hpp>
#include <core/core.hpp>
#include "opencv2/calib3d/calib3d.hpp"
#include <legacy/legacy.hpp>
#include "cvgabor.h"

class Feature
{
public:
	double* fHSV1;		//(H, S, V) = (8, 8, 0)
	double* fHSV2;		//(H, S, V) = (6, 6, 6)
	double* fHSV3;		//(H, S, V) = (12, 6, 6)
	double* fSurf;		//dim of SurfFeature is 24
	double* fWaveLet;   //dim of fWaveLet is 64
	//double* fPixel;     

	int totalDim;
	double* fTotal;


public:
	void Initial();

	void getColorHistogram(char* fileName);
	void getColorHistogramSingle(double* feature, int h_bins, int s_bins, int v_bins, char* fileName);
	void getColorHistogramT(double* feature, int type, int bins, IplImage * plane);
	void normalize(double* feature, int dims);

	void getSurfFeature(char* fileName);

	void getWaveLetFeature(char* fileName);
	double average_Image(IplImage* img);
	double variance_Image(IplImage* img);

	//����runFeatureǰ��Ҫ�ȵ���Initial()
	void runFeature(char* fileName);
};

extern char* concat(char* s1, char* s2);

#endif
