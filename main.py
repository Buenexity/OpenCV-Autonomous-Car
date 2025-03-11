from car import Motor
import cv2
import imageProcessing as imp
from pid import PIDcontroller;
import time
from findAngle import getAverageAngle

cap = cv2.VideoCapture(0)


# Initialize car class with a percentage of total speed
INIT_SPEED = 50
kp = .1
kd = 0
ki = .05
car = Motor(INIT_SPEED)

pid = PIDcontroller(kp, kd,ki, 0)
while True:
    if cap.isOpened(): 
        ret, frame = cap.read()
    if not cap.isOpened():
        print("Cannot open camera")
        image_col = cv2.imread('./images/track.jpg')
            
    radius = imp.Find_Stoplight(frame, 'red')
    if (radius >0):
        print("red light")
        car.stop_motors()
        time.sleep(1)
        continue
    # if frame is read correctly ret is True
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
    contours = cv2.findContours(image_col, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # change carOffset to be proportional to angle!
    lineAngle = getAverageAngle(contours, image_col)
    carOffset = imp.FindOffset(frame, ret)
    car.set_pid_speed(int(pid.ComputeError(carOffset)))
    
    #if (carOffset < -40):
     #   car.TurnLeft()
      #  print("turn left")
    #elif (carOffset > 40):
     #   car.TurnRight()
     #   print("turn right")
    #else:
     #   car.MoveForward()
     #   print("go straight")
    
    if cv2.waitKey(1) == ord('q'):
        break

# speedLimit = imp.SpeedLimitDetection('./images/yellownumber.PNG')

cv2.destroyAllWindows()
