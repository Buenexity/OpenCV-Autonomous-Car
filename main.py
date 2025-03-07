from car import Motor
import cv2
import imageProcessing as imp
from pid import PIDcontroller;

cap = cv2.VideoCapture(0)


# Initialize car class with a percentage of total speed
car = Motor(30)

pid = PIDcontroller(.1, .001,.05, 0)

while True:
    if cap.isOpened(): 
        ret, frame = cap.read()
    if not cap.isOpened():
        print("Cannot open camera")
        image_col = cv2.imread('./images/track.jpg')
            
         
    # if frame is read correctly ret is True
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
    # change carOffset to be proportional to angle!
    carOffset = imp.FindOffset(frame, ret)
    car.set_pid_speed(int(pid.ComputeError(carOffset - 0)))
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

speedLimit = imp.SpeedLimitDetection('./images/yellownumber.PNG')

cv2.destroyAllWindows()
