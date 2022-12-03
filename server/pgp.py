import gnupg
import os
import sys
import distutils.spawn


class PGP:
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

    def sign(self, cert):
        response = self.gpg.sign(cert)
        print(response)
        return response

    def list_public_keys(self):
        return self.gpg.list_keys()

    def list_private_keys(self):
        return self.gpg.list_keys(True)

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

    def verify(self):
        print("unimplemented")

    def add_key(self, data):
        # temp
        #self.gpg.import_keys_file(os.path.dirname(os.path.realpath(__file__)) + "/public_key.key")
        #self.gpg.import_keys_file(os.path.dirname(os.path.realpath(__file__)) + "/private_key.key")
        result = self.gpg.import_keys(data)
        print("%s key(s) imported" %result.count)