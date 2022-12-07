import socket
import pickle
import base64

class client:
    s = socket.socket()

    def __init__(self, ip: str, port: int):
        # Init socket params
        self.ip = ip
        self.port = port

    def connect(self):
        self.s.connect((self.ip, self.port))

    def parse(self, data):

        if data[:4] == "list":
            private_start = data.find("private") + len("private") + 1
            private_end = data.find("endprivate")
            public_start = data.find("public") + len("public") + 1
            public_end = data.find("endpublic")
            private_string = data[private_start:private_end]
            private = pickle.loads(base64.b64decode(private_string))
            public_string = data[public_start:public_end]
            public = pickle.loads(base64.b64decode(public_string))

            parsed = {
                "function": "list",
                "private": private,
                "public": public
            }

            return parsed

    def list(self, private, public):
        print("Received %d private keys and %d public keys from the server" % (len(private), len(public)))

    def send(self,text:str):
        self.s.send(text.encode())

        data = self.s.recv(10000)
        if data:
            data = data.decode()
            data = self.parse(data)
            if data["function"] == "list":
                self.list(data["private"], data["public"])
