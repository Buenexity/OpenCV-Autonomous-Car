import cv2 as cv2
import numpy as np

font = cv2.FONT_HERSHEY_COMPLEX 



# Load the image
image_col = cv2.imread('./images/track.jpg')
height, width , channels = image_col.shape

#Guide Line
center_x, center_y = width // 2, height // 2
cv2.line(image_col, (center_x, 0), (center_x, height), (255, 0, 0), 5)  # Blue line with thickness of 5


# Convert to grayscale
image = cv2.cvtColor(image_col, cv2.COLOR_BGR2GRAY)

# Apply thresholding 
# inverted background so that border dosent show up
ret, image = cv2.threshold(image, 120, 255, cv2.THRESH_BINARY_INV)

# Define kernel for erosion
kernel = np.ones((17, 17), np.uint8)

# Apply erosion
image = cv2.erode(image, kernel, iterations=1)

# Find contours
contours, hierarchy = cv2.findContours(image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# Iterate through contours
for cnt in contours:
    if cv2.contourArea(cnt) > 100:  # Ignore small contours
        approx = cv2.approxPolyDP(cnt, 0.009 * cv2.arcLength(cnt, True), True)
        
        #red contour on original image
        cv2.drawContours(image_col, [approx], 0, (0, 0, 255), 5)
        

        x, y, w, h = cv2.boundingRect(cnt)
        cv2.rectangle(image_col, (x, y), (x + w, y + h), (0, 255, 0), 5)
        
        #center of screen
        box_center_x = x + w // 2
        box_center_y = y + h // 2

        #Line from center of box to middle of screen for error refrence
        cv2.line(image_col, (box_center_x, box_center_y), (center_x, box_center_y), (0, 255, 255), 2)  # Yellow line

        # Annotate points
        n = approx.ravel()
        i = 0
        for j in n:
            if i % 2 == 0:
                x = n[i]
                y = n[i + 1]
                
                # Label first point as "Arrow tip"
                if i == 0:
                    cv2.putText(image_col, "Arrow tip", (x, y), font, 0.5, (255, 0, 0))
                else:
                    cv2.putText(image_col, f"{x}, {y}", (x, y), font, 0.5, (0, 255, 0))
            i += 1

#grayscale back to BGR
image_bgr = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)

#contours on processed image
cv2.drawContours(image_bgr, contours, -1, (0, 255, 128), 3)

# Resize images for display
new_width = image.shape[1] // 2
new_height = image.shape[0] // 2

# helps to make the window smaller
scale_factor = 0.25 
resized_image = cv2.resize(image_bgr, None, fx=scale_factor, fy=scale_factor, interpolation=cv2.INTER_AREA)
resized_image_col = cv2.resize(image_col, None, fx=scale_factor, fy=scale_factor, interpolation=cv2.INTER_AREA)

# Display results
cv2.imshow('Processed Image', resized_image)
cv2.imshow('Contours on Original', resized_image_col)
cv2.waitKey(0)
cv2.destroyAllWindows()