import time
from scservo_sdk import *


class STS3215Servo:
    # Registres EEPROM
    ADDR_SERVO_ID = 5
    ADDR_MIN_POSITION_LIMIT = 9
    ADDR_MAX_POSITION_LIMIT = 11
    ADDR_MAX_TORQUE = 48

    # Registres RAM
    ADDR_TORQUE_ENABLE = 40
    ADDR_POSITION_GOAL = 42
    ADDR_SPEED_GOAL = 46
    ADDR_POSITION_CURRENT = 56
    ADDR_SPEED_CURRENT = 58
    ADDR_TEMPERATURE_CURRENT = 63
    ADDR_VOLTAGE_CURRENT = 62
    ADDR_TORQUE_CURRENT = 60
    ADDR_MODE_SERVO = 33

    def __init__(self, port_handler, packet_handler, servo_id):

        self.port_handler = port_handler
        self.packet_handler = packet_handler
        self.servo_id = servo_id

        self.zero = 0
        self.range = 0

    def enable_torque(self, enable=True):
        self.packet_handler.write1ByteTxRx(self.port_handler, self.servo_id, self.ADDR_TORQUE_ENABLE, int(enable))

    def set_torque_limit(self, max):
        self.packet_handler.write2ByteTxRx(self.port_handler, self.servo_id, self.ADDR_MAX_TORQUE, max)

    def set_position_limit(self, min ,max):
        self.packet_handler.write2ByteTxRx(self.port_handler, self.servo_id, self.ADDR_MIN_POSITION_LIMIT, min)
        self.packet_handler.write2ByteTxRx(self.port_handler, self.servo_id, self.ADDR_MAX_POSITION_LIMIT, max)

    def set_position(self, angle, unit="pos"):
        if unit == "deg":
            pos = int(angle / 0.088)  # résolution ≈ 0.088° par unité
        else:
            pos = int(angle)
        self.packet_handler.write2ByteTxRx(self.port_handler, self.servo_id, self.ADDR_POSITION_GOAL, pos)

    def set_position_calib(self, pos):
        pos = self.zero + (self.range - int(pos))
        self.packet_handler.write2ByteTxRx(self.port_handler, self.servo_id, self.ADDR_POSITION_GOAL, pos)

    def set_speed(self, speed):
        if(speed < 0):
            speed_val = int(-speed) + 32768
        else:
            speed_val = int(speed) 
        self.packet_handler.write2ByteTxRx(self.port_handler, self.servo_id, self.ADDR_SPEED_GOAL, speed_val)

    def read_torque(self):
        torque, _, _ = self.packet_handler.read2ByteTxRx(self.port_handler, self.servo_id, self.ADDR_TORQUE_CURRENT)
        return torque

    def read_position(self, unit="pos"):
        pos, _, _ = self.packet_handler.read2ByteTxRx(self.port_handler, self.servo_id, self.ADDR_POSITION_CURRENT)
        return pos * 0.088 if unit == "deg" else pos

    def read_speed(self, unit="raw"):
        speed, _, _ = self.packet_handler.read2ByteTxRx(self.port_handler, self.servo_id, self.ADDR_SPEED_CURRENT)
        return speed * 0.01465 if unit == "rpm" else speed

    def read_temperature(self):
        temp, _, _ = self.packet_handler.read1ByteTxRx(self.port_handler, self.servo_id, self.ADDR_TEMPERATURE_CURRENT)
        return temp

    def read_voltage(self):
        volt, _, _ = self.packet_handler.read1ByteTxRx(self.port_handler, self.servo_id, self.ADDR_VOLTAGE_CURRENT)
        return volt / 10.0  # Tension en V

    def set_mode(self, mode="servo"):
        if mode == "servo":
            mode_val = 0
        elif mode == "speed":
            mode_val = 1
        else:
            mode_val = 0
        self.packet_handler.write1ByteTxRx(self.port_handler, self.servo_id, self.ADDR_MODE_SERVO, mode_val)

    def ping(self):
        return self.packet_handler.ping(self.port_handler, self.servo_id)

    def set_id(self, new_id):
        self.packet_handler.write1ByteTxRx(self.port_handler, self.servo_id, self.ADDR_SERVO_ID, new_id)
        self.servo_id = new_id

    def read_id(self):
        id, _, _ = self.packet_handler.read1ByteTxRx(self.port_handler, self.servo_id, self.ADDR_SERVO_ID)
        return id 
    
    def homing_find_max(self, torque):
        self.set_mode("speed")

        self.set_speed(1000)
        time.sleep(0.05)
        while(self.read_torque() < torque): #550 1570
            # print("torque", self.read_torque())
            # print("speed", self.read_speed())
            # print("position", self.read_position())
            pass
        self.set_speed(0)
        time.sleep(1)
        self.set_speed(0)

        return self.read_position()

    
    def homing_find_zero(self, torque):
        prec = self.read_position()
        n = 0

        self.set_mode("speed")
        self.set_speed(-1000)
        time.sleep(0.05)
        while(self.read_torque() < torque): #550 1570
            # print("torque", self.read_torque())
            # print("speed", self.read_speed())
            pos = self.read_position()
            #print("position", pos)
            if pos > prec:
                n = n + 1
            prec = pos
        self.set_speed(0)
        time.sleep(1)
        self.set_speed(0)
        self.zero = self.read_position()
        return n

    def homing(self):
        print("Homing servo ID", self.read_id() ,"in progress...")

        torque_max = 1570
        torque_min = 570

        while(self.range < 10000 or self.range > 16000):
            max = self.homing_find_max(torque_max)
            n = self.homing_find_zero(torque_min)

            self.range = max - self.zero + n*4096
            if self.range < 10000:
                torque_max = torque_max + 10
                torque_min = torque_min + 10
         

        print("ID : ", self.read_id() ,"; Zero : ", self.zero, "; Range : ", self.range)
        self.set_mode("servo")

        self.set_position_limit(self.zero + 300, self.zero + self.range - 300)  