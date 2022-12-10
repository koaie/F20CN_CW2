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
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="CustomTkinter", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame, text="Send keys", command=self.add_keys)
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)
        self.sidebar_button_2 = customtkinter.CTkButton(self.sidebar_frame, command=self.sidebar_button_event)
        self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)
        self.sidebar_button_3 = customtkinter.CTkButton(self.sidebar_frame, command=self.sidebar_button_event)
        self.sidebar_button_3.grid(row=3, column=0, padx=20, pady=10)

        # create main entry and button
        self.entry = customtkinter.CTkEntry(self, placeholder_text="CTkEntry")
        self.entry.grid(row=3, column=1, columnspan=2, padx=(20, 0), pady=(20, 20), sticky="nsew")

        self.keys_box = customtkinter.CTkTextbox(self, state=tkinter.DISABLED)
        self.keys_box.grid(row=0, column=1, columnspan=2, padx=20, pady=20, sticky="nsew")

        self.main_button_1 = customtkinter.CTkButton(master=self, fg_color="transparent", text="Send", border_width=2, text_color=("gray10", "#DCE4EE"), command=self.send_click)
        self.main_button_1.grid(row=3, column=3, padx=(20, 20), pady=(20, 20), sticky="nsew")

    def open_input_dialog_event(self):
        dialog = customtkinter.CTkInputDialog(text="Type in a number:", title="CTkInputDialog")
        print("CTkInputDialog:", dialog.get_input())

    def add_keys(self):
        initial = os.path.dirname(os.path.realpath(__file__))
        key = filedialog.askopenfilename(
            title="Open dataset",
            initialdir=initial,
            filetypes=[("Public/Private keys", "*.key")])
        if key:
            # need try catch
            key_file = open(key, "r")
            key_string = key_file.read()
            key_file.close()
            print(key_string)
            client.add_keys(key_string)

    def sidebar_button_event(self):
        print("sidebar_button click")

    def send_click(self):
        input = self.entry.get()
        client.send(input)
        self.entry.delete(0, len(input))

if __name__ == "__main__":
    app = App()
    app.mainloop()
