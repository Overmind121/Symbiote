import cv2
import serial #RUN THIS TWICE WHEN RPI IS CONNECTED WITH ARDUINO
import time
import socket
ser = serial.Serial('/dev/ttyUSB0', 9600)
ser.baudrate=9600


s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.bind(('192.168.1.147', 5560)) #rpi port 5560
s.listen(5)
t = 0
on = True

clientsocket, address = s.accept()
print("Connection has been established")
clientsocket.send("Welcome to the server!")
try:
    while on:
        
        msg=clientsocket.recv(4096)
        if len(msg) > 0 and t == 5:
            print(msg)
            t = 0
        t +=1
        if msg == "left":
            ser.write("l")
            
        if msg == "right":
            ser.write("r")
            
        if msg == "center":
            ser.write("s")
        if msg == "":
            break
        else:
            msg = ""
        
      
        
    
finally:
    ser.write("s")


#ser = serial.Serial('/dev/ttyUSB0', 9600)
#ser.baudrate=9600
#ser.write("f")
#time.sleep(5)
#ser.write("s")
#ser.close()
