

#include <stdio.h>
#include <stdlib.h>
#include "Python.h"
#include <unistd.h>
#include "Object.h"
FILE * fp;

void moveAxis(int z,int y,int x,int status)
{
	//printf("---------axisin--------\n");
	fp = fopen("/dev/ttyACM0","w+");
	fprintf(fp,"%d",status); fprintf(fp,"%c",',');
        fprintf(fp,"%d",z); fprintf(fp,"%c",','); 
        fprintf(fp,"%d",y); fprintf(fp,"%c",','); 
        fprintf(fp,"%d",x); fprintf(fp,"%c",','); 
	sleep(8);
	fclose(fp);
}

void moveServo(int degreeRotate,int degreeCatch,int degreestatus)
{
	//printf("----------servo---------\n");
	//printf("rotate=%d, catch=%d\n", degreeRotate, degreeCatch);
	fp = fopen("/dev/ttyACM0","w+");
	fprintf(fp,"%d",degreestatus);
	fprintf(fp,"%c",',');
	fprintf(fp,"%d",degreeRotate);
	fprintf(fp,"%c",',');
	fprintf(fp,"%d",degreeCatch);
	fprintf(fp,"%c",',');
	sleep(2);
	fclose(fp);

}

void setSenoid(int airstatus)
{
	fp = fopen("/dev/ttyACM0","w+");
	fprintf(fp,"%d",airstatus);
	fprintf(fp,"%c",' ');
	//sleep(1.5);	
	fclose(fp);
}

///////////////////////////////////////////

void binTobin(int bin1, int bin2)
{
	int x = -( bin1%3 - bin2%3 );
	int y = -( bin1/3 - bin2/3 );

	int finalx = x * 4990;
	int finaly = y * 500;

	if(finalx <= 0) finalx = -finalx;
	else
	{	finalx = finalx + 15000; 	}
	if(finaly <= 0) finaly = -finaly;
	else
	{	finaly = finaly + 2000;		} 
	moveAxis(0,finaly,finalx,1);
}

//////////////////////////////////////////

int pythonMethod_Tuple(const char *nameScript, const char *nameFunc ,int mode)
{
	Py_Initialize();

    	if ( !Py_IsInitialized() )
    	{
        	return -1;
    	}

	PyRun_SimpleString("import sys");
    	PyRun_SimpleString("sys.path.append('./')");
	PyObject *pName,*pModule,*pDict,*pFunc,*pArgs;
	pName = PyString_FromString(nameScript);
    	pModule = PyImport_Import(pName);
    	if ( !pModule )
    	{
        	printf("can't find relative script");
       		getchar();
        	return -1;
    	}
	pDict = PyModule_GetDict(pModule);
    	if ( !pDict )
    	{
        	return -1;
    	}
	pFunc = PyDict_GetItemString(pDict, nameFunc);
    	if ( !pFunc || !PyCallable_Check(pFunc) )
    	{
        	printf("can't find relative function");
        	getchar();
        	return -1;
    	}
	pArgs = PyTuple_New(1);
	PyTuple_SetItem(pArgs, 0, Py_BuildValue("l",mode));
	PyObject * pvalue = PyObject_CallObject(pFunc, pArgs);
	
	int value;
	PyArg_Parse(pvalue,"i",&value);

	Py_DECREF(pName);
	Py_DECREF(pModule);
	Py_DECREF(pvalue);

	
	return value;
	
}


//////////////////////////////////////////

int pythonMethod_Var(const char *nameScript, const char * variable)
{
	Py_Initialize();
	if ( !Py_IsInitialized() )
    	{
        	return -1;
    	}

	PyRun_SimpleString("import sys");
    	PyRun_SimpleString("sys.path.append('./')");
	PyObject *pName,*pModule,*pDict,*pVar;
	pName = PyString_FromString(nameScript);
    	pModule = PyImport_Import(pName);
    	if ( !pModule )
    	{
        	printf("can't find relative script");
       		getchar();
        	return -1;
    	}
    	pDict = PyModule_GetDict(pModule);
    	if ( !pDict )
    	{
        	return -1;
    	}
	pVar = PyDict_GetItemString(pDict, variable);
	if ( !pVar)
	{
		printf("No such variable");
		getchar();
		return -1;
	}
	int value;

	PyArg_Parse(pVar, "i", &value);
	
	Py_DECREF(pName);
	Py_DECREF(pModule);
	Py_DECREF(pVar);

	return value;
}



/////////////////////////////////////////

int pythonMethod_Func(const char * nameScript, const char * nameFunc, int mode)
{
	Py_Initialize();

    	if ( !Py_IsInitialized() )
    	{
        	return -1;
    	}

	PyRun_SimpleString("import sys");
    	PyRun_SimpleString("sys.path.append('./')");
	PyObject *pName,*pModule,*pDict,*pFunc,*pArgs;
	pName = PyString_FromString(nameScript);
    	pModule = PyImport_Import(pName);
    	if ( !pModule )
    	{
        	printf("can't find relative script");
       		getchar();
        	return -1;
    	}
	pDict = PyModule_GetDict(pModule);
    	if ( !pDict )
    	{
        	return -1;
    	}
	pFunc = PyDict_GetItemString(pDict, nameFunc);
    	if ( !pFunc || !PyCallable_Check(pFunc) )
    	{
        	printf("can't find relative function");
        	getchar();
        	return -1;
    	}
	
	int value;
	PyObject * pvalue = PyObject_CallObject(pFunc, NULL);
	PyArg_Parse(pvalue,"i",&value);
	
	Py_DECREF(pName);
	Py_DECREF(pModule);
	Py_DECREF(pvalue);

	if( mode ==1)
		return value;
	else 
		return 0;

}
//////////////////////////////////




