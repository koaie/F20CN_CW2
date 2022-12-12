import tkinter
from tkinter.messagebox import showerror, showwarning
from tkinter import filedialog
import os
import customtkinter
import sys
import client
import datetime
import base64

try:
    client = client.client("127.0.0.1", 8888)
    client.connect()
except ConnectionError:
    showerror(title="Connection error", message="Cannot connect to server. Check it is still running")
    sys.exit("Connection error")

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

class Key:
    type: str
    key: str
    def __init__(self, type, key):
        self.type = type
        self.key = key


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        # configure window
        self.title("F20CN CW2 client application")
        self.geometry(f"{1100}x{580}")

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="F20CN CW2 Client", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.send_key_button = customtkinter.CTkButton(self.sidebar_frame, text="Send key", command=self.add_keys)
        self.send_key_button.grid(row=1, column=0, padx=20, pady=10)
        self.list_keys_button = customtkinter.CTkButton(self.sidebar_frame, text="List keys", command=self.load_keys)
        self.list_keys_button.grid(row=2, column=0, padx=20, pady=10)
        self.command_button = customtkinter.CTkButton(self.sidebar_frame, text="Send Command", command=self.command_dialog)
        self.command_button.grid(row=3, column=0, padx=20, pady=10)
        self.keys_box = customtkinter.CTkTextbox(self)
        self.keys_box.configure(state="disabled")
        self.keys_box.grid(row=0, column=1, columnspan=1, padx=(20, 20), pady=(20, 20), sticky="nsew")
        # self.authors_box = customtkinter.CTkTextbox(self)
        # self.authors_box.configure(state="disabled")
        # self.authors_box.grid(row=0, column=2, columnspan=1, padx=(20, 20), pady=(20, 20), sticky="nsew")

        self.authors_frame = customtkinter.CTkFrame(self)
        self.authors_frame.grid(row=0, column=3, padx=(20, 20), pady=(20, 20), sticky="n")
        self.authors = customtkinter.CTkComboBox(master=self.authors_frame, values=list(self.load_authors()))
        self.authors.grid(row=1, column=3, padx=20, pady=10)
        self.label_radio_group = customtkinter.CTkLabel(master=self.authors_frame, text="Trusted Authors")
        self.label_radio_group.grid(row=0, column=3, columnspan=1, padx=10, pady=10, sticky="")
        self.author_download_button = customtkinter.CTkButton(master=self.authors_frame, text="Download File and Sig", command=self.download)
        self.author_download_button.grid(row=2, column=3, pady=(20,10), padx=20, sticky="n")
        self.author_view_button = customtkinter.CTkButton(master=self.authors_frame, text="View items",command=self.view)
        self.author_view_button.grid(row=3, column=3, pady=10, padx=20, sticky="n")
        self.author_verify_button = customtkinter.CTkButton(master=self.authors_frame, text="Verify File and Sig")
        self.author_verify_button.grid(row=4, column=3, pady=10, padx=20, sticky="n")
        self.author_sign_button = customtkinter.CTkButton(master=self.authors_frame, text="Sign Cert")
        self.author_sign_button.grid(row=5, column=3, pady=(10,20), padx=20, sticky="n")

        self.load_keys()
        self.load_authors()

    def command_dialog(self):
        dialog = customtkinter.CTkInputDialog(text="Type in a command:", title="CTkInputDialog")
        input = dialog.get_input()
        if(input):
            client.send(input)

    def add_keys(self):
        try:
            initial = os.path.dirname(os.path.realpath(__file__))
            key = filedialog.askopenfilename(
                title="Open dataset",
                initialdir=initial,
                filetypes=[("Public/Private keys", "*.asc")])
            if key:
                key_file = open(key, "r")
                key_string = key_file.read()
                key_file.close()
                client.add_keys(key_string)
        except UnicodeDecodeError:
            showwarning(title="Incorrect key file", message="Incorrect key file specified. Ensure key is exported "
                                                            "with --armor")
    def load_keys(self):
        client.send("list")
        private, public = client.get_keys()
        self.keys_box.configure(state="normal")
        self.keys_box.delete("0.0", "end")
        self.keys_box.insert("end", "Private keys:\n", "heading")
        for key in private:
            if key["expires"]:
                self.keys_box.insert("end", "key id: " + key["keyid"] + " uid: " + str(key["uids"]) + ", expires: " +
                                     str(datetime.datetime.fromtimestamp(int(key["expires"]))) + "\n", "key")
            else:
                self.keys_box.insert("end", "key id: " + key["keyid"] + ", expires: N/A\n", "key")
        self.keys_box.insert("end", "\nPrivate keys:\n", "heading")
        for key in public:
            if key["expires"]:
                self.keys_box.insert("end", "key id: " + key["keyid"] + ", expires: " +
                                     str(datetime.datetime.fromtimestamp(int(key["expires"]))) + "\n", "key")
            else:
                self.keys_box.insert("end", "key id: " + key["keyid"] + ", expires: N/A\n", "key")
        self.keys_box.tag_config("heading", underline=True)
        self.keys_box.configure(state="disabled")


    def load_authors(self):
        client.send("list")
        private, public = client.get_keys()
        authors = {

        }
        for key in private:
            for id in key["uids"]:
                if id in authors:
                    keys: list = authors[id]
                    keys.append(Key("private",key["keyid"]))
                    authors[id] = keys
                else:
                    authors[id] = [Key("private",key["keyid"])]
        for key in public:
            for id in key["uids"]:
                if id in authors:
                    keys: list = authors[id]
                    keys.append(Key("public",key["keyid"]))
                    authors[id] = keys
                else:
                    authors[id] = [Key("public",key["keyid"])]
        return authors.keys()

    def tob64(self, text):
        text = text.encode()
        text = base64.b64encode(text)
        text = text.decode()

    def downloadFile(self,ext):
        id = self.authors.get()
        id = self.tob64(id)
        msg = "file " + id + ext
        print(msg)
        client.send(msg)

    def download(self):
        self.downloadFile(".txt")
        self.downloadFile(".sig")

    
    def view(self):
        path = os.path.dirname(os.path.realpath(__file__)) + "\\files"
        if not os.path.isdir(path):
            os.makedirs(path)
        os.startfile(path) 




               

if __name__ == "__main__":
    app = App()
    app.mainloop()
