if __name__ != "__main__":
    print("Started <Pycraft_TkinterUtils>")

    class TkinterInfo:
        def __init__(self):
            pass

        def GetPermissions(self):
            try:
                import tkinter as tk
                from tkinter import messagebox
                root = tk.Tk()
                root.withdraw()

                answer = messagebox.askquestion(
                    "Check Permission",
                    "Can we have your permission to check the internet for updates to Pycraft?")

                if answer == "yes":
                    self.ConnectionPermission = True

                else:
                    self.ConnectionPermission = False

            except Exception as Message:
                self.ErrorMessage = "TkinterUtils > TkinterInfo > GetPermissions: "+str(Message)

                self.ErrorMessage_detailed = "".join(
                    self.mod_Traceback__.format_exception(
                        None,
                        Message,
                        Message.__traceback__))

                self.mod_ErrorUtils__.GenerateErrorScreen.ErrorScreen(self)

        def CreateTkinterWindow(self):
            try:
                DataWindow = self.mod_Tkinter__tk.Tk()
                DataWindow.title("Player Information")
                DataWindow.configure(width=500, height=300)
                DataWindow.configure(bg="darkgrey")

                text = self.mod_Tkinter__tk.Text(
                    DataWindow,
                    wrap=self.mod_Tkinter__tk.WORD,
                    relief=self.mod_Tkinter__tk.FLAT)

                text.insert(
                    self.mod_Tkinter__tk.INSERT,
                    f"Pycraft: v{self.version}\n")

                VariableData = vars(self)

                VariableInformation = []
                for key in VariableData:
                    VariableInformation.append(f"{key} = {str(VariableData[key])}\n")

                VariableInformation = sorted(VariableInformation, key=len)

                for i in range(len(VariableInformation)):
                    text.insert(self.mod_Tkinter__tk.INSERT, VariableInformation[i])

                text["state"] = self.mod_Tkinter__tk.DISABLED

                text["bg"] = "#%02x%02x%02x" % (self.BackgroundCol[0],
                                                    self.BackgroundCol[1],
                                                    self.BackgroundCol[2])

                text["fg"] = "#%02x%02x%02x" % (self.FontCol[0],
                                                    self.FontCol[1],
                                                    self.FontCol[2])

                text.place(
                    x=0,
                    y=0,
                    relwidth=1,
                    relheight=1)

                DataWindow.mainloop()
                DataWindow.quit()
            except Exception as Message:
                self.ErrorMessage = "".join(("TkinterUtils > TkinterInfo > ",
                                             f"CreateTkinterWindow: {str(Message)}"))

                self.ErrorMessage_detailed = "".join(
                    self.mod_Traceback__.format_exception(
                        None,
                        Message,
                        Message.__traceback__))

                self.mod_ErrorUtils__.GenerateErrorScreen.ErrorScreen(self)

    class TkinterInstaller:
        def __init__():
            pass

        def CreateDisplay(InstallerImportData, root):
            try:
                geometry = root.winfo_geometry().split("+")
                Xpos = geometry[1]
                Ypos = geometry[2]
                root.destroy()
            except:
                Xpos, Ypos = 0, 0

            root = InstallerImportData.mod_Tkinter_tk_.Tk()

            root.title("Pycraft Setup Wizard")

            root.resizable(
                False,
                False)

            root.configure(bg="white")
            root.geometry(f"850x537+{int(Xpos)}+{int(Ypos)}")

            if InstallerImportData.platform == "Linux":
                ImageFileLocation = InstallerImportData.mod_Os__.path.join(
                    InstallerImportData.base_folder,
                    ("Resources//Installer_Resources//Banner.png"))

            else:
                ImageFileLocation = InstallerImportData.mod_Os__.path.join(
                    InstallerImportData.base_folder,
                    ("Resources\\Installer_Resources\\Banner.png"))

            InstallerImportData.mod_ImageUtils__.TkinterInstaller.open_img(
                InstallerImportData,
                root,
                ImageFileLocation)
            return root

else:
    print("You need to run this as part of Pycraft")
    import tkinter as tk
    from tkinter import messagebox
    root = tk.Tk()
    root.withdraw()
    messagebox.showerror(
        "Startup Fail",
        "You need to run this as part of Pycraft, please run the 'main.py' file")

    quit()
