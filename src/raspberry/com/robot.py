"""
Project
-------
    ARC 2024-2025

Author
------
    PIROLA Damien - Halyre

Module
------
    Utils

Presentation
------------

    This module regroup all utility function of the backend of the project.

"""

import serial.tools.list_ports
import serial

import com.motor_communication as motor_communication
import utils.constant as constant

def port_com_available():
    """ 
    Function that list COM ports. 

    Return
    ------
        list_port_com : ?
            List of all available ports COM
    """

    return serial.tools.list_ports.comports()

class DCMotorSerial:
    """Create a class to control a physical DC motor."""
    def __init__(self, serial, id):
        """
        Parameters
        ----------
            serial : Serial
                serial connexion used for physical motors.
            id : int
                id of the motor.
        """
        self.serial = serial
        self.id = id

    def send_ki_speed(self, value):
        """
        Method that send ki speed parameter to the physical motor.
        
        Parameters
        ----------
            value : float
                value sent to the physical motor.
        
        Return
        ------
            constant.self.p_error
            constant.SUCCES
        """

        motor_communication.send_write_command(self.serial, self.id, "KIS", value)
        if not(motor_communication.rcv_write_command(self.serial, self.id, "KIS", value)):
            return constant.self.p_error
        else:
            return constant.SUCCES

    def send_kp_speed(self, value):
        """
        Method that send kp speed parameter to the physical motor.
        
        Parameters
        ----------
            value : float
                value sent to the physical motor.
        
        Return
        ------
            constant.self.p_error
            constant.SUCCES
        """ 
    
        motor_communication.send_write_command(self.serial, self.id, "KPS", value)
        if not(motor_communication.rcv_write_command(self.serial, self.id, "KPS", value)):
            return constant.self.p_error
        else:
            return constant.SUCCES

    def send_kd_speed(self, value):
        """
        Method that send kd speed parameter to the physical motor.
        
        Parameters
        ----------
            value : float
                value sent to the physical motor.
        
        Return
        ------
            constant.self.p_error
            constant.SUCCES
        """
     
        motor_communication.send_write_command(self.serial, self.id, "KDS", value)
        if not(motor_communication.rcv_write_command(self.serial, self.id, "KDS", value)):
            return constant.self.p_error
        else:
            return constant.SUCCES

    def send_speed_consigne(self, value):
        """
        Method that send speed consigne to the physical motor.
        
        Parameters
        ----------
            value : float
                value (in rpm) sent to the physical motor.
        
        Return
        ------
            constant.self.p_error
            constant.SUCCES
        """

        motor_communication.send_write_command(self.serial, self.id, "CS", value)
        if not(motor_communication.rcv_write_command(self.serial, self.id, "CS", value)):
            return constant.self.p_error
        else:
            return constant.SUCCES

    def send_tpr_encode(self, value):
        """
        Method that send ticks per revolution encoding to the physical motor.
        
        Parameters
        ----------
            value : float
                value (in N) sent to the physical motor.
        
        Return
        ------
            constant.self.p_error
            constant.SUCCES
        """

        motor_communication.send_write_command(self.serial, self.id, "TPR", value)
        if not(motor_communication.rcv_write_command(self.serial, self.id, "TPR", value)):
            return constant.self.p_error
        else:
            return constant.SUCCES

    def send_reduction(self, value):
        """
        Method that send reduction to the physical motor.
        
        Parameters
        ----------
            value : float
                value (in N) sent to the physical motor.
        
        Return
        ------
            constant.self.p_error
            constant.SUCCES
        """

        motor_communication.send_write_command(self.serial, self.id, "R", value)
        if not(motor_communication.rcv_write_command(self.serial, self.id, "R", value)):
            return constant.self.p_error
        else:
            return constant.SUCCES

    def send_flash_card_cte(self):
        """
        Method that send flash card in cte to the physical motor.

        No parameter, motor card wait Na value.
        
        Return
        ------
            constant.self.p_error
            constant.SUCCES
        """

        motor_communication.send_write_command(self.serial, self.id, "FL", None)
        if not(motor_communication.rcv_write_command(self.serial, self.id, "FL", None)):
            return constant.self.p_error
        else:
            return constant.SUCCES
        
    def send_stop(self):
        """
        Method that send stop to the physical motor.

        No parameter, motor card wait Na value.
        
        Return
        ------
            constant.self.p_error
            constant.SUCCES
        """

        motor_communication.send_write_command(self.serial, self.id, "STOP", None)
        if not(motor_communication.rcv_write_command(self.serial, self.id, "STOP", None)):
            return constant.self.p_error
        else:
            return constant.SUCCES

    def send_reset(self):
        """
        Method that send reset to the physical motor.

        No parameter, motor card wait Na value.
        Used after STOP command to restore consigne.
        
        Return
        ------
            constant.self.p_error
            constant.SUCCES
        """

        motor_communication.send_write_command(self.serial, self.id, "RST", None)
        if not(motor_communication.rcv_write_command(self.serial, self.id, "RST", None)):
            return constant.self.p_error
        else:
            return constant.SUCCES

    def send_polarity(self, value):
        """
        Method that send motor polarity to the physical motor.

        Parameters
        ----------
            value : Char
                value sent to the physical motor. Expected value N / I
            
        Return
        ------
            constant.self.p_error
            constant.SUCCES
        """

        motor_communication.send_write_command(self.serial, self.id, "POL", value)
        if not(motor_communication.rcv_write_command(self.serial, self.id, "POL", value)):
            return constant.self.p_error
        else:
            return constant.SUCCES

    def send_ki_position(self, value):
        """
        Method that send ki positition parameter to the physical motor.
        
        Parameters
        ----------
            value : float
                value sent to the physical motor.
        
        Return
        ------
            constant.self.p_error
            constant.SUCCES
        """

        motor_communication.send_write_command(self.serial, self.id, "KIP", value)
        if not(motor_communication.rcv_write_command(self.serial, self.id, "KIP", value)):
            return constant.self.p_error
        else:
            return constant.SUCCES

    def send_kp_position(self, value):
        """
        Method that send kp positition parameter to the physical motor.
        
        Parameters
        ----------
            value : float
                value sent to the physical motor.
        
        Return
        ------
            constant.self.p_error
            constant.SUCCES
        """ 
    
        motor_communication.send_write_command(self.serial, self.id, "KPP", value)
        if not(motor_communication.rcv_write_command(self.serial, self.id, "KPP", value)):
            return constant.self.p_error
        else:
            return constant.SUCCES

    def send_kd_position(self, value):
        """
        Method that send kp positition parameter to the physical motor.
        
        Parameters
        ----------
            value : float
                value sent to the physical motor.
        
        Return
        ------
            constant.self.p_error
            constant.SUCCES
        """ 
    
        motor_communication.send_write_command(self.serial, self.id, "KDP", value)
        if not(motor_communication.rcv_write_command(self.serial, self.id, "KDP", value)):
            return constant.self.p_error
        else:
            return constant.SUCCES

    def send_wheel_diameter(self, value):
        """
        Method that send wheel diameter to the physical motor.
        
        Parameters
        ----------
            value : float
                value (in mm) sent to the physical motor.
        
        Return
        ------
            constant.self.p_error
            constant.SUCCES
        """

        motor_communication.send_write_command(self.serial, self.id, "WD", value)
        if not(motor_communication.rcv_write_command(self.serial, self.id, "WD", value)):
            return constant.self.p_error
        else:
            return constant.SUCCES

    def send_max_command(self, value):
        """
        Method that send wheel diameter to the physical motor.
        
        Parameters
        ----------
            value : float
                value (in mm) sent to the physical motor.
        
        Return
        ------
            constant.self.p_error
            constant.SUCCES
        """

        motor_communication.send_write_command(self.serial, self.id, "MC", value)
        if not(motor_communication.rcv_write_command(self.serial, self.id, "MC", value)):
            return constant.self.p_error
        else:
            return constant.SUCCES

    def send_offset_command(self, value):
        """
        Method that send wheel diameter to the physical motor.
        
        Parameters
        ----------
            value : float
                value (in mm) sent to the physical motor.
        
        Return
        ------
            constant.self.p_error
            constant.SUCCES
        """

        motor_communication.send_write_command(self.serial, self.id, "OC", value)
        if not(motor_communication.rcv_write_command(self.serial, self.id, "OC", value)):
            return constant.self.p_error
        else:
            return constant.SUCCES

    def send_max_speed(self, value):
        """
        Method that send wheel diameter to the physical motor.
        
        Parameters
        ----------
            value : float
                value (in mm) sent to the physical motor.
        
        Return
        ------
            constant.self.p_error
            constant.SUCCES
        """

        motor_communication.send_write_command(self.serial, self.id, "MS", value)
        if not(motor_communication.rcv_write_command(self.serial, self.id, "MS", value)):
            return constant.self.p_error
        else:
            return constant.SUCCES

    def send_offset_speed(self, value):
        """
        Method that send wheel diameter to the physical motor.
        
        Parameters
        ----------
            value : float
                value (in mm) sent to the physical motor.
        
        Return
        ------
            constant.self.p_error
            constant.SUCCES
        """

        motor_communication.send_write_command(self.serial, self.id, "OS", value)
        if not(motor_communication.rcv_write_command(self.serial, self.id, "OS", value)):
            return constant.self.p_error
        else:
            return constant.SUCCES

    def send_wheel_distance(self, value):
        """
        Method that send wheel diameter to the physical motor.
        
        Parameters
        ----------
            value : float
                value (in mm) sent to the physical motor.
        
        Return
        ------
            constant.self.p_error
            constant.SUCCES
        """

        motor_communication.send_write_command(self.serial, self.id, "WO", value)
        if not(motor_communication.rcv_write_command(self.serial, self.id, "WO", value)):
            return constant.self.p_error
        else:
            return constant.SUCCES

    def get_ki_speed(self):
        """
        Method that ask the ki speed parameter value to the physical motor.

        Return
        ------
            value : float
        """

        motor_communication.send_read_command(self.serial, self.id, "KIS")
        return motor_communication.rcv_read_command(self.serial, self.id, "KIS")

    def get_kp_speed(self):
        """
        Method that ask the kp speed parameter value to the physical motor.

        Return
        ------
            value : float
        """
        motor_communication.send_read_command(self.serial, self.id, "KPS")
        return motor_communication.rcv_read_command(self.serial, self.id, "KPS")

    def get_kd_speed(self):
        """
        Method that ask the kd speed parameter value to the physical motor.

        Return
        ------
            value : float
        """

        motor_communication.send_read_command(self.serial, self.id, "KDS")
        return motor_communication.rcv_read_command(self.serial, self.id, "KDS")

    def get_speed_consigne(self):
        """
        Method that ask the speed consigne value to the physical motor.

        Return
        ------
            value : float (in rpm)
        """

        motor_communication.send_read_command(self.serial, self.id, "CS")
        return motor_communication.rcv_read_command(self.serial, self.id, "CS")

    def get_speed(self):
        """
        Method that ask the actual speed value to the physical motor.

        Return
        ------
            value : float (in rpm)
        """

        motor_communication.send_read_command(self.serial, self.id, "S")
        return motor_communication.rcv_read_command(self.serial, self.id, "S")
   
    def get_tpr_encode(self):
        """
        Method that ask the tick per revolution encoding value to the physical motor.

        Return
        ------
            value : float (in N)
        """

        motor_communication.send_read_command(self.serial, self.id, "TPR")
        return motor_communication.rcv_read_command(self.serial, self.id, "TPR")

    def get_reduction(self):
        """
        Method that ask the reduction value to the physical motor.

        Return
        ------
            value : float (in N)
        """

        motor_communication.send_read_command(self.serial, self.id, "R")
        return motor_communication.rcv_read_command(self.serial, self.id, "R")

    def get_polarity(self):
        """
        Method that ask the polarity value to the physical motor.

        Return
        ------
            value : char (N or I)
        """

        motor_communication.send_read_command(self.serial, self.id, "POL")
        return motor_communication.rcv_read_command(self.serial, self.id, "POL")
    
    def get_command(self):
        """
        Method that ask the polarity value to the physical motor.

        Return
        ------
            value : char (N or I)
        """

        motor_communication.send_read_command(self.serial, self.id, "C")
        return motor_communication.rcv_read_command(self.serial, self.id, "C")
    
    def get_ki_position(self):
        """
        Method that ask the ki position parameter value to the physical motor.

        Return
        ------
            value : float
        """

        motor_communication.send_read_command(self.serial, self.id, "KIP")
        return motor_communication.rcv_read_command(self.serial, self.id, "KIP")

    def get_kp_position(self):
        """
        Method that ask the kp position parameter value to the physical motor.

        Return
        ------
            value : float
        """
        motor_communication.send_read_command(self.serial, self.id, "KPP")
        return motor_communication.rcv_read_command(self.serial, self.id, "KPP")

    def get_kd_position(self):
        """
        Method that ask the kd position parameter value to the physical motor.

        Return
        ------
            value : float
        """

        motor_communication.send_read_command(self.serial, self.id, "KDP")
        return motor_communication.rcv_read_command(self.serial, self.id, "KDP")

    def get_max_command(self):
        """
        Method that ask the wheel reduction value to the physical motor.

        Return
        ------
            value : float (in mm)
        """

        motor_communication.send_read_command(self.serial, self.id, "MC")
        return motor_communication.rcv_read_command(self.serial, self.id, "MC")

    def get_offset_command(self):
        """
        Method that ask the wheel reduction value to the physical motor.

        Return
        ------
            value : float (in mm)
        """

        motor_communication.send_read_command(self.serial, self.id, "OC")
        return motor_communication.rcv_read_command(self.serial, self.id, "OC")

    def get_max_speed(self):
        """
        Method that ask the wheel reduction value to the physical motor.

        Return
        ------
            value : float (in mm)
        """

        motor_communication.send_read_command(self.serial, self.id, "MS")
        return motor_communication.rcv_read_command(self.serial, self.id, "MS")
    
    def get_offset_speed(self):
        """
        Method that ask the wheel reduction value to the physical motor.

        Return
        ------
            value : float (in mm)
        """

        motor_communication.send_read_command(self.serial, self.id, "OS")
        return motor_communication.rcv_read_command(self.serial, self.id, "OS")

    def get_wheel_distance(self):
        """
        Method that ask the wheel reduction value to the physical motor.

        Return
        ------
            value : float (in mm)
        """

        motor_communication.send_read_command(self.serial, self.id, "WO")
        return motor_communication.rcv_read_command(self.serial, self.id, "WO")
    
