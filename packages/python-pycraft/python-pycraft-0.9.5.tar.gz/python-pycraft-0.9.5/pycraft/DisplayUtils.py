if __name__ != "__main__":
    print("Started <Pycraft_DisplayUtils>")

    class DisplayFunctionality:
        def __init__(self):
            pass

        def CoreDisplayFunctionality(self, location="Home", checkEvents=True):
            if self.UseMouseInput is False:
                self.mod_Pygame__.mouse.set_visible(False)
                if self.JoystickMouse[0] == "Right":
                    self.Mx += 3
                if self.JoystickMouse[0] == "Left":
                    self.Mx -= 3
                if self.JoystickMouse[1] == "Up":
                    self.My += 3
                if self.JoystickMouse[1] == "Down":
                    self.My -= 3
                self.mod_Pygame__.mouse.set_pos(
                    self.Mx,
                    self.My)
            else:
                self.JoystickConfirm = False
                self.Mx = self.mod_Pygame__.mouse.get_pos()[0]
                self.My = self.mod_Pygame__.mouse.get_pos()[1]
                self.mod_Pygame__.mouse.set_visible(True)

            self.realWidth = self.mod_Pygame__.display.get_window_size()[0]
            self.realHeight = self.mod_Pygame__.display.get_window_size()[1]

            if self.realWidth < 1280:
                self.mod_DisplayUtils__.DisplayUtils.GenerateMinDisplay(
                    self,
                    1280,
                    self.SavedHeight)

            if self.realHeight < 720:
                self.mod_DisplayUtils__.DisplayUtils.GenerateMinDisplay(
                    self,
                    self.SavedWidth,
                    720)

            if self.SavedWidth == self.FullscreenX:
                self.SavedWidth = 1280

            if self.SavedHeight == self.FullscreenY:
                self.SavedHeight = 720

            if self.realWidth != self.FullscreenX and self.realHeight != self.FullscreenY:
                self.SavedWidth = self.mod_Pygame__.display.get_window_size()[0]
                self.SavedHeight = self.mod_Pygame__.display.get_window_size()[1]

            self.eFPS = self.clock.get_fps()
            self.aFPS += self.eFPS
            self.Iteration += 1

            if self.UseMouseInput is False:
                if self.JoystickExit:
                    self.JoystickExit = False
                    if self.sound:
                        self.mod_SoundUtils__.PlaySound.PlayClickSound(self)
                    self.StartAnimation = True
                    self.RunTimer = 0
                    self.GoTo = location

            if self.JoystickConfirm:
                self.mousebuttondown = True
                self.JoystickConfirm = False

            if checkEvents:
                DisplayEvents = self.mod_Pygame__.event.get()
                for event in DisplayEvents:
                    if (event.type == self.mod_Pygame__.QUIT
                            or (event.type == self.mod_Pygame__.KEYDOWN
                                and event.key == self.mod_Pygame__.K_ESCAPE)):

                        self.JoystickExit = False

                        if self.sound:
                            self.mod_SoundUtils__.PlaySound.PlayClickSound(
                                self)

                        self.StartAnimation = True
                        self.RunTimer = 0
                        self.GoTo = location

                    elif event.type == self.mod_Pygame__.KEYDOWN:
                        if event.key == self.mod_Pygame__.K_SPACE and self.Devmode < 10:
                            self.Devmode += 1

                        if event.key == self.mod_Pygame__.K_q:
                            self.mod_TkinterUtils__.TkinterInfo.CreateTkinterWindow(
                                self)

                        if event.key == self.mod_Pygame__.K_F11:
                            self.mod_DisplayUtils__.DisplayUtils.UpdateDisplay(self)

                        if event.key == self.mod_Pygame__.K_x:
                            self.Devmode = 1

                return DisplayEvents


    class DisplayUtils:
        def __init__(self):
            pass


        def UpdateDisplay(self):
            self.Data_aFPS = []
            self.Data_CPUUsE = []
            self.Data_eFPS = []
            self.Data_MemUsE = []

            self.Timer = 0

            self.Data_aFPS_Max = 1
            self.Data_CPUUsE_Max = 1
            self.Data_eFPS_Max = 1
            self.Data_MemUsE_Max = 1

            try:
                try:
                    self.FullscreenX = self.mod_Pyautogui__.size()[0]
                    self.FullscreenY = self.mod_Pyautogui__.size()[1]

                    self.mod_Pygame__.display.set_icon(self.WindowIcon)

                    if self.Fullscreen is False:
                        self.Fullscreen = True
                        self.Display = self.mod_Pygame__.display.set_mode(
                            (self.SavedWidth, self.SavedHeight),
                            self.mod_Pygame__.RESIZABLE)

                    elif self.Fullscreen:
                        self.Fullscreen = False
                        self.Display = self.mod_Pygame__.display.set_mode(
                            (self.FullscreenX, self.FullscreenY),
                            self.mod_Pygame__.FULLSCREEN|
                            self.mod_Pygame__.HWSURFACE|
                            self.mod_Pygame__.DOUBLEBUF)

                except Exception as Message:
                    print("DisplayUtils > DisplayUtils > UpdateDisplay: "+ str(Message))
                    self.Fullscreen = True
                    self.SavedWidth = 1280
                    self.SavedHeight = 720
                    self.mod_Pygame__.display.quit()
                    self.mod_Pygame__.init()
                    self.Display = self.mod_Pygame__.display.set_mode(
                        (self.SavedWidth, self.SavedHeight))

                self.mod_Pygame__.display.set_icon(self.WindowIcon)
            except Exception as Message:
                self.ErrorMessage = "DisplayUtils > DisplayUtils > UpdateDisplay: "+str(Message)
                self.ErrorMessage_detailed = "".join(
                    self.mod_Traceback__.format_exception(
                        None,
                        Message,
                        Message.__traceback__))

                self.mod_ErrorUtils__.GenerateErrorScreen.ErrorScreen(self)

        def SetDisplay(self):
            self.Data_aFPS = []
            self.Data_CPUUsE = []
            self.Data_eFPS = []
            self.Data_MemUsE = []

            self.Timer = 0

            self.Data_aFPS_Max = 1
            self.Data_CPUUsE_Max = 1
            self.Data_eFPS_Max = 1
            self.Data_MemUsE_Max = 1

            try:
                try:
                    self.FullscreenX = self.mod_Pyautogui__.size()[0]
                    self.FullscreenY = self.mod_Pyautogui__.size()[1]

                    if self.Fullscreen:
                        self.Display = self.mod_Pygame__.display.set_mode(
                            (self.SavedWidth, self.SavedHeight),
                            self.mod_Pygame__.RESIZABLE)

                    elif self.Fullscreen is False:
                        self.Display = self.mod_Pygame__.display.set_mode(
                            (self.FullscreenX, self.FullscreenY),
                            self.mod_Pygame__.FULLSCREEN|
                            self.mod_Pygame__.HWSURFACE|
                            self.mod_Pygame__.DOUBLEBUF)

                except Exception as Message:
                    print("".join(
                        self.mod_Traceback__.format_exception(
                            None,
                            Message,
                            Message.__traceback__)))

                    print("DisplayUtils > DisplayUtils > SetDisplay:", Message)
                    self.SavedWidth = 1280
                    self.SavedHeight = 720
                    self.mod_Pygame__.display.quit()
                    self.mod_Pygame__.init()
                    self.Display = self.mod_Pygame__.display.set_mode(
                        (self.SavedWidth, self.SavedHeight))

                self.mod_Pygame__.display.set_icon(self.WindowIcon)
            except Exception as Message:
                self.ErrorMessage = "DisplayUtils > DisplayUtils > SetDisplay: "+str(Message)
                self.ErrorMessage_detailed = "".join(
                    self.mod_Traceback__.format_exception(
                        None,
                        Message,
                        Message.__traceback__))

                self.mod_ErrorUtils__.GenerateErrorScreen.ErrorScreen(self)


        def GenerateMinDisplay(self, width, height):
            try:
                self.Display = self.mod_Pygame__.display.set_mode(
                    (width, height),
                    self.mod_Pygame__.RESIZABLE)

                self.mod_Pygame__.display.set_icon(self.WindowIcon)
            except Exception as Message:
                self.ErrorMessage = "".join(("DisplayUtils > DisplayUtils > ",
                                             f"GenerateMinDisplay: {str(Message)}"))

                self.ErrorMessage_detailed = "".join(
                    self.mod_Traceback__.format_exception(
                        None,
                        Message,
                        Message.__traceback__))

                self.mod_ErrorUtils__.GenerateErrorScreen.ErrorScreen(self)


        def GetDisplayLocation(self):
            try:
                hwnd = self.mod_Pygame__.display.get_wm_info()["window"]

                prototype = self.mod_Ctypes__.WINFUNCTYPE(
                    self.mod_Ctypes__.wintypes.BOOL,
                    self.mod_Ctypes__.wintypes.HWND,
                    self.mod_Ctypes__.POINTER(
                        self.mod_Ctypes__.wintypes.RECT))

                paramflags = (1, "hwnd"), (2, "lprect")

                GetWindowRect = prototype(
                    ("GetWindowRect",self.mod_Ctypes__.windll.user32),
                    paramflags)

                rect = GetWindowRect(hwnd)
                return rect.left+8, rect.top+31
            except Exception:
                pass


        def GetPlayStatus(self):
            try:
                if self.mod_Pygame__.display.get_active():
                    tempFPS = self.FPS
                    self.Project_Sleeping = False
                    if not (self.Command == "Play" or self.Command == "Benchmark"):
                        if self.music:
                            self.mod_Pygame__.mixer.music.unpause()
                            if self.mod_Pygame__.mixer.music.get_busy() == 0:
                                self.mod_SoundUtils__.PlaySound.PlayInvSound(self)
                else:
                    tempFPS = 5
                    self.Project_Sleeping = True
                    self.mod_Pygame__.mixer.music.fadeout(500)

                if self.FPS_Overclock:
                    tempFPS = 2000

                return tempFPS
            except Exception as Message:
                self.ErrorMessage = "DisplayUtils > DisplayUtils > GetPlayStatus: "+str(Message)
                self.ErrorMessage_detailed = "".join(
                    self.mod_Traceback__.format_exception(
                        None,
                        Message,
                        Message.__traceback__))

                self.mod_ErrorUtils__.GenerateErrorScreen.ErrorScreen(self)


    class DisplayAnimations:
        def __init__(self):
            pass


        def FadeIn(self):
            try:
                if self.StartAnimation:
                    HideSurface = self.mod_Pygame__.Surface(
                        (self.realWidth, self.realHeight))

                    SurfaceAlpha = 255-(self.RunTimer*1000)
                    HideSurface.set_alpha(SurfaceAlpha)
                    HideSurface.fill(self.BackgroundCol)
                    self.Display.blit(
                        HideSurface,
                        (0, 100))

                    if SurfaceAlpha <= 0:
                        self.StartAnimation = False
            except Exception as Message:
                self.ErrorMessage = "DisplayUtils > DisplayAnimations > FadeIn: "+str(Message)
                self.ErrorMessage_detailed = "".join(
                    self.mod_Traceback__.format_exception(
                        None,
                        Message,
                        Message.__traceback__))

                self.mod_ErrorUtils__.GenerateErrorScreen.ErrorScreen(self)



        def FadeOut(self):
            try:
                if self.StartAnimation:
                    HideSurface = self.mod_Pygame__.Surface(
                        (self.realWidth, self.realHeight))

                    SurfaceAlpha = 255-(self.RunTimer*1000)
                    HideSurface.set_alpha(255-SurfaceAlpha)
                    HideSurface.fill(self.BackgroundCol)

                    if self.GoTo == "Credits":
                        self.Display.blit(
                            HideSurface,
                            (0, 0))
                    else:
                        self.Display.blit(
                            HideSurface,
                            (0, 100))

                    if SurfaceAlpha <= 0:
                        self.StartAnimation = False
            except Exception as Message:
                self.ErrorMessage = "DisplayUtils > DisplayAnimations > FadeOut: "+str(Message)
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
