import serial
import time

ser=serial.Serial("/dev/ttyACM0", 9600) #change ACM number later
ser.baudrate=9600


