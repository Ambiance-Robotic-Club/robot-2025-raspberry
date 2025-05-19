import math
import time
import utils.constant as constant

def modulo(a, b):
    return a - int(a / b) * b

class Strategy:
    def __init__(self, robot, servos):

        self.robot = robot
        self.servos = servos

        self.consigne_queue = [(100,0,90), (100,200,0)]
        self.step_consigne = None
        self.actual_type_consigne = 0
        self.consigne = 0

        self.is_consigne = False
        self.actual_x = 0
        self.actual_y = 0
        self.actual_theta = 0

        self.theta_degrees = 0

        self.old_actual_x = 0
        self.old_actual_y = 0
        self.timeout_busy = 0

        self.robot_busy = False
        self.old_robot_busy = False

    def update_robot(self):

        if self.robot.serial != None:
            self.actual_x = self.robot.get_actual_x()
            self.actual_y = self.robot.get_actual_y()
            self.actual_theta = self.robot.get_actual_theta()
            self.robot_busy = self.robot.get_busy(10) if self.actual_theta != 0 or self.actual_x != 0 or self.actual_y != 0 else False
            
            # Timeout part
            if self.robot_busy != self.old_robot_busy:
                self.old_robot_busy = not self.old_robot_busy
                if self.robot_busy:
                    self.old_actual_x = self.actual_x
                    self.old_actual_y = self.actual_y
                    self.timeout_busy = time.time()

            if self.robot_busy and time.time()-self.timeout_busy >= 5 and self.actual_x < self.old_actual_x+10 and self.actual_x > self.old_actual_x-10 and self.actual_y < self.old_actual_y+10 and self.actual_y > self.old_actual_y-10:
                print("TIMEOUT : ROBOT BLOQUE")
                self.robot_busy = False  
             
            # Process part
            if not self.robot_busy and len(self.consigne_queue) > 0:
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

            dx = self.step_consigne[0] - self.actual_x
            dy = self.step_consigne[1] - self.actual_y
            theta_target = math.degrees(math.atan2(dy, dx))

            # Marche avant
            forward_rot1 = modulo(theta_target - self.actual_theta, 360)
            if forward_rot1 > 180:
                forward_rot1 -= 360
            theta_after_forward = modulo(self.step_consigne[2] - theta_target, 360)
            if theta_after_forward > 180:
                theta_after_forward -= 360
            total_forward = abs(forward_rot1) + abs(theta_after_forward)

            # Marche arrière
            theta_backward_target = modulo(theta_target + 180, 360)
            backward_rot1 = modulo(theta_backward_target - self.actual_theta, 360)
            if backward_rot1 > 180:
                backward_rot1 -= 360
            theta_after_backward = modulo(self.step_consigne[2] - theta_backward_target, 360)
            if theta_after_backward > 180:
                theta_after_backward -= 360
            total_backward = abs(backward_rot1) + abs(theta_after_backward)

            # Choix optimal
            if total_forward <= total_backward:
                self.theta_degrees = forward_rot1
                self.forward = True
            else:
                self.theta_degrees = backward_rot1
                self.forward = False

            if abs(self.theta_degrees) > constant.CONSIGNE_MIN_THETA:
                self.consigne = self.theta_degrees
                self.is_consigne = True
            else:
                self.actual_type_consigne = 1

        if self.actual_type_consigne == 1:
            distance = math.sqrt((self.actual_x - self.step_consigne[0]) ** 2 +
                                (self.actual_y - self.step_consigne[1]) ** 2)

            if distance > constant.CONSIGNE_MIN_POS:
                self.consigne = distance if self.forward else -distance
                self.is_consigne = True
            else:
                self.actual_type_consigne = 2

        if self.actual_type_consigne == 2:
            alignment_theta = modulo(self.step_consigne[2] - self.actual_theta, 360)
            if alignment_theta > 180:
                alignment_theta -= 360
            if alignment_theta < -180:
                alignment_theta += 360

            if abs(alignment_theta) > constant.CONSIGNE_MIN_THETA:
                self.consigne = alignment_theta
                self.is_consigne = True
            else:
                self.actual_type_consigne = 0

