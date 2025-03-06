#from car import TurnLeft, MoveForward, TurnRight
import cv2
import imageProcessing as imp
#cap = cv2.VideoCapture(0)

# while True:
#     if cap.isOpened(): 
#         ret, frame = cap.read()
#     if not cap.isOpened():
#         print("Cannot open camera")
#         image_col = cv2.imread('./images/track.jpg')
            
         
#     # if frame is read correctly ret is True
#     if not ret:
#         print("Can't receive frame (stream end?). Exiting ...")
#     carOffset = imp.FindOffset(frame, ret)
#     if (carOffset < -40):
#         TurnLeft()
#         print("turn left")
#     elif (carOffset > 40):
#         TurnRight()
#         print("turn right")
#     else:
#         MoveForward()
#         print("go straight")
    
#     if cv2.waitKey(1) == ord('q'):
#         break

speedLimit = imp.SpeedLimitDetection('./images/yellownumber.PNG')

#print(f"Speed Limit: {speedLimit}")

cv2.destroyAllWindows()

