if __name__ != "__main__":
    print("Started <Pycraft_ThreadingUtils>")

    class ThreadingUtils:
        def __init__(self):
            pass

        def StartVariableChecking(self):
            try:
                while True:
                    if self.Iteration > 1000:
                        self.aFPS = (self.aFPS/self.Iteration)
                        self.Iteration = 1

                    if self.FPS < 15 or self.FPS > 500:
                        print("".join(("ThreadingUtil > ThreadingUtils > ",
                                       "StartVariableChecking: 'self.FPS' ",
                                       "variable contained an invalid value, ",
                                       f"this has been reset to 60 from {self.FPS} previously")))
                        self.FPS = 60

                    else:
                        if self.FPS_Overclock is False:
                            self.FPS = int(self.FPS)

                    if self.FPS_Overclock is False:
                        self.eFPS = int(self.eFPS)

                    else:
                        if self.aFPS == float("inf"):
                            self.aFPS = 1
                            self.Iteration = 1

                    if self.Command == "Settings":
                        self.MovementSpeed = 1

                    else:
                        self.MovementSpeed = 3

                    self.mod_Time__.sleep(1)
            except Exception as Message:
                print("'Thread_StartLongThread' has stopped")
                self.ErrorMessage = "".join(("ThreadingUtils > ThreadingUtils ",
                                             f"> StartVariableChecking: {str(Message)}"))

                self.ErrorMessage_detailed = "".join(
                    self.mod_Traceback__.format_exception(
                        None,
                        Message,
                        Message.__traceback__))

                self.mod_ErrorUtils__.GenerateErrorScreen.ErrorScreen(self)
            finally:
                print("'Thread_StartLongThread' has stopped")

        def StartCPUlogging(self):
            try:
                while True:
                    if self.Devmode == 10:
                        if self.Timer >= 2:
                            CPUPercent = self.mod_Psutil__.cpu_percent(0.2)
                            if CPUPercent > self.Data_CPUUsE_Max:
                                self.Data_CPUUsE_Max = CPUPercent

                            self.Data_CPUUsE.append([
                                ((self.realWidth/2)+100)+(self.Timer),
                                200-(2)*CPUPercent])

                        else:
                            self.mod_Time__.sleep(0.2)

                    else:
                        self.mod_Time__.sleep(1)
            except Exception as Message:
                print("'Thread_GetCPUMetrics' has stopped")
                self.ErrorMessage = "".join(("ThreadingUtils > ThreadingUtils ",
                                             f"> StartCPUlogging: {str(Message)}"))

                self.ErrorMessage_detailed = "".join(
                    self.mod_Traceback__.format_exception(
                        None,
                        Message,
                        Message.__traceback__))

                self.mod_ErrorUtils__.GenerateErrorScreen.ErrorScreen(self)
            finally:
                print("'Thread_GetCPUMetrics' has stopped")


        def AdaptiveMode(self):
            try:
                while True:
                    if self.SettingsPreference == "Adaptive":
                        ProcessPercent = self.mod_Psutil__.Process().cpu_percent(0.1)
                        CPUPercent = self.mod_Psutil__.cpu_percent(0.1)

                        try:
                            gpus = self.mod_GPUtil__.getGPUs()

                            GPUPercent = 0
                            NumOfGPUs = 0

                            for gpu in gpus:
                                NumOfGPUs += 1
                                GPUPercent += gpu.load*100

                            GPUPercent = GPUPercent/NumOfGPUs

                        except:
                            GPUPercent = CPUPercent

                        if CPUPercent > 75 and self.FPS > 25:
                            self.FPS -= 1
                            if CPUPercent > 90 and self.FPS > 25:
                                self.FPS -= 9

                        elif ProcessPercent > 50 and self.FPS > 25:
                            self.FPS -= 1
                            if ProcessPercent > 75 and self.FPS > 25:
                                self.FPS -= 9

                        else:
                            if GPUPercent > 50 and self.FPS > 25:
                                self.FPS -= 1
                                if GPUPercent > 75 and self.FPS > 25:
                                    self.FPS -= 9

                            else:
                                if self.FPS < 500:
                                    self.FPS += 1
                    else:
                        self.mod_Time__.sleep(1)
            except Exception as Message:
                print("'Thread_AdaptiveMode' has stopped")
                self.ErrorMessage = "ThreadingUtils > ThreadingUtils > AdaptiveMode: "+str(Message)

                self.ErrorMessage_detailed = "".join(
                    self.mod_Traceback__.format_exception(
                        None,
                        Message,
                        Message.__traceback__))

                self.mod_ErrorUtils__.GenerateErrorScreen.ErrorScreen(self)
            finally:
                print("'Thread_AdaptiveMode' has stopped")

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
