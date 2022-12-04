import socket
import time
class client:
    s = socket.socket()
    def __init__(self,ip:str,port:int):
        # Init socket params
        self.ip = ip
        self.port = port

    def connect(self):
        self.s.connect((self.ip, self.port))

    def send(self,text:str):
        self.s.send(text.encode())

    async def start(self):
        while True:
            data = self.s.recv(1024)
            if data:
                s = "print data %s" % data.decode
                print("sending print command")
                self.send("print hello")
            time.sleep(1)