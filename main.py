from car import Motor
import cv2
import imageProcessing as imp
from pid import PIDcontroller;
import time
from findAngle import getAverageAngle

cap = cv2.VideoCapture(0)


# Initialize car class with a percentage of total speed
INIT_SPEED = 30
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
    

    image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    image = cv2.GaussianBlur(image, (5, 5), 0)
    speedLimit = imp.detectSpeedLimit(frame, car)
    ret, image = cv2.threshold(image, 120, 255, cv2.THRESH_BINARY_INV)
    contours, hierarchy = cv2.findContours(image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # change carOffset to be proportional to angle!
    lineAngle = getAverageAngle(contours)
    carOffset = imp.findOffset(frame, ret)
    car.set_pid_speed(int(pid.ComputeError(carOffset)), lineAngle)
    
    
    
    if (speedLimit == 1):
        car.changeBaseSpeed(30)
    elif(speedLimit == 2):
        car.changeBaseSpeed(40)
    elif (speedLimit == 3):
        car.changeBaseSpeed(50)
    else: 
        pass
        
    
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
