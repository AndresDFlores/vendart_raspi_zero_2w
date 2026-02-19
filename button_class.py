from machine import Pin


class ButtonPress:
    
    def __init__(self, pin:int):       
        self.button = Pin(pin, Pin.IN, Pin.PULL_UP)


    def get_button_pin_state(self):
        return self.button.value()
    
    
    
if __name__=="__main__":
    import time
    button_class = ButtonPress(pin=5)
    
    while True:
        print(button_class.get_button_pin_state())
        time.sleep(0.1)
