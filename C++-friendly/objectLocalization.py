#
#	localize the object 
#	get the distance and the slope rate
#	decide whether use grippig hand 
#	or suction cup
#


import cv2
from PIL import Image
from imgops import imutils

import predictImage
import gripMethod
import CVAlgo
import numpy as np


am='am'

perPixel = 4.677083333
perZdistance = 76.923076923 

imh = 600
imw = 960
#realh = 2*25.4		# need to modify based on different object
sensorh = 1.75*25.4	# 
focalLength = 2
imgCentre = imw/2

path = "./demo/2.jpg"


def getRealheight():
	
	labelnumber = predictImage.main0()
	print labelnumber
	if(labelnumber == 0):		# crayola
		realh = 1 * 25.4
	elif(labelnumber == 1):		# duck
		realh = 2.25*25.4
	elif(labelnumber == 2):		# index-card
		realh = 5*25.4
	elif(labelnumber == 3):		# dove
		realh = 3.5*25.4
	elif(labelnumber == 4):		# mirado
		realh = 0.625*25.4
	elif(labelnumber == 5):		# greenies
		realh = 8.5*25.4
	elif(labelnumber == 6):		# outlet-plug
		realh = 2.125*25.4
	elif(labelnumber == 7):		# glue
		realh = 4*25.4
	elif(labelnumber == 8):		# highlighter
		realh = 0.625*25.4
	elif(labelnumber == 9):		# cheezit
		realh = 8.5*25.4
	elif(labelnumber == 10):	# spark-plug
		realh = 1 * 25.4
	else:				# expo
		realh = 5.125*25.4
	return realh

def distance_to_camera(focalLength, realh,imh,objh,sensorh):
        return np.int0( focalLength*realh*imh/(objh*sensorh) * perZdistance)




def detectDistance():

	img = cv2.imread(path)				
	imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)	# converted into grayscale image

	img = imutils.resize(img, height = 600)		# resize image
	imgray = imutils.resize(imgray, height = 600)

	final = img.copy()

	# call CVAlgo script -- filtering function to process image
	thresh, imgray = CVAlgo.filtering(img, imgray, am)  

	# get contours situation by threshold situation
	__ , contours, hierarchy = cv2.findContours(thresh.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
	# sort the size of contours
	#print contours
	c = sorted(contours, key = cv2.contourArea, reverse = True)[0]

	# construct to form the minimal rectangular 
	rect = cv2.minAreaRect(c)

	#print img.shape

	# here save the variables -- centre of object, width and height of object	
	centreRect = np.int0(rect[0])
	angleRotated = np.int0(rect[2])
	objw = abs(rect[1][0])
	objh = abs(rect[1][1])

	if( rect[1][1]/2+rect[0][1] > img.shape[0]):
		objh = rect[1][0]
		objw = rect[1][1]
	elif ( rect[1][0]/2+rect[0][0] > img.shape[1]):
		objw = rect[1][1]
		objh = rect[1][0]

	realh = getRealheight()
	print realh
	# calculate the distance between object and webcam
	z = distance_to_camera(focalLength, realh, imh, objh,sensorh)
	#print z
	# calculate the bias of y between object and bottom bin
	ybias = np.int0(600 - centreRect[1]) 

	# construct 4 points to form the rectangular box
	box = np.int0(cv2.boxPoints(rect))
	# draw the box in original image
	cv2.drawContours(final,[box],-1,(0,255,0),2)

	#print centreRect
	
	objCentre = np.int0(centreRect[0])

	xbias = np.int0( gripMethod.proofCentre(objCentre,imgCentre) )
	
	if objw < 400:      
		status = 0
	else:		    
		status = 0 	
		
	return xbias,ybias,z,status
		
		

print detectDistance()
