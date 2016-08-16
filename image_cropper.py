from PIL import Image
import os

root_path = '../../dataset/'
slash = '/'
root = os.listdir(root_path)

print 'Iterating through folders:'

# Iterating through the item directories to get dir
for folders in root:

	print folders

	folders = folders + slash

	i = 0
	for files in os.listdir(root_path + folders):
		img = Image.open(root_path + folders + files)
		width = img.size[0]
		height = img.size[1]

		half_width = img.size[0]/2
		half_height = img.size[1]/2

		img2 = img.crop(
			(
				half_width-200,
				half_height-300,
				half_width+400,
				half_height+250
			)
		)
		saveStr = "images/" + folders + str(i) + ".jpg"
		img2.save(saveStr)
		i = i + 1
