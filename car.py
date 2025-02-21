import RPi.GPIO as GPIO
import time

# Motor Pins
# Left motor (Motor IN1 - Pin 17, Motor IN2 - Pin 18)
Motor_IN1 = 17
Motor_IN2 = 18

# Right motor (Motor IN3 - Pin 23, Motor IN4 - Pin 24)
Motor_IN3 = 23
Motor_IN4 = 24

Pwm_ENA = 18
Pwm_ENB = 19

GPIO.setmode(GPIO.BCM)  # Set GPIO pin mode

#pwm pins
GPIO.setup(Pwm_ENA, GPIO.OUT)
GPIO.setup(Pwm_ENB, GPIO.OUT)

#setup pins
GPIO.setup(Motor_IN1, GPIO.OUT)
GPIO.setup(Motor_IN2, GPIO.OUT)
GPIO.setup(Motor_IN3, GPIO.OUT)
GPIO.setup(Motor_IN4, GPIO.OUT)


#PWM pins @ 100hz frequency
pwm_motor_1 = GPIO.PWM(Pwm_ENA, 100) 
pwm_motor_2 = GPIO.PWM(Pwm_ENB, 100)

#start the motors @ 0% duty cycle
pwm_motor_1.start(0)
pwm_motor_2.start(0)

#Motor Functions

def MoveForward():
    GPIO.output(Motor_IN1, GPIO.HIGH)  # Left motor forward
    GPIO.output(Motor_IN2, GPIO.LOW)   
    GPIO.output(Motor_IN3, GPIO.HIGH)  # Right motor forward
    GPIO.output(Motor_IN4, GPIO.LOW)   
    print("forward")


def MoveBackward():
    GPIO.output(Motor_IN1, GPIO.LOW)   # Left motor backward
    GPIO.output(Motor_IN2, GPIO.HIGH)  
    GPIO.output(Motor_IN3, GPIO.LOW)   # Right motor backward
    GPIO.output(Motor_IN4, GPIO.HIGH)  
    print("back")

def TurnLeft():
    GPIO.output(Motor_IN1, GPIO.LOW)   
    GPIO.output(Motor_IN2, GPIO.HIGH)  # Left motor reverse
    GPIO.output(Motor_IN3, GPIO.HIGH)  
    GPIO.output(Motor_IN4, GPIO.LOW)   # Right motor stop
    print("Left")

def TurnRight():
    GPIO.output(Motor_IN1, GPIO.HIGH)  # Left motor forward
    GPIO.output(Motor_IN2, GPIO.LOW)   
    GPIO.output(Motor_IN3, GPIO.LOW)   # Right motor stop
    GPIO.output(Motor_IN4, GPIO.HIGH)  
    print("Right")

def StopMotors():
    GPIO.output(Motor_IN1, GPIO.LOW)   
    GPIO.output(Motor_IN2, GPIO.LOW)   
    GPIO.output(Motor_IN3, GPIO.LOW)   
    GPIO.output(Motor_IN4, GPIO.LOW)   
    print("STOP")

# Test drive loop
"""
try:
    MoveForward()
    time.sleep(10)
    
    pwm_motor_1.ChangeDutyCycle(100)
    pwm_motor_2.ChangeDutyCycle(100)

    
    TurnLeft()
    time.sleep(2)
    
    pwm_motor_1.ChangeDutyCycle(70)
    pwm_motor_2.ChangeDutyCycle(70)


    
    MoveBackward()
    time.sleep(10)
    
    TurnRight()
    time.sleep(2)

    StopMotors()

#end test program via keyboard
except KeyboardInterrupt:
    print("Program Interrupted")
    
#we stop the pwm 
finally:
    pwm_motor_1.stop()
    pwm_motor_2.stop()
    GPIO.cleanup()  
"""