import configparser
from pathlib import Path
from PowerSupplyer import PowerSupply
import datetime
import time
from pandas import DataFrame , concat

class Load_Config:

    def __init__(self):
        self.config_file_path = Path.cwd() / 'DC_setting.cfg'
        self.config = configparser.ConfigParser()
        self.config.read(self.config_file_path)

    def __enter__(self):

        self.ps=PowerSupply()
        self.ps.voltage, self.ps.current, self.ps.CURR_PROT_VALUE, self.ps.CURR_PROT = (
            self.config.get('DC_power', setting)
            for setting in ('voltage', 'current', 'CURR_PROT_VALUE', 'CURR_PROT') 
        )
        check=[self.ps.voltage, self.ps.current, self.ps.CURR_PROT_VALUE, self.ps.CURR_PROT]

        return check
    
    def __exit__(self):
        self.ps=PowerSupply()



class PowerSupplyMonitor:

    def __init__(self):
        self.ps=PowerSupply()
        self.voltage_data = []
        self.current_data = []
        self.current_time = datetime.datetime.now().strftime("%H_%M_%S")
        self.filename = f"Power_{self.current_time}.csv"

    def start(self):
        self.ps.on()

    def Measure(self):

        Test_interval =int(input( " 設定紀錄頻率：(次/秒) " ))
        self.DataFrame = DataFrame(columns=['Time (s)', 'Voltage (V)', 'Current (A)'])
        while True:
            self.measure_time = datetime.datetime.now().time()
            self.voltage = self.ps.read_voltage()
            self.current = self.ps.read_current()      
            self.data = {'Time (s)': self.measure_time, 'Voltage (V)': self.voltage, 'Current (A)': self.current}
            print(f"Time (s): {self.measure_time} Voltage (V): {self.voltage:.4f}, Current (A): {self.current:.4f}")
            self.DataFrame = concat([self.DataFrame, DataFrame([self.data])], ignore_index=True)
            time.sleep(1/Test_interval)


    def save_data(self):

        with open(self.filename, mode='a', newline='') as file:
            self.DataFrame.to_csv(self.filename, index=True)


if __name__ == '__main__':

    PS=PowerSupply()
    print(PS.GPIB[0])

    LC=Load_Config()
    print(LC.__enter__())


    PSM=PowerSupplyMonitor()
    PSM.start()

    try:
        PSM.Measure()
    except KeyboardInterrupt:
        PSM.save_data()
        PS.off()