import configparser
from pathlib import Path
from PowerSupplyer import PowerSupply



class PowerSupplyConfig:
    def __init__(self, config_file_path , auto_off=True):
        self.config_file_path = Path(config_file_path)
        self.config = configparser.ConfigParser()
        self.config.read(self.config_file_path)
        self.ps = PowerSupply()
        self.auto_off = auto_off
        self.voltage_data = []
        self.current_data = []
        self.should_stop = False

    def __enter__(self):
        self.ps.on()
        self.ps.voltage, self.ps.current, self.ps.CURR_PROT_VALUE, self.ps.CURR_PROT = (
            self.config.get('DC_power', setting)
            for setting in ('voltage', 'current', 'CURR_PROT_VALUE', 'CURR_PROT')
        )
        check=[self.ps.voltage, self.ps.current, self.ps.CURR_PROT_VALUE, self.ps.CURR_PROT]
        return self.ps ,check

    def __exit__(self, exc_type, exc_value, traceback):
        if self.auto_off:
            self.ps.off()


# with PowerSupplyConfig('DC_setting.cfg', auto_off=True) as (ps, check):
#     print(f"voltage: {check[0]}, current: {check[1]}, CURR_PROT_VALUE: {check[2]}, CURR_PROT: {check[3]}")
