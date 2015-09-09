#include <iostream>
#include "FANN.h"
#include "Feature.h"
#include "Interfaces.h"
#include <Python.h>
#include <fstream>
#include <boost/lexical_cast.hpp>
#include <boost/algorithm/string/join.hpp>

using std::vector;
using std::ofstream;
using std::ifstream;
using std::string;
vector<char*> IR_string_to_charStar(vector<string> titleList);
int main(int argc, char *argv[])
{
	FANN app;
	app.establishFANN();

	Py_SetProgramName(argv[0]);
	Py_Initialize();
	char name[1000];
	while(true)
	{
		std::cout<<"Please enter the path of query image"<<std::endl;
		std::cin>>name;
		vector<string> result = app.SingleQuery(name);
		Interfaces app2;
		app2.ShowTheResult(name, IR_string_to_charStar(result));
		PyRun_SimpleString("import webbrowser\n""webbrowser.open(\"test.html\")");
	}
	Py_Finalize();

/*	string output = string("testQueryResult.txt");
	ofstream outputWriter(output.c_str());
	ifstream inputReader("resultTitle");
	for(int i = 0 ; i < 2000 ; i++)
	{
		string tempFile;
		inputReader>>tempFile;
		string tempName = string("ir/") + tempFile;
		char* name = new char[tempName.size() + 10];
		for(int j = 0 ; j < tempName.size() ; j++)
			name[j] = tempName[j];
		name[tempName.size()] = '\0';
		vector<string> result = app.SingleQuery(name);
//output the result
		outputWriter<<boost::algorithm::join(result, ",")<<std::endl;
		std::cout<<i<<std::endl;
	}*/

	system("pause");
	return 0;
}
vector<char*> IR_string_to_charStar(vector<string> titleList)
{
	vector<char*> result = vector<char*>(titleList.size(), NULL);
	for(int i = 0 ; i < result.size() ; i++)
	{
		result[i] = new char[titleList[i].size() + 1];
		for(int j = 0 ; j < titleList[i].size() ; j++)
			result[i][j] = titleList[i][j];
		result[i][titleList[i].size()] = '\0';
	}
	return result;

}
