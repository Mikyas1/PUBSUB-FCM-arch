from typing import List, Tuple
from state_machines.FSM import FSM, State
from event_bus.EventBus import EventBus
from . import PureController


class SensorController(PureController.PureController):
    def __init__(self, name: str, states: List[State], rule: List[Tuple[State, State]]):
        self.name = name
        super(SensorController, self).__init__(name=name, states=states, rule=rule)
        self.event_bus = EventBus()

    def sensing_logic(self):
        # implement logic in child class
        pass

    def get_sensor_event_bus(self):
        return self.event_bus
