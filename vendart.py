from time import sleep
from datetime import datetime as dt
import logging

from webhook_udp_listener import *
from solenoid_manager import *
from button_class import *


class VendArt(SolenoidManager):    
    
    #  class variables
    _solenoid_pin=26
    _engage_button_pin=23
    _disengage_button_pin=24
    
    _solenoid_engage_timeout=15
    
    
    def __init__(self, literal:bool=False):


        #  display debug nmessages for dev
        self.literal=literal
        
        #  initialize solenoid pin
        self.vend_solenoid = SolenoidManager(pin=self._solenoid_pin)
        
        #  initialize POS API connection
        self.udp_listener = UDPListener()
        
        #  initialize button instances for the engage and disengage parameters
        self.engage_button = ButtonPress(pin=self._engage_button_pin)
        self.disengage_button = ButtonPress(pin=self._disengage_button_pin)


        #  ---LOGGER---

        # Configure the root logger
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.StreamHandler(),
                logging.FileHandler("vendart_telemetry_log.log")
            ]
        )

        # Get a logger for the current module
        self.logger = logging.getLogger(__name__)

        
                
    def main(self, stop_event):
        
        self.logger.info("Vendart Initiated")
        while not stop_event.is_set():


            #  check the state of the button
            #  default boolean: 0=button pressed, 1=button NOT pressed
            engage_button_state = not(self.engage_button.get_button_pin_state())  # not aligns 0 with button NOT pressed
            
            
            #  check data received from point of sale webhook endpoint
            self.udp_listener.get_data()
            pos_webhook_endpoint = self.udp_listener.bool_state
            
            
            #  debug message output for dev
            if self.literal: print(f'\n\n{dt.now()}\nbutton: {engage_button_state}\napi: {pos_webhook_endpoint}')

            
            #  define solenoid pin state based on button state/webhook
            if pos_webhook_endpoint==False and engage_button_state==False:
                pin_state = False

            #  engage solenoid if Digital Payment Method (DPP) webhook POST received
            elif pos_webhook_endpoint==True:
                pin_state = True
                self.logger.info("Digital Payment Method (DPP): Transaction Event Initiated")

            #  engage solenoid if override button pressed
            elif engage_button_state==True:
                self.logger.info("Override Button: Transaction Event Initiated")
                pin_state = True
                

            #  debug message output for dev
            if self.literal: print(f'pin state: {pin_state}')


            #  command solenoid state
            self.vend_solenoid.set_engage_flag(pin_state)
            self.vend_solenoid.drive_solenoid()
                        

            #  if solenoid is engaged, begin disengage protocol
            if pin_state:
                
                #  log solenoid engage
                self.logger.info("Solenoid Engaged - Transaction Event Initiated")

                seconds_elapsed=0
                while not stop_event.is_set():
                    

                    #  check the state of the button: 0=disengage, 1=engage
                    disengage_button_state = self.disengage_button.get_button_pin_state()
                    
                    #  solenoid timed disengage summer
                    time_incrememnt = .01
                    sleep(time_incrememnt)
                    seconds_elapsed+=time_incrememnt
                                        

                    #  disengage criteria
                    if disengage_button_state==0:
                        #  disengage solenoid if disengage button state is 0


                        # reset variables
                        self.vend_solenoid.set_engage_flag(False)
                        self.vend_solenoid.drive_solenoid()
                        self.udp_listener.set_bool_state(bool_state=False)
                        
                        #  log completed transaction solenoid disengage
                        self.logger.info("Solenoid Disengaged - Transaction Event Completion")
                        
                        break


                    elif seconds_elapsed>=self._solenoid_engage_timeout:
                        #  disengage solenoid if the engage timeout is exceeded
                        #  engage timeout is a safety parameter to ensure that the solenoid does not burn out with an extended hold time


                        #  reset variables
                        self.vend_solenoid.set_engage_flag(False)
                        self.vend_solenoid.drive_solenoid()
                        self.udp_listener.set_bool_state(bool_state=False)
                        
                        #  log timeout solenoid disengage
                        self.logger.info("Solenoid Disengaged - Timeout Without Transaction Event Completion")
                        
                        break


            sleep(0.05)

        self.logger.info("Vendart Terminated")
