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
	# setup the figure
	fig = plt.figure(title)
	plt.suptitle("MSE: %.2f, SSIM: %.2f" % (m, s))
	# show first image
	ax = fig.add_subplot(1, 2, 1)
	plt.imshow(imageA, cmap = plt.cm.gray)
	plt.axis("off")
	# show the second image
	ax = fig.add_subplot(1, 2, 2)
	plt.imshow(imageB, cmap = plt.cm.gray)
	plt.axis("off")
	# show the images
	plt.show()


original = cv2.imread("testimg.bmp") #load imgs
adaptive = cv2.imread("doutput/b.bmp")
jpeg = cv2.imread("jpegs/70/b.jpg")

original = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY) #convert og to grayscale
adaptive = cv2.cvtColor(adaptive, cv2.COLOR_BGR2GRAY)
jpeg = cv2.cvtColor(jpeg, cv2.COLOR_BGR2GRAY)

fig = plt.figure("Images")
images = ("Original", original), ("Adaptive", adaptive), ("JPEG", jpeg)


# loop over the images
for (i, (name, image)) in enumerate(images):
	# show the image
	ax = fig.add_subplot(1, 3, i + 1)
	ax.set_title(name)
	plt.imshow(image, cmap = plt.cm.gray)
	plt.axis("off")
# show the figure
plt.show()
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

