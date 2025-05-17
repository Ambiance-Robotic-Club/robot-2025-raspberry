import serial as ser

class Screen:
    def __init__(self, port):

        self.serial = ser.Serial(port, 115200, timeout=1)
    
    def get_color(self):

        self.serial.write("C\n".encode('utf-8'))
        try:
            return self.serial.readline().decode('utf-8').strip()
        
        except Exception as e:
            return None

    def get_current(self):

        self.serial.write("A\n".encode('utf-8'))
        try:
            return self.serial.readline().decode('utf-8').strip()
        
        except Exception as e:
            return None

    def get_battery(self):

        self.serial.write("V\n".encode('utf-8'))
        try:
            return self.serial.readline().decode('utf-8').strip()
        
        except Exception as e:
            return None

    def set_score(self, value):

        while self.get_score() != value:
            self.serial.write(f"{value:03}"+"\n".encode('utf-8'))

    def get_score(self):

        self.serial.write("S\n".encode('utf-8'))
        try:
            return self.serial.readline().decode('utf-8').strip()
        
        except Exception as e:
            return None

    def send_msg_pami(self, address, msg):
        self.serial.write(address+";"+msg+"\n".encode('utf-8'))


        
    def get_zone(self):

        self.serial.write("Z\n".encode('utf-8'))
        try:
            return self.serial.readline().decode('utf-8').strip()
        
        except Exception as e:
            return None

    def get_init_act(self):

        self.serial.write("I\n".encode('utf-8'))
        try:
            return self.serial.readline().decode('utf-8').strip()
        
        except Exception as e:
            return False
        
    def send_stop_pami(self, address):
        self.serial.write(address+";STOP\n".encode('utf-8'))

    def send_color_pami(self, address):
        self.serial.write(address+";"+self.get_color()+"\n".encode('utf-8'))

    def get_color_pami(self, address):
        self.serial.write(address+";C\n".encode('utf-8'))
        try:
            return self.serial.readline().decode('utf-8').strip()[18:]
        
        except Exception as e:
            return False

    def get_actual_pos_pami(self, address):
        self.serial.write(address+";P\n".encode('utf-8'))
        try:
            return self.serial.readline().decode('utf-8').strip()[18:].split(';')
        
        except Exception as e:
            return False

    def send_pos_pami(self, address, x, y, theta):
        self.serial.write(address+";P:"+x+";"+y+";"+theta+"\n".encode('utf-8'))