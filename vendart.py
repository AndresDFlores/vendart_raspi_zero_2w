from time import sleep
from datetime import datetime as dt

from pico_client import *
from solenoid_manager import *
from button_class import *


class VendArt(SolenoidManager):    
    
    
    #  class variables
    _solenoid_pin=0
    _engage_button_pin=5
    _disengage_button_pin=26
    
    _solenoid_engage_timeout=5
    
    
    def __init__(self):
        
        #  initialize solenoid pin
        self.vend_solenoid = SolenoidManager(pin=self._solenoid_pin)
        
        #  initialize POS API connection
        self.pico_client_class = PicoClient()
        
        #  initialize button instances for the engage and disengage parameters
        self.engage_button = ButtonPress(pin=self._engage_button_pin)
        self.disengage_button = ButtonPress(pin=self._disengage_button_pin)
        
                
    def main(self):
        
        while True:

            #  check the state of the button
            #  default boolean: 0=button pressed, 1=button NOT pressed
            engage_button_state = not(self.engage_button.get_button_pin_state())  # not aligns 0 with button NOT pressed
            
            
            #  check data received from point of sale webhook endpoint
            self.pico_client_class.get_data()
            pos_webhook_endpoint = self.pico_client_class.bool_state
            
            
            
            print(f'\n\n{dt.now()}\nbutton: {engage_button_state}\napi: {pos_webhook_endpoint}')


            
            #  define solenoid pin state based on button state/webhook
            if pos_webhook_endpoint==False and engage_button_state==False:
                pin_state = False
            else:
                pin_state = True
                

            print(f'pin state: {pin_state}')



            #  command solenoid state
            self.vend_solenoid.set_engage_flag(pin_state)
            self.vend_solenoid.drive_solenoid()
            
            

            #  if solenoid is engaged, begin disengage protocol
            if pin_state:
                
                seconds_elapsed=0
                while True:
                    
                    #  check the state of the button: 0=disengage, 1=engage
                    disengage_button_state = self.disengage_button.get_button_pin_state()
                    
                    #  solenoid timed disengage summer
                    sleep(.01)
                    seconds_elapsed+=.01
                    
                    
                    #  if disengage button state is 0 or the engage timeout is exceeded, disengage solenoid
                    #  engage timeout is a safety parameter to ensure that the solenoid does not burn out with an extended hold time
                    if disengage_button_state==0 or seconds_elapsed>=self._solenoid_engage_timeout:
                        self.vend_solenoid.set_engage_flag(False)
                        self.vend_solenoid.drive_solenoid()
                        
                        self.pico_client_class.set_bool_state(bool_state=False)
                        break
