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

    def send_msg_pami_score(self, address, msg):

        self.serial.write(address+";"+msg+"\n".encode('utf-8'))
        try:
            return self.serial.readline().decode('utf-8').strip()
        
        except Exception as e:
            return None
        
    def get_zone(self):

        self.serial.write("Z\n".encode('utf-8'))
        try:
            return self.serial.readline().decode('utf-8').strip()
        
        except Exception as e:
            return None
