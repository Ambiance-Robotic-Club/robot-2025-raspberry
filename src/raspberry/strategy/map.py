class Map:
    def __init__(self, color):
        
        self.blue_areas = []
        self.yellow_areas = []

        self.blue_objects = []
        self.yellow_objects = []


        self.color = color

    def get_objects(self):
        return self.yellow_objects if self.color == "Yellow" else self.blue_objects

    def get_areas(self):
        return self.yellow_areas if self.color == "Yellow" else self.blue_areas
    
    #TO DO
    def moove_object_to_areas(self, area, object):
        pass