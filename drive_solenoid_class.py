import RPi.GPIO as GPIO


class DriveSolenoid:
    
    def __init__(self, pin:int):       
        self.pin = pin

        GPIO.setmode(GPIO.BCM) 
        GPIO.setup(pin, GPIO.OUT) 
        
            
    def set_sol_pin_state(self, pin_state:bool=True):
        GPIO.output(self.pin, pin_state)


if __name__=="__main__":

    import time

    sol_class = DriveSolenoid(26)

    state = True
    for i in range(10):

        sol_class.set_sol_pin_state(pin_state=state)
        time.sleep(1)

        state=not(state)