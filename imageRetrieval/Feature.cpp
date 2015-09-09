#include "Feature.h"
#include <iostream>
#include <core/core.hpp>
using namespace std;
using namespace cv;

char* concat(char* s1, char* s2)
{
    int length_s1=0, length_s2=0;
	while(s1[length_s1] != '\0')  length_s1++;
	while(s2[length_s2] != '\0')  length_s2++;

	int length = length_s1+length_s2+1;
	char* temp = new char[length];
	for(int i = 0; i<length; ++i)
		temp[i] = '\0';
	int i=0;
	while(*s1 != '\0')
		temp[i++] = *s1++;
	while(*s2 != '\0')
		temp[i++] = *s2++;
	temp[i] = '\0';
	return temp;
}

void Feature::Initial()
{
	totalDim = 146;

	fHSV1 = new double[16];
	memset(fHSV1, 0, sizeof(double)*16);

	fHSV2 = new double[12];
	memset(fHSV2, 0, sizeof(double)*12);

	fHSV3 = new double[24];
	memset(fHSV3, 0, sizeof(double)*24);

	fSurf = new double[24];
	memset(fSurf, 0, sizeof(double)*24);

	fWaveLet = new double[64];
	memset(fWaveLet, 0, sizeof(double)*64);
	//fPixel = new double[];

	fTotal = new double[totalDim];
	memset(fTotal, 0, sizeof(double) * totalDim);
}

void Feature::getColorHistogramSingle(double* feature, int h_bins, int s_bins, int v_bins, char* fileName)
{
	IplImage * src= cvLoadImage(fileName);
	IplImage* hsv = cvCreateImage( cvGetSize(src), 8, 3 );

	//cvNamedWindow( "Source", 1 );
	//cvShowImage( "Source", src );

	IplImage* h_plane = cvCreateImage( cvGetSize(src), 8, 1 );
	IplImage* s_plane = cvCreateImage( cvGetSize(src), 8, 1 );
	IplImage* v_plane = cvCreateImage( cvGetSize(src), 8, 1 );
	//ÊäÈëÍŒÏñ×ª»»µœHSVÑÕÉ«¿ÕŒä
	cvCvtColor(src, hsv, CV_BGR2HSV);
	cvCvtPixToPlane(hsv, h_plane, s_plane, v_plane, 0);

	int type;		//type =0: H; type=1: S; type=2: V;
	for(int type = 0; type < 3; type++)
	{
		int bins;
		IplImage* plane;
		switch(type)
		{
		case 0: bins = h_bins;
			plane = h_plane;
			break;
		case 1: bins = s_bins;
			plane = s_plane;
			break;
		case 2: bins = v_bins;
			plane = v_plane;
			break;
		default:
			plane = NULL;
			cout << "type³öÏÖÒâÍâÇé¿ö" << endl;
		}

		double* feature_single = new double[bins]; 
		getColorHistogramT(feature_single, type, bins, plane);
		for(int i = 0; i<bins; i++)	*feature++ = feature_single[i];
		delete []feature_single;
	}
	cvReleaseImage(&src);
    cvReleaseImage(&hsv);
	cvReleaseImage(&h_plane);
	cvReleaseImage(&s_plane);
	cvReleaseImage(&v_plane);
}

void Feature::getColorHistogramT(double* feature, int type, int bins, IplImage * plane)
{
	if(bins <= 1) return;

	//opencvÖÐµÄ H·ÖÁ¿ÊÇ 0~180£¬ S·ÖÁ¿ÊÇ0~255£¬ V·ÖÁ¿ÊÇ0~255
	float h_ranges[] = {0, 180}; 
	float s_ranges[] = {0, 255};
	float v_ranges[] = {0, 255};
	float* range;
	switch(type)
	{
	case 0: range = h_ranges;
		break;
	case 1: range = s_ranges;
		break;
	case 2: range = v_ranges;
		break;
	default: 
		cout << "type ³öÏÖÒâÍâÇé¿ö" << endl;
	}
	CvHistogram * hist = cvCreateHist(1 , &bins, CV_HIST_ARRAY, &range, 1 );
	cvCalcHist( &plane, hist, 0, 0 );
	
	for(int i = 0; i<bins; ++i)
	{
		float bin_val = cvQueryHistValue_1D(hist, i);
		feature[i] = bin_val;
	}
	normalize(feature, bins);
	cvReleaseHist (&hist);
}

void Feature::normalize(double* feature, int dims)
{
	int sum = 0;
	for(int i = 0; i<dims; i++)
		sum+=feature[i];
	for(int i = 0; i<dims; i++)
		feature[i] = cvRound((double)feature[i] / sum * 10000);
}

void Feature::getColorHistogram(char* fileName)
{
	getColorHistogramSingle(fHSV1, 8, 8, 0, fileName);
	getColorHistogramSingle(fHSV2, 6, 6, 6, fileName);
	getColorHistogramSingle(fHSV3, 12, 6, 6, fileName);
}

