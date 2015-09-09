/*************************************************************
 * Copyright (C) 2014 by Yang Yanzhe(2012013323)   All rights reserved*
 * yangyanzhe@126.com   *
 * Function: Show the Result in a html document
*************************************************************/
#include <iostream>
using namespace std;
#include "Interfaces.h"
#include <fstream>

void Interfaces::ShowTheResult(char* name, std::vector<char*> ResultList)
{
	/*char path[30];
	for(int i = 0; i<30; i++)	path[i] = '\0';
	int i = 0;*/
/*	for(i = 0; name[i] != '.' && name[i] != '\0'; i++)
		path[i] = name[i];
	path[i] = '.';
	path[i+1] = 'h';
	path[i+2] = 't';
	path[i+3] = 'm';
	path[i+4] = 'l';*/
	char path[] = "test.html";

	cout << path << endl;
	ofstream outFile;
	outFile.open(path, ios::out);
	outFile << "<!DOCTYPE html>" << endl;
	outFile << "<html>" << endl << "<head>" << endl
	<< "<meta charset=\"utf-8\" />"
	<< "<title>Retrieve Result </title>" << endl
	<< "<style>" << endl
	<< "#n{margin:10px auto; width:920px; border:1px solid #CCC;font-size:12px; line-height:30px;}" << endl
	<< "#n a{ padding:0 4px; color:#333}" << endl
	<< "</style>" << endl
	<< "</head>" << endl
	<< "<body>" << endl
	<< "<p>Input Image</p>" << endl
	<< "<p>"  << endl
	<< "<img src=\""
	<< name
	<<"\" width=\"300\" height=\"300\" />" << endl
	<< "</p>" << endl
	<< "<p>10 Nearest Queries</p>" << endl
	<< "<p>" << endl;

	for(int i = 0; i<10; i++)
	{
		outFile << "<img src=\"image/"
		<< ResultList[i]
		<< "\" width=\"250\" height=\"250\" />" << endl;
	}
	outFile << "</p>" << endl
	<< "</body>" << endl
	<< "</html>" << endl;
}
