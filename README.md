A Python implementation of multi-traded publisher-subscriber architecture with a built-in finite state machine library. Ideal to be used in complex event-driven sensor-controller applications mainly with microcontrollers like Raspberry Pi and Jetson boards.

This is a core part that can be used to build your automated, IoT.... systems.
Feel free to create pull request!!

### Create an Entity
An entity can be a sensor, a controler or anything you want, something that can emit or receive an event.
Create your entities under the entites folder for organazation purposes
## PureSensor entites
This entites will have methods for sensing and emiting event
- Ex entities/Sensor40.py
```python
def sensing_logic(self):
        while True:
            current_40 = self.source.current
            if current_40 > 0.5:
                self.event_bus.publish('detected-at-sensor-40')
            time.sleep(0.3)
```

## PureController entites
This entites define methods to subscribe to events
- Ex entites/Stopper.py

```python
    @atomic(device='stopper')
    def camara_handler(self, event):
        self.transition(Stopper.open_state, self._open)
```

## SensorController entites
This entites can both emit and receive events

## FSM
Controller entites can inherit from lib.state_machines.FSM to handle complex state managment using FSM

```python
from lib.state_machines.FSM import State

class Stopper(PureController):
    closed_state = State(name='Closed', initial=True)
    open_state = State(name='Opened')

    rule = [
        (closed_state, open_state),
        (open_state, closed_state),
    ]

    states = [closed_state, open_state]

    def __init__(self, controller_pin=None):
        super(Stopper, self).__init__(name='stopper', states=Stopper.states, rule=Stopper.rule)

    @atomic(device='stopper')
    def camara_handler(self, event):
        self.transition(Stopper.open_state, self._open)
```

### How to wire things up
Initialize the entity and call handel_events with the event sourses event bus and the method to be called when event is emited
- Ex wiring/wiring.py
  
```python
camera = Camera(args=args)
sensor_41 = Sensor41()
stopper = Stopper()
stopper.handel_events(event_handler_pairs=[
    (camera.get_sensor_event_bus(), stopper.camara_handler),
    (sensor_41.get_sensor_event_bus(), stopper.handle_sensor_41_detection)
])
```
