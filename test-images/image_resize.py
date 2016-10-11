from PIL import Image
import os
from time import time

new_width = 32
new_height = 32


root_path = './'
slash = '/'
root = os.listdir(root_path)

print 'Iterating through folders:'

t0 = time()

# Iterating through the item directories to get dir
for folders in root:

	print folders

	folders = folders + slash
	folders = './imagesToResize'

	i = 0
	for files in os.listdir(folders):
		img = Image.open(folders + slash + files)
		width = img.size[0]
		height = img.size[1]

		
		img2 = img.resize((new_width, new_height), Image.ANTIALIAS)

		saveStr = folders + slash + str(i) + ".jpg"
		img2.save(saveStr)
		i = i + 1

total_time = time() - t0
print 'Resize time: ', total_time, 's'
