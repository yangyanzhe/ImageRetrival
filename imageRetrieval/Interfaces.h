/*************************************************************
 * Copyright (C) 2014 by Yang Yanzhe(2012013323)   All rights reserved*
 * yangyanzhe@126.com   *
 * Function: Show the Result in a html document
*************************************************************/

#ifndef INTERFACES_H
#define INTERFACES_H

#include <vector>

class Interfaces
{
public:
	//char* name Ϊ��������ͼƬ�����ƣ�������html�ļ�����
	void ShowTheResult(char* name, std::vector<char*> ResultList);
};

#endif