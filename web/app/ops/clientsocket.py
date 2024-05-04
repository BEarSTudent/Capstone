import socket
import sys
import cv2
import time
import datetime
import numpy as np
import base64
from dataclasses import dataclass
import json
# import threading

@dataclass(
    frozen=False
)

@dataclass
class User:
    input_type:int
    transfer_type:int
    target_image_path:str
    source_image_path:str

class clientsocket:
    def __init__(self, ip, port, user:User):
        self.__IP = ip
        self.__PORT = port
        self.connectCount = 0
        self.__user = user
        
    def connectServer(self):
        try:
            self.sock = socket.socket()
            self.sock.connect((self.__IP, self.__PORT))
            print(u'Client socket is connected with Server socket [ TCP_SERVER_IP: ' + self.__IP + ', TCP_SERVER_PORT: ' + str(self.__PORT) + ' ]')
            self.connectCount = 0
            self.sendImages()
            transfer_img = self.recvImage()
            return transfer_img
        except Exception as e:
            print(e)
            self.connectCount += 1
            if self.connectCount == 10:
                print(u'Connect fail %d times. exit program'%(self.connectCount))
                sys.exit()
            print(u'%d times try to connect with server'%(self.connectCount))
            self.connectServer()
            
    def sendImages(self):
        try:
            source_data_len = None
            if self.__user.transfer_type is not 1:
                source_image = cv2.imread(self.__user.source_image_path)
                source_data = np.array(source_image)
                string_source_data = base64.b64encode(source_data)
                source_data_len = str(len(string_source_data))
                
            target_image = cv2.imread(self.__user.target_image_path)
            target_data = np.array(target_image)
            string_target_data = base64.b64encode(target_data)
            target_data_len = str(len(string_target_data))
            
            user_json = json.dumps(vars(self.__user))
            user_json_len = str(len(user_json))
        except Exception as e:
            pass
        
        try:
            self.sock.sendall(user_json_len.encode('utf-8').ljust(64))
            self.sock.send(user_json.encode('utf-8'))
            
            self.sock.sendall(target_data_len.encode('utf-8').ljust(64))
            self.sock.send(string_target_data)
            
            if source_data_len is not None:
                self.sock.sendall(source_data_len.encode('utf-8').ljust(64))
                self.sock.send(string_source_data)
            print("Complete send image")
            
        except Exception as e:
            print(e)
            self.sock.close()
            time.sleep(1)
            self.connectServer()
            self.sendImages()
            
    def recvImage(self):
        try:
            length = self._recvall(self.sock, 64)
            length = int(length.decode('utf-8'))
            stringData = self._recvall(self.sock, length)
            data = np.frombuffer(base64.b64decode(stringData), np.uint8)
            transfer_img = cv2.imdecode(data, 1)
            self.sock.close()
            
            return transfer_img
        
        except Exception as e:
            pass
        
    def _recvall(self, sock, count):
        buf = b''
        while count:
            newbuf = sock.recv(count)
            if not newbuf: return None
            buf += newbuf
            count -= len(newbuf)
        return buf