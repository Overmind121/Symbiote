import serial #RUN THIS TWICE WHEN RPI IS CONNECTE WITH ARDUINO
import time
ser = serial.Serial('/dev/ttyUSB0', 9600)
ser.baudrate=9600
ser.write("f")
time.sleep(5)
ser.write("s")
ser.close()
