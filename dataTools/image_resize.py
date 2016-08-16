from PIL import Image
import os

new_width = 75
new_height = 75


root_path = '../images/'
slash = '/'
root = os.listdir(root_path)

print 'Iterating through folders:'

# Iterating through the item directories to get dir
for folders in root:

	print folders

	folders = folders + slash

	i = 0
	for files in os.listdir(root_path + slash + folders):
		img = Image.open(root_path + folders + files)
		width = img.size[0]
		height = img.size[1]

		
		img2 = img.resize((new_width, new_height), Image.ANTIALIAS)

		saveStr = "../images/" + folders + str(i) + ".jpg"
		img2.save(saveStr)
		i = i + 1
