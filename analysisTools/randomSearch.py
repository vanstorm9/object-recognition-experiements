# Simple CNN model for CIFAR-10
import numpy
from time import time
import sys
import os


from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import Flatten
from keras.constraints import maxnorm
from keras.optimizers import SGD
from keras.layers.convolutional import Convolution2D
from keras.layers.convolutional import MaxPooling2D
from keras.utils import np_utils

from sklearn.grid_search import RandomizedSearchCV
from scipy.stats import uniform as sp_rand
from keras.wrappers.scikit_learn import KerasClassifier


# To reference a python file that in another directory
sys.path.append('../')

import imageDataExtract as dataset


response = 'a'

# Will ask the user whether he wants to load or create new matrix
while True:
	print 'Press [l] to load matrix or [n] to create new dataset'
	response = raw_input()

	if response == 'l':
		break
	if response == 'n':
		break



os.chdir('../')

# fix random seed for reproducibility
seed = 7
numpy.random.seed(seed)

# load data 
if response == 'l':
	matrix_path = 'numpy-matrix/main-0.npy'
	label_path = 'numpy-matrix/label-0.npy'
	X, y = dataset.load_matrix_no_cross(matrix_path, label_path)

else:
	X, y = dataset.load_data_no_cross()


# normalize inputs from 0-255 to 0.0-1.0
X = X.astype('float32')

print X.shape



X = X / 255.0

# one hot encode outputs
y = np_utils.to_categorical(y)
num_classes = y.shape[1]

# Function to create model, required for KerasClassifier
def create_model(optimizer='sgd'):
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
	model.compile(loss='categorical_crossentropy', optimizer=optimizer, metrics=['accuracy'])
	return model

t0 = time()



model = KerasClassifier(build_fn=create_model, verbose=0)

batch_size = [10,20,32,50,60,80,100]
epochs = [15, 20, 25, 30, 40]

param_grid = {'kernel': sp_rand()}

param_grid = dict(batch_size=batch_size, nb_epoch=epochs)
grid = RandomizedSearchCV(estimator=model, param_distributions=param_grid, n_iter=100)

t0 = time()

print 'Analyzing model. This can take a while . . .'
grid_result = grid.fit(X,y)
print grid

total_time = time() - t0
print 'Analysis time: ',total_time,' s'

# summarize results
print("Best: %f using %s" % (grid_result.best_score_, grid_result.best_params_))
for params, mean_score, scores in grid_result.grid_scores_:
	print("%f (%f) with: %r" % (scores.mean(), scores.std(), params))

