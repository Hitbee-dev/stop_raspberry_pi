"""
    Title.  packet/packetCreator.py
    Autor.  K9714(github.com/k9714)
    Date.   21. 05. 17
    Desc.
        패킷 Encoding 전 Dictionary 형태로 변환하는 부분입니다.
"""
from packet import PacketManager as Manager

class PacketCreator():
    # res
    # 0 : fail, 해당 킥보드 연결 끊김
    # 1 : fail, 이미 사용중
    # 2 : success
    def kickboardReq(res):
        data = {}
        data["part"] = Manager.KICKBOARD_REQ
        data["res"] = res
        return data

    # res
    # 0 : fail, 해당 킥보드 연결 끊김
    # 1 : fail, 킼보드가 이미 반납됨
    # 2 : success
    def kickboardRet(res):
        data = {}
        data["part"] = Manager.KICKBOARD_RET
        data["res"] = res
        return data

    # 킥보드 BLE 스캔 요청
    def kickboardRegion(useridx):
        data = {}
        data["part"] = Manager.KICKBOARD_REGION
        data["useridx"] = useridx
        return data


    def piCapture():
        data = {}
        data["part"] = Manager.PI_CAPTURE
        return data