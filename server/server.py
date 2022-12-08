import socket
import pickle
import base64
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
        self.pgp = PGP()

    def listen(self):
        self.s.listen(1)

    def accept(self):
        conn, addr = self.s.accept()
        print('Connected by', addr)
        return conn, addr

    def listKeys(self):
        private = pickle.dumps(self.pgp.list_public_keys())
        public = pickle.dumps(self.pgp.list_private_keys())
        private = base64.b64encode(private).decode('ascii')
        public = base64.b64encode(public).decode('ascii')
        print(private)
        packet = "list private %s endprivate public %s endpublic" % (private, public)
        return packet

    def addKeys(self, data):
        try:
            keys_start = data.find("startkeys") + len("startkeys") + 1
            keys_end = data.find("endkeys")
            keys__string = data[keys_start:keys_end]
            keys = pickle.loads(base64.b64decode(keys__string))
            self.pgp.add_key(keys)
            return "OK"
        except EOFError:
            return "Incorrect input"


    def connection(self, conn: socket, addr):
        while True:
            data = conn.recv(1024)
            if data:
                data = data.decode()
                if data[:4] == "list":
                    self.pgp.list()
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
                else:
                    error = "unexpected command"
                    print("%s %s" % (error, data))
                    conn.send(error.encode())
            else:
                print("Client quit, closing", addr)
                conn.close()
                break