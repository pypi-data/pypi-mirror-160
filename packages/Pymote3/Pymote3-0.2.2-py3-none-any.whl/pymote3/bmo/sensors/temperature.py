import random
from pymote3.sensor import Sensor


class TemperatureSensor(Sensor):
    '''
    This class implements a TemperatureSensor.
    '''
    def __init__(self, min_temp=-10.0, max_temp=80.0):
        '''
        Initialization of a TemperatureSensor

        Keyword arguments:
            min_temp -- lowest temperature possible (default -10.0)
            max_temp -- Highest temperature possible (default 80.0)
        '''
        
        self.min_temp = min_temp
        self.max_temp = max_temp

    def read(self, node):
        '''
        This method returns a randomly chosen temperature
        value between min_temp and max_temp
        '''

        temperature = random.randrange(
            self.min_temp,
            self.max_temp
        )

        return {
            'Temperature': temperature
        }
