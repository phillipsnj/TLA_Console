import threading
import serial
import time


class soloUART(threading.Thread):
    def __init__(self, port, myFunction, outfunction):
        threading.Thread.__init__(self)
        self.function = myFunction
        self.outfunction = outfunction
        self.vars = []
        self.ser = serial.Serial(port, 9600)
        #self.ser.write(str.encode("TYP\n"))
        #self.ser.write("TYP\n")

    def processData(self, info):
        print(info)

    def run(self):
        count = 0
        buffer = ''
        char=''
        while True:
            if (self.ser.in_waiting):
                data = self.ser.readline().decode()[:-1]
                # info = data.split('=')
                self.function(data)
                print("Data : "+data)
            time.sleep(.001)
            count +=1
            # print(self.ser.inWaiting())

    def send(self, data):
        print("Send : "+data)
        self.outfunction(data)
        data = data
        for i in data:
            self.ser.write(str.encode(str(i)))
            time.sleep(0.0005)
        #self.ser.write(str.encode(data+"\r\n"))