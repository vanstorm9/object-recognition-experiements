from PIL import Image
import numpy as np
import os

root_path = 'images/'
slash = '/'
root = os.listdir(root_path)

print 'Iterating through folders'

# Iterating through the item directories


i = 0
for folders in root:
	print '-',folders

	folders = folders + slash

	j = 0
	for files in os.listdir(root_path + folders):
		imgO = Image.open(root_path + folders + files)
		img = np.array(imgO)
		
		if i == 0:
			# This is our first time with the image, so we initalize our main array
			main_ar = np.array([img])
		else:
			# We will just concatenate the array then
			main_ar = np.concatenate((main_ar, [img]))

		i = i + 1


print main_ar.shape	
