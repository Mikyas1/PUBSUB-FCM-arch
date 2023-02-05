import time
from lib.entity_types.PureController import PureController
from lib.event_bus.decorators import atomic
from lib.state_machines.FSM import State


class Stopper(PureController):
    # initial_state = State(name='Initial', initial=True)
    # detecting_state = State(name='Detecting')
    # passing_state = State(name='Passing')

    closed_state = State(name='Closed', initial=True)
    open_state = State(name='Opened')

    rule = [
        # (initial_state, detecting_state),
        # (initial_state, passing_state),
        # (passing_state, detecting_state),
        # (detecting_state, passing_state),
        (closed_state, open_state),
        (open_state, closed_state),
    ]

    states = [closed_state, open_state]

    def __init__(self, controller_pin=None):
        self.controller_pin = controller_pin
        super(Stopper, self).__init__(name='stopper', states=Stopper.states, rule=Stopper.rule)

    def _open(self):
        print("Stopper - opening*************")
        # self.controller_pin.value = True
        time.sleep(2)
        print("Stopper - opened**************")
        print()

    def _close(self):
        print("Stopper - closing*************")
        # self.controller_pin.value = False
        time.sleep(2)
        print("Stopper - closed**************")
        print()

    @atomic(device='stopper')
    def sensor_40_handler(self, event):
        # if event.get('event') == '1':
        self.transition(Stopper.closed_state, self._close)
        # elif event.get('event') == '2':
        #     self.transition(Stopper.passing_state, self._open)
        # else:
        #     self.transition(Stopper.initial_state, self._close)

    @atomic(device='stopper')
    def camara_handler(self, event):
        self.transition(Stopper.open_state, self._open)

    # def handle_pusher_event(self, event):
    #     self.transition(Stopper.passing_state, self._open)
