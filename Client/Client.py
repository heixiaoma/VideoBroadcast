import sys
import socket
import struct
import cv2
import numpy as np

def initSocket(multicastGroupIP, multicastGroupPORT): # Create socket

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP) # socket udp

    sock.setsockopt(socket.SOL_SOCKET,  socket.SO_REUSEPORT, 1)

    sock.bind(('', multicastGroupPORT))  # use multicastGroupIP instead of '' to listen only
                             # to multicastGroupIP, not all groups on multicastGroupPORT

    mreq = struct.pack("4sl", socket.inet_aton(multicastGroupIP), socket.INADDR_ANY)

    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)


    return sock

def reciveMessages(sock): # keep reciving messages

    while True:
        data, (addrIP, addrPort) = sock.recvfrom(90456) # msg with 90456 bytes

        img = messageToImg(data) # convert to img

        cv2.imshow('Live', img) # show img

        if cv2.waitKey(1) & 0xFF == ord('q'): # break case
            break



def messageToImg(imgStr): # convert recved bytes to img

    nparr = np.fromstring(imgStr, np.uint8)

    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR) # decode

    return img

if __name__ == "__main__":

    sock = initSocket("224.0.0.1", 5999)

    reciveMessages(sock)

    sock.close()

    exit(0)
