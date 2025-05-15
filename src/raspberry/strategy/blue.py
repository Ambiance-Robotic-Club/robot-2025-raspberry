import math
import utils.constant as constant

def blue_strat(robot, servos):
    pass

"""
def process_step(self):
        s = self.main_class_instance

        step_consigne = s.consigne_queue[0]

        if s.actual_type_consigne == 0:

            theta_radians = math.atan2(step_consigne[1] - s.actual_y, step_consigne[0] - s.actual_x)
            theta_degrees = (math.degrees(theta_radians) - s.actual_theta) % 360
            if theta_degrees > 180:
                theta_degrees -= 360

            if theta_degrees > constant.CONSIGNE_MIN_THETA or theta_degrees < -constant.CONSIGNE_MIN_THETA:
                s.consigne = theta_degrees
                s.is_consigne = True
            else:
                s.actual_type_consigne = 1

        if s.actual_type_consigne == 1:
            distance = math.sqrt((s.actual_x - step_consigne[0]) ** 2 + (s.actual_y - step_consigne[1]) ** 2)

            if distance > constant.CONSIGNE_MIN_POS:
                s.consigne = distance
                s.is_consigne = True
            else:
                s.actual_type_consigne = 2

        if s.actual_type_consigne == 2:
            s.consigne_queue = s.consigne_queue[1:]

            alignment_theta = (s.actual_theta - theta_degrees - step_consigne[2]) % 360
            if alignment_theta > 180:
                alignment_theta -= 360

            if alignment_theta > constant.CONSIGNE_MIN_THETA or alignment_theta < -constant.CONSIGNE_MIN_THETA:
                s.consigne = alignment_theta
                s.is_consigne = True
            else:
                s.actual_type_consigne = 0


"""