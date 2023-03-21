import pyvisa
import time
import configparser
from pathlib import Path

class PowerSupply:

    def __init__(self):
        
        # Find instrument
        config_file_path = Path.cwd() / 'DC_setting.cfg'
        config = configparser.ConfigParser()
        config.read(config_file_path)
        Port = config.get('DC_power' ,'Port')

        # Initialize PyVISA resource manager
        self.rm = pyvisa.ResourceManager()
        # Open the power supply
        self.inst = self.rm.open_resource('%s'%Port)
        # Set termination characters
        self.inst.read_termination = '\n'
        self.inst.write_termination = '\n'
        self.data = []

    def __del__(self):
        # Close the instrument when the object is deleted
        self.inst.close()

    #--- public methods ---

    @property        
    def voltage(self):
        """
        Returns the voltage setting
        """
        return float(self.inst.query('VOLTage:LEVel?'))

    @voltage.setter
    def voltage(self, volts):
        """
        Sets the voltage of the instrument
        """
        self.inst.write(f'VOLTage:LEVel {volts}')

    @property
    def current(self):
        """
        Returns the current setting in Amps
        """
        return float(self.inst.query('CURRent:LEVel?'))

    @current.setter
    def current(self, amps):
        """
        Set the current of the instrument
        """
        self.inst.write(f'CURRent:LEVel {amps}')
    
    @property
    def CURR_PROT(self):
        """
        Returns the protect current setting in Amps
        """
        return bool(int(self.inst.query('CURRent:PROTection:STATe?')))

    @CURR_PROT.setter
    def CURR_PROT(self, state):
        """
        Set the protection current of the instrument
        """
        if state:
            self.inst.write('CURRent:PROTection:STATe ON')
        else:
            self.inst.write('CURRent:PROTection:STATe OFF')
    
    @property
    def CURR_PROT_VALUE(self):
        """
        Returns the protect current setting in Amps
        """
        return float(self.inst.query('CURRent:PROTection:STATe?'))


    @CURR_PROT_VALUE.setter
    def CURR_PROT_VALUE(self, amps):
        """
        Set the protection current of in Amps
        """
        self.inst.write(f'CURRent:PROTection {amps}')


    def on(self):
        """
        Turns the output on
        """
        self.inst.write('OUTPut:STATe ON')

    def off(self):
        """
        Turns the output off
        """
        self.inst.write('OUTPut:STATe OFF')
        self.inst.write('CURRent:PROTection:STATe OFF')

    def read_current(self):
        """
        Returns the measured current in Amps
        """
        return float(self.inst.query('MEASure:CURRent?'))
    
    def read_voltage(self):

        """
        Returns the measured current in Amps
        """
        return float(self.inst.query('MEASure:VOLTage:DC?'))
    


