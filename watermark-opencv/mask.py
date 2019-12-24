#basic python/opencv program for watermark placement (bottom right approx). Binary layer blending only.

import cv2
import numpy as np
import imutils
#load the images
#----------

img1 = cv2.imread("sydney.jpg")
img2 = cv2.imread("yuniktmr.jpg")
x1, y1 = img1.shape[:2]
img2 = imutils.resize(img2, width = 200)
aspect_ratio = img2.shape[1]/img2.shape[0]

#info display

print("[INFO] Your background image is {} px tall and {} px wide".format(x1, y1))
print("[INFO] Your watermark image is {} px tall and {} px wide".format(img2.shape[0], img2.shape[1]))
print("[INFO] Aspect ratio for your watermark = {}".format(aspect_ratio))

#INPUT LINE FOR THE WATERMARK PLACEMENT
offset = int(input("\n\nEnter the offset for the watermark to be placed \n"))
if offset > 100 or offset < 0:
	print("Incompatble offset. Setting default offset to 50")
	offset = 50
#---------------------------------------

#x = int(input("\n\nEnter the x-cordinate for the watermark to be placed \n"))
#y = int(input("Enter the y-cordinate for the watermark to be placed \n"))

#------------------------------------------------

rows, cols, channels = img2.shape

#handle errant placement coordinates

#if x + rows > img1.shape[0]:
#	x = img1.shape[0] - x
#if y + rows > img1.shape[1]:
#	y = img1.shape[0] - y

#placement region 

x2,y2 = img2.shape[:2]


roi = img1[x1 - x2 - offset : x1 - offset, y1 - y2- offset : y1 - offset]

# foreground masking

img2gray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

ret, mask = cv2.threshold(img2gray, 220, 255, cv2.THRESH_BINARY)

cv2.imshow("mask",mask)

mask_inv = cv2.bitwise_not(mask)
cv2.imshow("inverted mask", mask_inv)


#background image with the fg mask applied

img1_bg = cv2.bitwise_and(roi, roi, mask = mask)
cv2.imshow("img1 bg", img1_bg)

#foreground image with the white on black mask applied
img2_fg = cv2.bitwise_and(img2, img2, mask = mask_inv)
img2_fg = cv2.dilate(img2_fg, (5,5), iterations = 1)
cv2.imshow("img2_fg", img2_fg)

#blend the two layers
dst = cv2.add(img1_bg, img2_fg)

#replace the background roi with the foreground layer

img1[x1 - x2 - offset : x1 - offset, y1 - y2- offset : y1 - offset] = dst

#final output image
cv2.imshow("dest", img1)


cv2.waitKey(0)