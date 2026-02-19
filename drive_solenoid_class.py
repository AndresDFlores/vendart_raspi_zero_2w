from machine import Pin


class DriveSolenoid:
    
    def __init__(self, pin:int):       
        self.sol = Pin(pin, Pin.OUT)
        
            
    def set_sol_pin_state(self, pin_state:bool=True):
        self.sol.value(int(pin_state))
