import time
import threading
from scservo_sdk import *
from STS3215 import STS3215Servo

import board
import busio
from adafruit_pca9685 import PCA9685
from adafruit_motor import servo

import serial
import serial.tools.list_ports
from utils import DCMotorSerial
import motor_communication as motor_communication

import RPi.GPIO as GPIO
from datetime import datetime

import serial.tools.list_ports
import pyudev

def find_ports():
    context = pyudev.Context()
    sts3215_port = None
    motor_port = None

    for device in context.list_devices(subsystem='tty'):
        if 'ID_VENDOR_FROM_DATABASE' in device:
            vendor = device.get('ID_VENDOR_FROM_DATABASE')
            if vendor:
                if 'QinHeng Electronics' in vendor:
                    sts3215_port = device.device_node
                elif 'Silicon Labs' in vendor:
                    motor_port = device.device_node

        # fallback: use USB ID
        if not sts3215_port and 'CH340' in str(device):
            sts3215_port = device.device_node
        if not motor_port and 'CP210' in str(device):
            motor_port = device.device_node

    return sts3215_port, motor_port

nbr_step = 16

servo_positions = [
    [30, 120,  55,  180,   155,   0, 0, 0, 0, 0,  0,  30,   0, 140,   55,  125,     0,     0,    0],  
    [30, 120,  55,   90,   155,   0, 0, 0, 0, 0,  0,  30,  90, 140,   55,  125,     0,     0,    0],  
    [30, 120,  55,   90,   155,   0, 0, 0, 0, 0,  0,  30,  90, 140,   55,  125,     0,     0,  200],  
    [10, 120,  30,   90,   155,   0, 0, 0, 0, 0,  0,  30,  90, 165,   55,  145,     0,     0,    0],  
    [10, 120,  55,   90,   155,   0, 0, 0, 0, 0,  0,  30,  90, 140,   55,  145,  1000,  1000,    0],  
    [10, 120,  55,   90,   155,   0, 0, 0, 0, 0,  0,  30,  90, 140,   55,  145,  1000,  1000, -150],  
    [10, 120,  55,   90,    37,   0, 0, 0, 0, 0,  0, 155,  90, 140,   55,  145,  1000,  1000,    0],  
    [10, 120,  55,    0,    37,   0, 0, 0, 0, 0,  0, 155, 180, 140,   55,  145,  1000,  1000,    0],  
    [10, 120,  55,  180,    37,   0, 0, 0, 0, 0,  0, 155,   0, 140,   55,  145,  1000,  1000,    0],  
    [10, 120,  55,   90,   155,   0, 0, 0, 0, 0,  0,  30,  90, 140,   55,  145, 14000, 14000,    0], 
    [10, 120,  55,   90,   155,   0, 0, 0, 0, 0,  0,  30,  90, 140,   55,  145, 14000, 14000,  150],  
    [10, 120,  30,   90,   155,   0, 0, 0, 0, 0,  0,  30,  90, 165,   55,  145, 13500, 13500,    0],  
    [10,  55,  30,   90,   155,   0, 0, 0, 0, 0,  0,  30,  90, 165,  120,  145, 13500, 13500,    0],  
    [30,  55,  55,   90,   155,   0, 0, 0, 0, 0,  0,  30,  90, 140,  120,  125, 13500, 13500,    0], 
    [30,  55,  55,   90,   155,   0, 0, 0, 0, 0,  0,  30,  90, 140,  120,  125, 11000, 11000, -200],  
    [30, 120,  55,   90,   155,   0, 0, 0, 0, 0,  0,  30,  90, 140,   55,  125,     0,     0,    0],  
]

port_STS3215, port_Motor = find_ports()
if port_STS3215 is None or port_Motor is None:
    raise RuntimeError("Error : failed to detect USB ports")
  
port_handler = PortHandler(port_STS3215)
packet_handler = PacketHandler(0)

port_handler.openPort()
port_handler.setBaudRate(1000000)

ser = motor_communication.init_serial(port_Motor, 115200)
Motor1 = DCMotorSerial(ser, 1)
Motor2 = DCMotorSerial(ser, 2)


try:
    # Initialisation
    servo1 = STS3215Servo(port_handler, packet_handler, servo_id=1)
    servo2 = STS3215Servo(port_handler, packet_handler, servo_id=2)

    i2c = busio.I2C(board.SCL, board.SDA)
    pca = PCA9685(i2c)
    pca.frequency = 50
    servos = [servo.Servo(pca.channels[i]) for i in range(16)]

    for servo_id in range(16):
            servos[servo_id].angle = servo_positions[0][servo_id]
    time.sleep(0.5)
    
    for servo_id in range(16):
            servos[servo_id].angle = servo_positions[1][servo_id]

    servo1.homing()
    servo2.homing()
    servo1.set_position_calib(servo_positions[0][16])
    servo2.set_position_calib(servo_positions[0][17])


    # GPIO.setmode(GPIO.BCM)
    # GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    # print("\n")   
    # while(1):
    #     state = GPIO.input(17)
    #     now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    #     sys.stdout.write("\033[F") 
    #     sys.stdout.write("\033[F")
    #     sys.stdout.write(f"{now}\n")
    #     sys.stdout.write(f"État GPIO17 : {'HAUT (1)' if state else 'BAS (0)'}   \n")

    #     sys.stdout.flush()
    #     time.sleep(0.1)

    #     if(state):
    #         break

    while(1):
        if(input("press return (exit to quit)\n") == "exit"):
            break

        move = False

        for step in range(1,nbr_step):
            #input()
            print("Step :", step)
            for servo_id in range(16):
                servos[servo_id].angle = servo_positions[step][servo_id]
                # print(f"Servo {servo_id} réglé à {servo_positions[step][servo_id]}°")
            for servo_id in range (16,18):
                if(servo_id == 16):
                    servo1.set_position_calib(servo_positions[step][servo_id])
                if(servo_id == 17):
                    servo2.set_position_calib(servo_positions[step][servo_id])
            Motor1.send_position_consigne(servo_positions[step][18])
            Motor2.send_position_consigne(servo_positions[step][18])
            
            if(servo_positions[step][3] != 90):
                time.sleep(0.8)

            time.sleep(0.5)

            if((servo_positions[step][18] != 0) or (servo_positions[step][16] != servo_positions[step-1][16])):
                time.sleep(1)
                while(abs(int(Motor1.get_speed())) > 1 or abs(int(Motor2.get_speed()) > 1)):
                    pass
                
                while(servo1.read_speed() > 10 or servo2.read_speed() > 10):
                    pass

        time.sleep(3)


except Exception as e:
    print(f"Error : {e}")
    print("Exit...")
    port_handler.closePort()
    motor_communication.close_serial(ser)
    pca.deinit()
    print("Bye!!")
    sys.exit(1)

finally:
    print("Exit...")
    port_handler.closePort()
    motor_communication.close_serial(ser)
    pca.deinit()
    print("Bye!!")

