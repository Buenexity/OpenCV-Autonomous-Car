#import RPi.GPIO as GPIO
# import time

# #Pwm 

# Pwm_Speed = 30

# # Motor Pins
# # Left motor (Motor IN1 - Pin 17, Motor IN2 - Pin 18)
# Motor_IN4 = 24
# Motor_IN3 = 23

# # Right motor (Motor IN3 - Pin 23, Motor IN4 - Pin 24)
# Motor_IN2 = 18
# Motor_IN1 = 17

# Pwm_ENA = 12
# Pwm_ENB = 13

# GPIO.setmode(GPIO.BCM)  # Set GPIO pin mode

# #pwm pins
# GPIO.setup(Pwm_ENA, GPIO.OUT)
# GPIO.setup(Pwm_ENB, GPIO.OUT)

# #setup pins
# GPIO.setup(Motor_IN1, GPIO.OUT)
# GPIO.setup(Motor_IN2, GPIO.OUT)
# GPIO.setup(Motor_IN3, GPIO.OUT)
# GPIO.setup(Motor_IN4, GPIO.OUT)


# #PWM pins @ 100hz frequency
# pwm_motor_1 = GPIO.PWM(Pwm_ENA, 1000) 
# pwm_motor_2 = GPIO.PWM(Pwm_ENB, 1000)
# print("initiLIIG PQM")
# #start the motors @ 0% duty cycle

# pwm_motor_1.start(Pwm_Speed)
# pwm_motor_2.start(Pwm_Speed)

# #Motor Functions

# def MoveForward():
#     pwm_motor_1.ChangeDutyCycle(Pwm_Speed)       
#     pwm_motor_2.ChangeDutyCycle(Pwm_Speed)
#     GPIO.output(Motor_IN1, GPIO.HIGH)  # Left motor forward
#     GPIO.output(Motor_IN2, GPIO.LOW)   
#     GPIO.output(Motor_IN3, GPIO.LOW)  # Right motor forward
#     GPIO.output(Motor_IN4, GPIO.HIGH)   
#     print("forward")


# def MoveBackward():
#     pwm_motor_1.ChangeDutyCycle(Pwm_Speed)       
#     pwm_motor_2.ChangeDutyCycle(Pwm_Speed)
#     GPIO.output(Motor_IN1, GPIO.LOW)   # Left motor backward
#     GPIO.output(Motor_IN2, GPIO.HIGH)  
#     GPIO.output(Motor_IN3, GPIO.LOW)   # Right motor backward
#     GPIO.output(Motor_IN4, GPIO.HIGH)  
#     print("back")

# def TurnLeft():
#     pwm_motor_1.ChangeDutyCycle(Pwm_Speed/2)       
#     pwm_motor_2.ChangeDutyCycle(Pwm_Speed)
#     GPIO.output(Motor_IN1, GPIO.LOW)   
#     GPIO.output(Motor_IN2, GPIO.LOW)  # Left motor reverse
#     GPIO.output(Motor_IN3, GPIO.LOW)  
#     GPIO.output(Motor_IN4, GPIO.HIGH)   # Right motor stop
#     print("Right")

# def TurnRight():
#     pwm_motor_1.ChangeDutyCycle(Pwm_Speed)       
#     pwm_motor_2.ChangeDutyCycle(Pwm_Speed/2)
#     GPIO.output(Motor_IN1, GPIO.HIGH)   
#     GPIO.output(Motor_IN2, GPIO.LOW)  # Left motor reverse
#     GPIO.output(Motor_IN3, GPIO.LOW)  
#     GPIO.output(Motor_IN4, GPIO.LOW)   # Right motor stop
#     print("Left")

# def StopMotors():
#     pwm_motor_1.ChangeDutyCycle(0)       
#     pwm_motor_2.ChangeDutyCycle(0)
#     GPIO.output(Motor_IN1, GPIO.LOW)   
#     GPIO.output(Motor_IN2, GPIO.LOW)   
#     GPIO.output(Motor_IN3, GPIO.LOW)   
#     GPIO.output(Motor_IN4, GPIO.LOW)   
#     print("STOP")