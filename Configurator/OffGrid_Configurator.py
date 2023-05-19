import tkinter
import customtkinter
import os
from datetime import datetime

customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # Commands
        def add_path():
            try:
                currdir = os.getcwd()
                path = tkinter.filedialog.askdirectory(initialdir=currdir, title='Please select Bash Bunny root folder')
                self.pathEntry.delete("0", "end")
                self.pathEntry.insert("0", path)
            except Exception as e:
                self.logs_textbox.insert("0.0", datetime.now().strftime('%H:%M:%S') + " - Error: "+str(e)+"\n")


        def configure_bash_bunny():
            try:
                pathBashBunny = self.pathEntry.get()
                switch = int(self.radio_var.get())
                if switch == 1:
                    print("Switch 1")
                    # TODO
                if switch == 2:
                    print("Switch 2")
                    # TODO
                action = self.action_menu.get()
                os = self.os_menu.get()
                self.logs_textbox.insert("0.0", datetime.now().strftime('%H:%M:%S') + " - Configuration loaded in: "+pathBashBunny+" | Switch: "+str(switch)+" | Action: "+action+" | OS: "+os+"\n")
            except Exception as e:
                self.logs_textbox.insert("0.0", datetime.now().strftime('%H:%M:%S') + " - Error: "+str(e)+"\n")



        # Window configuration
        self.title("OffGrid_Configurator.py")
        self.geometry(f"{660}x{510}")
        self.resizable(False, False)

        # First frame : Path to the Bash Bunny
        self.frame1 = customtkinter.CTkFrame(self)
        self.frame1.grid(row=0, column=0, sticky="nsew")

        self.pathEntry = customtkinter.CTkEntry(self.frame1, placeholder_text="Path to Bash Bunny root folder", width=420)
        self.pathEntry.grid(row=0, column=0, padx=(50, 0), pady=(20, 0), sticky="nsew")

        self.addPath = customtkinter.CTkButton(master=self.frame1, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), text="Add Path", command=add_path)
        self.addPath.grid(row=0, column=1, padx=(20, 30), pady=(20, 0), sticky="nsew")

        # Second frame : Configuration for the Bash Bunny (switch / action / OS)
        self.frame2 = customtkinter.CTkFrame(self)
        self.frame2.grid(row=1, column=0, sticky="nsew")

        self.switch_label = customtkinter.CTkLabel(self.frame2, text="Select Switch :", font=customtkinter.CTkFont(size=14, weight="bold"))
        self.switch_label.grid(row=1, column=0, pady=(35, 0), padx=(50,0))
        self.radio_var = tkinter.IntVar(value=1)
        self.radio_button_switch1 = customtkinter.CTkRadioButton(master=self.frame2, variable=self.radio_var, text="Switch 1", value=1)
        self.radio_button_switch1.grid(row=2, column=0, pady=(20, 0), padx=(50,0), sticky="n")
        self.radio_button_switch2 = customtkinter.CTkRadioButton(master=self.frame2, variable=self.radio_var, text="Switch 2", value=2)
        self.radio_button_switch2.grid(row=3, column=0, pady=(20, 20), padx=(50,0), sticky="n")

        self.action_label = customtkinter.CTkLabel(self.frame2, text="Select Action :", font=customtkinter.CTkFont(size=14, weight="bold"))
        self.action_label.grid(row=1, column=1, pady=(35, 0), padx=(50,0))
        self.action_menu = customtkinter.CTkOptionMenu(self.frame2, width=200, values=["RAM Dump", "Other action", "Another Action"])
        self.action_menu.grid(row=2, column=1, padx=(60,0), pady=(20, 0))

        self.os_label = customtkinter.CTkLabel(self.frame2, text="Select OS :", font=customtkinter.CTkFont(size=14, weight="bold"))
        self.os_label.grid(row=1, column=2, pady=(35, 0), padx=(50,0))
        self.os_menu = customtkinter.CTkOptionMenu(self.frame2, width=150, values=["Windows", "Ubuntu", "Debian"])
        self.os_menu.grid(row=2, column=2, padx=(60,0), pady=(20, 0))

        # Third frame : Main button
        self.frame3 = customtkinter.CTkFrame(self)
        self.frame3.grid(row=3, column=0, sticky="nsew")
        self.main_button = customtkinter.CTkButton(master=self.frame3, border_width=2, text="Configure Bash Bunny", font=customtkinter.CTkFont(size=15, weight="bold"), width=300, height=50, command=configure_bash_bunny)
        self.main_button.grid(row=3, column=0, padx=(160, 0), pady=(30, 0), sticky="nsew")

        # Last frame : Logs
        self.frame4 = customtkinter.CTkFrame(self)
        self.frame4.grid(row=4, column=0, sticky="nsew")
        self.logs_textbox = customtkinter.CTkTextbox(self.frame4, width=550, height=150)
        self.logs_textbox.insert("0.0", "----- Here are your logs stored -----")
        self.logs_textbox.grid(row=4, column=0, padx=(50, 0), pady=(30, 30), sticky="nsew")


if __name__ == "__main__":
    app = App()
    app.mainloop()