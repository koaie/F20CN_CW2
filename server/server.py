import socket
import time
import gnupg
import os
import sys
import distutils.spawn
import ctypes

class Server:
    # Create socket
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as err:
        print ("socket creation failed with error %s" %(err))
    
    def __init__(self,ip,port):
        # Init socket params
        self.s.bind((ip,port))
        print("starting server on port " + str(port))
        self.gpg = self.initiate_gpg()
        

    def start(self):
        self.s.listen(5)  
        while True:
             (conn, address) = self.s.accept()
             data = conn.recv(1024)
             if data:
                data = data.decode()
                print(data)
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

    def sign_cert(self, cert):
        response = self.gpg.sign(cert)
        print(response)
        return response

class Send:
    def __init__(self,s: socket):
        self.s = s

    def text(self,text: str):
        self.s.send(text.encode())


# class Listen:
#     def __init__(self,s: socket):
#         self.s = s

#     def text(self):
#         data = self.s.recv(1024)
#         if data:
#             return data.decode()