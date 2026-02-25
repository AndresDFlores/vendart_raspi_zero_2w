from drive_solenoid_class import *


#  multiple inheritance
class SolenoidManager(DriveSolenoid):        
    
    @classmethod
    def set_engage_flag(cls, flag:bool=False):
        #  boolean input, where True is engaged and False is disengaged
        cls.engage_flag=flag
    
        
    def __init__(self, pin:bool):
        DriveSolenoid.__init__(self, pin)  # inherit methods and attributes from solenoid parent classe
        
        self.set_engage_flag()  # initialize class variable
        
        
    def drive_solenoid(self):
        self.set_sol_pin_state(self.engage_flag)  #  set solenoid state
        