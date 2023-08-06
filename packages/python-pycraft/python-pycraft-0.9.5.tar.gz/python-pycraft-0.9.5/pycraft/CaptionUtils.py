if __name__ != "__main__":
    print("Started <Pycraft_CaptionUtils>")

    class GenerateCaptions:
        def __init__(self):
            pass

        def GetLoadingCaption(self, num):
            try:
                if num == 0:
                    self.mod_Pygame__.display.set_caption(f"Pycraft: v{self.version}: Loading (-)")
                elif num == 1:
                    self.mod_Pygame__.display.set_caption(f"Pycraft: v{self.version}: Loading (\)")
                elif num == 2:
                    self.mod_Pygame__.display.set_caption(f"Pycraft: v{self.version}: Loading (|)")
                elif num == 3:
                    self.mod_Pygame__.display.set_caption(f"Pycraft: v{self.version}: Loading (/)")
                else:
                    self.mod_Pygame__.display.set_caption(f"Pycraft: v{self.version}: Loading")
                self.mod_Pygame__.display.update()
            except Exception as Message:
                self.ErrorMessage = "".join(("CaptionUtils > GenerateCaptions ",
                                             f"> GetLoadingCaption: {str(Message)}"))

                self.ErrorMessage_detailed = "".join(
                    self.mod_Traceback__.format_exception(
                        None,
                        Message,
                        Message.__traceback__))

                self.mod_ErrorUtils__.GenerateErrorScreen.ErrorScreen(self)


        def GetNormalCaption(self, location):
            try:
                if self.Devmode >= 5 and self.Devmode <= 9:
                    self.mod_Pygame__.display.set_caption(
                        "".join((f"Pycraft: v{self.version}: {location}",
                                 " | ",
                                 f"you are: {10-self.Devmode} steps away from being a developer")))

                elif self.Devmode == 10:
                    hours = int((self.PlayTime/60)/60)
                    minutes = int(self.PlayTime/60)
                    seconds = int(self.PlayTime)

                    Position = f"{round(self.X, 2)}, {round(self.Y, 2)}, {round(self.Z, 2)}"
                    Velocity = f"{self.Total_move_x}, {self.Total_move_y}, {self.Total_move_z}"

                    time = f"{hours} : {minutes} : {seconds}"

                    if self.FPS_Overclock:
                        try:
                            FPS = "".join((f"FPS: 2000 eFPS: {int(self.eFPS)} ",
                                           f"aFPS: N/A Iteration: {self.Iteration} | "))

                            self.mod_Pygame__.display.set_caption(
                                "".join((f"Pycraft: v{self.version}: {location} | ",
                                         "Dev Mode | ",
                                         f"Play Time: {time} | ",
                                         f"Pos: {Position} | ",
                                         f"V: {Velocity} | ",
                                         FPS,
                                         f"MemUsE: {int(self.CurrentMemoryUsage)}% | ",
                                         f"CPUUsE: {self.mod_Psutil__.cpu_percent()}% | ",
                                         f"Theme: {self.theme} | ",
                                         f"Thread Count: {self.mod_Threading__.active_count()}")))

                        except:
                            FPS = f"FPS: 2000 eFPS: NaN* aFPS: N/A Iteration: {self.Iteration} | "

                            self.mod_Pygame__.display.set_caption(
                                "".join((f"Pycraft: v{self.version}: {location} | ",
                                         "Dev Mode | ",
                                         f"Play Time: {time} | ",
                                         f"Pos: {Position} | ",
                                         f"V: {Velocity} | ",
                                         FPS,
                                         f"MemUsE: {int(self.CurrentMemoryUsage)}% | ",
                                         f"CPUUsE: {self.mod_Psutil__.cpu_percent()}% | ",
                                         f"Theme: {self.theme} | ",
                                         f"Thread Count: {self.mod_Threading__.active_count()}")))

                    else:
                        FPS = "".join((f"FPS: {self.FPS} eFPS: {int(self.eFPS)} ",
                                       f"aFPS: {int(self.aFPS/self.Iteration)} ",
                                       f"Iteration: {self.Iteration} | "))

                        self.mod_Pygame__.display.set_caption(
                            "".join((f"Pycraft: v{self.version}: {location} | ",
                                     "Dev Mode | ",
                                     f"Play Time: {time} | ",
                                     f"Pos: {Position} | ",
                                     f"V: {Velocity} | ",
                                     FPS,
                                     f"MemUsE: {int(self.CurrentMemoryUsage)}% | ",
                                     f"CPUUsE: {self.mod_Psutil__.cpu_percent()}% | ",
                                     f"Theme: {self.theme} | ",
                                     f"Thread Count: {self.mod_Threading__.active_count()}")))

                else:
                    self.mod_Pygame__.display.set_caption(f"Pycraft: v{self.version}: {location}")
            except Exception as Message:
                self.ErrorMessage = "".join(("CaptionUtils > GenerateCaptions ",
                                             f"> GetNormalCaption: {str(Message)}"))

                self.ErrorMessage_detailed = "".join(
                    self.mod_Traceback__.format_exception(
                        None,
                        Message,
                        Message.__traceback__))

                self.mod_ErrorUtils__.GenerateErrorScreen.ErrorScreen(self)


        def GetOpenGLCaption(self, GameData):
            try:
                if self.Devmode >= 5 and self.Devmode <= 9:
                    GameData.wnd.title = "".join((f"Pycraft: v{self.version}: Playing | ",
                                                  f"you are: {10-self.Devmode} steps ",
                                                  "away from being a developer"))

                elif self.Devmode == 10:
                    time_seconds = int(self.PlayTime)
                    time_minutes = int(self.PlayTime/60)
                    time_hours = int((self.PlayTime/60)/60)

                    minutes = time_minutes-(60*time_hours)
                    seconds = time_seconds-(60*time_minutes)

                    time = f"{time_hours} : {minutes} : {seconds}"

                    PlayTime = "".join((f"Play Time: {time} Game Time: ",
                                        f"{round(GameData.Time_Percent, 1)} ",
                                        f": {GameData.day-1} | "))

                    Position = "".join((f"Pos: {round(self.X, 2)}, ",
                                        f"{round(self.Y, 2)}, ",
                                        f"{round(self.Z, 2)} | "))

                    Velocity = "".join((f"V: {self.Total_move_x}, ",
                                        f"{self.Total_move_y}, ",
                                        f"{self.Total_move_z} | "))

                    MemUse = f"MemUsE: {int(self.CurrentMemoryUsage)}% | "

                    CPUUsE = f"CPUUsE: {self.mod_Psutil__.cpu_percent()}% | "

                    ThreadCount = f"Thread Count: {self.mod_Threading__.active_count()}"

                    if self.FPS_Overclock:
                        try:
                            FPS = "".join((f"FPS: 2000 eFPS: {int(self.eFPS)} ",
                                           f"aFPS: N/A Iteration: {self.Iteration} | "))

                            GameData.wnd.title = "".join((f"Pycraft: v{self.version}: Playing ",
                                                          "| Dev Mode | ",
                                                          PlayTime,
                                                          f"Weather: {GameData.weather} | ",
                                                          Position,
                                                          Velocity,
                                                          FPS,
                                                          MemUse,
                                                          CPUUsE,
                                                          ThreadCount))
                        except:
                            FPS = f"FPS: 2000 eFPS: NaN* aFPS: N/A Iteration: {self.Iteration} | "

                            GameData.wnd.title = "".join((f"Pycraft: v{self.version}: Playing ",
                                                          "| Dev Mode | ",
                                                          PlayTime,
                                                          f"Weather: {GameData.weather} | ",
                                                          Position,
                                                          Velocity,
                                                          FPS,
                                                          MemUse,
                                                          CPUUsE,
                                                          ThreadCount))
                    else:
                        try:
                            FPS = "".join((f"FPS: {self.FPS} eFPS: ",
                                    f"{int(self.eFPS)} aFPS: ",
                                    f"{int(self.aFPS/self.Iteration)} ",
                                    f"Iteration: {self.Iteration} | "))

                            GameData.wnd.title = "".join((f"Pycraft: v{self.version}: Playing ",
                                                          "| Dev Mode | ",
                                                          PlayTime,
                                                          f"Weather: {GameData.weather} | ",
                                                          Position,
                                                          Velocity,
                                                          FPS,
                                                          MemUse,
                                                          CPUUsE,
                                                          ThreadCount))

                        except:
                            FPS = "".join((f"FPS: {self.FPS} eFPS: ",
                                    f"{int(self.eFPS)} aFPS: ",
                                    f"{int(self.aFPS/self.Iteration)} ",
                                    f"Iteration: {self.Iteration} | "))

                            GameData.wnd.title = "".join((f"Pycraft: v{self.version}: Playing ",
                                                          "| Dev Mode | ",
                                                          PlayTime,
                                                          f"Weather: {GameData.weather} | ",
                                                          Position,
                                                          Velocity,
                                                          FPS,
                                                          MemUse,
                                                          CPUUsE,
                                                          ThreadCount))
                else:
                    GameData.wnd.title = f"Pycraft: v{self.version}: Playing"
            except Exception as Message:
                self.ErrorMessage = "".join(("CaptionUtils > GenerateCaptions ",
                                             f"> GetNormalCaption: {str(Message)}"))

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
