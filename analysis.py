# import the necessary packages
from skimage.metrics import structural_similarity as ssim
import matplotlib.pyplot as plt
import numpy as np
import cv2

import subprocess
import os
from PIL import Image

def mse(imageA, imageB):
	# the 'Mean Squared Error' between the two images is the
	# sum of the squared difference between the two images;
	# NOTE: the two images must have the same dimension

    # mse is derived from eucledian distance

	err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
	err /= float(imageA.shape[0] * imageA.shape[1])
	
	# return the MSE, the lower the error, the more "similar"
	# the two images are
	return err


def compare_images(imageA, imageB):
	# compute the mean squared error and structural similarity
	# index for the images
	m = mse(imageA, imageB)
	s = ssim(imageA, imageB)
	print("mse: ", m, "  ssim: ", s)


def one_image():

	original = cv2.imread("testimg.bmp") #load imgs
	adaptive = cv2.imread("doutput/b.bmp")
	jpeg = cv2.imread("jpegs/70/b.jpg")

	original = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY) #convert og to grayscale
	adaptive = cv2.cvtColor(adaptive, cv2.COLOR_BGR2GRAY)
	jpeg = cv2.cvtColor(jpeg, cv2.COLOR_BGR2GRAY)


	# compare the images
	print("the lower the mse && the higher the ssim => imgs are more similar")
	print()
	print()

	print("og vs og: ")
	compare_images(original, original)

	print()
	print("og vs adaptive jpeg: ")
	compare_images(original, adaptive)

	print()
	print("og vs jpeg rate 70: ")
	compare_images(original, jpeg)




def make():
	makefile_dir = "./build"
	os.chdir(makefile_dir)
	# Run the make command
	subprocess.run(["make", "-j8"])
	os.chdir("..")


def convert_my_alg():			#convert all the images from the dataset using the new, adaptive algorithm
	make()

	dir_names = ["aerials", "misc", "sequences", "textures"]
	dir_imgs = "./images/"

	for i in range(4):			#go through all 4 folders
		input_dir = dir_imgs + dir_names[i]
		coutput_dir = "./coutput/" + dir_names[i]
		doutput_dir = "./doutput/" + dir_names[i]

		for filename in os.listdir(input_dir):   #for every image in those folders
			with Image.open(os.path.join(input_dir, filename)) as im:
				cfilename = os.path.splitext(filename)[0] + ".jpg"
				dfilename = os.path.splitext(filename)[0] + ".bmp"
				jpeg_filename = os.path.splitext(filename)[0] + ".jpg"
				
				subprocess.run(["cjpeg", "-grayscale", "-outfile", os.path.join(coutput_dir, filename), os.path.join(input_dir, filename)])
				subprocess.run(["djpeg", "-bmp", "-outfile", os.path.join(doutput_dir, filename), os.path.join(coutput_dir, filename)])


def convert_all_jpegs():
	dir_names = ["aerials", "misc", "sequences", "textures"]
	out_dirs = ["55", "60", "65", "70", "75", "80", "85", "90", "95"]
	rates = [55, 60, 65, 70, 75, 80, 85, 90, 95]

	for i in range(4):
		input_dir = "./images/" + dir_names[i]

		for filename in os.listdir(input_dir):   #for every image in those folders
			with Image.open(os.path.join(input_dir, filename)) as im:
				jpeg_filename = os.path.splitext(filename)[0] + ".jpg"

				for j in range(len(out_dirs)):
					if not os.path.exists(os.path.join("jpegs", out_dirs[j], dir_names[i])):
						os.mkdir(os.path.join("jpegs", out_dirs[j], dir_names[i]))
					im.save(os.path.join("jpegs", out_dirs[j], dir_names[i], filename), 'JPEG', quality=50)



# convert_all_jpegs()
# one_image()

