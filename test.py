import cv2
import numpy as np

# Load the image
image_col = cv2.imread('./images/imagecarpet.jpg')

# Convert the image to grayscale
image_gray = cv2.cvtColor(image_col, cv2.COLOR_BGR2GRAY)

# Enhance contrast (optional, depends on your image quality)
image_contrast = cv2.equalizeHist(image_gray)

# Apply a binary threshold to isolate the black line (dark regions)
_, binary_image = cv2.threshold(image_contrast, 50, 255, cv2.THRESH_BINARY_INV)

# Morphological transformation to fill small gaps and connect lines
kernel = np.ones((5, 5), np.uint8)  # Kernel for dilation
dilated_image = cv2.dilate(binary_image, kernel, iterations=1)

# Find contours (the edges of the black line)
contours, _ = cv2.findContours(dilated_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Draw the contours on the original image (for visualization)
cv2.drawContours(image_col, contours, -1, (0, 255, 0), 2)

# Resize the image to its original size before showing it
height, width = image_col.shape[:2]
cv2.namedWindow('Detected Line', cv2.WINDOW_NORMAL)
cv2.resizeWindow('Detected Line', width, height)

# Display the original image with contours
cv2.imshow('Detected Line', image_col)

# Wait for a key press and close all OpenCV windows
cv2.waitKey(0)
cv2.destroyAllWindows()
