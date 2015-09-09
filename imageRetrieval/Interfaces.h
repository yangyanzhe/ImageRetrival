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
	//char* name 为输入搜索图片的名称，用来给html文件命名
	void ShowTheResult(char* name, std::vector<char*> ResultList);
};

#endif