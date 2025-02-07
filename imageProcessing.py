import cv2 as cv2
import numpy as np


font = cv2.FONT_HERSHEY_COMPLEX 

# Load the image
# image = cv2.imread('image.jpg')
image_col = cv2.imread('./images/imagecarpet.jpg')
#image_col = cv2.imread('./images/imagecarpet2.jpg')

# Convert to grayscale
image = cv2.cvtColor(image_col, cv2.COLOR_BGR2GRAY)

# Apply thresholding
ret, image = cv2.threshold(image, 120, 255, cv2.THRESH_BINARY)



kernel = np.ones((17, 17), np.uint8)

# # Apply erosion
image = cv2.erode(image, kernel, iterations=1)



# Find contours
contours, hierarchy = cv2.findContours(image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# Draw contours
#cv2.drawContours(image, contours, -1, (0, 255, 0), 3)




# Going through every contours found in the image. 
for cnt in contours : 
  
    approx = cv2.approxPolyDP(cnt, 0.009 * cv2.arcLength(cnt, True), True) 
  
    # draws boundary of contours. 
    cv2.drawContours(image_col, [approx], 0, (0, 0, 255), 5)  
  
    # Used to flatted the array containing 
    # the co-ordinates of the vertices. 
    n = approx.ravel()  
    i = 0
  
    for j in n : 
        if(i % 2 == 0): 
            x = n[i] 
            y = n[i + 1] 
  
            # String containing the co-ordinates. 
            string = str(x) + " " + str(y)  
  
            if(i == 0): 
                # text on topmost co-ordinate. 
                cv2.putText(image_col, "Arrow tip", (x, y), 
                                font, 0.5, (255, 0, 0))  
            else: 
                # text on remaining co-ordinates. 
                cv2.putText(image_col, string, (x, y),  
                          font, 0.5, (0, 255, 0))  
        i = i + 1
  
# Showing the final image. 


new_width = image.shape[1] // 2
new_height = image.shape[0] // 2

# Resize the image
resized_image = cv2.resize(image, (new_width, new_height))
resized_image_col = cv2.resize(image_col, (new_width, new_height))

cv2.imshow('image2', resized_image)
cv2.imshow('image_col', resized_image_col)    
cv2.waitKey(0)
cv2.destroyAllWindows()

