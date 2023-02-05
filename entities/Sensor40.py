import time

from lib.entity_types.PureSensor import PureSensor


class Sensor40(PureSensor):
    def __init__(self, source=None):
        super(Sensor40, self).__init__(name="sensor_40")
        self.source = source
        self.previous_detected = False

    def sensing_logic(self):
        while True:
            # data = input(f'input sensor data for {self.name}: ')
            # todo add some sensing logic here
            current_40 = self.source.current
            # (1.2 + 2.6) / 2 = 1.9
            if current_40 > 1.9 and not self.previous_detected:
                self.previous_detected = True
                self.event_bus.publish('cylinder-detected-at-sensor-40')
            else:
                self.previous_detected = False
            time.sleep(0.3)
