import com.motor_communication as motor_communication
import utils.constant as constant


class Pami:

    def __init__(self, serial):
        self.serial = serial

    def get_color_pami(self, address):
        motor_communication.send_read_command(self.serial, address+";0", "C")
        return motor_communication.rcv_read_command_pami(self.serial, address+";0", "C")

    def get_actual_x_pami(self, address):
        motor_communication.send_read_command(self.serial, address+";0", "X")
        return motor_communication.rcv_read_command_pami(self.serial, address+";0", "X")

    def get_actual_y_pami(self, address):
        motor_communication.send_read_command(self.serial, address+";0", "Y")
        return motor_communication.rcv_read_command_pami(self.serial, address+";0", "Y")
    
    def get_actual_theta_pami(self, address):
        motor_communication.send_read_command(self.serial, address+";0", "THETA")
        return motor_communication.rcv_read_command_pami(self.serial, address+";0", "THETA")
    
    def send_stop_pami(self, address):
        motor_communication.send_write_command(self.serial, address+";0", "STOP", None)
        if not(motor_communication.rcv_write_command_pami(self.serial, address+";0", "STOP", None)):
            return constant.ERROR
        else:
            return constant.SUCCES

    def send_color_pami(self, address, value): # 1 Yellow, 0 Blue
        color = 1 if value == "Yellow" else 0
        
        motor_communication.send_write_command(self.serial, address+";0", "C", color)
        if not(motor_communication.rcv_write_command_pami(self.serial, address+";0", "C", color)):
            return constant.ERROR
        else:
            return constant.SUCCES

    def send_x_pami(self, address, value):
        motor_communication.send_write_command(self.serial, address+";0", "X", value)
        if not(motor_communication.rcv_write_command_pami(self.serial, address+";0", "X", value)):
            return constant.ERROR
        else:
            return constant.SUCCES

    def send_y_pami(self, address, value):
        motor_communication.send_write_command(self.serial, address+";0", "Y", value)
        if not(motor_communication.rcv_write_command_pami(self.serial, address+";0", "Y", value)):
            return constant.ERROR
        else:
            return constant.SUCCES
        
    def send_theta_pami(self, address, value):
        motor_communication.send_write_command(self.serial, address+";0", "THETA", value)
        if not(motor_communication.rcv_write_command_pami(self.serial, address+";0", "THETA", value)):
            return constant.ERROR
        else:
            return constant.SUCCES