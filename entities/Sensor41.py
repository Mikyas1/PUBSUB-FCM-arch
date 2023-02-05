import time

from entity_types.PureSensor import PureSensor


class Sensor41(PureSensor):
    def __init__(self, source=None):
        self.source = source
        super(Sensor41, self).__init__(name="sensor_41")

    def sensing_logic(self):
        while True:
            # data = input(f'input sensor data for {self.name}: ')
            # data = self.source.current
            # todo add some sensing logic here
            # self.event_bus.publish(data)
            time.sleep(15)
            self.event_bus.publish("sensor41")
