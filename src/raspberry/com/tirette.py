import RPi.GPIO as GPIO


def wait_tirette(pin=17):

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    print("\n")   
    while(not GPIO.input(pin)):
        pass

    return 1