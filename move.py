import threading
import time
import serial

class Move(object):
    def __init__(self):
        self.ser = serial.Serial(port = '/dev/ttyUSB0', baudrate=9600)
        # port = "/dev/ttyUSB2",

    def runRight(self):
        try:
            self.ser.write('')
            self.ser.close()
        except:
            print 'serial is not open'
        # print 'turn right'
        time.sleep(0.25)

    def runLeft(self):
        try:
            self.ser.write('')
            self.ser.close()
        except:
            print 'serial is not open'
        # print 'turn left'
        time.sleep(0.25)

    def runStop(self):
        try:
            self.ser.write('')
            self.ser.close()
        except:
            print 'serial is not open'
        # print 'turn stop'



