import com.motor_communication as motor_communication
import utils.constant as constant


class Pami:

    def __init__(self, serial):
        self.serial = serial

    def get_color_pami(self, address):
        motor_communication.send_read_command(self.serial, address, "C")
        return motor_communication.rcv_read_command_pami(self.serial, address, "C")

    def get_actual_x_pami(self, address):
        motor_communication.send_read_command(self.serial, address, "X")
        return motor_communication.rcv_read_command_pami(self.serial, address, "X")

    def get_actual_x_pami(self, address):
        motor_communication.send_read_command(self.serial, address, "Y")
        return motor_communication.rcv_read_command_pami(self.serial, address, "Y")
    
    def get_actual_x_pami(self, address):
        motor_communication.send_read_command(self.serial, address, "THETA")
        return motor_communication.rcv_read_command_pami(self.serial, address, "THETA")
    
    def send_stop_pami(self, address):
        motor_communication.send_write_command(self.serial, address, "STOP", None)
        if not(motor_communication.rcv_write_command_pami(self.serial, address, "STOP", None)):
            return constant.ERROR
        else:
            return constant.SUCCES

    def send_color_pami(self, address, value):
        motor_communication.send_write_command(self.serial, address, "C", value)
        if not(motor_communication.rcv_write_command_pami(self.serial, address, "C", value)):
            return constant.ERROR
        else:
            return constant.SUCCES

    def send_x_pami(self, address, value):
        motor_communication.send_write_command(self.serial, address, "X", value)
        if not(motor_communication.rcv_write_command_pami(self.serial, address, "X", value)):
            return constant.ERROR
        else:
            return constant.SUCCES

    def send_y_pami(self, address, value):
        motor_communication.send_write_command(self.serial, address, "Y", value)
        if not(motor_communication.rcv_write_command_pami(self.serial, address, "Y", value)):
            return constant.ERROR
        else:
            return constant.SUCCES
        
    def send_theta_pami(self, address, value):
        motor_communication.send_write_command(self.serial, address, "THETA", value)
        if not(motor_communication.rcv_write_command_pami(self.serial, address, "THETA", value)):
            return constant.ERROR
        else:
            return constant.SUCCES