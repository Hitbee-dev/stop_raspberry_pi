"""
    Title.  packet/packetManager.py
    Autor.  K9714(github.com/k9714)
    Date.   21. 05. 17
    Desc.
        패킷 상수를 정의하고, 소켓 응답을 받는 부분입니다.
"""

import numpy as np
from packet.PacketHandle import *
from packet.Protocol import Decode, HEADER_SIZE
from client.ClientData import clientList


#{ PACKET_PART
USER_LOGIN      = 101
USER_REGISTER   = 102

KICKBOARD_REQ   = 103
KICKBOARD_RET   = 104
KICKBOARD_REGION= 105


PI_CONNECT      = 200
PI_CAPTURE      = 201

DIALOG          = 300


#} END PACKET_PART

# Broadcast
def broadcast(packet):
    for c in clientList:
        c.sendPacket(packet)

# Packet receiver
def recv(clientData):
    try:
        rbuff = clientData.socket.recv(65536)
        if not rbuff:
            return False
        # Check protocol
        clientData.buff += rbuff
        
        while len(clientData.buff) > 0:
            psize = int(str(clientData.buff[:HEADER_SIZE], encoding='utf-8'))
            if len(clientData.buff) >= psize + HEADER_SIZE:
                data = Decode(clientData.buff[HEADER_SIZE:psize + HEADER_SIZE])
                clientData.buff = clientData.buff[psize + HEADER_SIZE:]
                handler(clientData, data)
            else:
                break
    except Exception as e:
        print("[ERROR]", e)
        return False

    return True

def handler(clientData, data):
    print("\t[handler]", data)
    part = data["part"]
    if (part == USER_LOGIN):
        user_login(clientData, data)

    if (part == USER_REGISTER):
        user_register(clientData, data)

    if (part == PI_CAPTURE):
        pi_capture(clientData, data)

    if (part == KICKBOARD_REQ):
        kickboard_request(clientData, data)

    if (part == KICKBOARD_RET):
        kickboard_return(clientData, data)

    if (part == KICKBOARD_REGION):
        kickboard_region(clientData, data)

    if (part == PI_CONNECT):
        pi_connect(clientData, data)

