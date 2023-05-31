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

        def delete_all(pathKey):
            try:
                for filename in os.listdir(pathKey):
                    file_path = os.path.join(pathKey, filename)
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
            except Exception as e:
                self.logs_textbox.insert("0.0", datetime.now().strftime('%H:%M:%S') + " - Error: "+str(e)+"\n")

        def copy_configuration(pathConfig, environment, pathSwitch, pathUSB):
            try:
                if environment == 1:    
                    pathConfBashBunny = os.path.join(pathConfig, "bash_bunny/GUI")
                if environment == 2:
                    pathConfBashBunny = os.path.join(pathConfig, "bash_bunny/CLI")
                pathConfUSB= os.path.join(pathConfig, "usb_key")
                shutil.copytree(pathConfBashBunny, pathSwitch, dirs_exist_ok = True)
                shutil.copytree(pathConfUSB, pathUSB, dirs_exist_ok = True)
            except Exception as e:
                self.logs_textbox.insert("0.0", datetime.now().strftime('%H:%M:%S') + " - Error: "+str(e)+"\n")

        def replace_pass_and_name(pathSwitch, password, nameUSB, pathFiles, pathUSB):
            try:
                for filename in os.listdir(pathSwitch):
                    file_path = os.path.join(pathSwitch, filename)
                    file = open(file_path, "r")
                    lines = file.readlines()
                    file.close()
                    newFile = open(file_path, "w")
                    for line in lines:
                        if "[password]" in line:
                            line = line.replace("[password]", password)
                        if "[nameUSB]" in line:
                            line = line.replace("[nameUSB]", nameUSB)
                        if pathFiles != "" and "REM PathFilesToSave" in line:
                            line = line.replace("REM PathFilesToSave1", "DELAY 3000")
                            line = line.replace("REM PathFilesToSave2", f"STRING cp -r {pathFiles} {pathUSB}/saved_files")
                            line = line.replace("REM PathFilesToSave3", "DELAY 1000")
                            line = line.replace("REM PathFilesToSave4", "ENTER")
                        newFile.write(line)
                    newFile.close()           
            except Exception as e:
                self.logs_textbox.insert("0.0", datetime.now().strftime('%H:%M:%S') + " - Error: "+str(e)+"\n")
            

        def configure_bash_bunny():
            try:
                # Get entries
                pathBashBunny = self.pathEntryBashBunny.get()
                pathUSB = self.pathEntryUSB.get()
                action = self.tabview.get()
                switch = int(self.radio_var.get())
                environment = int(self.radio_environment_var.get())
                pathFiles = self.pathFiles.get()
                if environment == 1:
                    text_environment = "With GUI"
                if environment == 2:
                    text_environment = "No GUI (only CLI)"
                osDevice = self.os_menu.get() 
                nameUSB = self.nameUSB.get() 
                password = self.adminPassword.get()
                pathSwitch = os.path.join(pathBashBunny, "payloads/switch"+str(switch))

                # Delete all files and folders in the bash bunny switch folder and usb key
                delete_all(pathSwitch)
                delete_all(pathUSB)

                # Copy files for the good action and OS
                if action == "RAM Dump":
                    if osDevice == "Windows":
                        # Copy configuration and tools in the paths specified
                        pathConfigurationWindows = os.path.join(os.getcwd(), "configurations/Ram_Dump/Windows")
                        copy_configuration(pathConfigurationWindows, environment, pathSwitch, pathUSB)
                        replace_pass_and_name(pathSwitch, password, nameUSB, pathFiles, pathUSB)
                    if osDevice == "Debian":
                        # Copy configuration and tools in the paths specified
                        pathConfigurationDebian = os.path.join(os.getcwd(), "configurations/Ram_Dump/Debian")
                        copy_configuration(pathConfigurationDebian, environment, pathSwitch, pathUSB)
                        replace_pass_and_name(pathSwitch, password, nameUSB, pathFiles, pathUSB)
                    if osDevice == "Ubuntu":
                        # Copy configuration and tools in the paths specified
                        pathConfigurationUbuntu = os.path.join(os.getcwd(), "configurations/Ram_Dump/Ubuntu")
                        copy_configuration(pathConfigurationUbuntu, environment, pathSwitch, pathUSB)
                        replace_pass_and_name(pathSwitch, password, nameUSB, pathFiles, pathUSB)
                elif action == "Other action":
                    print("TODO")

                # Insert configuration in logs
                self.logs_textbox.insert("0.0", "**********\n" + datetime.now().strftime('%H:%M:%S') + " --- Configuration loaded: \n- Path to Bash Bunny: "+pathBashBunny+"\n- Path to exfiltration key: "+pathUSB+"\n- Action: "+action+"\n- Switch: "+str(switch)+"\n- Environment: "+text_environment+"\n- OS: "+osDevice+"\n- Path to files to save: "+pathFiles+"\n")
            except Exception as e:
                # Insert error in logs
                self.logs_textbox.insert("0.0", datetime.now().strftime('%H:%M:%S') + " - Error: "+str(e)+"\n")



        # Window configuration
        self.title("OffGrid_Configurator.py")
        self.geometry(f"{690}x{850}")
        self.resizable(False, False)

        # First frame : Path to Bash bunny
        self.frame1 = customtkinter.CTkFrame(self)
        self.frame1.grid(row=0, column=0, sticky="nsew")
        self.pathEntryBashBunny = customtkinter.CTkEntry(self.frame1, placeholder_text="Path to Bash Bunny root folder", width=420)
        self.pathEntryBashBunny.grid(row=0, column=0, padx=(58, 0), pady=30, sticky="nsew")
        self.addPathBashBunny = customtkinter.CTkButton(master=self.frame1, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), text="Add Path", command=add_path_bash_bunny)
        self.addPathBashBunny.grid(row=0, column=1, padx=(20, 30), pady=30, sticky="nsew")

        # Tabview (differents actions)
        self.frame2 = customtkinter.CTkFrame(self)
        self.frame2.grid(row=1, column=0, sticky="nsew")
        self.tabview = customtkinter.CTkTabview(self.frame2, width=650)
        self.tabview.grid(row=1, column=0, padx=(20, 20), pady=(5,20), sticky="nsew")
        self.tabview.add("RAM Dump")
        self.tabview.add("Other Action")
        self.tabview.add("Another action")


        # First frame RAM Dump : path to exfiltartion key, name and password
        self.frame1_ram = customtkinter.CTkFrame(self.tabview.tab("RAM Dump"))
        self.frame1_ram.grid(row=0, column=0, sticky="nsew")
        self.pathEntryUSB = customtkinter.CTkEntry(self.frame1_ram, placeholder_text="Path to USB exfiltration key root folder", width=420)
        self.pathEntryUSB.grid(row=1, column=0, padx=(30, 0), pady=(20, 0), sticky="nsew")

        self.addPathUSB = customtkinter.CTkButton(self.frame1_ram, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), text="Add Path", command=add_path_usb)
        self.addPathUSB.grid(row=1, column=1, padx=(20, 30), pady=(20, 0), sticky="nsew")

        self.nameUSB= customtkinter.CTkEntry(self.frame1_ram, placeholder_text="Enter name of USB exfiltration key", width=300)
        self.nameUSB.grid(row=2, column=0, pady=(20,0), padx=(80,0))

        self.adminPassword = customtkinter.CTkEntry(self.frame1_ram, placeholder_text="Enter admin password", show="\u25CF", width=300)
        self.adminPassword.grid(row=3, column=0, pady=(20,0), padx=(80,0))

        self.pathFiles = customtkinter.CTkEntry(self.frame1_ram, placeholder_text="Path to root folder of files you want to save (optionnal)", width=420)
        self.pathFiles.grid(row=4, column=0, padx=(30, 0), pady=(30, 30), sticky="nsew")


        # Second frame RAM Dump : Configuration for the Bash Bunny (switch / environment / OS)
        self.frame2_ram = customtkinter.CTkFrame(self.tabview.tab("RAM Dump"))
        self.frame2_ram.grid(row=1, column=0, sticky="nsew")

        self.switch_label = customtkinter.CTkLabel(self.frame2_ram, text="Select Switch :", font=customtkinter.CTkFont(size=14, weight="bold"))
        self.switch_label.grid(row=1, column=0, pady=(25, 0), padx=(30,0))
        self.radio_var = tkinter.IntVar(value=1)
        self.radio_button_switch1 = customtkinter.CTkRadioButton(self.frame2_ram, variable=self.radio_var, text="Switch 1", value=1)
        self.radio_button_switch1.grid(row=2, column=0, pady=(20, 0), padx=(30,0), sticky="n")
        self.radio_button_switch2 = customtkinter.CTkRadioButton(master=self.frame2_ram, variable=self.radio_var, text="Switch 2", value=2)
        self.radio_button_switch2.grid(row=3, column=0, pady=(20, 20), padx=(30,0), sticky="n")

        self.environment_label = customtkinter.CTkLabel(self.frame2_ram, text="Select Environment :", font=customtkinter.CTkFont(size=14, weight="bold"))
        self.environment_label.grid(row=1, column=1, pady=(25, 0), padx=(70,0))
        self.radio_environment_var = tkinter.IntVar(value=1)
        self.radio_environment1 = customtkinter.CTkRadioButton(self.frame2_ram, variable=self.radio_environment_var, text="With GUI", value=1)
        self.radio_environment1.grid(row=2, column=1, pady=(20, 0), padx=(40,0), sticky="n")
        self.radio_environment2 = customtkinter.CTkRadioButton(master=self.frame2_ram, variable=self.radio_environment_var, text="No GUI (only CLI)", value=2)
        self.radio_environment2.grid(row=3, column=1, pady=(20, 20), padx=(63,0), sticky="n")

        self.os_label = customtkinter.CTkLabel(self.frame2_ram, text="Select OS :", font=customtkinter.CTkFont(size=14, weight="bold"))
        self.os_label.grid(row=1, column=2, pady=(25, 0), padx=(50,0))
        self.os_menu = customtkinter.CTkOptionMenu(self.frame2_ram, width=170, values=["Windows", "Ubuntu", "Debian"])
        self.os_menu.grid(row=2, column=2, padx=(60,0), pady=(20, 0))

        # Second frame : Main button
        self.frame3 = customtkinter.CTkFrame(self)
        self.frame3.grid(row=2, column=0, sticky="nsew")
        self.main_button = customtkinter.CTkButton(master=self.frame3, border_width=2, text="Configure Bash Bunny", font=customtkinter.CTkFont(size=15, weight="bold"), width=300, height=50, command=configure_bash_bunny)
        self.main_button.grid(row=2, column=0, padx=(190, 0), pady=(30, 0), sticky="nsew")

        # Third frame : Logs
        self.frame4 = customtkinter.CTkFrame(self)
        self.frame4.grid(row=3, column=0, sticky="nsew")
        self.logs_textbox = customtkinter.CTkTextbox(self.frame4, width=560, height=150)
        self.logs_textbox.insert("0.0", "----- Here are your logs stored -----")
        self.logs_textbox.grid(row=4, column=0, padx=(50, 0), pady=(30, 30), sticky="nsew")


if __name__ == "__main__":
    app = App()
    app.mainloop()