import socket
import time
import gnupg
import os
import sys
import distutils.spawn
import ctypes
import pickle


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
        self.gpg = self.initiate_gpg()

    def start(self):
        self.s.listen(5)
        while True:
            (self.conn, self.address) = self.s.accept()
            data = self.conn.recv(1024)
            if data:
                data = data.decode()
                if data[:4] == "list":
                    self.list()
                if data[:4] == "sign":
                    self.sign()
                if data[:6] == "verify":
                    self.verify()
                if data[:3] == "add":
                    self.add_key(data[4:])
            else:
                print("Unexpected command %s" % data)

            time.sleep(1)

    @staticmethod
    def initiate_gpg():
        if os.name == "nt":
            path = os.path.dirname(os.path.realpath(__file__)) + "\\bin\\gpg.exe"
            if os.path.exists(path):
                gpg = gnupg.GPG(gpgbinary=path)
            else:
                sys.exit("Error: gpg windows binary is missing from bin folder")
        else:
            if distutils.spawn.find_executable("gpg"):
                gpg = gnupg.GPG()
            else:
                sys.exit("Error: gpg needs installing using your chosen package manager")
        return gpg

    def sign(self, cert):
        response = self.gpg.sign(cert)
        print(response)
        return response

    def list(self):
        public = self.gpg.list_keys()
        private = self.gpg.list_keys(True)
        numKeys = len(public) + len(private)
        print("|----------------------------|")
        print("| Keys: %d                    |" % numKeys)
        print("|----------------------------|")
        if numKeys > 0:
            print("|  Type   |        ID        |")
            print("|---------|------------------|")
            for key in public:
                print("| public  | %s |" % key["keyid"])
                print("|----------------------------|")
            for key in private:
                print("| private | %s |" % key["keyid"])
                print("|----------------------------|")

        private = pickle.dumps(private)
        public = pickle.dumps(public)
        #Send(self.s).text("list private %s public %s" %(private, public))
        self.conn.send("list private %s public %s".encode() %(private, public))

    def verify(self):
        print("unimplemented")
    def add_key(self, data):
        # temp
        #self.gpg.import_keys_file(os.path.dirname(os.path.realpath(__file__)) + "/public_key.key")
        #self.gpg.import_keys_file(os.path.dirname(os.path.realpath(__file__)) + "/private_key.key")
        result = self.gpg.import_keys(data)
        print("%s key(s) imported" %result.count)


class Send:
    def __init__(self, s: socket):
        self.s = s

    def text(self, text: str):
        self.s.send(text.encode())

# class Listen:
#     def __init__(self,s: socket):
#         self.s = s

#     def text(self):
#         data = self.s.recv(1024)
#         if data:
#             return data.decode()
