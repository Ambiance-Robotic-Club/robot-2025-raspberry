from com.init_serial import init_coms_robot
from com.tirette import wait_tirette
from strategy.obstacle import find_safe_place
from strategy.blue import Strategy

import threading
import time

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))


if __name__ == "__main__":
    wait_tirette()

    sts3215, robot, lidar, servos= init_coms_robot()

    t_lidar = threading.Thread(target=lidar.read_lidar_data)
    t_lidar.start()

    strategy = Strategy(robot, sts3215)

    try:
        while(True):
            if lidar.f_stop:
                find_safe_place(robot)
            else:
                strategy.update_robot()
            
            time.sleep(0.01)

    except KeyboardInterrupt:
        print("Stop")
    except Exception as e:
        print(f"Error : {e}")

    t_lidar.join()