void Feature::getSurfFeature(char* fileName)
{
	Mat img = imread(fileName, CV_LOAD_IMAGE_GRAYSCALE);
	SURF surf_extractor(2.0e2);
    vector<KeyPoint> keypoints;
	surf_extractor(img, Mat(), keypoints);

	int col = img.cols;
	int row = img.rows;

	vector<KeyPoint> partKeyPoints[4];
	for (int i = 0; i < keypoints.size(); i++)
	{
		if (keypoints[i].pt.x > col / 4 && keypoints[i].pt.x < col / 2 && keypoints[i].pt.y > row / 4 && keypoints[i].pt.y < row / 2)
			partKeyPoints[0].push_back(keypoints[i]);
		else if (keypoints[i].pt.x > col / 2 && keypoints[i].pt.x < col * 3 / 4 && keypoints[i].pt.y > row / 4 && keypoints[i].pt.y < row / 2)
			partKeyPoints[1].push_back(keypoints[i]);
		else if (keypoints[i].pt.x > col / 2 && keypoints[i].pt.x < col * 3 / 4 && keypoints[i].pt.y > row / 2 && keypoints[i].pt.y < row  * 3 / 4)
			partKeyPoints[2].push_back(keypoints[i]);
		else if (keypoints[i].pt.x > col / 4 && keypoints[i].pt.x < col / 2 && keypoints[i].pt.y > row / 2 && keypoints[i].pt.y < row * 3 / 4)
			partKeyPoints[3].push_back(keypoints[i]);
	}
	
	for (int i = 0; i < 24; i++)
		fSurf[i] = 0;
	int n = 0;

	for (int i = 0; i < 4; i++)
	{
		if (partKeyPoints[i].size() == 0)
		{
			n += 6;
			continue;
		}

		for (int j = 0; j < partKeyPoints[i].size(); j++)
		{
			fSurf[n] += partKeyPoints[i][j].pt.x / col;
			fSurf[n + 1] += partKeyPoints[i][j].pt.y / row;
			fSurf[n + 2] += partKeyPoints[i][j].angle / 100;
		}
		fSurf[n] /= partKeyPoints[i].size();
		fSurf[n + 1] /= partKeyPoints[i].size();
		fSurf[n + 2] /= partKeyPoints[i].size();

		for (int j = 0; j < partKeyPoints[i].size(); j++)
		{
			fSurf[n + 3] += pow((partKeyPoints[i][j].pt.x / col - fSurf[n]), 2);
			fSurf[n + 4] += pow((partKeyPoints[i][j].pt.y / row - fSurf[n + 1]), 2);
			fSurf[n + 5] += pow((partKeyPoints[i][j].angle / 100 - fSurf[n + 2]), 2);
		}
		fSurf[n + 3] /= partKeyPoints[i].size();
		fSurf[n + 4] /= partKeyPoints[i].size();
		fSurf[n + 5] /= partKeyPoints[i].size();
		n += 6;
	}
}

void Feature::getWaveLetFeature(char* fileName)
{
	 //ŽŽœšÒ»žö·œÏòÊÇi*PI/8¶ø³ß¶ÈÊÇ3µÄgabor
    double Sigma = 2*PI;    
    double F = sqrt(2.0);    
	
    CvGabor *gabor1 = new CvGabor;    
	IplImage *img = cvLoadImage(fileName, CV_LOAD_IMAGE_GRAYSCALE );  

	for(int i = 0; i<8; i++)
	{
		for(int j = 1; j<=4; j++)
		{
			gabor1->Init( i * PI/8, j, Sigma, F);  
			IplImage *reimg = cvCreateImage(cvSize(img->width,img->height), IPL_DEPTH_8U, 1);  
			gabor1->conv_img(img, reimg, CV_GABOR_REAL);  
			fWaveLet[i*4+j-1] = (average_Image(reimg) / 255 - 0.45) * 10;
			fWaveLet[i*4+j-1+32] = (variance_Image(reimg) / 255 - 0.45) * 10;
			cvReleaseImage(&reimg);
		}
	}
	cvReleaseImage(&img);
}

double Feature::average_Image(IplImage* img)
{
	unsigned char *data;//ÖžÏòÔ­ÍŒÏñµÄÖžÕë
	int i,j;//Ñ­»·±äÁ¿
	int height,width,step;
	double aver = 0;

	//ÔØÈëÍŒÏñµÄÊýŸÝ
	height=img->height;
	width=img->width;
	step=img->widthStep;
	data=(uchar*)img->imageData;

	for(i=0;i<height;i++)
	{
		for(j=0;j<width;j++)
			aver+=data[i*step+j];	
	}
   aver=aver/height/width;
   return aver;
}

double Feature::variance_Image(IplImage* img)
{
	unsigned char *data;	//ÖžÏòÔ­ÍŒÏñµÄÖžÕë
	int i, j;	//Ñ­»·±äÁ¿
	int height,width,step;
	double aver=0;
	double variance=0;

	//ÔØÈëÍŒÏñµÄÊýŸÝ
	height=img->height;
	width=img->width;
	step=img->widthStep;
	data=(uchar*)img->imageData;

	aver = average_Image(img);

	for(i=0;i<height;i++)
	{
		for(j=0;j<width;j++)
		{
			double distance = data[i*step + j] - aver;
			variance+=pow(data[i*step+j],2);			
		}
	}
	variance=variance/height/width;
	//variance=variance-(aver*aver);
	variance=sqrt(variance);
	return variance;
}

//µ÷ÓÃrunFeatureÇ°ÐèÒªÏÈµ÷ÓÃInitial()
void Feature::runFeature(char* fileName)
{
	getSurfFeature(fileName);
	getColorHistogram(fileName);
	getWaveLetFeature(fileName);

	for (int i = 0; i < 16; i++)
		fTotal[i] = fHSV1[i] / 10000;
	for (int i = 16; i < 34; i++)
		fTotal[i] = fHSV2[i - 16] / 10000;
	for (int i = 34; i < 58; i++)
		fTotal[i] = fHSV3[i - 34] / 10000;
	for (int i = 58; i < 82; i++)
		fTotal[i] = fSurf[i - 58];
	for (int i = 82; i < 146; i++)
		fTotal[i] = fWaveLet[i - 82];
}
