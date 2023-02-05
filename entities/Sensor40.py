from entity_types.PureSensor import PureSensor


class Sensor40(PureSensor):
    def __init__(self, source=None):
        self.source = source
        super(Sensor40, self).__init__(name="sensor_40")

    def sensing_logic(self):
        while True:
            data = input(f'input sensor data for {self.name}: ')
            # todo add some sensing logic here
            # current_40 = self.source.current
            # if current_40 > 0.6:
            #   self.event_bus.publish(data)
            # time.sleep(0.3)
            self.event_bus.publish(data)
