import cv2
import numpy as np


font = cv2.FONT_HERSHEY_COMPLEX 
STOPLIGHT_SIZE = 40

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

# Returns 0 for not close enough to any stoplight, 1 for red, and 2 for green
light_test = cv2.imread('./images/stoplights.jpg')


def Find_Stoplight(image_rgb):
    # Call helper function to create blob detector
    circle_detector = Create_Circle_Detector()

    # It converts the BGR color space of image to HSV color space 
    image_hsv = cv2.cvtColor(image_rgb, cv2.COLOR_BGR2HSV)

    # Threshold of red and green in HSV space 
    lower_red = np.array([0, 140, 100]) 
    upper_red = np.array([10, 255, 255]) 
    lower_green = np.array([80, 160, 40])
    upper_green = np.array([90, 255, 255])
  
    # Black-and-white masks for each color
    red_mask = cv2.inRange(image_hsv, lower_red, upper_red)
    red_mask = cv2.bitwise_not(red_mask)
    green_mask = cv2.inRange(image_hsv, lower_green, upper_green) 

    # Blur and erode to eliminate noise
    red_mask = cv2.blur(red_mask, (40, 40))
    red_mask = cv2.erode(red_mask, (80,80), iterations=4)
    #green_mask = cv2.blur(green_mask, (4,4))

    # TODO: just pick an area of interest and count the pixels in the mask
    
    # The black region in the mask has the value of 0, 
    # so when multiplied with original image removes all regions of other colors
    red = cv2.bitwise_and(image_rgb, image_rgb, mask = red_mask) 
    #green = cv2.bitwise_and(image_rgb, image_rgb, mask = green_mask)

    # Detect blobs 
    rlight_keypoints = circle_detector.detect(red_mask)
    
    # Draw blobs on our image as red circles 
    blank = np.zeros((1, 1))  
    image_rgb = cv2.drawKeypoints(image_rgb, rlight_keypoints, blank, (0, 0, 255), 
                            cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS) 
    
    number_of_blobs = len(rlight_keypoints) 
    text = "Number of Circular Blobs: " + str(len(rlight_keypoints)) 
    cv2.putText(image_rgb, text, (20, 550), 
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 100, 255), 2) 
    
    # Show blobs 
    cv2.imshow("Filtering Circular Blobs Only", image_rgb)
    cv2.imshow('rmask', red_mask) 
    cv2.waitKey(0)

    #image_rgb = cv2.resize(image_rgb, (image_rgb.shape[1] // 8, image_rgb.shape[0] // 8))
    #red_mask = cv2.resize(red_mask, (red_mask.shape[1] // 8, red_mask.shape[0] // 8))
    #red_result = cv2.resize(red_result, (red_result.shape[1] // 8, red_result.shape[0] // 8))
    #green_mask = cv2.resize(green_mask, (green_mask.shape[1] // 8, green_mask.shape[0] // 8))
    #green_result = cv2.resize(green_result, (green_result.shape[1] // 8, green_result.shape[0] // 8))

    #cv2.imshow('rgb', image_rgb) 
    #cv2.imshow('rresult', red_result)
    #cv2.imshow('gmask', green_mask) 
    #cv2.imshow('gresult', green_result) 
      
    #cv2.waitKey(0) 
    #acicv2.destroyAllWindows() 

    return

def Create_Circle_Detector():
    # Set our filtering parameters 
    # Initialize parameter setting using cv2.SimpleBlobDetector 
    params = cv2.SimpleBlobDetector_Params() 
    
    # Set Area filtering parameters 
    params.filterByArea = True
    params.minArea = STOPLIGHT_SIZE
    
    # Create a detector with the parameters 
    detector = cv2.SimpleBlobDetector_create(params) 
        
    return detector 


