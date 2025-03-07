import RPi.GPIO as GPIO
import time

class PIDcontroller:
    def __init__(self,kp, ki, kd, target):
        # PID constants
        self.kp = kp
        self.ki = ki
        self.kd = kd

        # PID variables
        self.setpoint = target 
        self.prev_error = 0 
        self.integral = 0
        self.output = 0
        self.last_time = time.time() #last time we measured

    def ComputeError(self, error):
        error = self.setpoint - error

        # Proportional
        proproportional =  self.kp * error # proportional error =  kp * (target - error)

        # check elapsed time 
        now = time.time()   #current time
        self.dt = now - self.last_time #time since last update
        self.last_time = now #update for next reading

        #Derivative
        derivative = (error - self.prev_error) / self.dt if self.dt != 0 else 0
        derivative = self.kd * derivative

        #Integral
        self.integral += error * self.dt
        integral = self.ki * self.integral
                    
        self.output = proproportional + integral + derivative

        # Store error for the next derivative calculation
        self.prev_error = error
                    
        #Integral
        return int(self.output)
        
