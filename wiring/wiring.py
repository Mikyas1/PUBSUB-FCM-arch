from entities.Sensor40 import Sensor40
from entities.Stopper import Stopper
from entities.Camera import Camera
from entities.Pusher import Pusher
from entities.Sensor41 import Sensor41

# import board
# from adafruit_ina219 import ADCResolution, BusVoltageRange, INA219
#
# i2c_bus = board.I2C()


def wire_entities():
    # sensor_40 = Sensor40(source=INA219(i2c_bus, 0x40))
    sensor_40 = Sensor40()
    camera = Camera()
    camera.handel_events(event_handler_pairs=[(sensor_40.get_sensor_event_bus(), camera.sensor_40_handler)])
    stopper = Stopper()
    stopper.handel_events(event_handler_pairs=[
        (sensor_40.get_sensor_event_bus(), stopper.sensor_40_handler),
        (camera.get_sensor_event_bus(), stopper.camara_handler),
    ])
    sensor_41 = Sensor41()
    pusher = Pusher()
    pusher.handel_events(event_handler_pairs=[
        (camera.get_sensor_event_bus(), pusher.handel_no_cup_or_not_detected),
        (sensor_41.get_sensor_event_bus(), pusher.handle_sensor_41_detection)
    ])
