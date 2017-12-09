import sys
import socket
import struct
import time
import cv2
import subprocess

def initSocket(): # Create socket

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP) # socket udp

    ttl = struct.pack('b', 1) # time to alive, 1 = does not allow to go through the local network

    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl) # set to multicast

    return sock

def sendMessage(sock, msg, destIP, destPORT): # send msg (in bytes) to desired destination

    sock.sendto(msg, (destIP, destPORT))

def streamCamera(sock, multicastGroupIP, multicastGroupPORT): # get camera img and send

    cam = cv2.VideoCapture(0) # camera

    while(1):

        ret_val, img = cam.read() # get camera img

        img = cv2.resize(img, (0,0), fx=0.5, fy=0.5) # resize to fit UDP dgram

        imgData = cv2.imencode('.jpg', img)[1].tostring() # encode to bytes

        sendMessage(sock, imgData, multicastGroupIP, multicastGroupPORT)

if __name__ == "__main__":

    serverSocket = initSocket()

    (multicastGroupIP, multicastGroupPORT) = ("224.0.0.1", 5999)

    streamCamera(serverSocket, multicastGroupIP, multicastGroupPORT)

    serverSocket.close()

    exit(0)
