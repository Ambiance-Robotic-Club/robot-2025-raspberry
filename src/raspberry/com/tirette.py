import RPi.GPIO as GPIO
import time

servo_positions_init = [
    [30, 120, 55, 180, 155, 0, 0, 0, 0, 0,  0, 30, 0, 140, 55, 125, 0],  
    [30, 120, 55, 90, 155, 0, 0, 0, 0, 0, 0, 30, 90, 140, 55, 125, 0]]

def wait_tirette(pin, screen, servos, sts3215):

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    print("\n")   
    while(not GPIO.input(pin)):
        if screen.get_init_act() == 1:
            for servo_id in range(16):
                servos[servo_id].angle = servo_positions_init[0][servo_id]
            time.sleep(0.5)
    
            for servo_id in range(16):
                servos[servo_id].angle = servo_positions_init[1][servo_id]

            sts3215[0].homing()
            sts3215[1].homing()

            # Set position départ
            sts3215[0].set_position_calib(0)
            sts3215[1].set_position_calib(0)

    return 1