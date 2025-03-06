import cv2
import numpy as np
import re
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"




font = cv2.FONT_HERSHEY_COMPLEX 

ROI_WIDTH_CONSTANT = 0.5
ROI_HEIGHT_CONSTANT = 4

def FindOffset():
        image_col = cv2.imread('./images/image.jpg')

        # Image dimensions
        height, width, channels = image_col.shape

        # Convert to grayscale
        image = cv2.cvtColor(image_col, cv2.COLOR_BGR2GRAY)
        image = cv2.GaussianBlur(image, (5, 5), 0)

        # Apply thresholding
        ret, image = cv2.threshold(image, 120, 255, cv2.THRESH_BINARY_INV)
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

        # Apply erosion
        image = cv2.erode(roi,None, iterations=2)

        # Find contours
        contours, hierarchy = cv2.findContours(roi, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # Find the average distance of dashes from center line
        offsetSum = 0

        # Area to remove really small contours that maybe noise 
        min_contour_area = 500

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
            print(offsetSum)
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
        resized_image = cv2.resize(image, (new_width, new_height))
        resized_image_col = cv2.resize(image_col, (new_width, new_height))

        # resize the windows
        cv2.namedWindow('image', cv2.WINDOW_NORMAL)
        cv2.namedWindow('image_col', cv2.WINDOW_NORMAL)

        cv2.resizeWindow('image', 800, 600)
        cv2.resizeWindow('image_col', 800, 600)

        # cv2.imshow('image', image)
        # cv2.imshow('image_col', image_col)

        cv2.imshow('image', resized_image)
        cv2.imshow('image_col', resized_image_col)    

        cv2.waitKey(0)
        cv2.destroyAllWindows()
        return offsetSum

def SpeedLimitDetection():
    # Load the image
    # image_col = cv2.imread('./images/numbers/twenty.jpg')
    image_col = cv2.imread('./images/numbers/twenty.jpg')
    if image_col is None:
        print("Image not found.")
        return None

    # Convert to grayscale
    gray = cv2.cvtColor(image_col, cv2.COLOR_BGR2GRAY)
    # Apply Gaussian blur to reduce noise
    gray = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # Apply thresholding to get a binary image
    ret, thresh = cv2.threshold(gray, 120, 255, cv2.THRESH_BINARY_INV)
    
    # Define a region of interest (ROI) where the speed limit number is expected.
    # Here, we choose the central portion of the image (adjust these values as needed).
    height, width = gray.shape[:2]
    roi_x = int(width * 0.25)
    roi_y = int(height * 0.25)
    roi_w = int(width * 0.5)
    roi_h = int(height * 0.5)
    roi = thresh[roi_y:roi_y+roi_h, roi_x:roi_x+roi_w]

    # Optionally, resize the ROI to enhance OCR accuracy
    roi_resized = cv2.resize(roi, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    
    # Optionally, apply a morphological opening to remove noise
    kernel = np.ones((3, 3), np.uint8)
    roi_clean = cv2.morphologyEx(roi_resized, cv2.MORPH_OPEN, kernel)
    
    # Set up pytesseract to detect only digits.
    # "--psm 8" treats the image as a single word.
    config = "--psm 8 -c tessedit_char_whitelist=0123456789"
    detected_text = pytesseract.image_to_string(roi_clean, config=config)
    
    # Clean the result (remove any whitespace/newlines)
    detected_text = detected_text.strip()
    print("Detected speed limit:", detected_text)
    
    # Optionally, display the ROI window for debugging
    cv2.namedWindow('Speed Limit ROI', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('Speed Limit ROI', 400, 400)
    cv2.imshow('Speed Limit ROI', gray)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    return detected_text


