import pyudev
from scservo_sdk import *
from adafruit_pca9685 import PCA9685
from adafruit_motor import servo
import board
import busio
import serial as ser
import time

from com.motor_communication import init_serial
from com.robot import RobotSerial
from com.STS3215 import STS3215Servo
from com.lidar import Lidar
from com.screen import Screen
from com.pami import Pami

def find_ports():
    context = pyudev.Context()
    sts3215_port = None
    robot_port = None
    screen_port = None
    lidar_port = None

    CH340_port = []
    CP210_port = []

    for device in context.list_devices(subsystem='tty'):
        if 'ID_VENDOR_FROM_DATABASE' in device:
            vendor = device.get('ID_VENDOR_FROM_DATABASE')
            if vendor:
                if 'QinHeng Electronics' in vendor:
                    CH340_port.append(device.device_node)
                elif 'Silicon Labs' in vendor:
                    CP210_port.append(device.device_node)

    for port in CH340_port:
        serial = ser.Serial(port, 115200, timeout=1)
        serial.write("Screen:R:S\n".encode('utf-8'))
        try:
            reponse = serial.readline().decode('utf-8').strip()
        except Exception as e:
            reponse = None

        if reponse == "Screen:R:S:0:OK":
            print("Port screen : ", port)
            screen_port = port
        else:
            print("Port sts3215 : ", port)
            sts3215_port = port

        serial.close()

    for port in CP210_port:
        serial = ser.Serial(port, 115200, timeout=1)
        serial.write("1:R\n".encode('utf-8'))
        try:
            reponse = serial.readline().decode('utf-8').strip()
        
        except Exception as e:
            reponse = None

        if reponse == "1:R:?":
            print("Port robot : ", port)
            robot_port = port
        else:
            print("Port lidar : ", port)
            lidar_port = port
        serial.close()

    return sts3215_port, robot_port, screen_port, lidar_port


def init_coms_robot():
    init_success = "OUI\n"
    try:
        sts3215_port, robot_port, screen_port, lidar_port = find_ports()
        sts3215 = []
        port_handler = PortHandler(sts3215_port)
        packet_handler = PacketHandler(0)

        port_handler.openPort()
        port_handler.setBaudRate(1000000)

        ser = init_serial(robot_port, 115200)

        robot = RobotSerial(ser)
        robot.get_actual_x()

        sts3215.append(STS3215Servo(port_handler, packet_handler, servo_id=1))
        sts3215.append(STS3215Servo(port_handler, packet_handler, servo_id=2))

        i2c = busio.I2C(board.SCL, board.SDA)
        pca = PCA9685(i2c)
        pca.frequency = 50
        servos = [servo.Servo(pca.channels[i]) for i in range(16)]

        screen = Screen(screen_port)
        
    except Exception as e:
        init_success = "NON\n"
    screen.serial.write(("Serial init : "+init_success).encode('utf-8'))
    return sts3215, robot, Lidar(lidar_port), servos, screen, Pami(screen.serial), pca
