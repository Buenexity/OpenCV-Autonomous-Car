#import car
#import videoProcessing
import imageProcessing as imp

# carOffset = imp.FindOffset()

# if (carOffset < -50):
#     #car.MoveLeft()
#     print("turn left")
# elif (carOffset > 50):
#     #car.MovRight()
#     print("turn right")
# else:
#     #car.MoveForward()
#     print("go straight")

speedLimit = imp.SpeedLimitDetection()

print(f"Speed Limit: {speedLimit}")