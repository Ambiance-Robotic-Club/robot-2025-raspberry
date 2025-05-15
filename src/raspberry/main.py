from com.init_serial import init_coms_robot
from com.tirette import wait_tirette
from strategy.obstacle import find_safe_place
from strategy.blue import blue_strat

import threading

if __name__ == "__main__":
    wait_tirette()

    servos, robot, lidar = init_coms_robot()

    t_lidar = threading.Thread(target=lidar.read_lidar_data)
    t_lidar.start()

    try:
        while(True):
            if lidar.f_stop:
                find_safe_place(robot)
            else:
                blue_strat(robot, servos)

    except KeyboardInterrupt:
        print("Stop")
    except Exception as e:
        print(f"Error : {e}")

    t_lidar.join()


