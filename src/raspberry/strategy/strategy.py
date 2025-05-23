import math
import time
import utils.constant as constant
import numpy as np

def modulo(a, b):
    return a - int(a / b) * b

class Strategy:
    def __init__(self, robot, servos):

        self.init = True
        self.robot = robot
        self.servos = servos

        self.consigne_queue = [(200,0,90), (200,200,0), (0,500,0)]
        self.step_consigne = None
        self.actual_type_consigne = 0
        self.consigne = 0

        self.is_consigne = False
        self.actual_x = 0
        self.actual_y = 0
        self.actual_theta = 0

        self.error_line = None
        self.line_start_x = 0
        self.line_start_y = 0
        self.theoric_theta = 0
        self.theta_error = 0
        self.theta_degrees = 0
        self.direction = constant.IDLE

        self.old_actual_x = 0
        self.old_actual_y = 0
        self.old_actual_theta = 0
        self.timeout_busy = 0

        self.robot_busy = False
        self.old_robot_busy = False

    def update_robot(self):

        if self.robot.serial != None:
            self.actual_x = self.robot.get_actual_x()
            self.actual_y = self.robot.get_actual_y()
            self.actual_theta = self.robot.get_actual_theta()
            self.robot_busy = self.robot.get_busy(10) if not(self.init) else False

            line = math.sqrt((self.actual_x - self.line_start_x) ** 2 + (self.actual_y - self.line_start_y) ** 2)
            self.error_line = abs(math.sin(self.theoric_theta - self.actual_theta)*line)
            self.init = False
            
            # Timeout part
            if self.robot_busy != self.old_robot_busy:
                self.old_robot_busy = not self.old_robot_busy
                if self.robot_busy:
                    self.old_actual_x = self.actual_x
                    self.old_actual_y = self.actual_y
                    self.old_actual_theta = self.actual_theta
                    self.timeout_busy = time.time()

            if self.robot_busy and time.time()-self.timeout_busy >= 5 and self.actual_x < self.old_actual_x+10 and self.actual_x > self.old_actual_x-10 and self.actual_y < self.old_actual_y+10 and self.actual_y > self.old_actual_y-10 and self.actual_theta < self.old_actual_theta+5 and self.actual_theta > self.old_actual_theta-5:
                print("TIMEOUT : ROBOT BLOQUE")
                self.robot_busy = False  
             
            # Process part
            if not self.robot_busy and (len(self.consigne_queue) > 0 or self.actual_type_consigne != 0):
                self.process_step()
            
            # Send to robot part
            if not self.robot_busy and self.is_consigne:
                if self.actual_type_consigne == 1:
                    self.robot.send_position_consigne(self.consigne)
                    print("Consigne en position : ", self.consigne)

                else:
                    self.robot.send_rotation_consigne(self.consigne)
                    print("Consigne en rotation : ", self.consigne)
          
                self.actual_type_consigne = (self.actual_type_consigne + 1) % 3
                self.is_consigne = False
    
    def process_step(self):
        if self.actual_type_consigne == 0:
            self.step_consigne = self.consigne_queue[0]
            self.consigne_queue = self.consigne_queue[1:]

            theta_radians = math.atan2(self.step_consigne[1] - self.actual_y, self.step_consigne[0] - self.actual_x)
            if math.isnan(theta_radians):
                theta_radians = 0
            self.theta_degrees = modulo((math.degrees(theta_radians) - self.actual_theta), 360)

            if self.theta_degrees > 180:
                self.theta_degrees -= 360
            if self.theta_degrees < -180:
                self.theta_degrees += 360

            #Choice forward/backward
            alignment_theta = modulo((self.step_consigne[2] - self.theta_degrees), 360)
            if abs(alignment_theta) > 90:
                self.direction = constant.BACKWARD
                if self.theta_degrees <= 0:
                    self.theta_degrees += 180
                else:
                    self.theta_degrees -= 180
            else:
                self.direction = constant.FORWARD

            if abs(self.theta_degrees) > constant.CONSIGNE_MIN_THETA:
                self.consigne = self.theta_degrees
                self.is_consigne = True
            else:
                self.actual_type_consigne = 1

        if self.actual_type_consigne == 1:
            distance = math.sqrt((self.actual_x - self.step_consigne[0]) ** 2 + (self.actual_y - self.step_consigne[1]) ** 2)
            if self.direction == constant.BACKWARD:
                distance = - distance
            if abs(distance) > constant.CONSIGNE_MIN_POS:
                self.consigne = distance
                self.is_consigne = True

                self.line_start_x = self.actual_x
                self.line_start_y = self.actual_y
                self.theoric_theta = self.actual_theta + self.theta_degrees
            else:
                self.actual_type_consigne = 2

        if self.actual_type_consigne == 2:
            self.direction = constant.IDLE
            alignment_theta = modulo((self.step_consigne[2] - self.actual_theta), 360)
            if alignment_theta > 180:
                alignment_theta -= 360
            if alignment_theta < -180:
                alignment_theta += 360

            if abs(alignment_theta) > constant.CONSIGNE_MIN_THETA:
                self.consigne = alignment_theta
                self.is_consigne = True
            else:
                self.actual_type_consigne = 0

            

    def path_correction(self):
        if self.actual_type_consigne == 1:
            try:
                print("OK")
             
                ref_point = np.array([self.actual_x, self.actual_y])
                print("OK")
                dist = np.linalg.norm(self.theoric_line - ref_point, axis=1)
                closest_index = np.argmin(dist)

                self.theoric_actual_x = self.theoric_line[closest_index][0]
                self.theoric_actual_y = self.theoric_line[closest_index][1]
            except Exception as e:
                print("Erreur path correction : ", e)


        else:
            self.theoric_actual_x = None
            self.theoric_actual_y = None

