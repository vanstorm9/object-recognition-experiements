#
#	decide whether to use gripping hand
#	or use suction cup and some specific
#	parameters that we need
#


from PIL import Image
import numpy as np
import cv2
from imgops import imutils
import CVAlgo
#above is the module called
#####

perPixel = 4.677083333
deviation = 350/ perPixel  # arduino number converted to the pixel numbel

def proofCentre(objCentre,imgCentre):   #This help to make centre of robotic 
					#hand face with the centre of the object
					#only for x axis, y is processed in
					#objectMethod function
	#however img centre is the centre of webcam, not the robotic hand, so we should minus the deviation in arduino 
	handCentre = imgCentre - deviation
	
	#Get the bias between centre of robotic hand and centre of object
	bias=handCentre-objCentre
	if bias < 0 : 		#This means hand need to move rightward 
		bias = -bias * perPixel 
	else :			# move leftward
		bias = bias * perPixel

	return np.int0(bias)





#def objectMethod(obj):





