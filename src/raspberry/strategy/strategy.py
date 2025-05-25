import math
import time
import utils.constant as constant
import numpy as np
from utils.utils import modulo, get_distance, min_distance
class Strategy:
    def __init__(self, robot, servos, map):

        self.init = True
        self.robot = robot
        self.servos = servos
        self.map = map

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

            #### Path correction ####
            if self.actual_type_consigne == 2:
                line = get_distance(self.actual_x, self.actual_y, self.line_start_x , self.line_start_y)
                self.error_line += math.sin(math.radians(self.theoric_theta - self.actual_theta))*line

                self.line_start_x = self.actual_x
                self.line_start_y = self.actual_y
                self.theoric_theta = self.actual_theta + self.theta_degrees
            else:
                self.error_line = 0
            #########################
            
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
        
            # if abs(self.error_line) > constant.DISTANCE_ERROR_CORRECTION:
            #     self.consigne_queue.insert(0,self.step_consigne)                
            #     self.robot.send_position_consigne(50)
            #     self.actual_type_consigne = 0
            #     self.update_robot()
            #     print("------- Recalcul consigne -------")
    
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
            # alignment_theta = modulo((self.step_consigne[2] - self.theta_degrees), 360)
            # if abs(alignment_theta) > 90:
            #     if abs(self.theta_degrees) < 10:
            #         pass
            #     elif self.theta_degrees <= 0:
            #         self.theta_degrees += 180
            #         self.direction = constant.BACKWARD
            #     else:
            #         self.theta_degrees -= 180
            #         self.direction = constant.BACKWARD
            # else:
            #     self.direction = constant.FORWARD

            if abs(self.theta_degrees) > constant.CONSIGNE_MIN_THETA:
                self.consigne = self.theta_degrees
                self.is_consigne = True

                #### Path correction ####
                self.line_start_x = self.actual_x
                self.line_start_y = self.actual_y
                self.theoric_theta = self.actual_theta + self.theta_degrees
                self.error_line = 0
                #########################
            else:
                self.actual_type_consigne = 1

        if self.actual_type_consigne == 1:
            distance = get_distance(self.actual_x, self.actual_y, self.step_consigne[0], self.step_consigne[1])
            if self.direction == constant.BACKWARD:
                distance = - distance
            if abs(distance) > constant.CONSIGNE_MIN_POS:
                self.consigne = distance
                self.is_consigne = True
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

    
    def process_queue(self):
        if self.consigne_queue == []:


            distance, num_object = min_distance(self.actual_x, self.actual_y, self.map.objects)

            print("Debug distance plus court objet :  ", distance)
            pos_object = self.map.objects[num_object]
            if pos_object[2] == 0:
                positions = [[pos_object[0]-constant.DISTANCE_OBJECT, pos_object[1], 0],[pos_object[0]+constant.DISTANCE_OBJECT, pos_object[1], 180]]
            else:
                positions = [[pos_object[0], pos_object[1]-constant.DISTANCE_OBJECT, 90],[pos_object[0], pos_object[1]+constant.DISTANCE_OBJECT, -90]]
            
            for pos in positions:
                if pos[1] < 200:
                    positions.remove(pos)
            
            _, index = min_distance(self.actual_x, self.actual_y, positions)
            
            pos_consigne_1 = positions[index]

            self.consigne_queue.append(pos_consigne_1)

            if pos_consigne_1[2] == 0:
                pos_consigne_2 = [pos_consigne_1[0]+constant.DISTANCE_QUALIB_OBJECT, pos_consigne_1[1], pos_consigne_1[2]]
            elif pos_consigne_1[2] == 180:
                pos_consigne_2 = [pos_consigne_1[0]-constant.DISTANCE_QUALIB_OBJECT, pos_consigne_1[1], pos_consigne_1[2]]
            elif pos_consigne_1[2] == 90:
                pos_consigne_2 = [pos_consigne_1[0], pos_consigne_1[1]+constant.DISTANCE_QUALIB_OBJECT, pos_consigne_1[2]]
            elif pos_consigne_1[2] == -90:
                pos_consigne_2 = [pos_consigne_1[0], pos_consigne_1[1]-constant.DISTANCE_QUALIB_OBJECT, pos_consigne_1[2]]

            self.consigne_queue.append(pos_consigne_2)
                        
            if pos_consigne_1[2] == 0:
                pos_consigne_3 = [pos_consigne_2[0]+constant.DISTANCE_FINAL_OBJECT, pos_consigne_2[1], pos_consigne_2[2]]
            elif pos_consigne_1[2] == 180:
                pos_consigne_3 = [pos_consigne_2[0]-constant.DISTANCE_FINAL_OBJECT, pos_consigne_2[1], pos_consigne_2[2]]
            elif pos_consigne_1[2] == 90:
                pos_consigne_3 = [pos_consigne_2[0], pos_consigne_2[1]+constant.DISTANCE_FINAL_OBJECT, pos_consigne_2[2]]
            elif pos_consigne_1[2] == -90:
                pos_consigne_3 = [pos_consigne_2[0], pos_consigne_2[1]-constant.DISTANCE_FINAL_OBJECT, pos_consigne_2[2]]

            self.consigne_queue.append(pos_consigne_3)
                        


