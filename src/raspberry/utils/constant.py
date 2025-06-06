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
SPEED_BUSY = 2

TIMEOUT = 3

DISTANCE_ERROR_CORRECTION = 100

#Distance objects
DISTANCE_OBJECT = 350
DISTANCE_QUALIB_OBJECT = 200
DISTANCE_FINAL_OBJECT = 50

DISTANCE_OBJECT_POUSSER = 250
#Distance zones
DISTANCE_ZONE = 225


#Lidar trig distance
DETECT_OBSTACLE = 3600
STOP_DISTANCE_DISABLE = 0
STOP_DISTANCE_FORWARD = 300 #450
STOP_DISTANCE_BACKWARD = 200 #450
STOP_DISTANCE_ROTATION_FRONT = 350 #450
STOP_DISTANCE_ROTATION_BACK = 200#450
STOP_DISTANCE_IDLE = 200#450

STOP_DISTANCE = 30
STOP_ANGLE = 3

TIME_RETURN_ZONE = 85
TIME_STOP = 97
TIME_PAMI_GO = 85
TIME_PAMI_STOP = 99

#Init Zone positions
pos_zone = [
            [375,225,90],
            [225,1125,0],
            [1225,1775,90],#1225
            [2625,225,90],
            [2775,1125,0],
            [1775,1775, 90],
            [225,1950,90],
            [775,1950,90],
            [2775,1950,90],
            [2225,1950,90],
            [1000,1000,-90]]

pos_objects = [
            [825,275,-90],
            [75,675,0],
            [1075,1050,-90],
            [75,1600,0],
            [775,1750,-90],
            [2175,275,-90],
            [2925,275,0],
            [1925,1050,-90],
            [2925,1600,0],
            [2225,1750,-90]]

SERVOS_INIT = [
    [10, 120, 55, 180, 155, 0, 0, 0, 0, 0,  0, 30, 0, 140, 55, 140],  
    [30, 120, 55, 90, 155, 0, 0, 0, 0, 0, 0, 30, 90, 140, 55, 125]]

SERVOS_GET_CAN = [[30, 120,  55,   90,   155,   0, 0, 0, 0, 0,  0,  30,  90, 140,   55,  125, 0],
                [5, 120,  25,   90,   155,   0, 0, 0, 0, 0,  0,  30,  90, 170,   55,  150, 0]]   

DEPOSE_CAN = [ 
    [10, 120,  55,   90,   155,   0, 0, 0, 0, 0,  0,  30,  90, 140,   55,  145, 0],
    [10, 120,  55,    90,    37,   0, 0, 0, 0, 0,  0, 155, 90, 140,   55,  145, 0.5],
    [10, 120,  55,    0,    37,   0, 0, 0, 0, 0,  0, 155, 180, 140,   55,  145, 0.5],  
    [10, 120,  55,  180,    37,   0, 0, 0, 0, 0,  0, 155,   0, 140,   55,  145, 0.5],
    [10, 120,  55,   90,   155,   0, 0, 0, 0, 0,  0,  30,  90, 140,   55,  145, 0],
    [14000, 14000],
    [150], 
    [10, 120,  30,   90,   155,   0, 0, 0, 0, 0,  0,  30,  90, 165,   55,  145, 0],
    [11000, 11000],  
    [10,  55,  30,   90,   155,   0, 0, 0, 0, 0,  0,  30,  90, 165,  120,  145, 0.5],
    [30,  55,  55,   90,   155,   0, 0, 0, 0, 0,  0,  30,  90, 140,  120,  125, 0], 
    [-100],
    [30, 120,  55,   90,   155,   0, 0, 0, 0, 0,  0,  30,  90, 140,   55,  125, 0],
    [0, 0]]

DEPOSE_ONE_STAGE = [
    [30, 120,  55,   90,   155,   0, 0, 0, 0, 0,  0,  30,  90, 140,   55,  125, 0],
    [-100]
]
    

SERVOS_BANNIERE = [30, 170,  55,   90,   155,   0, 0, 0, 0, 0,  0,  30,  90, 140,   10,  125]


DISTANCE_CAN_1 = 150
DISTANCE_CAN_2 = 100


MAC_PAMI = ["F8:B3:B7:22:24:34", "F8:B3:B7:21:F1:6C","24:6F:28:10:5E:A4"]
