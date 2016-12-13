

from PIL import Image
import numpy as np
import cv2
from imgops import imutils
import CVAlgo

saveStr1 = "./demo/1.jpg";
saveStr2 = "./demo/2.jpg";
saveStr0 = "./demo/";
z='am';

kw = 5.125
kd = 11.00
imh = 600
realh = 4*25.4
sensorh = 1.75*25.4
focalLength = 2

def distance_to_camera(focalLength, realh,imh,objh,sensorh):
        return focalLength*realh*imh/(objh*sensorh)	


def process():
	
	img = cv2.imread(saveStr1)
	imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

	img = imutils.resize(img, height = 600)
	imgray = imutils.resize(imgray, height = 600)

	final = img.copy()
	
	#cv2.imshow("grayscale",imgray)
	cv2.imwrite(saveStr0+"grayscale.jpg",imgray)
	thresh, imgray = CVAlgo.filtering(img, imgray, z)
	#cv2.imshow("thresh",thresh)
	cv2.imwrite(saveStr0+"thresh.jpg",thresh)

	__ , contours, hierarchy = cv2.findContours(thresh.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
	
	c = sorted(contours, key = cv2.contourArea, reverse = True )[0]
	
	rect =  cv2.minAreaRect(c)
	print img.shape
	objw = rect[1][0]
	objh = rect[1][1]
	if( rect[1][1]/2+rect[0][1] > img.shape[0]):
		objh = rect[1][0]
		objw = rect[1][1]
	elif ( rect[1][0]/2+rect[0][0] > img.shape[1]):
		objw = rect[1][1]
		objh = rect[1][0]
	cx = np.int0(rect[0][0])
	cy = np.int0(rect[0][1])
	#focalLength = (objw * kd) / kw
	#print focalLength
	inches = distance_to_camera(focalLength, realh, imh, objh,sensorh)
	#print inches	
	box = np.int0(cv2.boxPoints(rect))

	cv2.drawContours(img,[box],-1,(0,255,0),2)
	cv2.circle(img,(cx,cy),10,(0,0,255), -1)
	#cv2.putText(img,"Distance=%.3f", %(inches/25.4),(img.shape[1]- 200,img.shape[0]-200), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0,255,0), 2)
	cv2.putText(img,"Distance=%.3f" %(inches), (img.shape[1] - 320, img.shape[0] - 500), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0,255,0), 2)
	print rect
	print objw,'---',objh
	#cv2.putText(image,, (image.shape[1] - 200, image.shape[0] - 20), cv2.FONT_HERSHEY_SIMPLEX, 2.0, (0,255,0), 3)
	cv2.imwrite(saveStr2,img)
	cv2.imshow("Image",img)

	#cv2.waitKey(0)


def detectBin():
	cap = cv2.VideoCapture(0)
	t = 0
	while (t<1):

		ret,frame = cap.read()
		cv2.imshow('img',frame)
		cv2.imwrite(saveStr1,frame);	
		img = Image.open(saveStr1);
        	new_width=32;		
		new_height=32;
		width = img.size[0]
        	height = img.size[1]
        	xp1 = 0
        	xp2 = 0
        	yp1 = width
        	yp2 = height - 80
        	bound = (xp1, xp2, yp1, yp2)
        	img = img.crop(bound)
#		img = imutils.resize(img, width = 700)
		img.save(saveStr1)
		img = process()
        	#img2 = img.resize((new_width, new_height), Image.ANTIALIAS)
		#img2.save(saveStr2)
	
		if cv2.waitKey(1)&0xFF == ord('q'):
			cv2.destroyAllWindows()
			break
		t = t + 1
		if( t > 1000) :
			t = 1
		cv2.waitKey(0)

detectBin();
