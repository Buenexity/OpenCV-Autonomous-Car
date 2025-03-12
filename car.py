import RPi.GPIO as GPIO
import time

class Motor:
    def __init__(self, pwm_speed):
        self.pwm_speed = pwm_speed
        
        # Motor Pins
        self.Motor_IN4 = 24
        self.Motor_IN3 = 23
        self.Motor_IN2 = 18
        self.Motor_IN1 = 17
        self.Pwm_ENA = 12
        self.Pwm_ENB = 13
        self.MotorSpeedA = pwm_speed
        self.MotorSpeedB = pwm_speed
        
        GPIO.setmode(GPIO.BCM)  # Set GPIO pin mode

        # Setup PWM pins
        GPIO.setup(self.Pwm_ENA, GPIO.OUT)
        GPIO.setup(self.Pwm_ENB, GPIO.OUT)

        # Setup motor control pins
        GPIO.setup(self.Motor_IN1, GPIO.OUT)
        GPIO.setup(self.Motor_IN2, GPIO.OUT)
        GPIO.setup(self.Motor_IN3, GPIO.OUT)
        GPIO.setup(self.Motor_IN4, GPIO.OUT)

        # PWM initialization @ 1000Hz frequency
        self.pwm_motor_1 = GPIO.PWM(self.Pwm_ENA, 1000)
        self.pwm_motor_2 = GPIO.PWM(self.Pwm_ENB, 1000)
        self.pwm_motor_1.start(0)
        self.pwm_motor_2.start(0)
    
    def move_forward(self):
        self.pwm_motor_1.ChangeDutyCycle(self.pwm_speed)
        self.pwm_motor_2.ChangeDutyCycle(self.pwm_speed)
        GPIO.output(self.Motor_IN1, GPIO.HIGH)
        GPIO.output(self.Motor_IN2, GPIO.LOW)
        GPIO.output(self.Motor_IN3, GPIO.LOW)
        GPIO.output(self.Motor_IN4, GPIO.HIGH)
        print("Moving forward")

    def move_backward(self):
        self.pwm_motor_1.ChangeDutyCycle(self.pwm_speed)
        self.pwm_motor_2.ChangeDutyCycle(self.pwm_speed)
        GPIO.output(self.Motor_IN1, GPIO.LOW)
        GPIO.output(self.Motor_IN2, GPIO.HIGH)
        GPIO.output(self.Motor_IN3, GPIO.LOW)
        GPIO.output(self.Motor_IN4, GPIO.HIGH)
        print("Moving backward")
    
    def turn_left(self):
        self.pwm_motor_1.ChangeDutyCycle(self.pwm_speed / 2)
        self.pwm_motor_2.ChangeDutyCycle(self.pwm_speed)
        GPIO.output(self.Motor_IN1, GPIO.LOW)
        GPIO.output(self.Motor_IN2, GPIO.LOW)
        GPIO.output(self.Motor_IN3, GPIO.LOW)
        GPIO.output(self.Motor_IN4, GPIO.HIGH)
        print("Turning left")
    
    def turn_right(self):
        self.pwm_motor_1.ChangeDutyCycle(self.pwm_speed)
        self.pwm_motor_2.ChangeDutyCycle(self.pwm_speed / 2)
        GPIO.output(self.Motor_IN1, GPIO.HIGH)
        GPIO.output(self.Motor_IN2, GPIO.LOW)
        GPIO.output(self.Motor_IN3, GPIO.LOW)
        GPIO.output(self.Motor_IN4, GPIO.LOW)
        print("Turning right")
    
    def stop_motors(self):
        self.pwm_motor_1.ChangeDutyCycle(0)
        self.pwm_motor_2.ChangeDutyCycle(0)
        GPIO.output(self.Motor_IN1, GPIO.LOW)
        GPIO.output(self.Motor_IN2, GPIO.LOW)
        GPIO.output(self.Motor_IN3, GPIO.LOW)
        GPIO.output(self.Motor_IN4, GPIO.LOW)
        print("Stopping motors")
    
    # Changes left and right motor speeds according to calculated pid values
    # left motor - offset is subtracted from current base speed
    # right motor - offset is added from current base speed

    def set_pid_speed(self, pid_offset, angle):
        # Ensure motor speed stays between 0 and 100
        MotorSpeedA = max(0, min(self.pwm_speed - pid_offset, 60))
        MotorSpeedB = max(0, min(self.pwm_speed + pid_offset, 60))

        MotorSpeedA /= (angle / 90)
        MotorSpeedB /= (angle / 90)
        
        self.pwm_motor_1.ChangeDutyCycle(MotorSpeedA)
        self.pwm_motor_2.ChangeDutyCycle(MotorSpeedB)
        
        GPIO.output(self.Motor_IN1, GPIO.HIGH)
        GPIO.output(self.Motor_IN2, GPIO.LOW)
        GPIO.output(self.Motor_IN3, GPIO.LOW)
        GPIO.output(self.Motor_IN4, GPIO.HIGH)
        
        print(f"Left motor speed: {MotorSpeedA}")
        print(f"Right motor speed: {MotorSpeedB}")

    def getMotorspeed(self):
        return self.MotorSpeedA, self.MotorSpeedB
    
    # value must be between 0 - 100
    def changeBaseSpeed(self, newSpeed):
        self.pwm_speed = newSpeed
