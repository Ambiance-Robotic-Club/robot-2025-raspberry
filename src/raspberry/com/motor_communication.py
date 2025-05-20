"""
Project
-------
    ARC 2024-2025

Author
------
    PIROLA Damien - Halyre

Module
------
    Motor communication

Presentation
------------
    This module define all functions to communicate with STM32 motor controler. 
    It also defines function to set servo-control parameters.

    The following UART protocol is used :

        Baudrate : 115200
        Only 3 motors can be processed in same time

        Read message :

            Message send to get actual value of a specified command. 
            Can be send only one by one.

            Message architecture :  MOTOR:R:COMMAND
                whith : 
                    MOTOR : 1 / 2 / 3 (only one by one)
                    R : Read
                    COMMAND : S (Speed) / P (Position) / TPR (Ticks per revolution) / R (Reduction) / WD (Wheel diameter) / POL (Motor polarity)
            
            Response expected : MOTOR:R:COMMAND:VALUE:OK

        Write message :

            Message send to modify actual consigne of a specified command

            Message architecture :  MOTOR:W:COMMAND:VALUE\\n
                with :
                    MOTOR : 1 / 2 / 3 / 12 / 23 / 13 / 123
                    W : Write
                    COMMAND = CS (Speed) / CP (Position) / KP / KI / KD / TPR (Ticks per revolution) / R (Reduction) / WD (Wheel diameter) / FL (Write flash in cte) / STOP / RST (Reset motor value) / POL (Motor Polarity) 
                    VALUE : New consigne value to reach

            Response expected : MOTOR:W:COMMAND:VALUE:OK
"""

import serial as ser
import time
import numpy as np
import re

def init_serial(port, baudrate):
    """ 
    Function to init UART port. 
    This function wait a line from the serial to validate the init.
    It also init timeout to 0.5 second.

    Parameters
    ----------
        port : int
            port COM
        baudrate : int
            baudrate of the connexion

    Return
    ------
        init serial
        False
    """

    try:
        serial = ser.Serial(port, baudrate)

        print("Serial Init Success")
        serial.timeout = 0.5

        return serial
    except Exception as e:
        print("\033[91mError serial init: \033[0m", e)
        return False

def close_serial(serial):  
    """ 
    Function to close UART port. 
    
    Parameters
    ----------
        serial : ? 
            Initialized serial

    Return
    ------
        True
        False
    """ 
   
    try:
        serial.close()
        print("Serial Close Success")
        time.sleep(1)
        return True
    except Exception as e:
        print("\033[91mError serial close: \033[0m", e)
        return False

def accept_rcv(serial):
    """ 
    Function to verify a receive message.
    
    Accepted message : X:X:X:X:X (X can be anything)

    Parameters
    ----------
        serial : ? 
            Initialized serial

    Return
    ------ 
        Splited message
        None
    """

    try:
        frame_split = read_serial(serial).split(":")
        frame_split[-1] = re.sub(r'\r\n', '', frame_split[-1])

        if len(frame_split)  != 5:
            return None
        else:
            return frame_split
    except Exception as e:
        print("\033[91mError split rcv: \033[0m", e)
        return None

def accept_rcv_pami(serial):
    """ 
    Function to verify a receive message.
    
    Accepted message : X:X:X:X:X (X can be anything)

    Parameters
    ----------
        serial : ? 
            Initialized serial

    Return
    ------ 
        Splited message
        None
    """

    try:
        frame = read_serial(serial)
        frame_split = frame[:17] + frame[20:].split(":")
        frame_split[-1] = re.sub(r'\r\n', '', frame_split[-1])

        if len(frame_split)  != 5:
            return None
        else:
            return frame_split
    except Exception as e:
        print("\033[91mError split rcv: \033[0m", e)
        return None
    
def read_serial(serial):
    """ 
    Function to read a line of a serial UART.
    Read until '\\n'.

    Parameters
    ----------
        serial : ?
            Initialized serial
        
    Return
    ------ 
        Line message
        None   
    """

    try:
        frame = serial.readline().decode('utf-8')
        return frame[:len(frame)-1]
    
    except Exception as e:
        print("\033[91mError read data: \033[0m", e)
        return None

