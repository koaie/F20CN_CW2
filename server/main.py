import gnupg
import os
import sys
import distutils.spawn
import ctypes

class Server:
    def __init__(self):
        self.gpg = self.initiate_gpg()

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

test = Server()
test.sign_cert("test")