#!/usr/bin/env python

import socket
import select
from collections import deque
from imutils.video import VideoStream
import numpy as np
import argparse
import cv2
import imutils
import time
import RPi.GPIO as GPIO

class SocketServer:
    
    coil_A_1_pin = 4 # pink
    coil_A_2_pin = 17 # orange
    coil_B_1_pin = 23 # blue
    coil_B_2_pin = 24 # yellow
    
            
    def initializeGPIO(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        #GPIO.setup(enable_pin, GPIO.OUT)
        GPIO.setup(self.coil_A_1_pin, GPIO.OUT)
        GPIO.setup(self.coil_A_2_pin, GPIO.OUT)
        GPIO.setup(self.coil_B_1_pin, GPIO.OUT)
        GPIO.setup(self.coil_B_2_pin, GPIO.OUT)

    def setGPIO(self, w1, w2, w3, w4, holdTime):
        GPIO.output(self.coil_A_1_pin, w1)
        GPIO.output(self.coil_A_2_pin, w2)
        GPIO.output(self.coil_B_1_pin, w3)
        GPIO.output(self.coil_B_2_pin, w4)
        time.sleep(holdTime)
        
    def moveRight(self, time):
        print('Moving Right')
        self.setGPIO(0,0,0,1,time)
        #setGPIO(0,0,0,0,1)
        
    def moveLeft(self, time):
        print('Moving Left')
        self.setGPIO(0,0,1,0,time)
        #setGPIO(0,0,0,0,1)
        
    def moveForward(self, time):
        print('Moving Forward')
        self.setGPIO(0,0,1,1,time)
    
    
    def __init__(self, host = '0.0.0.0', port = 2010):
        self.initializeGPIO()
        
        """ Initialize the server with a host and port to listen to. """
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.host = host
        self.port = port
        self.sock.bind((host, port))
        self.sock.listen(1)

    def close(self):
        """ Close the server socket. """
        print('Closing server socket (host {}, port {})'.format(self.host, self.port))
        if self.sock:
            self.sock.close()
            self.sock = None
    
    def open(self):
        return self.sock.accept()

    def run_server(self):
        """ Accept and handle an incoming connection. """
        print('Starting socket server (host {}, port {})'.format(self.host, self.port))

        client_sock, client_addr = self.sock.accept()

        print('Client {} connected'.format(client_addr))

        stop = False
        while not stop:
            if client_sock:
                # Check if the client is still connected and if data is available:
                try:
                    rdy_read, rdy_write, sock_err = select.select([client_sock,], [], [])
                except select.error:
                    print('Select() failed on socket with {}'.format(client_addr))
                    return 1

                if len(rdy_read) > 0:
                    read_data = client_sock.recv(255)
                    # Check if socket has been closed
                    if len(read_data) == 0:
                        print('{} closed the socket.'.format(client_addr))
                        stop = False # True
                        client_sock, client_addr = self.sock.accept()
                        print("New connection opened")
                    else:
                        print('>>> Received: {}'.format(read_data.rstrip()))
                        if read_data.rstrip() == 'quit':
                            stop = False #True
                        else:
                            if read_data == 'right':
                                self.moveRight(0.5)
                            elif read_data == 'left':
                                self.moveLeft(0.5)
                            elif read_data == 'forward':
                                self.moveForward(0.5)
                            self.setGPIO(0,0,0,0,.01)
                            client_sock.send(read_data)
            else:
                print("No client is connected, SocketServer can't receive data")
                #stop = True
                time.delay(1)
                client_sock, client_addr = self.sock.accept()
                print("New connection opened")

        # Close socket
        print('Closing connection with {}'.format(client_addr))
        client_sock.close()
        return 0

def main():
    server = SocketServer()
    server.run_server()
    print 'Exiting'

if __name__ == "__main__":
    main()
