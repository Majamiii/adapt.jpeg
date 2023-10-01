# import the necessary packages
from skimage.metrics import structural_similarity as ssim
import matplotlib.pyplot as plt
import numpy as np
import cv2

import subprocess
import os
from PIL import Image
from array import *

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

	return m, s


def one_image(og, ad, jpg):

	original = cv2.imread(og) #load imgs
	adaptive = cv2.imread(ad)
	jpeg = cv2.imread(jpg)

	original = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY) #convert og to grayscale
	adaptive = cv2.cvtColor(adaptive, cv2.COLOR_BGR2GRAY)
	jpeg = cv2.cvtColor(jpeg, cv2.COLOR_BGR2GRAY)

	adapt_m, adapt_s = compare_images(original, adaptive)

	# the lower the mse && the higher the ssim => imgs are more similar

	jpeg_m, jpeg_s = compare_images(original, jpeg)

	dif_m = jpeg_m - adapt_m
	dif_s = adapt_s - jpeg_s

	# if both are positive it means that the adapt. is closer to the original than the jpeg of that rate

	return dif_m, dif_s





def comparison():

	dir_names = ["aerials", "misc", "sequences", "textures"]

	cntr = 0

	mse_arr = list()
	ssim_arr = list()

	rate_dirs = ["55", "60", "65", "70", "75", "80", "85", "90", "95"]


	for i in range(len(dir_names)):			#loop through all 4 folders

		input_dir = "./doutput/" + dir_names[i]

		for filename in os.listdir(input_dir):   #for every image in folders with images compressed with the adaptive jpeg
				adapt_jpg = os.path.join(input_dir, filename)
				original = os.path.join("./images", dir_names[i], filename)

				for j in range(len(rate_dirs)):				#for every rate of regularly compressed jpegs
					reg_jpg = os.path.join("jpegs", rate_dirs[j], dir_names[i], filename)

					cntr = cntr + 1

					m, s = one_image(original, adapt_jpg, reg_jpg)

					mse_arr.append(m)
					ssim_arr.append(s)
					print(mse_arr[cntr-1])

	# find_avgs(mse_arr, ssim_arr)


	

comparison()




# CODE BELOW THIS POINT:
# for new (de)compression when something is changed in libjpeg
	
# + regular jpeg compression (9 different rates)

# basically getting the dataset ready for the comparisons








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
					im.save(os.path.join("jpegs", out_dirs[j], dir_names[i], filename), 'JPEG', quality=rates[j])


