import RPi.GPIO as GPIO
import time
import sys
from datetime import datetime

# Configuration de la numérotation BCM
GPIO.setmode(GPIO.BCM)

# Configuration de la broche 17 en entrée avec résistance pull-up
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)

print("\n" * 2)  # Réserve deux lignes au début

try:
    while True:
        state = GPIO.input(17)
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Déplace le curseur 2 lignes vers le haut
        sys.stdout.write("\033[F")  # Ligne de l'état GPIO
        sys.stdout.write("\033[F")  # Ligne du timestamp

        # Affiche le timestamp
        sys.stdout.write(f"{now}\n")

        # Affiche l'état GPIO
        sys.stdout.write(f"État GPIO17 : {'HAUT (1)' if state else 'BAS (0)'}   \n")

        sys.stdout.flush()
        time.sleep(0.1)

except KeyboardInterrupt:
    print("\nArrêt du script.")
finally:
    GPIO.cleanup()
