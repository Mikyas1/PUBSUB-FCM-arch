import logging
import time
from entity_types.PureController import PureController
from event_bus.decorators import atomic
from state_machines.FCM import State


class Stopper(PureController):
    initial_state = State(name='Initial', initial=True)
    detecting_state = State(name='Detecting')
    passing_state = State(name='Passing')

    rule = [
        (initial_state, detecting_state),
        (initial_state, passing_state),
        (passing_state, detecting_state),
        (detecting_state, passing_state),
    ]

    states = [initial_state, detecting_state, passing_state]

    def __init__(self, controller_pin=None):
        self.controller_pin = controller_pin
        super(Stopper, self).__init__(name='stopper', states=Stopper.states, rule=Stopper.rule)

    def _open(self):
        print("opening*************")
        time.sleep(2)
        print("opened**************")
        print()

    def _close(self):
        print("closing*************")
        time.sleep(2)
        print("closed**************")
        print()

    @atomic()
    def sensor_40_handler(self, event):
        # if event.get('event') == '1':
        self.transition(Stopper.detecting_state, self._close)
        # elif event.get('event') == '2':
        #     self.transition(Stopper.passing_state, self._open)
        # else:
        #     self.transition(Stopper.initial_state, self._close)

    # other eventbus handlers can be register here
    @atomic()
    def camara_handler(self, event):
        self.transition(Stopper.passing_state, self._open)