def send_read_command(serial, num_motor, command):
    """ 
    Function to send read command to serial UART.
    It uses utf-8 encoding

    Command read protocol : MOTOR:R:COMMAND (refer to the protocol description)

    Parameters
    ----------
        serial (?) : Initialized serial
        num_motor (int) : target motor
        command (str) : target command

    Return
    ------
        True OR False
    """

    frame = str(num_motor) + ":R:" + command + "\n"
    print("Frame send : ", frame)
    frame_byte = frame.encode('utf-8')
    try :
        serial.write(frame_byte)
        return True
    except Exception as e:
        print("\033[91mError sending read command : \033[0m", e)
        return False

def send_write_command(serial, num_motor, command, value):
    """ 
    Function to send write command to serial UART.
    It uses utf-8 encoding

    Command write protocol : MOTOR:W:COMMAND\\n (refer to the protocol description)

    Parameters
    ----------
        serial : ?
            Initialized serial
        num_motor : int 
            target motor
        command : str 
            target command
        value : int 
            value set

    Return
    ------ 
        True
        False
    """

    frame = str(num_motor) + ":W:" + command + ":" + str(value) + "\n"
    frame_byte = frame.encode('utf-8')

    try :
        serial.write(frame_byte)
        return True
    except Exception as e:
        print("\033[91mError sending write command : \033[0m", e)
        return False

def rcv_read_command(serial, num_motor, command_send):
    """ 
    Function to receive result of read command of serial UART.
    
    Command receive read protocol : MOTOR:R:COMMAND:VALUE:OK (refer to the protocol description)
        
    Parameters
    ----------
        serial : ?
            Initialized serial
        num_motor : int
            target motor
        command_send : ?
            target command

    Return
    ------
        value
        np.nan
    """
    
    frame = accept_rcv(serial)
    print("Frame rcv : ",frame)
    if frame == None or frame[0] != str(num_motor) or frame[1] != "R" or frame[2] != command_send or frame[4] != "OK":
        return np.nan
    
    return float(frame[3])

def rcv_read_command_pami(serial, num_motor, command_send):
    """ 
    Function to receive result of read command of serial UART.
    
    Command receive read protocol : MOTOR:R:COMMAND:VALUE:OK (refer to the protocol description)
        
    Parameters
    ----------
        serial : ?
            Initialized serial
        num_motor : int
            target motor
        command_send : ?
            target command

    Return
    ------
        value
        np.nan
    """
    
    frame = accept_rcv(serial)
    if frame == None or frame[0] != str(num_motor) or frame[1] != "R" or frame[2] != command_send or frame[4] != "OK":
        return np.nan
    
    return float(frame[3])

def rcv_write_command(serial, num_motor, command_send, value): 
    """ 
    Function to receive result of write command of serial UART
    
    Command receive read protocol : MOTOR:R:VALUE:COMMAND:OK (refer to the protocol description)

    Parameters
    ----------
        serial : ?
            Initialized serial
        num_motor : int
            target motor
        command_send : ? 
            target command
        value : ?
            value set 

    Return
    ------
        True
        False
    """

    frame = accept_rcv(serial)

    if frame == None or frame[0] != str(num_motor) or frame[1] != "W" or frame[3] != str(value) or frame[2] != command_send or frame[4] != "OK":
        return False
    
    return True

def rcv_write_command_pami(serial, num_motor, command_send, value): 
    """ 
    Function to receive result of write command of serial UART
    
    Command receive read protocol : MOTOR:R:VALUE:COMMAND:OK (refer to the protocol description)

    Parameters
    ----------
        serial : ?
            Initialized serial
        num_motor : int
            target motor
        command_send : ? 
            target command
        value : ?
            value set 

    Return
    ------
        True
        False
    """

    frame = accept_rcv(serial)

    if frame == None or frame[0] != str(num_motor) or frame[1] != "W" or frame[3] != str(value) or frame[2] != command_send or frame[4] != "OK":
        return False
    
    return True