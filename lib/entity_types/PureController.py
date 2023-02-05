from typing import List, Tuple
import time
from threading import Thread
from event_bus.decorators import atomic
from state_machines.FSM import FSM, State


# stateful FSM with locks
class PureController(FSM):
    def __init__(self, name: str, states: List[State], rule: List[Tuple[State, State]]):
        self.name = name
        super(PureController, self).__init__(states=states, rule=rule)

    def handle_event_on_separate_thread(self, event_bus, handler):
        Thread(target=event_bus.subscribe, args=(handler,), daemon=False).start()

    def handel_events(self, event_handler_pairs: List[Tuple]):
        for event_handler_pair in event_handler_pairs:
            self.handle_event_on_separate_thread(event_bus=event_handler_pair[0], handler=event_handler_pair[1])
