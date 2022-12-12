import socket
import pickle
import base64
import sys
import os
import time
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
from pgp import PGP


class Server:
    def __init__(self, ip, port):
        # Create socket
        try:
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error as err:
            print("socket creation failed with error %s" % err)
        # Init socket params
        self.s.bind((ip, port))
        print("starting server on port " + str(port))
        path = os.path.dirname(os.path.realpath(__file__)) + "\\bin"
        self.pgp = PGP(path)

    def listen(self):
        self.s.listen(1)

    def accept(self):
        conn, addr = self.s.accept()
        print('Connected by', addr)
        return conn, addr

    def listKeys(self):
        public = pickle.dumps(self.pgp.list_public_keys())
        private = pickle.dumps(self.pgp.list_private_keys())
        public = base64.b64encode(public).decode('ascii')
        private = base64.b64encode(private).decode('ascii')
        packet = "list private %s endprivate public %s endpublic" % (private, public)
        return packet

    def sendFile(self,path:str,conn: socket):
        size = os.path.getsize(path)
        path = os.path.abspath(path)

        msg = "file %d" % size
        print("sending %s size %d" % (path,size))
        conn.send(msg.encode())

        f = open(path, "rb")
        while True:
            data = f.read(1024)
            
            if data:
                conn.send(data)
            else:
                f.close()
                break


    def addKeys(self, data):
        try:
            if "PUBLIC" in data:
                key_start = data.find("-----BEGIN PGP PUBLIC KEY BLOCK-----")
                key_end = data.find("-----END PGP PUBLIC KEY BLOCK-----") + len("-----END PGP PUBLIC KEY BLOCK-----")
                key_string = data[key_start:key_end]
                self.pgp.add_key(key_string)
            elif "PRIVATE" in data:
                key_start = data.find("-----BEGIN PGP PRIVATE KEY BLOCK-----")
                key_end = data.find("-----END PGP PRIVATE KEY BLOCK-----") + len("-----END PGP PRIVATE KEY BLOCK-----")
                key_string = data[key_start:key_end]
                self.pgp.add_key(key_string)
            return "OK"
        except EOFError:
            return "Incorrect input"


    def connection(self, conn: socket, addr):
        while True:
            data = conn.recv(10000)
            if data:
                data = data.decode()
                if data[:4] == "list":
                    # self.pgp.list()
                    packet = self.listKeys()
                    conn.send(packet.encode())
                elif data[:4] == "sign":
                    cert = "pickle."
                    self.pgp.sign(cert)
                elif data[:6] == "verify":
                    self.pgp.verify()
                elif data[:3] == "add":
                    res = self.addKeys(data)
                    conn.send(res.encode())
                elif data[:4] == "file":
                    path = "C:\\Users\\Koa\\Downloads\\Archive\\private.asc"
                    self.sendFile(path,conn);
                else:
                    error = "unexpected command %s" % (data)
                    print(error)
                    conn.send(error.encode())
            else:
                print("Client quit, closing", addr)
                conn.close()
                break