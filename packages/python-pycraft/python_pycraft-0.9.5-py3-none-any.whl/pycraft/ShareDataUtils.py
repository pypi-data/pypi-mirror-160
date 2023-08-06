if __name__ != "__main__":
    print("Started <Pycraft_ShareDataUtil>")

    class Share:
        def __init__(self):
            pass

        def initialize(Data):
            try:
                global Class_Startup_variables
                Class_Startup_variables = Data
            except Exception as Message:
                self.ErrorMessage = "ShareDataUtils > Share > initialize: "+str(Message)

                self.ErrorMessage_detailed = "".join(
                    self.mod_Traceback__.format_exception(
                        None,
                        Message,
                        Message.__traceback__))

                self.mod_ErrorUtils__.GenerateErrorScreen.ErrorScreen(self)

        def initialize_controller(Data):
            try:
                global Controller
                Controller = Data
            except Exception as Message:
                self.ErrorMessage = "ShareDataUtils > Share > initialize_controller: "+str(Message)

                self.ErrorMessage_detailed = "".join(
                    self.mod_Traceback__.format_exception(
                        None,
                        Message,
                        Message.__traceback__))

                self.mod_ErrorUtils__.GenerateErrorScreen.ErrorScreen(self)

        def initialize_controller_game(Data):
            try:
                global Game_SharedData
                Game_SharedData = Data
            except Exception as Message:
                self.ErrorMessage = "".join(("ShareDataUtils > Share > ",
                                             f"initialize_controller_game: {str(Message)}"))

                self.ErrorMessage_detailed = "".join(
                    self.mod_Traceback__.format_exception(
                        None,
                        Message,
                        Message.__traceback__))

                self.mod_ErrorUtils__.GenerateErrorScreen.ErrorScreen(self)

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
