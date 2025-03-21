import cv2
import numpy as np
import re
import pytesseract
from findAngle import getAverageAngle
pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"

font = cv2.FONT_HERSHEY_COMPLEX

ROI_WIDTH_CONSTANT = 1
ROI_HEIGHT_CONSTANT = 1.5

# Thresholds of signal and sign colors
SIGN_MIN_SIZE = 20
LOWER_RED = np.array([0, 110, 110]) 
UPPER_RED = np.array([5, 255, 255]) 

LOWER_GREEN = np.array([80, 100, 40])
UPPER_GREEN = np.array([90, 255, 255])

LOWER_BLUE = np.array([105, 100,  100])
UPPER_BLUE = np.array([115, 250, 255])

def findOffset(frame, ret):
    image_col = frame

    # Image dimensions
    height, width, channels = image_col.shape

    # Convert to grayscale
    image = cv2.cvtColor(image_col, cv2.COLOR_BGR2GRAY)
    image = cv2.GaussianBlur(image, (5, 5), 0)

    # Apply thresholding
    # ret, image = cv2.threshold(image, 120, 255, cv2.THRESH_BINARY_INV)
    #kernel = np.ones((20, 20), np.uint8)

    # Region of interest for line detection
    # adjust constants to change roi dimension
    box_width_track = int(width * ROI_WIDTH_CONSTANT)  
    box_height_track = int(height // ROI_HEIGHT_CONSTANT)      
    box_x_track = (width - box_width_track) // 2
    box_y_track = height - box_height_track  

    # ROI variables
    roi_x, roi_y, roi_w, roi_h = box_x_track, box_y_track, box_width_track, box_height_track
        
    # square where tracking takes place
    roi = image[roi_y:roi_y + roi_h, roi_x:roi_x + roi_w]
    cv2.rectangle(image_col, (roi_x, roi_y), (roi_x + roi_w, roi_y + roi_h), (255, 255, 0), 5)
    ret, roi = cv2.threshold(roi, 120, 255, cv2.THRESH_BINARY_INV)
    # Apply erosion
    roi = cv2.erode(roi,None, iterations=2)

    # Find contours
    contours, hierarchy = cv2.findContours(roi, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Find the average distance of dashes from center line
    offsetSum = 0

    # Area to remove really small contours that maybe noise 
    min_contour_area = 20

    for cnt in contours: 
        approx = cv2.approxPolyDP(cnt, 0.009 * cv2.arcLength(cnt, True), True) 

        # Bound rectangles around contours
        x, y, w, h = cv2.boundingRect(cnt)

        # Check if the contour is within the ROI bounds
        area = cv2.contourArea(cnt)
        if area < min_contour_area :
            continue

        # Aspect ratio for filtering
        aspect_ratio = w / float(h)

        # Solidity filtering
        hull = cv2.convexHull(cnt)
        hull_area = cv2.contourArea(hull)
        solidity = area / hull_area if hull_area > 0 else 0
        
        # method to avoid really irregular shapes
        if aspect_ratio < .2 or aspect_ratio > 4.5:  # avoid thin shapes
            continue
        if solidity < .2:  # avoid weird shapes
            continue

        # Adjusting the roi offset
        approx[:, 0, 0] += roi_x # add all x-approx & y-approx values with roi offset
        approx[:, 0, 1] += roi_y 
        x += roi_x # add all x&y values with roi offset
        y += roi_y

        # Draw contours and bounding box on the original image
        cv2.drawContours(image_col, [approx], 0, (0, 0, 255), 5)  
        cv2.rectangle(image_col, (x, y), (x + w, y + h), (0, 255, 0), 5)

        # Center of the box
        box_center_x = x + w // 2
        box_center_y = y + h // 2

        # Line from center of box to middle of screen for error reference
        contour_distance = box_center_x - (width // 2)
        offsetSum += contour_distance
        # print(contour_distance)
        cv2.line(image_col, (box_center_x, box_center_y), (width // 2, box_center_y), (0, 255, 255), 2)
        text = f"Error: {contour_distance} px" 
        cv2.putText(image_col, text, (box_center_x + 10, box_center_y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 255), 2, cv2.LINE_AA)

        # Used to flatten the array containing the coordinates of the vertices
        n = approx.ravel()  
        i = 0
    
        for j in n: 
            if(i % 2 == 0): 
                x = n[i] 
                y = n[i + 1] 
    
                # String containing the coordinates
                string = str(x) + " " + str(y)  
    
                if(i == 0): 
                    # Text on topmost coordinate
                    cv2.putText(image_col, "Arrow tip", (x, y), font, 0.5, (255, 0, 0))  
                else: 
                    # Text on remaining coordinates
                    cv2.putText(image_col, string, (x, y), font, 0.5, (0, 255, 0))  
            i = i + 1

    # Showing the final image. 
    new_width = image.shape[1] 
    new_height = image.shape[0] 
    # Guide line for center
    center_x, center_y = width // 2, height // 2
    cv2.line(image_col, (center_x, 0), (center_x, height), (255, 0, 0), 5)

    # Resize the image
    #resized_image = cv2.resize(image, (new_width, new_height))
    #resized_image_col = cv2.resize(image_col, (new_width, new_height))

    # debug sum value
    # print(offsetSum)
    
    cv2.imshow('image', image)
    cv2.imshow('image_col', image_col)
    return offsetSum

#  Returns number on yellow circular speed limit signs. Returns Null if none are found.
def detectSpeedLimit(image_rgb, car):
    circles = findColorCircles(image_rgb, 'blue')

    if circles is None:
        return 0
    else:
        circle = getBiggestCircle(circles)
    car.stop_motors()
    # if circles is not None:
    #     circles = np.uint16(np.around(circles))
    #     for i in circles[0, :]:
    #         center = (i[0], i[1])
    #         cv2.circle(image_rgb, center, 1, (0, 0, 0), 3) # draw center
    #         radius = i[2]
    #         cv2.circle(image_rgb, center, radius, (0, 0, 0), 8) #draw outline
    
    #image_rgb = cv2.resize(image_rgb, (image_rgb.shape[1] // 6, image_rgb.shape[0] // 6)

    #circle = np.uint16(np.around(circles))
    #print(circle)
    x = int(circle[0])
    y = int(circle[1]) 
    r = int(circle[2])

    # Use a fraction of the detected radius to crop only the inner region.
    new_r = int(r * 0.6)
    
    # Define cropping boundaries while preventing going out of the image bounds
    x1 = max(0, x - new_r)
    y1 = max(0, y - new_r)
    x2 = min(image_rgb.shape[1], x + new_r)
    y2 = min(image_rgb.shape[0], y + new_r)
    
    # Crop the ROI from the image
    cropped = image_rgb[y1:y2, x1:x2]
    #print(f"{image_rgb[y1:y2, x1:x2]}")
    
    # Preprocess the cropped image for OCR:
    # 1. Convert to grayscale.
    gray_cropped = cv2.cvtColor(cropped, cv2.COLOR_BGR2GRAY)
    # 2. Apply thresholding with Otsu's method.
    _, thresh = cv2.threshold(gray_cropped, 130, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    thresh = cv2.dilate(thresh, np.ones((3, 3), np.uint8), iterations=1)
    
    cv2.imshow("iMAGE MASK", thresh)
    
    # 3. Optionally perform morphological opening to reduce noise.
    #kernel = np.ones((1, 1), np.uint8)
    #thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=10)
    
    # Configure pytesseract to read only digits:
    config = r'-c tessedit_char_whitelist=0123456789 --psm 7'
    text = pytesseract.image_to_string(thresh, config=config)
    print(f"Detected text: {text.strip()}")
    text = text.strip()
    # For visualization, draw the detected circle and ROI on the original image
    #cv2.circle(image_rgb, (x, y), r, (0, 255, 0), 2)
    #cv2.rectangle(image_rgb, (x1, y1), (x2, y2), (255, 0, 0), 2)
    #cv2.putText(image_rgb, text.strip(), (x1, y1 - 10),
    #cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                
    return 0 if text == '' else int(text)
   
   
# Takes an image and a color either 'red' or 'green.' Finds a circle of that color and returns it's radius.
# Returns 0 if no circles found.
def findStoplight(image_rgb, color):

    circles = findColorCircles(image_rgb, color)

    # Each circle in circles [h, k, r]
    if circles is None:
        return 0
    else:
        circle = getBiggestCircle(circles)
        return circle[2]
    
# Detects circles of a specific color and returns a list of circle's with each circle represented with it's center 
# and radius in [h, k, r] format.
def findColorCircles(image_rgb, color):
    # convert to HSV color space for better thresholding
    image_hsv = cv2.cvtColor(image_rgb, cv2.COLOR_BGR2HSV)

    # Make a black-and-white mask of a specific color
    if (color == 'red'):
        mask = cv2.inRange(image_hsv, LOWER_RED, UPPER_RED)
    elif (color == 'green'):
        mask = cv2.inRange(image_hsv, LOWER_GREEN, UPPER_GREEN) 
    elif (color == 'blue'):
        mask = cv2.inRange(image_hsv, LOWER_BLUE, UPPER_BLUE)
    else:
        return None

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
                               minRadius=SIGN_MIN_SIZE, maxRadius=0)
    return circles

# Takes a list of circles and returns the radius of the largest circle
def getBiggestCircle(circles):

    if circles is not None:
        biggestCircle = circles[0][0]
        for circle in circles[0, :]:
            #print(f"maxRadius: {biggestCircle[2]} currentRadius: {circle[2]}")
            if circle[2] > biggestCircle[2]:
                biggestCircle = circle
        return biggestCircle
    else:
        return 0