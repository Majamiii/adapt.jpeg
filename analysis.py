# import the necessary packages
from skimage.metrics import structural_similarity as ssim
import matplotlib.pyplot as plt
import numpy as np
import cv2


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


def compare_images(imageA, imageB, title):
	# compute the mean squared error and structural similarity
	# index for the images
	m = mse(imageA, imageB)
	s = ssim(imageA, imageB)
	print("mse: ", m, "  ssim: ", s)
	


original = cv2.imread("testimg.bmp") #load imgs
adaptive = cv2.imread("doutput/b.bmp")
jpeg = cv2.imread("jpegs/70/b.jpg")

original = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY) #convert og to grayscale
adaptive = cv2.cvtColor(adaptive, cv2.COLOR_BGR2GRAY)
jpeg = cv2.cvtColor(jpeg, cv2.COLOR_BGR2GRAY)

fig = plt.figure("Images")
images = ("Original", original), ("Adaptive", adaptive), ("JPEG", jpeg)


# compare the images
print("the lower the mse && the higher the ssim => imgs are more similar")
print()
print()

print("og vs og: ")
compare_images(original, original, "Original vs. Original")

print()
print("og vs adaptive jpeg: ")
compare_images(original, adaptive, "Original vs. adaptive jpeg")

print()
print("og vs jpeg rate 70: ")
compare_images(original, jpeg, "Original vs. JPEG")

