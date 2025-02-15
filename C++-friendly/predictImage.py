# Simple CNN model for CIFAR-10
import numpy
import matplotlib.pyplot as plt
from time import time

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
import cv2

imgToLoad = '../test-images/imagesToTest/9.jpg'


modelPath = "../models/model-0.h5"


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
	#print labelName
	###

	predVal = 26-1-pred[0]   
	result = getPredictionValue(predVal)
	
	return result



num = main()
print 'Here is the prediction:'
print num
