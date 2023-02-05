from threading import Lock
from typing import List, Tuple, Callable, Optional


class State:
    def __init__(self, name, initial=False):
        self.name = name
        self.initial = initial

    def __eq__(self, other):
        return self.name == other.name

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        return self.name


class FSM:
    def __init__(self, states: List[State], rule: List[Tuple[State, State]]):
        self.states = states
        self.rule = rule
        self.state = None
        self.name = 'FCM machine'
        self.state_lock = Lock()
        for state in self.states:
            if state.initial:
                self.state_lock.acquire()
                self.state = state
                self.state_lock.release()
        # todo raise exception if no initial state is provided/ multiple initial states provided

    def _is_allowed(self, starting_state: State, ending_state: State):
        for rule_tuple in self.rule:
            if rule_tuple[0] == starting_state and rule_tuple[1] == ending_state:
                return True
        return False

    @property
    def get_state(self):
        self.state_lock.acquire()
        state = self.state
        self.state_lock.release()
        return state

    def transition(self, state: State, func: Optional[Callable[[], None]] = None,
                   final_state: State | None = None) -> bool:
        result = False
        self.state_lock.acquire()
        if self._is_allowed(starting_state=self.state, ending_state=state):
            self.state = state
            result = True
            if func is not None:
                func()
            if final_state is not None:
                self.state = final_state
        else:
            # todo raise exception if transition is not allowed
            print(f"Error: {self.name} transition from '{self.state}' is not allowed to '{state}'")
        self.state_lock.release()
        return result
