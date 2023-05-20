import tkinter
import customtkinter
import os, shutil
from datetime import datetime

customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # Commands
        def add_path_bash_bunny():
            try:
                currdir = os.getcwd()
                path = tkinter.filedialog.askdirectory(initialdir=currdir, title='Please select Bash Bunny root folder')
                self.pathEntryBashBunny.delete("0", "end")
                self.pathEntryBashBunny.insert("0", path)     
            except Exception as e:
                self.logs_textbox.insert("0.0", datetime.now().strftime('%H:%M:%S') + " - Error: "+str(e)+"\n")

        def add_path_usb():
            try:
                currdir = os.getcwd()
                path = tkinter.filedialog.askdirectory(initialdir=currdir, title='Please select USB exfiltration key root folder')
                self.pathEntryUSB.delete("0", "end")
                self.pathEntryUSB.insert("0", path)
            except Exception as e:
                self.logs_textbox.insert("0.0", datetime.now().strftime('%H:%M:%S') + " - Error: "+str(e)+"\n")


        def configure_bash_bunny():
            try:
                # Get entries
                pathBashBunny = self.pathEntryBashBunny.get()
                pathUSB = self.pathEntryUSB.get()
                switch = int(self.radio_var.get())
                action = self.action_menu.get()
                os = self.os_menu.get()  
                password = self.adminPassword.get()
                pathSwitch = pathBashBunny+"payloads/switch"+str(switch)   
                print(pathSwitch)  

                # Delete all files and folders in the switch folder (doesn't work)
                """
                for root, dirs, files in os.walk(pathSwitch):
                    for f in files:
                        os.unlink(os.path.join(root, f))
                    for d in dirs:
                        shutil.rmtree(os.path.join(root, d))
                """

                # Copy files for the good action and OS
                if action == "RAM Dump":
                    if os == "Windows":
                        print("TODO")
                    if os == "Debian":
                        print("TODO")
                    if os == "Ubuntu":
                        print("TODO")
                elif action == "Other action":
                    print("TODO")

                self.logs_textbox.insert("0.0", "**********\n" + datetime.now().strftime('%H:%M:%S') + " --- Configuration loaded: \n- Path to Bash Bunny: "+pathBashBunny+"\n- Path to exfiltration key: "+pathUSB+"\n- Switch: "+str(switch)+"\n- Action: "+action+"\n- OS: "+os+"\n")
            except Exception as e:
                self.logs_textbox.insert("0.0", datetime.now().strftime('%H:%M:%S') + " - Error: "+str(e)+"\n")



        # Window configuration
        self.title("OffGrid_Configurator.py")
        self.geometry(f"{660}x{610}")
        self.resizable(False, False)

        # First frame : Path to the Bash Bunny
        self.frame1 = customtkinter.CTkFrame(self)
        self.frame1.grid(row=0, column=0, sticky="nsew")

        self.pathEntryBashBunny = customtkinter.CTkEntry(self.frame1, placeholder_text="Path to Bash Bunny root folder", width=420)
        self.pathEntryBashBunny.grid(row=0, column=0, padx=(50, 0), pady=(20, 0), sticky="nsew")

        self.addPathBashBunny = customtkinter.CTkButton(master=self.frame1, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), text="Add Path", command=add_path_bash_bunny)
        self.addPathBashBunny.grid(row=0, column=1, padx=(20, 30), pady=(20, 0), sticky="nsew")

        self.pathEntryUSB = customtkinter.CTkEntry(self.frame1, placeholder_text="Path to USB exfiltration key root folder", width=420)
        self.pathEntryUSB.grid(row=1, column=0, padx=(50, 0), pady=(20, 0), sticky="nsew")

        self.addPathUSB = customtkinter.CTkButton(master=self.frame1, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), text="Add Path", command=add_path_usb)
        self.addPathUSB.grid(row=1, column=1, padx=(20, 30), pady=(20, 0), sticky="nsew")

        self.adminPassword = customtkinter.CTkEntry(master=self.frame1, placeholder_text="Enter admin password", show="\u25CF", width=300)
        self.adminPassword.grid(row=2, column=0, pady=(20,0), padx=(100,0))

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
        self.logs_textbox = customtkinter.CTkTextbox(self.frame4, width=560, height=150)
        self.logs_textbox.insert("0.0", "----- Here are your logs stored -----")
        self.logs_textbox.grid(row=4, column=0, padx=(50, 0), pady=(30, 30), sticky="nsew")


if __name__ == "__main__":
    app = App()
    app.mainloop()