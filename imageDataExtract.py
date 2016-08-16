from PIL import Image
from sklearn import cross_validation
import numpy as np
import os

def load_data():
	root_path = 'images/'
	slash = '/'
	root = os.listdir(root_path)

	print 'Iterating through folders'

	# Iterating through the item directories

	labelnum = 0
	i = 0
	for folders in root:
		print '-',folders


		folders = folders + slash
		
		j = 0
		for files in os.listdir(root_path + folders):
			imgO = Image.open(root_path + folders + files)
			img = np.array(imgO).transpose()
		
		
			if i == 0:
				# This is our first time with the image, so we initalize our main array
				main_ar = np.array([img])
				label = np.array([labelnum])
			else:
				# We will just concatenate the array then
				main_ar = np.concatenate(([img], main_ar))
				label = np.concatenate((label, [labelnum]))

			# Adding our label array
			i = i + 1
		labelnum = labelnum + 1


	# We have our maian array and label array
	'''
	print main_ar.shape	
	print label.shape
	'''

	# Now we shall preform cross validation
	X_train, X_test, y_train, y_test = cross_validation.train_test_split(main_ar, label, test_size = 0.2, random_state=0)
	'''
	print X_train.shape
	print X_test.shape
	print y_train.shape
	print y_test.shape
	'''
	return X_train, y_train, X_test, y_test




