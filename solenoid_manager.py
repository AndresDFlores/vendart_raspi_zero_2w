from board_led_class import *
from drive_solenoid_class import *


#  multiple inheritance
class SolenoidManager(BoardLED, DriveSolenoid):        
    
    @classmethod
    def set_engage_flag(cls, flag:bool=False):
        #  boolean input, where True is engaged and False is disengaged
        cls.engage_flag=flag
    
        
    def __init__(self, pin:bool):
        BoardLED.__init__(self)  # inherit methods and attributes from LED parent classe
        DriveSolenoid.__init__(self, pin)  # inherit methods and attributes from solenoid parent classe
        
        self.set_engage_flag()  # initialize class variable
        
        
    def drive_solenoid(self):
        self.set_led_pin_state(self.engage_flag)  # set LED state
        self.set_sol_pin_state(self.engage_flag)  #  set solenoid state
        