class PositionMotorSerial:
    """Create a class to control the position of a physical DC motor."""
    def __init__(self, serial, id):
        """
        Parameters
        ----------
            serial : Serial
                serial connexion used for physical motors.
            id : int
                id of the motor.
            speed_motor : DCMotorSerial
                class that control speed of physical motor.
        """
        self.serial = serial
        self.id = id

    def send_ki_position(self, value):
        """
        Method that send ki positition parameter to the physical motor.
        
        Parameters
        ----------
            value : float
                value sent to the physical motor.
        
        Return
        ------
            constant.self.p_error
            constant.SUCCES
        """

        motor_communication.send_write_command(self.serial, self.id, "KIP", value)
        if not(motor_communication.rcv_write_command(self.serial, self.id, "KIP", value)):
            return constant.self.p_error
        else:
            return constant.SUCCES

    def send_kp_position(self, value):
        """
        Method that send kp positition parameter to the physical motor.
        
        Parameters
        ----------
            value : float
                value sent to the physical motor.
        
        Return
        ------
            constant.self.p_error
            constant.SUCCES
        """ 
    
        motor_communication.send_write_command(self.serial, self.id, "KPP", value)
        if not(motor_communication.rcv_write_command(self.serial, self.id, "KPP", value)):
            return constant.self.p_error
        else:
            return constant.SUCCES

    def send_kd_position(self, value):
        """
        Method that send kd positition parameter to the physical motor.
        
        Parameters
        ----------
            value : float
                value sent to the physical motor.
        
        Return
        ------
            constant.self.p_error
            constant.SUCCES
        """
     
        motor_communication.send_write_command(self.serial, self.id, "KDP", value)
        if not(motor_communication.rcv_write_command(self.serial, self.id, "KDP", value)):
            return constant.self.p_error
        else:
            return constant.SUCCES

    def send_wheel_diameter(self, value):
        """
        Method that send wheel diameter to the physical motor.
        
        Parameters
        ----------
            value : float
                value (in mm) sent to the physical motor.
        
        Return
        ------
            constant.self.p_error
            constant.SUCCES
        """

        motor_communication.send_write_command(self.serial, self.id, "WD", value)
        if not(motor_communication.rcv_write_command(self.serial, self.id, "WD", value)):
            return constant.self.p_error
        else:
            return constant.SUCCES

    def send_position_consigne_abs(self, value):
        """
        Method that send position consigne to the physical motor.
        
        Parameters
        ----------
            value : float
                value (in mm) sent to the physical motor.
        
        Return
        ------
            constant.self.p_error
            constant.SUCCES
        """
        motor_communication.send_write_command(self.serial, self.id, "CPA", value)
        if not(motor_communication.rcv_write_command(self.serial, self.id, "CPA", value)):
            return constant.self.p_error
        else:
            return constant.SUCCES

    def send_position_consigne(self, value):
        """
        Method that send position consigne to the physical motor.
        
        Parameters
        ----------
            value : float
                value (in mm) sent to the physical motor.
        
        Return
        ------
            constant.self.p_error
            constant.SUCCES
        """
        motor_communication.send_write_command(self.serial, self.id, "CP", value)
        if not(motor_communication.rcv_write_command(self.serial, self.id, "CP", value)):
            return constant.self.p_error
        else:
            return constant.SUCCES

    def send_rotation_consigne(self, value):
        """
        Method that send position consigne to the physical motor.
        
        Parameters
        ----------
            value : float
                value (in mm) sent to the physical motor.
        
        Return
        ------
            constant.self.p_error
            constant.SUCCES
        """
        motor_communication.send_write_command(self.serial, self.id, "CPR", value)
        if not(motor_communication.rcv_write_command(self.serial, self.id, "CPR", value)):
            return constant.self.p_error
        else:
            return constant.SUCCES


    def get_ki_position(self):
        """
        Method that ask the ki position parameter value to the physical motor.

        Return
        ------
            value : float
        """

        motor_communication.send_read_command(self.serial, self.id, "KIP")
        return motor_communication.rcv_read_command(self.serial, self.id, "KIP")

    def get_kp_position(self):
        """
        Method that ask the kp position parameter value to the physical motor.

        Return
        ------
            value : float
        """
        motor_communication.send_read_command(self.serial, self.id, "KPP")
        return motor_communication.rcv_read_command(self.serial, self.id, "KPP")

    def get_kd_position(self):
        """
        Method that ask the kd position parameter value to the physical motor.

        Return
        ------
            value : float
        """

        motor_communication.send_read_command(self.serial, self.id, "KDP")
        return motor_communication.rcv_read_command(self.serial, self.id, "KDP")

    def get_position(self):
        """
        Method that ask the actual position value to the physical motor.

        Return
        ------
            value : float (in mm)
        """

        motor_communication.send_read_command(self.serial, self.id, "P")
        return motor_communication.rcv_read_command(self.serial, self.id, "P")

    def get_wheel_diameter(self):
        """
        Method that ask the wheel reduction value to the physical motor.

        Return
        ------
            value : float (in mm)
        """

        motor_communication.send_read_command(self.serial, self.id, "WD")
        return motor_communication.rcv_read_command(self.serial, self.id, "WD")

    def send_reset(self):
        """
        Method that send reset to the physical motor.

        No parameter, motor card wait Na value.
        Used after STOP command to restore consigne.
        
        Return
        ------
            constant.self.p_error
            constant.SUCCES
        """

        motor_communication.send_write_command(self.serial, self.id, "RST", None)
        if not(motor_communication.rcv_write_command(self.serial, self.id, "RST", None)):
            return constant.self.p_error
        else:
            return constant.SUCCES

