import time

from lib.entity_types.SensorController import SensorController
from lib.state_machines.FSM import State
from lib.event_bus.decorators import atomic
from threading import Thread


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

    def __init__(self, args):
        # Thread(target=self._set_up_camera, args=('',), daemon=False)
        super(Camera, self).__init__(name='stopper', states=Camera.states, rule=Camera.rule)

    def _set_up_camera(self, args):
        # return CameraUtil(args)
        pass

    # display should be other class
    def _set_up_display(self):
        # open_window(
        #     'WINDOW_NAME', 'Camera TensorRT YOLO Cap',
        #     self.cam.img_width, self.cam.img_height)
        pass

    def _do_detect(self):
        print("Camera detecting")
        time.sleep(5)
        print("Camera done detecting")
        self.event_bus.publish("cap-detected")

    @atomic(device='camera')
    def sensor_40_handler(self, event):
        # if event.get('event') == '1':
        self.transition(Camera.detecting_state, self._do_detect, Camera.ignoring_state)
