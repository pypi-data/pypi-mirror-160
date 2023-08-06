if __name__ != "__main__":
    print("Started <Pycraft_ErrorUtils>")

    class GenerateErrorScreen:
        def __init__(self):
            pass

        def ErrorScreen(self):
            import tkinter as TKINTER
            import sys
            from tkinter import messagebox as msgbox

            try:
                BaseWindow = TKINTER.Tk()
                BaseWindow.withdraw()
                if self.Devmode == 10:
                    print(self.ErrorMessage_detailed)
                    msgbox.showerror("Pycraft closed because an error occurred",
                                         "".join(("Pycraft closed because an error occurred\n\n",
                                                  f"More Details:\n{self.ErrorMessage_detailed}")))

                else:
                    print(self.ErrorMessage)
                    msgbox.showerror("Pycraft closed because an error occurred",
                                         "".join(("Pycraft closed because an error occurred\n\n",
                                                  f"More Details:\n{self.ErrorMessage}")))

                sys.exit()
            except Exception as Message:
                sys.exit(Message)

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
