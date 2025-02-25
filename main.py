#import car
#import videoProcessing
import imageProcessing as imp
'''
carOffset = imp.FindOffset()

if (carOffset < -50):
    #car.MoveLeft()
    print("turn left")
elif (carOffset > 50):
    #car.MovRight()
    print("turn right")
else:
    #car.MoveForward()
    print("go straight")
'''

light_test = imp.cv2.imread('./images/stoplights.jpg')
imp.Find_Stoplight(light_test)