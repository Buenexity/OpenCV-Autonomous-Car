import cv2 as cv2
import numpy as np


font = cv2.FONT_HERSHEY_COMPLEX 

def FindOffset():
    # Load the image
    image_col = cv2.imread('./images/track.jpg')

    #image dimensions
    height, width, channels = image_col.shape

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

    # Find the average distance of dashes from center line
    offsetSum = 0
    for cnt in contours : 
        approx = cv2.approxPolyDP(cnt, 0.009 * cv2.arcLength(cnt, True), True) 

        #Bound rectangles around contours
        x, y, w, h = cv2.boundingRect(cnt)

        # draws boundary of contours. 
        cv2.drawContours(image_col, [approx], 0, (0, 0, 255), 5)  
        #Display rectangle
        cv2.rectangle(image_col, (x, y), (x + w, y + h), (0, 255, 0), 5)

        # Center of the box
        box_center_x = x + w // 2
        box_center_y = y + h // 2

        #Line from center of box to middle of screen for error reference
        # Error = Image X/2 - Contour X/2
        contour_distance = box_center_x - (width // 2)
        offsetSum += contour_distance
        print(offsetSum)
        cv2.line(image_col, (box_center_x, box_center_y), (width // 2, box_center_y), (0, 255, 255), 2)
        text = f"Error: {contour_distance} px" 
        cv2.putText(image_col, text, (box_center_x + 10, box_center_y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2, cv2.LINE_AA)

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
    # Guide line for center
    center_x, center_y = width // 2, height // 2
    cv2.line(image_col, (center_x, 0), (center_x, height), (255, 0, 0), 5)

    # Resize the image
    resized_image = cv2.resize(image, (new_width, new_height))
    resized_image_col = cv2.resize(image_col, (new_width, new_height))

    cv2.imshow('image', resized_image)
    cv2.imshow('image_col', resized_image_col)    
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return offsetSum