if __name__ != "__main__":
    print("Started <Pycraft_PycraftStartupTest>")

    class StartupTest:
        def __init__(self):
            pass

        def PycraftSelfTest(self):
            try:
                self.mod_Pygame__.display.set_icon(self.WindowIcon)

                SDLversion = self.mod_Pygame__.get_sdl_version()[0]
                RAM = ((self.mod_Psutil__.virtual_memory().available)/1000000)
                # expressed in MB
                OpenGLversion = self.mod_ModernGL_window_.conf.settings.WINDOW["gl_version"]

                if OpenGLversion[0] < 2 and OpenGLversion[1] >= 8:
                    root = self.mod_Tkinter__tk.Tk()
                    root.withdraw()
                    self.mod_Tkinter_messagebox_.showerror(
                        "Invalid OpenGL version",
                        "".join((f"OpenGL version: {OpenGLversion[0]}.{OpenGLversion[1]} ",
                                 "is not supported; try a version greater than 2.7")))

                    quit()

                if SDLversion < 2:
                    root = self.mod_Tkinter__tk.Tk()
                    root.withdraw()
                    self.mod_Tkinter_messagebox_.showerror(
                        "Invalid SDL version",
                        "".join((f"SDL version: {SDLversion} is not supported; try a ",
                                 "version greater than or equal to 2")))

                    quit()

                if RAM < 260:
                    root = self.mod_Tkinter__tk.Tk()
                    root.withdraw()
                    self.mod_Tkinter_messagebox_.showerror(
                        "Minimum system requirements not met",
                        "".join(("Your system does not meet the minimum 260mb free ",
                                 "memory specification needed to play this game")))

                    quit()

                if self.mod_Sys__.platform == "win32" or self.mod_Sys__.platform == "win64":
                    self.mod_OS__.environ["SDL_VIDEO_CENTERED"] = "1"
            except Exception as Message:
                self.ErrorMessage = "".join(("PycraftStartupTest > StartupTest > ",
                                             f"PycraftSelfTest: {str(Message)}"))

                self.ErrorMessage_detailed = "".join(
                    self.mod_Traceback__.format_exception(
                        None,
                        Message,
                        Message.__traceback__))

                self.mod_ErrorUtils__.GenerateErrorScreen.ErrorScreen(self)


        def PycraftResourceTest(self):
            try:
                if (self.currentDate != self.lastRun or
                        self.crash or
                        self.RunFullStartup):

                    if self.ResourceCheckTime[0] >= 25:
                        self.ResourceCheckTime = [0, 0]

                    self.mod_ModernGL_window_.activate_context(
                        self.Display,
                        self.mod_ModernGL__.create_standalone_context())

                    StartTime = self.mod_Time__.perf_counter()
                    if self.platform == "Linux":
                        for trackID in range(6):
                            self.mod_Pygame__.mixer.Sound(
                                self.mod_OS__.path.join(
                                    self.base_folder,
                                        (f"Resources//G3_Resources//GameSounds//footstep//footsteps{trackID}.wav")))

                        self.mod_Pygame__.mixer.Sound(
                            self.mod_OS__.path.join(
                                self.base_folder,
                                    ("Resources//G3_Resources//GameSounds//FieldAmb.ogg")))

                        for trackID in range(11):
                            self.mod_Pygame__.mixer.Sound(
                                self.mod_OS__.path.join(
                                    self.base_folder,
                                    (f"Resources//G3_Resources//GameSounds//thunder//thunder{trackID}.ogg")))

                        self.mod_Pygame__.image.load(
                            self.mod_OS__.path.join(
                                self.base_folder,
                                "Resources//General_Resources//selectorICONlight.jpg")).convert()

                        self.mod_Pygame__.image.load(
                            self.mod_OS__.path.join(
                                self.base_folder,
                                "Resources//General_Resources//selectorICONdark.jpg")).convert()

                        SkyPath = "Resources//G3_Resources//skysphere//ClearSkyTransition.gif"
                        self.mod_Pygame__.image.load(
                            self.mod_OS__.path.join(
                                self.base_folder,
                                SkyPath)).convert()

                        self.mod_Pygame__.image.load(
                            self.mod_OS__.path.join(
                                self.base_folder,
                                "Resources//G3_Resources//map//GrassTexture.png")).convert()

                        self.mod_Pygame__.image.load(
                            self.mod_OS__.path.join(
                                self.base_folder,
                                "Resources//Benchmark_Resources//Crate.png")).convert()

                        self.mod_Pygame__.mixer.music.load(
                            self.mod_OS__.path.join(
                                self.base_folder,
                                ("Resources//General_Resources//InventoryGeneral.ogg")))

                        self.mod_Pygame__.mixer.music.load(
                            self.mod_OS__.path.join(
                                self.base_folder,
                                ("Resources//General_Resources//Click.ogg")))

                        self.mod_ModernGL_window_.WindowConfig.load_scene(
                            self.mod_ModernGL_window_.WindowConfig,
                            self.mod_OS__.path.join(
                                self.base_folder,
                                ("Resources//G3_Resources//map//map.obj")),
                            cache=True)

                        self.mod_ModernGL_window_.WindowConfig.load_scene(
                            self.mod_ModernGL_window_.WindowConfig,
                            self.mod_OS__.path.join(
                                self.base_folder,
                                ("Resources//Benchmark_Resources//Crate.obj")),
                            cache=True)
                            
                    else:
                        for trackID in range(6):
                            self.mod_Pygame__.mixer.Sound(
                                self.mod_OS__.path.join(
                                    self.base_folder,
                                        (f"Resources\\G3_Resources\\GameSounds\\footstep\\footsteps{trackID}.wav")))

                        self.mod_Pygame__.mixer.Sound(
                            self.mod_OS__.path.join(
                                self.base_folder,
                                    ("Resources\\G3_Resources\\GameSounds\\FieldAmb.ogg")))

                        for trackID in range(11):
                            self.mod_Pygame__.mixer.Sound(
                                self.mod_OS__.path.join(
                                    self.base_folder,
                                    (f"Resources\\G3_Resources\\GameSounds\\thunder\\thunder{trackID}.ogg")))

                        self.mod_Pygame__.image.load(
                            self.mod_OS__.path.join(
                                self.base_folder,
                                "Resources\\General_Resources\\selectorICONlight.jpg")).convert()

                        self.mod_Pygame__.image.load(
                            self.mod_OS__.path.join(
                                self.base_folder,
                                "Resources\\General_Resources\\selectorICONdark.jpg")).convert()

                        SkyPath = "resources\\G3_Resources\\skysphere\\ClearSkyTransition.gif"
                        self.mod_Pygame__.image.load(
                            self.mod_OS__.path.join(
                                self.base_folder,
                                SkyPath)).convert()

                        self.mod_Pygame__.image.load(
                            self.mod_OS__.path.join(
                                self.base_folder,
                                "Resources\\G3_Resources\\map\\GrassTexture.png")).convert()

                        self.mod_Pygame__.image.load(
                            self.mod_OS__.path.join(
                                self.base_folder,
                                "Resources\\Benchmark_Resources\\Crate.png")).convert()

                        self.mod_Pygame__.mixer.music.load(
                            self.mod_OS__.path.join(
                                self.base_folder,
                                ("Resources\\General_Resources\\InventoryGeneral.ogg")))

                        self.mod_Pygame__.mixer.music.load(
                            self.mod_OS__.path.join(
                                self.base_folder,
                                ("Resources\\General_Resources\\Click.ogg")))

                        self.mod_ModernGL_window_.WindowConfig.load_scene(
                            self.mod_ModernGL_window_.WindowConfig,
                            self.mod_OS__.path.join(
                                self.base_folder,
                                ("Resources\\G3_Resources\\map\\map.obj")),
                            cache=True)

                        self.mod_ModernGL_window_.WindowConfig.load_scene(
                            self.mod_ModernGL_window_.WindowConfig,
                            self.mod_OS__.path.join(
                                self.base_folder,
                                ("Resources\\Benchmark_Resources\\Crate.obj")),
                            cache=True)

                    self.AnimateLogo = True
                    self.CurrentResourceCheckTime = self.mod_Time__.perf_counter()-StartTime
            except Exception as Message:
                self.ErrorMessage = "".join(("PycraftStartupTest > StartupTest > ",
                                             f"PycraftResourceTest: {str(Message)}"))

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
