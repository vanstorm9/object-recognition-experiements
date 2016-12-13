

import cv2
from PIL import Image
import numpy as np
from imgops import imutils
import CVAlgo

saveStr0 = "./demo/2.jpg"		# path for image to do recognition
saveStr = "./test-images/1.jpg"		# path for image
def process():
	
	img = cv2.imread(saveStr0)		# load image
	img = imutils.resize(img, height = 600)	# resize image
	cv2.imwrite(saveStr0,img);		# save image


def detectBin():
	cap = cv2.VideoCapture(0)		# use the video
	ret,frame = cap.read()			# load the image of video
	#cv2.imshow('img',frame)		
	cv2.imwrite(saveStr,frame)
	img = Image.open(saveStr)
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
	img.save(saveStr0)
	process()
        img2 = img.resize((new_width, new_height), Image.ANTIALIAS)
	img2.save(saveStr);

