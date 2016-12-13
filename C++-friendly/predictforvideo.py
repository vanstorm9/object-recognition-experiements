# Simple CNN model for CIFAR-10
import numpy

import matplotlib.pyplot as plt
from time import time
from imgops import imutils
import CVAlgo
#from imagenet_utils import *

from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import Flatten
from keras.constraints import maxnorm
from keras.optimizers import SGD
from keras.layers.convolutional import Convolution2D
from keras.layers.convolutional import MaxPooling2D
from keras.utils import np_utils
from keras.preprocessing import image as image_utils

from keras.preprocessing.image import ImageDataGenerator, array_to_img, img_to_array, load_img

from sklearn.metrics import confusion_matrix

import imageDataExtract as dataset

from PIL import Image
#import correct
import cv2

imgToLoad = 'test-images/2.jpg'
imgSource = 'test-images/'

modelPath = "../models/model.h5"
saveStr = "./test-images/1.jpg";
saveStr2= "./test-images/2.jpg";
z='am'

def printPrediction(pred):
	if pred >= 10 and pred <=15:
		print labelName[pred+1]
	else:
		print labelName[pred]


def getPredictionValue(pred):
	if pred >= 10 and pred <=15:
		return (pred+1)
	else:
		return pred
'''
def detectBin():

	new_width = 32
	new_height = 32
	cap = cv2.VideoCapture(0)
	ret, img = cap.read()
	width = img.size[0]
	height = img.size[1]
	xp1 = 0
	xp2 = 0
	yp1 = width
	yp2 = height - 100
	bound = (xp1, xp2, yp1, yp2)
	img = img.crop(bound)
	
	img2 = img.resize((new_width, new_height), Image.ANTIALIAS)

	saveStr = imgSource + str(1) + ".jpg"

	img2.save(saveStr)
'''
def main():
	# fix random seed for reproducibility
	seed = 7
	numpy.random.seed(seed)

	# load data

	matrix_path = '../numpy-matrix/main.npy'
	label_path = '../numpy-matrix/label.npy'
	labelName_path = '../numpy-matrix/labelName.npy'
	labelPath_path = '../numpy-matrix/labelPath.npy'


	main_matrix = numpy.load(matrix_path)
	label_matrix = numpy.load(label_path)
	labelName = numpy.load(labelName_path)


	labelPath = numpy.load(labelPath_path)


	# normalize inputs from 0-255 to 0.0-1.0
	x_mat = main_matrix.astype('float32')


	x_mat = x_mat / 255.0

	# one hot encode outputs
	y_mat = np_utils.to_categorical(label_matrix)
	num_classes = y_mat.shape[1]


	# Create the model
	model = Sequential()
	model.add(Convolution2D(32, 3, 3, input_shape=(3, 32, 32), border_mode='same', activation='relu', W_constraint=maxnorm(3)))
	model.add(Dropout(0.2))
	model.add(Convolution2D(32, 3, 3, activation='relu', border_mode='same', W_constraint=maxnorm(3)))
	model.add(MaxPooling2D(pool_size=(2, 2)))
	model.add(Flatten())
	model.add(Dense(512, activation='relu', W_constraint=maxnorm(3)))
	model.add(Dropout(0.5))
	model.add(Dense(num_classes, activation='softmax'))


	t0 = time()

	model.load_weights(modelPath)

	# Compile model

	epochs = 25
	lrate = 0.01
	decay = lrate/epochs

	sgd = SGD(lr=lrate, momentum=0.9, decay=decay, nesterov=False)

	model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])


	## Prediction phase ##

	imgO = Image.open(imgToLoad)
	imgO = imgO.resize((32,32), Image.ANTIALIAS) 
	test_img = numpy.array(imgO).transpose()


	test_img = test_img.reshape((1,) + test_img.shape)


	# normalizing inputs
	test_img = test_img.astype('float32')
	test_img = test_img / 255.0



	pred = model.predict_classes(test_img, 1, verbose=0)

	### To view all labels
	print labelName
	###

	predVal = 12-pred[0]-1   
	#result = getPredictionValue(predVal)
	
	return predVal

def Imagelabel(label):
	if(label==0):
		return "crayola";
	elif(label==1):
		return "duck";
	elif(label==2):
		return "index-card";
	elif(label==3):
		return "dove"
	elif(label==4):
		return "mirado"
	elif(label==5):
		return "greenies"
	elif(label==6):
		return "outlet-plug"
	elif(label==7):
		return "glue"
	elif(label==8):
		return "highlighter"
	elif(label==9):
		return "cheezit"
	elif(label==10):
		return "spark-plug"
	else:
		return "expo"
	

def process(result):
	
	img = cv2.imread(saveStr)
	imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

	img = imutils.resize(img, height = 600)
	imgray = imutils.resize(imgray, height = 600)

	final = img.copy()

	thresh, imgray = CVAlgo.filtering(img, imgray, z)

	__ , contours, hierarchy = cv2.findContours(thresh.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
	
	c = sorted(contours, key = cv2.contourArea, reverse = True )[0]
	
	rect =  cv2.minAreaRect(c)
	
	box = numpy.int0(cv2.boxPoints(rect))

	cv2.drawContours(img,[box],-1,(0,255,0),2)
	
	cv2.putText(img,Imagelabel(result), (img.shape[1]-400, img.shape[0] - 400), cv2.FONT_HERSHEY_SIMPLEX, 2.0, (0,255,0), 3)
	
	cv2.imshow("Image",img)
	cv2.imwrite(saveStr2,img);


cap = cv2.VideoCapture(0);

while(True):

	ret,frame= cap.read();
	cv2.imshow('img',frame);
	
	cv2.imwrite(saveStr,frame);
	img = Image.open(saveStr);
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
	img2 = img.resize((new_width, new_height), Image.ANTIALIAS)
	img2.save(saveStr2);
	
	img.save(saveStr)
	result = main()
	print result
	img=process(result)

	
	if cv2.waitKey(1)&0xFF == ord('q'):
		cv2.destroyAllWindows()
		break
	
#detect.detectBin()


num = main()
print 'Here is the prediction:'
print num
