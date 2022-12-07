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
                # This could do with a parsing function
                if data[:4] == "list":
                    self.pgp.list()
                    private = pickle.dumps(self.pgp.list_public_keys())
                    public = pickle.dumps(self.pgp.list_private_keys())
                    private = base64.b64encode(private).decode('ascii')
                    public = base64.b64encode(public).decode('ascii')
                    print(private)
                    packet = "list private %s endprivate public %s endpublic" % (private, public)
                    self.conn.send(packet.encode())
                elif data[:4] == "sign":
                    cert = "pickle."
                    self.pgp.sign(cert)
                elif data[:6] == "verify":
                    self.pgp.verify()
                if data[:3] == "add":
                    self.conn.send("OK".encode())
                    keys_start = data.find("startkeys") + len("startkeys") + 1
                    keys_end = data.find("endkeys")
                    keys__string = data[keys_start:keys_end]
                    keys = pickle.loads(base64.b64decode(keys__string))
                    self.pgp.add_key(keys)
            else:
                print("Unexpected command %s" % data)
                self.conn.send("unexpected command")

            time.sleep(1)
