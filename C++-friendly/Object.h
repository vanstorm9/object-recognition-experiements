
#include <stdio.h>
#include <stdlib.h>
#include "Python.h"
#include <unistd.h>

#ifndef __OBJECT_H__

#define __OBJECT_H__

extern void moveAxis(int z,int y,int x,int status);
extern void moveServo(int degreeRotate,int degreeCatch,int degreestatus);
extern void setSenoid(int airstatus);
extern int pythonMethod_Func(const char * nameScript, const char * nameFunc,int mode);
extern int pythonMethod_Var(const char * nameScript, const char * variable);
extern int pythonMethod_Tuple(const char *nameScript, const char *nameFunc ,int mode);
extern void binTobin(int bin1, int bin2);





#endif
