

//Arduino run order : z->y->x
/* Number relative to Object

0: crayola     1: duck     2: index-card   3: dove
4: mirado      5: greenies 6: outlet-plug  7: glue
8: highlighter 9: cheezit  10:spark-plug   11:expo



*/
#include <stdio.h>
#include <stdlib.h>
#include "Python.h"
#include <unistd.h>
#include "Object.h"

FILE * fp;
int horizontal = 133, vertical = 36;      // variable of rotating hand motor 
int handin = 210, handout = 50;		  // variable of picking up motor
// sleep time to make robotic move consistently
double sleeptime[10]={11.3,20.4,19.7,3.5,3.6,21.2,19.1,3.6,20.5,3.6};

struct Arduinotype		// a struct type for initialization
{
	int x[24];
	int y[24];
	int z[24];
	int degreeRotate;
	int degreeCatch;
	int axisstatus;
	int degreestatus;
	int airstatus;	
};




int pythonProcess(int choice)
{
	Py_Initialize();
	
        PyRun_SimpleString("import sys");
        PyRun_SimpleString("sys.path.append('./')");
        PyObject * pName, * pModule, * pDict, * pvalue, * pFunc;
        if(choice==1)	
	{
		int value=0;
		pName = PyString_FromString("predictImage");
        	pModule = PyImport_Import(pName);
	
        	if( !pModule)
        	{
        		printf("Can't find Relative Python Script\n");
                	return -1;
        	}
		pDict = PyModule_GetDict(pModule);
		pFunc = PyDict_GetItemString(pDict,"main0");
        	pvalue=PyObject_CallObject(pFunc,NULL);
        	PyArg_Parse(pvalue,"i",&value);
		
		return value;
		//Py_Finalize();
	}
	else
	{
		pName = PyString_FromString("correct");
		pModule = PyImport_Import(pName);
		if( !pModule)
		{
			printf("Can't find Relative Python Function\n");
			return -1;
		}
		pDict = PyModule_GetDict(pModule);
		pFunc = PyDict_GetItemString(pDict,"detectBin");
		PyObject_CallObject(pFunc,NULL);
		
		return 0;
	}	
}

void objFind(int value)				// For recognition, what item it is
{
	if(value==0)
		printf("This is crayola\n");
	else if(value==1)
		printf("This is duck\n");
	else if(value==2)
		printf("This is index-card\n");
	else if(value==3)
                printf("This is dove\n");
	else if(value==4)
                printf("This is mirado\n");
	else if(value==5)
                printf("This is greenies\n");
	else if(value==6)
                printf("This is outlet-plug\n");
	else if(value==7)
                printf("This is glue\n");
	else if(value==8)
                printf("This is highlighter\n");
	else if(value==9)
                printf("This is cheezit\n");
	else if(value==10)
                printf("This is spark-plug\n");
	else if(value==11)
		printf("This is expo\n");
	else 
		printf("Nothing is here\n");
	return;
}

int main(int argc, char * argv[])
{
	// release the restriction between Arduino and Linux, allow send data by serial
	system("cd /dev && sudo chmod 666 ttyACM0");
	system("cd /var/lock/ && sudo rm -f LCK*");
	
	// Input bins' coordinates from txt file
	int imgofbin[10], order[10];
	int i = 0 , counter = 0, origin = 7;

	// Initialize the robotic arm in angle, postion and suction cup status
	struct Arduinotype Initial;
	FILE * fp2;
	// Read bin postion data from outer txt file
	fp2 = fopen("coordinate.txt","r");
	Initial.degreeRotate = horizontal;		// hand move to horizontal
        Initial.degreeCatch = handout;			// release hand, not pick up
	Initial.axisstatus = 1;				
	Initial.degreestatus = 2;
        Initial.airstatus = 3;
	
	// run the Servo motor
        moveServo(Initial.degreeRotate,Initial.degreeCatch,Initial.degreestatus);
	// set the condition of Senoid	
	setSenoid(Initial.airstatus);
	// This for loop is to move to each bin and do recognition
	/*for(i=0;i<10;i++)
	{
		//printf("-----\n");
		// read bin coordinates for arduino
		fscanf(fp2,"%d%d%d",&Initial.z[i],&Initial.y[i],&Initial.x[i]);
		// move x,y,z direction
		moveAxis(Initial.z[i],Initial.y[i],Initial.x[i],Initial.axisstatus);
		sleep(sleeptime[i]+1);
		int nouse = pythonProcess(2);		// This for taking one picture
		int value = pythonProcess(1);		// This for recognition
		objFind(value);				// print out what item it is
		//printf("value=%d \n",value);
		if ( value <= 12 ) 
		{
			imgofbin[i]= value;		// record the object in ith bin
		}
		else
		{
			imgofbin[i]= -1;		// means no item
		}
		order[i]=i;
		//printf("-----\n");
	}*/
	for( i=0;i<10;i++)
		order[i] = i;
	order[0]=7;
	printf("   Recognition is completed   \n");
	printf("-----------------------------------\n");
	//system("pause");
	i=0; 
	// This while loop is to do localization and pick up item
	while(i < 1)
	{
		if(order[i] != -1 )		  	// There is item in current bin
		{
			printf("Now bin: %d moves to bin: %d",origin,order[i]);
			sleep(2);
			binTobin(origin, order[i]);    // From origin to ith bin
			int dx = abs(origin%3 - order[i]%3 );
			int dy = abs(origin/3 - order[i]/3 );
			//printf("Now bin: %d moves to bin: %d",origin,order[i]);
			/*

				here goes the process to pick up object,
				when this done, need to move back to the
				place that we took pictures
				
			*/
			sleep(dx*20+dy*3.6);
			int x = pythonMethod_Var("pickMethod","xbias");
			printf("xbias=%d\n",x);
			int y = pythonMethod_Var("pickMethod","ybias");
			printf("ybias=%d\n",y);
			int z = pythonMethod_Var("pickMethod","zbias");
			printf("zbias=%d\n",z);
			int status = pythonMethod_Var("pickMethod","status");
			printf("status=%d\n",status);
			int nouse = pythonProcess(2);
			sleep(5);
			if(status == 1)			// Using suction cup, y need adjust
			{				
				y = y + 240;
				z = z + 200;
			
				//moveAxis(z+2000,y+2000,x+15000,1);
				// first x , then y , last z
				moveAxis(0,0,x+15000,1);
				moveAxis(0,y,0,1);
				moveAxis(z+2000,0,0,1);				
				moveServo(38,50,2);
				setSenoid(3);		// Turn on suction cup	
			}
			else				// Using gripping hand
			{
				moveAxis(0,0,x+15000,1);
				moveAxis(0,y,0,1);
				moveAxis(z+2000,0,0,1);				
				moveServo(133,210,2);
			}
			printf("------------------------\n");
			printf("   Next is drop   \n");
			/*	
				here goes the process move back to the place
				that we took picktures				
			*/
				moveAxis(z,y+2000,x,1);
			/*
				here is for binTobin, to drop object, from current
				bin to orginial place -- bin 7
			*/
			binTobin(order[i],origin);	// To drop place
			if( status ==1 )		// if using suction, need roll back
			{
				setSenoid(4);		// Turn off suction cup
				sleep(2);		// Make sure object has dropped
				moveServo(133,50,2);
			}
			else				// move back
			{
				moveServo(133,50,2);
				sleep(1);
			}		
		}
		i++;
	}


	fclose(fp2);					// disable to send data by serial
	return 0;
}



