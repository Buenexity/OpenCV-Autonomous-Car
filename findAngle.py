import cv2
import numpy as np
import argparse
import imutils
import math

def getAverageAngle(contours):
	maxc_center = 0, 0
	count,asum = 0, 0
	# height, width = image.shape[:2]
	# loop over the contours
	for c in contours:
		if ((cv2.contourArea(c) > 10000) & (cv2.contourArea(c) < 1500000)):
			count+= 1
			# compute the center of the contour
			M = cv2.moments(c)
			cY = int(M["m01"] / M["m00"])
			cX = int(M["m10"] / M["m00"])
            
			epsilon = 0.02 * cv2.arcLength(c, True)
			approx = cv2.approxPolyDP(c, epsilon, True)
    

			if len(approx) == 4:  # Check if it is a rectangle
				# Sort the points based on x + y (top-left, bottom-right first)
				sorted_pts = sorted(approx[:, 0], key=lambda p: (p[0] + p[1]))

				# Get the four corner points
				top_left, bottom_right = sorted_pts[0], sorted_pts[3]
				top_right, bottom_left = sorted_pts[1], sorted_pts[2]

				# Compute midpoints of opposite sides based on which sides are shorter
				if (np.linalg.norm(top_left- top_right) < np.linalg.norm(top_left - bottom_left)):
					mid_top = ((top_left[0] + top_right[0]) // 2, (top_left[1] + top_right[1]) // 2)
					mid_bottom = ((bottom_left[0] + bottom_right[0]) // 2, (bottom_left[1] + bottom_right[1]) // 2)
				else:
					mid_top = ((top_left[0] + bottom_left[0]) // 2, (top_left[1] + bottom_left[1]) // 2)
					mid_bottom = ((top_right[0] + bottom_right[0]) // 2, (top_right[1] + bottom_right[1]) // 2)
					
				# # Draw the centerline
				# cv2.line(image, mid_top, mid_bottom, (0, 255, 0), 2)

				# # Draw rectangle for visualization
				# cv2.drawContours(image, [approx], -1, (255, 0, 0), 2)

				dx = mid_bottom[0] - mid_top[0]
				dy = mid_bottom[1] - mid_top[1]
				
				# calculate angle
				rect_angle = math.degrees(math.atan2(dy, dx))
				angle_diff = abs(rect_angle - 90)
				# cv2.line(image, (width // 2, 0), (width // 2, height), (255, 0, 0), 2)

				asum += angle_diff;

				# Display the angle on the image
				# cv2.putText(image, f"Angle: {angle_diff:.2f} deg", (mid_top[0] + 20, mid_top[1]),
				# 			cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 2)
				# # draw the contour and center of the shape on the image
				# cv2.putText(image, "center", (maxc_center[0] - 20, maxc_center[1] - 20),
				# 	cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
				# cv2.imshow('Angles', image)
			
	return asum / count