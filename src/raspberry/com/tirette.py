import RPi.GPIO as GPIO
import time
import utils.constant as constant
from strategy.strategy import banniere 
from com.init_serial import init_coms_robot
def wait_tirette(pin):
    init = True
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    print("\n")
    print(GPIO.input(pin))
    while GPIO.input(pin) == 1:   
         
         pass
    
    sts3215, robot, lidar, servos, screen, pami, pca = init_coms_robot()

    while(not GPIO.input(pin)):
        if init and screen.get_init_act() == 1:
            """
            for servo_id in range(16):
                servos[servo_id].angle = constant.SERVOS_INIT[0][servo_id]
            time.sleep(1)
    
            for servo_id in range(16):
                servos[servo_id].angle = constant.SERVOS_INIT[1][servo_id]
            """
            sts3215[0].homing()
            sts3215[1].homing()

            # Set position départ
            sts3215[0].set_position_calib(15000)
            sts3215[1].set_position_calib(15000)

            while(sts3215[0].read_speed() > 10 or sts3215[1].read_speed() > 10):
                    pass
            init = False

            time.sleep(3)
            servos[0].angle = 0
            servos[15].angle = 160
        else:
            time.sleep(0.2)
    
    
    screen.serial.reset_output_buffer()
    screen.serial.reset_input_buffer()


    return sts3215, robot, lidar, servos, screen, pami, pca