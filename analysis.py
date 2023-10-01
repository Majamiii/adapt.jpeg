# import the necessary packages
from skimage.metrics import structural_similarity as ssim
import matplotlib.pyplot as plt
import numpy as np
import cv2

import subprocess
import os
from PIL import Image
from array import *
from statistics import mean

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



def find_avgs(mse, ssim, size_arr):

	print("mse = mean squared error, ssim = structural similarity")
	print("the smaller the avg difference, more similar the new algorithm is to the og picture than that rate of jpeg compr")
	print("size difference is sizeof(our new pic) - sizeof(regular jpeg)")
	print()

	len_arr = int(len(mse)/9)

	mse_values = list()
	ssim_values = list()
	size_values = list()

	for rate_index in range(9):

		for num_el in range(len_arr):

			mse_values.append(mse[num_el*9 + rate_index])
			ssim_values.append(ssim[num_el*9 + rate_index])
			size_values.append(size_arr[num_el*9 + rate_index])

		mse_avg = round(mean(mse_values), 2)
		ssim_avg = round(mean(ssim_values), 4)
		size_avg = round(mean(size_values)/1000000, 4)

		print("jpeg compression rate: ", 55+rate_index*5)
		print("avg dif of:  1) MSE: ", mse_avg, "   2) SSIM: ", ssim_avg, "    3) size (in MB): ", size_avg)
		print()








def comparison():

	dir_names = ["aerials", "misc", "sequences", "textures"]

	mse_arr = list()
	ssim_arr = list()

	size_arr = list()

	rate_dirs = ["55", "60", "65", "70", "75", "80", "85", "90", "95"]


	for i in range(len(dir_names)):			#loop through all 4 folders

		input_dir = "./doutput/" + dir_names[i]

		for filename in os.listdir(input_dir):   #for every image in folders with images compressed with the adaptive jpeg
				adapt_jpg = os.path.join(input_dir, filename)
				original = os.path.join("./images", dir_names[i], filename)

				adapt_size = os.path.getsize(adapt_jpg)

				# a_size_arr.append(adapt_size)

				for j in range(len(rate_dirs)):				#for every rate of regularly compressed jpegs
					reg_jpg = os.path.join("jpegs", rate_dirs[j], dir_names[i], filename)

					jpg_size = os.path.getsize(reg_jpg)
					# jpg_size_arr.append(jpg_size)
					size_arr.append(adapt_size - jpg_size)		#size_arr contains the difference between size of jpeg pic and new pic

					m, s = one_image(original, adapt_jpg, reg_jpg)		#returns the difference between mses and ssims of adaptive and jpeg

					mse_arr.append(m)
					ssim_arr.append(s)

		print("hi")

	find_avgs(mse_arr, ssim_arr, size_arr)


	

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
