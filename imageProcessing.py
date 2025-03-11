import cv2
import numpy as np
import re
import pytesseract
from findAngle import getAverageAngle
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

font = cv2.FONT_HERSHEY_COMPLEX

LOWER_YELLOW = np.array([20, 200, 130])
UPPER_YELLOW = np.array([30, 255, 250])

STOPLIGHT_MIN_SIZE = 50
ROI_WIDTH_CONSTANT = 0.8
ROI_HEIGHT_CONSTANT = 2


# Threshold of red and green stoplights in HSV space 
lower_red = np.array([0, 140, 110]) 
upper_red = np.array([4, 255, 255]) 
lower_green = np.array([80, 160, 40])
upper_green = np.array([90, 255, 255])

def FindOffset(frame):
    image_col = frame;

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
        print(contour_distance)
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
    print(offsetSum)
    
    cv2.imshow('image', image)
    cv2.imshow('image_col', image_col)
    return offsetSum


def SpeedLimitDetection(image_path):
    # Read the input image
    src = cv2.imread(image_path)

    # Convert from BGR to HSV color space
    image_hsv = cv2.cvtColor(src, cv2.COLOR_BGR2HSV)

    # Create a mask for all pixels within the yellow range
    mask = cv2.inRange(image_hsv, LOWER_YELLOW, UPPER_YELLOW)

    # Optional: Blur the mask to reduce noise (you can adjust kernel size)
    mask = cv2.blur(mask, (5, 5))

    # Apply the mask to the original image
    single_color = cv2.bitwise_and(src, src, mask=mask)

    # Convert the masked image to grayscale
    gray = cv2.cvtColor(single_color, cv2.COLOR_BGR2GRAY)

    # (Optional) Apply a slight blur or threshold before HoughCircles if needed
    # gray = cv2.GaussianBlur(gray, (5, 5), 0)

    cv2.imshow("Gray", gray)

    # Use HoughCircles to detect circles in the grayscale image
    rows = gray.shape[0]
    # Adjust minRadius/maxRadius based on your expected circle sizes
    circles = cv2.HoughCircles(
        gray, 
        cv2.HOUGH_GRADIENT, 
        dp=1, 
        minDist=rows / 8, 
        param1=100, 
        param2=30, 
        minRadius=10,    # Example minimum radius
        maxRadius=300    # Example maximum radius
    )

    # Print or process the detected circles
    print(circles)
    iter = 0
    # Optionally, draw the circles on the original image for visualization
    if circles is not None:
        circles = np.uint16(np.around(circles))
        for circle in circles[0, :]:
            x, y, r = circle
            iter = iter + 1
            # Use a fraction of the detected radius to crop only the inner region.
            # Adjust the factor (e.g., 0.6) based on your image.
            new_r = int(r * 0.6)
            
            # Define new cropping boundaries based on the reduced radius
            x1 = max(0, x - new_r)
            y1 = max(0, y - new_r)
            x2 = min(src.shape[1], x + new_r)
            y2 = min(src.shape[0], y + new_r)
            
            # Crop the image to the new ROI
            cropped = src[y1:y2, x1:x2]
            
            # Preprocess the cropped image for OCR
            gray_cropped = cv2.cvtColor(cropped, cv2.COLOR_BGR2GRAY)
            _, thresh = cv2.threshold(gray_cropped, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
            
            #kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
            kernel = np.ones((3,3), np.uint8)

            thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=1)
            cv2.imshow(f"Window {iter}", thresh)

            # Configure pytesseract to read only digits
            config = r'-c tessedit_char_whitelist=0123456789 --psm 7'
            text = pytesseract.image_to_string(thresh, config=config)
            
            print(f"Detected text: {text.strip()}")
            
            # For visualization, draw the original circle and the new crop area on the image
            cv2.circle(src, (x, y), r, (0, 255, 0), 2)
            cv2.rectangle(src, (x1, y1), (x2, y2), (255, 0, 0), 2)

            cv2.putText(src, text.strip(), (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow("Detected Circles and Numbers", src)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    return text

      
      
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

