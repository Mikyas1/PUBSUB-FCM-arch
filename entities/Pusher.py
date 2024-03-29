import time

from lib.entity_types.SensorController import SensorController
from lib.state_machines.FSM import State
from lib.event_bus.decorators import atomic


class Pusher(SensorController):
    initial_state = State(name='Initial', initial=True)
    camera_detected = State(name='CameraDetected')
    cylinder_sensed = State(name='CylinderSensed')
    working_state = State(name='Working')

    rule = [
        (initial_state, camera_detected),
        (initial_state, cylinder_sensed),
        (camera_detected, working_state),
        (cylinder_sensed, working_state),
        (working_state, initial_state),
    ]

    states = [initial_state, camera_detected, cylinder_sensed, working_state]

    def __init__(self, controller_pin=None):
        self.controller_pin = controller_pin
        super(Pusher, self).__init__(name='pusher', states=Pusher.states, rule=Pusher.rule)

    def _do_pushing(self):
        print("Pusher - pushing*************")
        time.sleep(3)
        print("Pusher - pulling**************")
        print()
        self.event_bus.publish("sort-out-done")

    @atomic(device='pusher')
    def handel_no_cup_or_not_detected(self, event):
        # check event
        state = self.get_state
        if state == Pusher.cylinder_sensed:
            self.transition(Pusher.working_state, self._do_pushing, Pusher.initial_state)
        else:
            self.transition(Pusher.camera_detected)

    @atomic(device='pusher')
    def handle_sensor_41_detection(self, event):
        state = self.get_state
        if state == Pusher.camera_detected:
            self.transition(Pusher.working_state, self._do_pushing, Pusher.initial_state)
        else:
            self.transition(Pusher.cylinder_sensed)
