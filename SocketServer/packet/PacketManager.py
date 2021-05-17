"""
    Title.  packet/packetManager.py
    Autor.  K9714(github.com/k9714)
    Date.   21. 05. 17
    Desc.
        패킷 상수를 정의하고, 소켓 응답을 받는 부분입니다.
"""
from packet.PacketCreator import PacketCreator
from packet.Protocol import Decode
from client.ClientData import clientList

#{ PACKET_PART
DIALOG          = 3
USER_LOGIN      = 500
USER_IDCHECK    = 501
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
        psize = int(str(clientData.buff[:3], encoding='utf-8'))
        if len(clientData.buff) >= psize + 3:
            data = Decode(clientData.buff[3:psize + 3])
            clientData.buff = clientData.buff[psize + 3:]
            datacase(clientData, data)
        else:
            break

    return True

def datacase(clientData, data):
    if (data["part"] == USER_LOGIN):
        clientData.sendPacket(PacketCreator.dialog(0, "이것은 알림", "안녕하세여~"))
