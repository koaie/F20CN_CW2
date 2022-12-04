import socket
import time
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

    def start(self):
        self.s.listen(5)
        while True:
            (self.conn, self.address) = self.s.accept()
            print(str(self.address) + " connected.")
            data = self.conn.recv(1024)
            if data:
                data = data.decode()
                if data[:4] == "list":
                    self.pgp.list()
                    private = pickle.dumps(self.pgp.list_public_keys())
                    public = pickle.dumps(self.pgp.list_private_keys())
                    private = base64.b64encode(private).decode('ascii')
                    public = base64.b64encode(public).decode('ascii')
                    print(private)
                    packet = "list private %s endprivate public %s endpublic" % (private, public)
                    self.conn.send(packet.encode())
                if data[:4] == "sign":
                    cert = "pickle."
                    self.pgp.sign(cert)
                if data[:6] == "verify":
                    self.pgp.verify()
                if data[:3] == "add":
                    self.pgp.add_key(data[4:])
            else:
                print("Unexpected command %s" % data)
                self.conn.send("unexpected command")

            time.sleep(1)
