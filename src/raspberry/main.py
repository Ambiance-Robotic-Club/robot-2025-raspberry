from com.init_serial import init_coms_robot
from com.tirette import wait_tirette
from strategy.obstacle import find_safe_place
from strategy.strategy import Strategy
from strategy.map import Map
import utils.constant as constant
from utils.utils import modulo

import threading
import time

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))


if __name__ == "__main__":
    sts3215, robot, lidar, servos, screen, pami, pca = init_coms_robot()

    wait_tirette(17, screen, servos, sts3215)

    stop_lidar = threading.Event()
    t_lidar = threading.Thread(target=lidar.read_lidar_data, args=(stop_lidar,))
    t_lidar.start()

    zone_start = screen.get_zone()
    color = screen.get_color()

    map = Map(color)
    robot.init_zone_start(zone_start)

    timerStart = time.time()
    timer = 0
    
    zone_end = True
    pami_start = True
    pami_stop = True
    stop = True

    strategy = Strategy(robot, sts3215, servos, map)

    try:
        while(timer < 100):
            if not lidar.is_free and lidar.f_stop:
                find_safe_place(robot)
            elif lidar.is_free and lidar.f_stop:

                strategy.consigne_queue.insert(0,strategy.step_consigne)
                strategy.actual_type_consigne = 0
                strategy.robot_busy = False
                strategy.update_robot()
                lidar.f_stop = False
            else:
                strategy.update_robot()
 
            timer = time.time() - timerStart

            lidar.robot_position = [strategy.actual_x, strategy.actual_y, strategy.actual_theta]
            lidar.direction = robot.direction
            try:
                if robot.direction ==  constant.FORWARD:
                    direction = "FORWARD"
                elif robot.direction ==  constant.BACKWARD:
                    direction = "BACKWARD"
                elif robot.direction ==  constant.ROTATION_L:
                    direction = "ROTATION_L"
                elif robot.direction ==  constant.ROTATION_R:
                    direction = "ROTATION_R"
                else:
                    direction = "IDLE"

                print("__________________________________________")
                print(f"Robot datas")
                print("Zone de départ : ", zone_start, "| Couleur : ", color)
                print("Timer : ", timer)
                print("Position robot : x :", strategy.actual_x, "| y :", strategy.actual_y, "| θ :", modulo(strategy.actual_theta, 360))
                print("Position robot adverse : x :", lidar.robot_adv_positions[-1][0], "| y :", lidar.robot_adv_positions[-1][1])
                if strategy.step_consigne != None and len(strategy.step_consigne) == 3:
                    print("Consigne robot : x :", strategy.step_consigne[0], "| y :", strategy.step_consigne[1], "| θ :", strategy.step_consigne[2])
                else:
                    print("Taille step consigne :", len(strategy.step_consigne))
                print("Distance erreur :",strategy.error_line , " mm")
                print("\nObstacle : ", "Oui" if not lidar.is_free else "Non", "| Bloqué : ", "Oui" if lidar.f_stop else "Non")
                print("Busy : ", "Oui" if strategy.robot_busy else "Non", " | Direction : ", direction)
                print("Etape consigne : ", strategy.actual_type_consigne)
                print("Consigne actuelle (position / rotation) :", strategy.consigne)
                print("__________________________________________")
            except Exception as e:
                print(f"Error : {e}")

            if stop and timer >= constant.TIME_STOP:
                stop = False
                screen.set_score(999)
                # TO DO (1 ligne par pami avec adresse mac en argument)
                pami.send_stop_pami(0)
                robot.stop()
                
            if zone_end and timer >= constant.TIME_RETURN_ZONE:
                zone_end = False
                robot.stop()
                map.objects = []
                strategy.consigne_queue = []
                strategy.consigne_queue.insert(0,map.zone_end)
                strategy.actual_type_consigne = 0
                strategy.update_robot()

                
            screen.set_timer(int(timer))

            time.sleep(0.01)


    except Exception as e:
        print(e)
    finally:
        print("Stop")
        stop_lidar.set()
        t_lidar.join()
        lidar.serial.close()
        robot.send_reset()
        robot.serial.close()
        screen.serial.close()
        sts3215[0].port_handler.closePort()
        sts3215[1].port_handler.closePort()
        pca.deinit()  
