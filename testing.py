import cv2
import numpy as np

# Read the image
image = cv2.imread('./images/image.jpg')

# Define the coordinates of the top-left corner and the size of the ROI
x, y, w, h = 100, 100, 200, 200  # Example values for the ROI

# Extract the ROI using slicing
roi = image[y:y+h, x:x+w]

# Convert to grayscale
gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

# Apply threshold or edge detection to find contours (for example using Canny edge detection)
edges = cv2.Canny(gray, 100, 200)

# Find contours on the thresholded image
contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Create an empty image to draw contours on
contour_image = np.zeros_like(roi)

# Loop through all contours and draw the ones within the ROI on the contour image
for contour in contours:
    # If you want to filter based on area or any other criteria, you can do that here
    cv2.drawContours(contour_image, [contour], -1, (255, 255, 255), 1)  # White color for contours

# Show the contour image
cv2.imshow('Contours in ROI', contour_image)

# Wait for a key press and close the window
cv2.waitKey(0)
cv2.destroyAllWindows()
