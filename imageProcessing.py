import cv2 as cv2
import numpy as np

# Load the image
image = cv2.imread('image.jpg')

# Convert to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Apply thresholding
ret, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

# Find contours
contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# Draw contours
cv2.drawContours(image, contours, -1, (0, 255, 0), 3)


new_width = image.shape[1] // 2
new_height = image.shape[0] // 2

# Resize the image
resized_image = cv2.resize(image, (new_width, new_height))


# Display the image
cv2.imshow('Image with Contours', resized_image)
cv2.waitKey(0)
cv2.destroyAllWindows()

