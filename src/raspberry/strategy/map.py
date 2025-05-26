from utils.constant import pos_objects, pos_zone

class Map:
    def __init__(self, color):
        

        self.color = color

        self.our_zones = [pos_zone[i] for i in [0, 2, 4, 7, 8]] if self.color == "Yellow" else [pos_zone[i] for i in [1, 3, 5, 6, 9]]
        self.adv_zones = [pos_zone[i] for i in [1, 3, 5, 6, 9]] if self.color == "Yellow" else [pos_zone[i] for i in [0, 2, 4, 7, 8]]

        self.objects = [pos_objects[i] for i in [0, 1, 2, 3, 4, 6, 7, 8, 9]] if self.color == "Yellow" else [pos_zone[i] for i in [1, 2, 3, 4, 5, 6, 7, 8, 9]]

        self.objects = [[825,275,-90]]
        self.zone_end = pos_zone[3] if self.color == "Yellow" else pos_zone[0]
    #TO DO
    def moove_object_to_areas(self, area, object):
        pass