# Gladius test server
# This file should be run when running PG module without eye-tracker device
# This makes it easier to test experiments.

import time
import socket
from enum import IntEnum
from struct import unpack, pack
import random

class GladiusServer():
    def __init__(self):        
        self.TCP_IP = '127.0.0.1'
        self.TCP_PORT = 12345
        self.BUFFER_SIZE = 1024
        self.sizeof_gp = 40 

        self.sendDummyData()

    def sendDummyData(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((self.TCP_IP, self.TCP_PORT))
        s.listen()
        conn, addr = s.accept()
        #self.conn.setblocking(0)
        dataToSend = pack('iiiiiiiiii', 4,4,0,0,0,0,0,0,0,0)
        conn.sendall(dataToSend)
        time.sleep(.0001)
        print('Waiting for command from client')
        data = conn.recv(1024)
        print('data rcv,' , unpack('iiiiiiiiii',data))
        print('Sending data...')
        i = 0
        starttime=round(time.time() * 1000)
        while(1): # if disconnected, try to reconnect  
            # change boolean to int   
            dataToSend = pack('iiiiiiiiii', 6,0,0,0,int((round(time.time() * 1000)-starttime)%100000),0,random.randint(1,100), random.randint(1,100),1,0)
            conn.sendall(dataToSend)
            if i % 100 == 0:
                print('data sent, ', i)
            i = i + 1
            time.sleep(.0001)
            
        s.close()
        conn.close()

if __name__ == "__main__":
    gladServer = GladiusServer()
    
