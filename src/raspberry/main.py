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
    sts3215, robot, lidar, servos= init_coms_robot()

    wait_tirette()


    t_lidar = threading.Thread(target=lidar.read_lidar_data)
    t_lidar.start()

    strategy = Strategy(robot, sts3215)

    couleur = None
    timerStart = time.time()

    try:
        while(True):
            if not lidar.is_free and lidar.f_stop:
                find_safe_place(robot)
            elif lidar.is_free and lidar.f_stop:

                strategy.consigne_queue.insert(0,strategy.step_consigne)
                strategy.actual_type_consigne = 0
                strategy.robot_busy = False
                strategy.process_step()
                lidar.f_stop = False
            else:
                strategy.update_robot()
            
            timer = time.time() - timerStart

            lidar.robot_position = [strategy.actual_x, strategy.actual_y, strategy.actual_theta]
            try:
                print("__________________________________________")
                print(f"Robot datas")
                print("Couleur : ", couleur)
                print("Timer : ", timer)
                print("Position robot : x :", strategy.actual_x, "| y :", strategy.actual_y, "| θ :", strategy.actual_theta - int(strategy.actual_theta/360)*360)
                print("Consigne robot : x :", strategy.step_consigne[0], "| y :", strategy.step_consigne[1], "| θ :", strategy.step_consigne[2])
                print("Obstacle : ", "Oui" if not lidar.is_free else "Non", "| Bloqué : ", "Oui" if lidar.f_stop else "Non")
                print("Busy : ", "Oui" if strategy.robot_busy else "Non")
                print("Consigne actuelle (position / rotation) :", strategy.consigne)
                print("__________________________________________")
            except Exception as e:
                print(f"Error : {e}")

            time.sleep(0.01)

    except KeyboardInterrupt:
        print("Stop")
        t_lidar.join()

    except Exception as e:
        print(f"Error : {e}")

    t_lidar.join()
    lidar.serial.close()
    robot.serial.close()
    sts3215[0].port_handler.closePort()
    

