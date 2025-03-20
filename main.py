from car import Motor
import cv2
import imageProcessing as imp
from pid import PIDcontroller;
import time
from findAngle import getAverageAngle

cap = cv2.VideoCapture(0)


# Initialize car class with a percentage of total speed
INIT_SPEED = 40
kp = .1
kd = 0
ki = .05
car = Motor(INIT_SPEED)
flag = False;

pid = PIDcontroller(kp, kd,ki, 0)
while True:
    if cap.isOpened(): 
        ret, frame = cap.read()
    if not cap.isOpened():
        print("Cannot open camera")
        image_col = cv2.imread('./images/track.jpg')
            
    # if frame is read correctly ret is True
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")

    # detect red stoplight
    radius = imp.findStoplight(frame, 'red')
    if (radius >0):
        flag = True;
        print("red light")
        car.stop_motors()
        continue

    # if we're stopped, try detect a green light and go!
    if (flag):
        greenRadius = imp.findStoplight(frame, 'green')
        if (greenRadius > 0):
            flag = False
        continue
    
    carOffset = imp.findOffset(frame, ret)
    car.set_pid_speed(int(pid.ComputeError(carOffset)))
    speed = imp.detectSpeedLimit(frame)
    
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

cv2.destroyAllWindows()