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
CONSIGNE_MIN_THETA = 2.0

BAUDRATE_DEFAULT = 115200

PERROR = 10
SPEED_BUSY = 4

TIMEOUT = 3

DISTANCE_ERROR_CORRECTION = 100

#Distance objects
DISTANCE_OBJECT = 200
DISTANCE_QUALIB_OBJECT = 100
DISTANCE_FINAL_OBJECT = 50

#Distance zones
DISTANCE_ZONE = 225


#Lidar trig distance
DETECT_OBSTACLE = 3600
STOP_DISTANCE_DISABLE = 0
STOP_DISTANCE_FORWARD = 100
STOP_DISTANCE_BACKWARD = 100
STOP_DISTANCE_ROTATION_FRONT = 100
STOP_DISTANCE_ROTATION_BACK = 100
STOP_DISTANCE_IDLE = 100

STOP_DISTANCE = 30
STOP_ANGLE = 3

TIME_RETURN_ZONE = 90
TIME_STOP = 97
TIME_PAMI_GO = 90
TIME_PAMI_STOP = 99
#Init Zone positions
pos_zone = [
            [375,225,90],
            [225,1125,0],
            [1225,1775,-90],
            [2625,225,90],
            [2775,1125,0],
            [1775,1775,-90],
            [225,1950,-90],
            [775,1950,-90],
            [2775,1950,-90],
            [2225,1950,-90]]

pos_objects = [
            [825,275,-90],
            [75,675,0],
            [1100,1050,-90],
            [75,1600,0],
            [775,1750,-90],
            [2175,275,-90],
            [2925,275,0],
            [1900,1050,-90],
            [2925,1600,0],
            [2225,1750,-90]]

SERVOS_GET_CAN = [[30, 120,  55,   90,   155,   0, 0, 0, 0, 0,  0,  30,  90, 140,   55,  125, 0],
                [10, 120,  30,   90,   155,   0, 0, 0, 0, 0,  0,  30,  90, 165,   55,  145, 0]]   

DEPOSE_CAN = [ 
    [10, 120,  55,   90,   155,   0, 0, 0, 0, 0,  0,  30,  90, 140,   55,  145, 0],
    [10, 120,  55,    90,    37,   0, 0, 0, 0, 0,  0, 155, 90, 140,   55,  145, 0.5],
    [10, 120,  55,    0,    37,   0, 0, 0, 0, 0,  0, 155, 180, 140,   55,  145, 0.5],  
    [10, 120,  55,  180,    37,   0, 0, 0, 0, 0,  0, 155,   0, 140,   55,  145, 0.5],
    [10, 120,  55,   90,   155,   0, 0, 0, 0, 0,  0,  30,  90, 140,   55,  145, 0],
    [14000, 14000, 3, 3],
    # POS ROBOT 150 
    [10, 120,  30,   90,   155,   0, 0, 0, 0, 0,  0,  30,  90, 165,   55,  145, 0],
    [13500, 13500, 3, 3],  
    [10,  55,  30,   90,   155,   0, 0, 0, 0, 0,  0,  30,  90, 165,  120,  145, 0.5],  
    [30,  55,  55,   90,   155,   0, 0, 0, 0, 0,  0,  30,  90, 140,  120,  125, 0], 
    [30,  55,  55,   90,   155,   0, 0, 0, 0, 0,  0,  30,  90, 140,  120,  125, 0], 
    [11000, 11000, 3, 3],
    [30, 120,  55,   90,   155,   0, 0, 0, 0, 0,  0,  30,  90, 140,   55,  125, 0]]
    #POS_ROBOT -100]

DISTANCE_CAN_1 = 150
DISTANCE_CAN_2 = 100