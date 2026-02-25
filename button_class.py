import RPi.GPIO as GPIO


class ButtonPress:
    
    def __init__(self, pin:int):
        self.pin = pin

        GPIO.setmode(GPIO.BCM) 
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP) 


    def get_button_pin_state(self):
        return GPIO.input(self.pin)
    
    
    
if __name__=="__main__":
    import time
    button_class = ButtonPress(pin=23)
    
    while True:
        print(button_class.get_button_pin_state())
        time.sleep(0.1)