class RobotSerial:
    """Create a class to control 2 DC motors robot."""
    def __init__(self, serial, p_error=3):
        """
        Parameters
        ----------
            serial : Serial
                serial connexion used for physical motors.
            id : int
                id of the motor.
            speed_motor : DCMotorSerial
                class that control speed of physical motor.
        """
        self.serial = serial
        self.id = 12
        self.actual_x = 0
        self.actual_y = 0
        self.actual_theta = 0

        self.p_error = p_error
        self.isUsed = False

    def send_stop(self):
        """
        Method that send stop to the physical motor.

        No parameter, motor card wait Na value.
        
        Return
        ------
            constant.self.p_error
            constant.SUCCES
        """

        motor_communication.send_write_command(self.serial, self.id, "STOP", None)
        if not(motor_communication.rcv_write_command(self.serial, self.id, "STOP", None)):
            return constant.self.p_error
        else:
            return constant.SUCCES

    def send_position_consigne(self, value):
        """
        Method that send position consigne to the physical motor.
        
        Parameters
        ----------
            value : float
                value (in mm) sent to the physical motor.
        
        Return
        ------
            constant.self.p_error
            constant.SUCCES
        """
        motor_communication.send_write_command(self.serial, self.id, "CP", value)
        if not(motor_communication.rcv_write_command(self.serial, self.id, "CP", value)):
            return constant.self.p_error
        else:
            return constant.SUCCES
           
    def set_x(self, value):
        motor_communication.send_write_command(self.serial, 0, "X", value)
        return motor_communication.rcv_write_command(self.serial, 0, "X", value)

    def set_y(self, value):
        motor_communication.send_write_command(self.serial, 0, "Y", value)
        return motor_communication.rcv_write_command(self.serial, 0, "Y", value)
    
    def set_theta(self, value):
        motor_communication.send_write_command(self.serial, 0, "THETA", value)
        return motor_communication.rcv_write_command(self.serial, 0, "THETA", value)
      
    def send_rotation_consigne(self, value):
        """
        Method that send position consigne to the physical motor.
        
        Parameters
        ----------
            value : float
                value (in degree) sent to the physical motor.
        
        Return
        ------
            constant.self.p_error
            constant.SUCCES
        """
        motor_communication.send_write_command(self.serial, 0, "CPR", value)
        if not(motor_communication.rcv_write_command(self.serial, 0, "CPR", value)):
            return constant.self.p_error
        else:
            return constant.SUCCES
    
    def update_diff_position(self):
        self.diff_pos = self.left_pos - self.right_pos

    def get_actual_x(self):
        motor_communication.send_read_command(self.serial, 0, "X")
        return motor_communication.rcv_read_command(self.serial, 0, "X")

    def get_actual_y(self):
        motor_communication.send_read_command(self.serial, 0, "Y")
        return motor_communication.rcv_read_command(self.serial, 0, "Y")
    
    def get_actual_theta(self):
        motor_communication.send_read_command(self.serial, 0, "THETA")
        return motor_communication.rcv_read_command(self.serial, 0, "THETA")

    def get_busy(self, nb):
        counter = 0
        for _ in range(nb):
            motor_communication.send_read_command(self.serial, 1, "PERR")
            perr_1 = motor_communication.rcv_read_command(self.serial, 1, "PERR")
            
            motor_communication.send_read_command(self.serial, 2, "PERR")
            perr_2 = motor_communication.rcv_read_command(self.serial, 2, "PERR")

            if (perr_1 <= -self.p_error or perr_1 >= self.p_error) or (perr_2 <= -self.p_error or perr_2 >= self.p_error):
                counter += 1

        return nb == counter

    
  