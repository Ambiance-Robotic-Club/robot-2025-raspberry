import serial as ser

import com.motor_communication as motor_communication
import utils.constant as constant
class Screen:
    def __init__(self, port):

        self.serial = ser.Serial(port, 115200, timeout=1)
        self.id = "Screen"
    
    def get_color(self):
        motor_communication.send_read_command(self.serial, self.id, "C")
        return "Yellow" if motor_communication.rcv_read_command(self.serial, self.id, "C") == 1 else "Blue"


    def get_current(self):
        motor_communication.send_read_command(self.serial, self.id, "A")
        return motor_communication.rcv_read_command(self.serial, self.id, "A")


    def get_battery(self):
        motor_communication.send_read_command(self.serial, self.id, "V")
        return motor_communication.rcv_read_command(self.serial, self.id, "V")

    def get_score(self):
        motor_communication.send_read_command(self.serial, self.id, "S")
        return motor_communication.rcv_read_command(self.serial, self.id, "S")
        
    def get_zone(self):
        motor_communication.send_read_command(self.serial, self.id, "Z")
        return motor_communication.rcv_read_command(self.serial, self.id, "Z")

    def get_timer(self):
        motor_communication.send_read_command(self.serial, self.id, "T")
        return motor_communication.rcv_read_command(self.serial, self.id, "T")

    def get_init_act(self):
        motor_communication.send_read_command(self.serial, self.id, "I")
        return motor_communication.rcv_read_command(self.serial, self.id, "I")
    
    def set_score(self, value):
        motor_communication.send_write_command(self.serial, self.id, "S", value)
        if not(motor_communication.rcv_write_command(self.serial, self.id, "S", value)):
            return constant.ERROR
        else:
            return constant.SUCCES

    def set_timer(self, value):
        motor_communication.send_write_command(self.serial, self.id, "T", value)
        if not(motor_communication.rcv_write_command(self.serial, self.id, "T", value)):
            return constant.ERROR
        else:
            return constant.SUCCES