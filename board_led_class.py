from machine import Pin


class BoardLED:
    
    def __init__(self):       
        self.led = Pin("LED", Pin.OUT)
        
            
    def set_led_pin_state(self, pin_state:bool=True):
        self.led.value(int(pin_state))
