import cv2

# Open the default camera with the DirectShow backend
cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)

# Check if the camera opened successfully
if not cam.isOpened():
    print("Error: Could not open camera.")
    exit()

# Get the default frame width and height
frame_width = int(cam.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cam.get(cv2.CAP_PROP_FRAME_HEIGHT))

while True:
    ret, frame = cam.read()

    if not ret:
        print("Error: Failed to capture frame.")
        break

    # Display the captured frame in a window
    cv2.imshow('Constant Camera Feed', frame)

    # Press 'q' to exit the loop
    if cv2.waitKey(1) == ord('q'):
        break

# Release the camera and close the window
cam.release()
cv2.destroyAllWindows()
