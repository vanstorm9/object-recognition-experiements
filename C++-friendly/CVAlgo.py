import cv2
from numpy import *
from pylab import *
from imgops import imutils
from PIL import Image
import numpy as np
import math
import ImageDraw

def invert_img(img):			# image reversed
    img = (255-img)
    return img

def histogram_equalization(img):	# normalize the histogram situation of image
    hist,bins = np.histogram(img.flatten(),256,[0,256])
 
    cdf = hist.cumsum()     
    cdf_m = np.ma.masked_equal(cdf,0)
    cdf_m = (cdf_m - cdf_m.min())*255/(cdf_m.max()-cdf_m.min())
    cdf = np.ma.filled(cdf_m,0).astype('uint8')
    img2 = cdf[img]

    return img2

def histogram_backprojection(img):	# get the histogram situation of some part of 
					# background, and remove the noise it cause

    img_height = img.shape[0]
    img_width = img.shape[1]
    img_demi = img[0:3*(img_height/5) , 0:(img_width)]  # choose upper part
    hsv = cv2.cvtColor(img_demi,cv2.COLOR_BGR2HSV)


    #print hsv.shape
#    cv2.imshow("img_demi",img_demi)
    hsvt = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    
    # calculating object histogram
    roihist = cv2.calcHist([hsv],[0, 1], None, [180, 256], [0, img_height, 0, img_width] )
    #scv2.imshow("img_demi",roihist)
    # normalize histogram and apply backprojection
    cv2.normalize(roihist,roihist,0,255,cv2.NORM_MINMAX)
    #cv2.imshow("img_demi",roihist)
    dst = cv2.calcBackProject([hsvt],[0,1],roihist,[0,img_height,0,img_width],1)
    #cv2.imshow('dst1',dst)
    cv2.imwrite("./demo/dst1.jpg",dst)
    # Now convolute with circular disc
    disc = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5))
    cv2.filter2D(dst,-1,disc,dst)
    #cv2.imshow('dst',dst) 
    cv2.imwrite("./demo/dst.jpg",dst)
    # threshold and binary AND
    ret,thresh = cv2.threshold(dst,50,255,0)
    #cv2.imshow('thresh0',thresh)
    return thresh



def morph_trans(img):
    # Implementing morphological erosion & dilation
    kernel = np.ones((9,9),np.uint8)  # (6,6) to get more contours (9,9) to reduce noise
    img = cv2.erode(img, kernel, iterations = 3) # Shrink to remove noise
    img = cv2.dilate(img, kernel, iterations= 10)  # Grow to combine stray blobs

    return img


def morph_trans_shelf(img):
    # Implementing morphological erosion & dilation
    kernel = np.ones((4,4),np.uint8)  # (6,6) to get more contours (9,9) to reduce noise
    img = cv2.erode(img, kernel, iterations = 2) # Shrink to remove noise
    img = cv2.dilate(img, kernel, iterations= 4)  # Grow to combine stray blobs

    return img

def canny(imgray):
    imgray = cv2.GaussianBlur(imgray, (11,11), 200)
    canny_low = 0
    canny_high = 100

    thresh = cv2.Canny(imgray,canny_low,canny_high)
    return thresh

def cnt_gui(img, contours):
    cnts = sorted(contours, key = cv2.contourArea, reverse = True)

    for i in range(0,len(cnts)):
        sel_cnts = sorted(contours, key = cv2.contourArea, reverse = True)[i]

        area = cv2.contourArea(sel_cnts)

        if area < 1000:
            continue
        
        # get orientation angle and center coord
        center, axis,angle = cv2.fitEllipse(sel_cnts)
        
        hyp = 100  # length of the orientation line

        # Find out coordinates of 2nd point if given length of line and center coord 
        linex = int(center[0]) + int(math.sin(math.radians(angle))*hyp)
        liney = int(center[1]) - int(math.cos(math.radians(angle))*hyp)

	# Draw orienation
	cv2.line(img, (int(center[0]),int(center[1])), (linex, liney), (0,0,255),5)             
	cv2.circle(img, (int(center[0]), int(center[1])), 10, (255,0,0), -1)


    return img

def filtering(img, imgray, mode):
	if mode == 'am':
		thresh= invert_img(histogram_backprojection(img))
		#cv2.imshow("thresh1",thresh)
		cv2.imwrite("./demo/thresh1.jpg",thresh)
		thresh = morph_trans(thresh)
		#cv2.imshow("thresh_mor",thresh)

	elif mode == 'pr':


		imgray = cv2.medianBlur(imgray, 11)
		thresh = cv2.Canny(imgray,75,200)
	else:
		print 'error in filtering function'
		quit()

	return thresh, imgray



def shelfFiltering(img, imgray, mode):
    if mode == 'am':
	thresh= invert_img(histogram_backprojection(img))
	cv2.imshow('thresh_original',thresh)
	thresh = cv2.erode(thresh, None,iterations=3)
	cv2.imshow('thresh_erode',thresh)
	thresh = cv2.dilate(thresh,None,iterations=3)
	cv2.imshow('thresh_dilate',thresh)
        thresh = morph_trans_shelf(thresh)

    elif mode == 'pr':
        
        
        imgray = cv2.medianBlur(imgray, 11)
        thresh = cv2.Canny(imgray,75,200)
    else:
        print 'error in filtering function'
        quit()

    return thresh, imgray
def classifyObject(center,imgindex,base):

	width = imgindex[0]
	height = imgindex[1]

	shelfWidth = width - base[0]*2
	shelfHeight = height - base[1]*2

	rowwidthEvery = shelfWidth / 3   #label from left to right
	lineheightEvery = shelfHeight / 4  #label from up to down
	
	stdwidth = rowwidthEvery / 3
	stdheight = lineheightEvery
	# First label axis x   (x,y)
	index = 1
	while center[0] > (base[0] + index * stdwidth):
		index = index + 1   
	labelx = index

	index = 1
	# Second label axis y  (x,y)
	while center[1] > (base[1] + index * stdheight):
		index = index + 1 
	labely = index
	#adjust
	if labelx > 9 :
		labelx = 9
	if labely > 4 :
		labely = 4	
	label = np.array([labelx,labely])
	#print label
	return label

def contourCrop(contours,img):
	
	center = np.empty([len(contours),2])
	box_round = np.empty([len(contours),4,2])
	base = np.array([70,50])
	location = np.empty([len(contours),2])
	j = 0
	print len(contours)
	for i in range(0,len(contours)):
       		c = sorted(contours, key = cv2.contourArea, reverse = True )[i];
        	#print c[0]
		rect = cv2.minAreaRect(c)
        	#print rect
		box = np.int0(cv2.boxPoints(rect))
		#print box
		boxBound = [ box[:,0].min(), box[:,1].min(), box[:,0].max(),box[:,1].max() ]  # Get the crop size of the contour box
        	#print boxBound[2]
		imgCrop = img[boxBound[1]:boxBound[3], boxBound[0]:boxBound[2] ]
		
		saveFile = "cropImage/"
		cv2.imwrite(saveFile + str(i) +'.jpg',imgCrop)

		#cv2.drawContours(thresh,[box],-1,(255,0,255),1)
        	#a,axis,angle = cv2.fitEllipse(c);
        	a = rect[0]
		#center[i]=a;
	        print a		
		if a[0] > base[0] and a[0] < (img.shape[0] - base[0]) :
		#	print a[0],'---',base[0]
			box_round[j] = box
			label = classifyObject(a,img.shape,base)
			location[j] = label
			j = j + 1

#	print box_round[0]
	return location,box_round        
	


