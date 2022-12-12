import socket
import pickle
import base64
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA


class client:
    s = socket.socket()

    def __init__(self, ip: str, port: int):
        # Init socket params
        self.public = []
        self.private = []
        self.ip = ip
        self.port = port
        # Keys need moving obviously
        public_key_file = open("../server/certtest/my_public.key", "rb").read()
        self.public_key = RSA.importKey(public_key_file)
        self.verifier = PKCS1_v1_5.new(self.public_key)

    def connect(self):
        self.s.connect((self.ip, self.port))

    def disconnect(self):
        self.s.close()

    def parseKeys(self, data):
        private_start = data.find("private") + len("private") + 1
        private_end = data.find("endprivate")
        public_start = data.find("public") + len("public") + 1
        public_end = data.find("endpublic")
        private_string = data[private_start:private_end]
        private = pickle.loads(base64.b64decode(private_string))
        public_string = data[public_start:public_end]
        public = pickle.loads(base64.b64decode(public_string))

        keys = {
            "private": private,
            "public": public
        }
        return keys

    def add_keys(self, key):
        self.send("add " + key)

    def list(self, private, public):
        print("Received %d private keys and %d public keys from the server" % (len(private), len(public)))
        self.private = private
        self.public = public

    def get_keys(self):
        return self.private, self.public

    def send(self, text: str):
        self.s.send(text.encode())

        data = self.s.recv(20000)
        if data:
            data = data.decode()
            if data[:4] == "list":
                l = pickle.loads(base64.b64decode(data[5:]))
                message = l[0]
                signature = l[1]
                message_hash = SHA256.new(data=bytes(message, "utf-8"))
                print(self.verifier.verify(message_hash, signature))
                keys = self.parseKeys(message)
                self.list(keys["private"], keys["public"])
            else:
                print(data)
