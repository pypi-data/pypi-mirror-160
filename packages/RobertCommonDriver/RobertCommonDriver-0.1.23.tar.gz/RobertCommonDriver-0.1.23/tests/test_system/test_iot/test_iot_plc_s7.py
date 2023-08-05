import random
import time
from robertcommondriver.system.iot.iot_plc_s7 import IOTPlcS7


def logging_print(**kwargs):
    print(kwargs)


def test_simulate():
    dict_config = {'multi_read': 20, 'cmd_interval': 0.3, 'send_timeout': 15, 'rec_timeout': 3500}
    dict_point = {}
    dict_point['plc1'] = {'point_writable': True, 'point_name': 'plc1', 'point_device_address': 102, 'point_address': 'DB3,REAL4', 'point_scale': '1'}
    dict_point['plc2'] = {'point_writable': True, 'point_name': 'plc2', 'point_device_address': 102, 'point_address': 'DB3,REAL8', 'point_scale': '1'}

    client = IOTPlcS7(configs = dict_config, points= dict_point)
    client.logging(call_logging=logging_print)
    while True:
        try:
            for name, point in dict_point.items():
                point['point_value'] = f"{random.randint(1, 100)}"
            client.simulate(points=dict_point)
        except Exception as e:
            print(f"error: {e.__str__()}")
        time.sleep(4)


def test_read():
    pass

test_simulate()