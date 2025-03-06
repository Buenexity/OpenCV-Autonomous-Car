import cv2
import numpy as np

font = cv2.FONT_HERSHEY_COMPLEX 
STOPLIGHT_MIN_SIZE = 50

# Threshold of red and green stoplights in HSV space 
lower_red = np.array([0, 140, 110]) 
upper_red = np.array([4, 255, 255]) 
lower_green = np.array([80, 160, 40])
upper_green = np.array([90, 255, 255])

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

    # cv2.imshow('image', resized_image)
    # cv2.imshow('image_col', resized_image_col)    
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    return offsetSum


# takes an image and a color either 'red' or 'green.' Finds a circle of that color and returns it's radius.
def Find_Stoplight(image_rgb, color):
    # convert to HSV color space for better thresholding
    image_hsv = cv2.cvtColor(image_rgb, cv2.COLOR_BGR2HSV)

    # Make a black-and-white mask of a specific color
    if (color == 'red'):
        mask = cv2.inRange(image_hsv, lower_red, upper_red)
    elif (color == 'green'):
        mask = cv2.inRange(image_hsv, lower_green, upper_green) 
    else:
        return -1

    # Eliminate noise
    mask = cv2.erode(mask, np.ones((2, 2), np.uint8), iterations=1)
    mask = cv2.blur(mask, (70, 70))
    
    # The black region in the mask has the value of 0
    # so when multiplied with original image removes all regions of other colors
    single_color = cv2.bitwise_and(image_rgb, image_rgb, mask = mask) 

    # convert to grayscale to prepare for Hough transform
    gray = cv2.cvtColor(single_color, cv2.COLOR_BGR2GRAY)

    # Use Hough circles
    rows = gray.shape[0]
    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, rows / 8,
                               param1=100, param2=30,
                               minRadius=STOPLIGHT_MIN_SIZE, maxRadius=300)

    print(circles)
    
    # Drawing on and displaying the image for testing purposes
    if circles is not None:
        circles = np.uint16(np.around(circles))
        for i in circles[0, :]:
            center = (i[0], i[1]) # circle center
            cv2.circle(image_rgb, center, 1, (0, 100, 100), 3) # circle outline
            radius = i[2]
            cv2.circle(image_rgb, center, radius, (255, 0, 255), 3)

    image_rgb = cv2.resize(image_rgb, (image_rgb.shape[1] // 6, image_rgb.shape[0] // 6))
    single_color = cv2.resize(single_color, (single_color.shape[1] // 6, single_color.shape[0] // 6))

    cv2.imshow('circles', image_rgb) 
    cv2.imshow('single color', single_color)
      
    cv2.waitKey(0) 
    cv2.destroyAllWindows() 

    # Each circle in circles [h, k, r]
    if circles is None:
        return 0
    else:
        radius = int(circles[0][0][2])
        # I think this is being affected by earlier code for displaying and may have to remove a [0] in the future
        return radius