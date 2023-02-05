import time

from entity_types.SensorController import SensorController
from state_machines.FCM import State
from event_bus.decorators import atomic


class Camera(SensorController):
    initial_state = State(name='Initial', initial=True)
    detecting_state = State(name='Detecting')
    ignoring_state = State(name='Ignoring')

    rule = [
        (initial_state, detecting_state),
        (initial_state, ignoring_state),
        (ignoring_state, detecting_state),
        (detecting_state, ignoring_state),
    ]

    states = [initial_state, detecting_state, ignoring_state]

    def __init__(self):
        super(Camera, self).__init__(name='stopper', states=Camera.states, rule=Camera.rule)

    def _do_detect(self):
        print("detecting")
        time.sleep(5)
        print("done detecting")
        self.event_bus.publish("cap - detected")

    @atomic()
    def sensor_40_handler(self, event):
        # if event.get('event') == '1':
        self.transition(Camera.detecting_state, self._do_detect, Camera.ignoring_state)
