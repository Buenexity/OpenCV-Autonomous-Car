import cv2
import numpy as np
from imageProcessing import findOffset
from findAngle import getAverageAngle


# Load the image
image_col = cv2.imread('.\images\\track90revangled.png')

image = cv2.cvtColor(image_col, cv2.COLOR_BGR2GRAY)
image = cv2.GaussianBlur(image, (5, 5), 0)

ret, image = cv2.threshold(image, 120, 255, cv2.THRESH_BINARY_INV)

# Find contours (the edges of the black line)
contours, _ = cv2.findContours(image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

angle = getAverageAngle(contours, image_col)
print(angle)
# print(findOffset(image_col, _)) 

# Draw the contours on the original image (for visualization)
cv2.drawContours(image_col, contours, -1, (0, 255, 0), 2)

# Resize the image to its original size before showing it
# height, width = image_col.shape[:2]
cv2.namedWindow('Detected Line', cv2.WINDOW_NORMAL)
# cv2.resizeWindow('Detected Line', width, height)

# Display the original image with contours
cv2.imshow('Detected Line', image_col)

# Wait for a key press and close all OpenCV windows
cv2.waitKey(0)
cv2.destroyAllWindows()
