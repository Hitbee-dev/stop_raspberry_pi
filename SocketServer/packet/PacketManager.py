"""
    Title.  packet/packetManager.py
    Autor.  K9714(github.com/k9714)
    Date.   21. 05. 17
    Desc.
        패킷 상수를 정의하고, 소켓 응답을 받는 부분입니다.
"""
import packet
import share
import cv2
import numpy as np
import segmentation.predict
from packet.PacketCreator import PacketCreator
from packet.Protocol import Decode, HEADER_SIZE
from client.ClientData import ClientData, clientList

#{ PACKET_PART
DIALOG          = 3

KICKBOARD_CODE  = 100
USER_LOGIN      = 101
USER_REGISTER   = 102

PI_CAPTURE      = 200


#} END PACKET_PART

# Broadcast
def broadcast(packet):
    for c in clientList:
        c.sendPacket(packet)

# Packet receiver
def recv(clientData):
    rbuff = clientData.socket.recv(1024)
    if not rbuff:
        return False
    # Check protocol
    clientData.buff += rbuff
    while len(clientData.buff) > 0:
        psize = int(str(clientData.buff[:HEADER_SIZE], encoding='utf-8'))
        if len(clientData.buff) >= psize + HEADER_SIZE:
            data = Decode(clientData.buff[HEADER_SIZE:psize + HEADER_SIZE])
            clientData.buff = clientData.buff[psize + HEADER_SIZE:]
            datacase(clientData, data)
        else:
            break

    return True

def datacase(clientData, data):
    mysql = share.mysql
    part = data["part"]
    if (part == DIALOG):
        clientData.sendPacket(PacketCreator.picapture())

    if (part == PI_CAPTURE):
        strData = data["strData"]
        shape = (data["width"], data["height"])
        imgdata = np.array(strData.split(","), dtype="uint8")
        imgdata = np.reshape(imgdata, shape)
        print(imgdata.shape)
        img = cv2.imdecode(imgdata, cv2.IMREAD_COLOR)
        cv2.imwrite('./segmentation/test/jpgs/test.jpg', img)
        if (segmentation.predict.main()):
            print("img 판단 시작")

    if (part == KICKBOARD_CODE):
        clientData.sendPacket(PacketCreator.dialog(f"'{data['code']}' kickboard select!"))
    
    if (part == USER_REGISTER):
        id = data["id"]
        pw = data["pw"]
        rows = mysql.query(f"SELECT * FROM user_information WHERE id='{id}';")
        print(rows)
        if len(rows) > 0:
            clientData.sendPacket(PacketCreator.dialog('already id !!'))
        else:
            clientData.sendPacket(PacketCreator.dialog('register success !!'))

