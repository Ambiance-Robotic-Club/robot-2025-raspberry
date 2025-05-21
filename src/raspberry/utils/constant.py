"""
Project
-------
    ARC 2024-2025

Author
------
    PIROLA Damien - Halyre

Module
------
    Constant

Presentation
------------
    This module define all constants that are used in the entire project.
    We find default value, baudrate etc...

"""
ERROR = -1
SUCCES = 1
WARNING = 0

#Robot direction constants
IDLE = 0
FORWARD = 1
BACKWARD = 2
ROTATION_L = 3
ROTATION_R = 4

CONSIGNE_MIN_POS = 20.0
CONSIGNE_MIN_THETA = 5.0

BAUDRATE_DEFAULT = 115200

TIMEOUT = 3

#Lidar trig distance
DETECT_OBSTACLE = 3600
STOP_DISTANCE_DISABLE = 0
STOP_DISTANCE_FORWARD = 100
STOP_DISTANCE_BACKWARD = 100
STOP_DISTANCE_ROTATION_FRONT = 100
STOP_DISTANCE_ROTATION_BACK = 100
STOP_DISTANCE_IDLE = 100

#Init Zone positions
pos_zone = [
            [100,0,0],
            [0,100,0],
            [0,0,100],
            [100,100,0],
            [100,0,100],
            [0,100,100]]

