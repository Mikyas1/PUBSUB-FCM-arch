import time

from entity_types.PureController import PureController
from state_machines.FCM import State
from event_bus.decorators import atomic


class Pusher(PureController):
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
        print("pushing*************")
        time.sleep(3)
        print("pulling**************")
        print()

    @atomic()
    def handel_no_cup_or_not_detected(self, event):
        # check event
        state = self.get_state
        if state == Pusher.cylinder_sensed:
            self.transition(Pusher.working_state, self._do_pushing, Pusher.initial_state)
        else:
            self.transition(Pusher.camera_detected)

    @atomic()
    def handle_sensor_41_detection(self, event):
        state = self.get_state
        if state == Pusher.camera_detected:
            self.transition(Pusher.working_state, self._do_pushing, Pusher.initial_state)
        else:
            self.transition(Pusher.cylinder_sensed)
