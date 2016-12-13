// x and z moves, and all move with the same speed

#include <SoftwareSerial.h>
#include <Servo.h>

Servo servo;
Servo servos;
int pos1=0;
int pos2=0;
int servopin1=9;
int servopin2=10;
int servodelay=300;

#define directionpin 2  //z  
#define steppin 3
#define directionpins 4 //y
#define steppins 5
#define directionpinss 6 //x
#define steppinss 7
#define stepdelay 2000 //number of microseconds delay used to toggle step pin

int led = 12 ;
int stepper;
int x;
int x1;
int y;
int y1;
int z;
int z1;
int a;

int pos,buff[5],buffz[5],buffy[5],buffx[5],buffdeg[5],buffcat[5],buffair[5];
int j=-1,jz=-1,jy=-1,jx=-1,jdeg=-1,jcat=-1,jair=-1;
int num,numx,numy,numz,numdeg,numcat,numair;
int input;
int calc(int buff[],int j)
{
    int nm=0,xp=0;
 
    for(xp;xp<=j;xp++)
          nm=nm+(buff[xp]-48)*pow(10,j-xp);
 
    return nm;
}

void setup() {
  // put your setup code here, to run once:
pinMode(directionpin, OUTPUT);
pinMode(steppin, OUTPUT);
pinMode(directionpins, OUTPUT);
pinMode(steppins, OUTPUT);
pinMode(directionpinss, OUTPUT);
pinMode(steppinss, OUTPUT);
  Serial.begin(9600);
 pinMode(led, OUTPUT); 
 pinMode(13, OUTPUT);
  servo.attach(servopin1);  
 servos.attach(servopin2); 
  
}
  
void loop()
{
  Serial.println("xyz is 1, hand is 2, airoff is 3, airon is 4");
  while(Serial.available()==0)
  {
  }
  input = Serial.read();
  Serial.print("original=");
  Serial.println(input);
  Serial.print("\n");
  if(input==',')
  {
     num=calc(buff,j);
     j=-1;
     Serial.print("num==");
     Serial.println(num);
     if(num==1){
	  //z
	  Serial.println("Type the distance you want for z"); // z direction
	  while(Serial.available()==0)
	  {
	  }
	  int zt = Serial.read(); 
          Serial.print("zt=");
          Serial.println(zt);           
          if(zt==',')
          {
             z=calc(buffz,jz);
             jz=-1;
             Serial.println(z);
          }
          else
          {
            jz++;
            buffz[jz]=zt;
          }
	  if(0<z&&z<2000){
	  digitalWrite(directionpin, HIGH);
	  dosteps(z);
	  delay(1500);
	}

	  if(z>2000){  // z goes out
	  digitalWrite(directionpin, LOW);
	  z=z-2000;
	  dosteps(z);
	  delay(1500);
	}
        
        //********************************
        
        //y
	Serial.println("Type the distance you want for y"); // y direction
	  while(Serial.available()==0)
	  {
	  }
	  int yt = Serial.read(); 
          if(yt ==',')
          {
            y=calc(buffy,jy);
            jy=-1;
            //Serial.println(y);
          }
          else
          {
             jy++;
             buffy[jy]=yt;
          }
	  if(0<y&&y<2000){
	  digitalWrite(directionpins, HIGH);
	  dostep(y);
	  delay(1500);
	}

	  if(y>2000){
	  digitalWrite(directionpins, LOW);
	  y=y-2000;
	  dostep(y);
	  delay(1500);
	}

        //***************************
        //x
	  Serial.println("Type the distance you want for x"); // x direction
	  while(Serial.available()==0)
	  {
	  }
	  int xt = Serial.read(); 
	  if(xt==',')
          {
            x=calc(buffx,jx);
            jx=-1;
            //Serial.println(x);
          }
          else
          {
            jx++;
            buffx[jx]= xt;
          }
          if(0<x&&x<10000){
	  digitalWrite(directionpinss, HIGH);
	  dostepss(x);
	  delay(1500);
	}

	  if(x>10000){
	  digitalWrite(directionpinss, LOW);
	  x=x-10000;
	  dostepss(x);
	  delay(1500);
	}
    }
  }
  else
  {
      Serial.print("input=");
      Serial.println(input);
      j++;
      buff[j]=input;
  }
  
}

//z
void dosteps(double numsteps){
    for (double i = 0; i <= numsteps; i++){
      digitalWrite(steppin, HIGH);
      delayMicroseconds(stepdelay);
      digitalWrite(steppin, LOW);
      delayMicroseconds(stepdelay);
    }
}

//y
void dostep(double numsteps){
    for (double i = 0; i <= numsteps; i++){
      digitalWrite(steppins, HIGH);
      delayMicroseconds(stepdelay);
      digitalWrite(steppins, LOW);
      delayMicroseconds(stepdelay);
    }
}

//x
void dostepss(double numsteps){
    for (double i = 0; i <= numsteps; i++){
      digitalWrite(steppinss, HIGH);
      delayMicroseconds(stepdelay);
      digitalWrite(steppinss, LOW);
      delayMicroseconds(stepdelay);
    }
}
