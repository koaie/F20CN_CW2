import tkinter
from tkinter.messagebox import showerror
from tkinter import filedialog
import os
import customtkinter
import sys
import client
import time

try:
    client = client.client("127.0.0.1", 8888)
    client.connect()
except ConnectionError:
    showerror(title="Connection error", message="Cannot connect to server. Check it is still running")
    sys.exit("Connection error")

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


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
        self.command_button = customtkinter.CTkButton(self.sidebar_frame, text="Send Command", command=self.command_dialog)
        self.command_button.grid(row=2, column=0, padx=20, pady=10)
        self.keys_box = customtkinter.CTkTextbox(self)
        self.keys_box.configure(state="disabled")
        self.keys_box.grid(row=0, column=1, columnspan=2, padx=(20, 20), pady=(20, 20), sticky="nsew")
        self.load_keys()

    def command_dialog(self):
        dialog = customtkinter.CTkInputDialog(text="Type in a command:", title="CTkInputDialog")
        client.send(dialog.get_input())

    def add_keys(self):
        try:
            initial = os.path.dirname(os.path.realpath(__file__))
            key = filedialog.askopenfilename(
                title="Open dataset",
                initialdir=initial,
                filetypes=[("Public/Private keys", "*.asc")])
            if key:
                # need try catch
                key_file = open(key, "r")
                key_string = key_file.read()
                key_file.close()
                client.add_keys(key_string)
        except UnicodeDecodeError:
            print("Incorrect file - ensure exported with --armor")

    def load_keys(self):
        client.send("list")
        private, public = client.get_keys()
        self.keys_box.delete("0.0", "end")
        text = "Private keys:\n"
        for key in private:
            text += key["keyid"] + "\n"
        text += "\nPublic keys:\n"
        for key in public:
            text += key["keyid"] + "\n"
        # Very cool :(
        self.keys_box.configure(state="normal")
        self.keys_box.insert("0.0", text)
        self.keys_box.configure(state="disabled")


    def sidebar_button_event(self):
        print("sidebar_button click")


if __name__ == "__main__":
    app = App()
    app.mainloop()
