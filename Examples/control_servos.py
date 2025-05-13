import sys
import board
import busio
from adafruit_pca9685 import PCA9685
from adafruit_motor import servo

# Initialisation
i2c = busio.I2C(board.SCL, board.SDA)
pca = PCA9685(i2c)
pca.frequency = 50

# Initialisation des servos
servos = [servo.Servo(pca.channels[i]) for i in range(16)]

# Lire les arguments en ligne de commande
if len(sys.argv) == 3:
    servo_id = int(sys.argv[1])
    angle = int(sys.argv[2])
    if 0 <= servo_id < 16 and 0 <= angle <= 180:
        servos[servo_id].angle = angle
        print(f"Servo {servo_id} réglé à {angle}°")
    else:
        print("Valeurs hors limites")
else:
    print("Utilisation : python3 control_servos.py <servo_id> <angle>")

pca.deinit()
