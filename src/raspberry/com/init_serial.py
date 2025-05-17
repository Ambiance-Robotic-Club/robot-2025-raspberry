import pyudev
from scservo_sdk import *
from adafruit_pca9685 import PCA9685
from adafruit_motor import servo
import board
import busio

from com.motor_communication import init_serial
from com.robot import RobotSerial
from com.STS3215 import STS3215Servo
from com.lidar import Lidar

def find_ports():
    context = pyudev.Context()
    sts3215_port = None
    robot_port = None

    for device in context.list_devices(subsystem='tty'):
        if 'ID_VENDOR_FROM_DATABASE' in device:
            vendor = device.get('ID_VENDOR_FROM_DATABASE')
            if vendor:
                if 'QinHeng Electronics' in vendor:
                    sts3215_port = device.device_node
                elif 'Silicon Labs' in vendor:
                    robot_port = device.device_node

        if not sts3215_port and 'CH340' in str(device):
            sts3215_port = device.device_node
        if not robot_port and 'CP210' in str(device):
            robot_port = device.device_node

    return sts3215_port, robot_port


def init_coms_robot():
    
    sts3215_port, robot_port = find_ports()
    sts3215 = []
    port_handler = PortHandler(sts3215_port)
    packet_handler = PacketHandler(0)

    port_handler.openPort()
    port_handler.setBaudRate(1000000)

    ser = init_serial(robot_port, 115200)
    sts3215.append(STS3215Servo(port_handler, packet_handler, servo_id=1))
    sts3215.append(STS3215Servo(port_handler, packet_handler, servo_id=2))

    i2c = busio.I2C(board.SCL, board.SDA)
    pca = PCA9685(i2c)
    pca.frequency = 50
    servos = [servo.Servo(pca.channels[i]) for i in range(16)]


    return sts3215, RobotSerial(ser), Lidar(), servos

    