if __name__ != "__main__":
    print("Started <Pycraft_ExBenchmark>")

    class LoadBenchmark:
        def __init__(self):
            pass

        def ExitBenchmark(self):
            self.mod_Pygame__.display.quit()
            self.mod_Pygame__.display.init()
            self.Command = "Undefined"
            self.mod_DisplayUtils__.DisplayUtils.SetDisplay(self)
            self.mod_Main__.Initialize.MenuSelector(self)

        def run(self):
            try:
                FPSlistX = []
                FPSlistY = []

                FPSlistX2 = []
                FPSlistY2 = []

                FPSlistX3 = []
                FPSlistY3 = []

                SetFPS = [15,
                          30,
                          45,
                          60,
                          75,
                          90,
                          105,
                          120,
                          135,
                          150,
                          200,
                          250,
                          300,
                          350,
                          500]

                SetFPSlength = len(SetFPS)

                self.Display = self.mod_Pygame__.display.set_mode((1280, 720))

                iteration = 0
                self.FPScounter = 0
                MaxIteration = 500

                while iteration < (500*SetFPSlength):
                    self.mod_Pygame__.display.set_caption(
                        "".join((f"Pycraft: v{self.version}: Benchmark | ",
                                 f"Running Blank Window Benchmark @ {SetFPS[self.FPScounter]} FPS")))

                    while iteration != MaxIteration:
                        if not self.clock.get_fps() == 0:
                            FPSlistX.append(iteration)
                            FPSlistY.append(self.clock.get_fps())

                        self.Display.fill(self.BackgroundCol)

                        for event in self.mod_Pygame__.event.get():
                            if (event.type == self.mod_Pygame__.QUIT or
                                (event.type == self.mod_Pygame__.KEYDOWN and
                                 (not event.key == self.mod_Pygame__.K_SPACE))):

                                LoadBenchmark.ExitBenchmark(self)

                        self.mod_Pygame__.display.flip()
                        iteration += 1
                        self.clock.tick(SetFPS[self.FPScounter])
                    self.FPScounter += 1
                    MaxIteration += 500

                self.mod_Pygame__.display.set_caption(
                    "".join((f"Pycraft: v{self.version}: ",
                             "Benchmark | Preparing Animated Benchmark")))

                iteration = 0
                self.FPScounter = 0
                MaxIteration = 500

                while iteration != 60:
                    self.Display.fill(self.BackgroundCol)

                    for event in self.mod_Pygame__.event.get():
                        if (event.type == self.mod_Pygame__.QUIT or
                            (event.type == self.mod_Pygame__.KEYDOWN and
                             (not event.key == self.mod_Pygame__.K_SPACE))):

                            LoadBenchmark.ExitBenchmark(self)

                    self.mod_Pygame__.display.flip()
                    iteration += 1
                    self.clock.tick(60)


                iteration = 0
                self.FPScounter = 0
                MaxIteration = 500

                while iteration < (500*SetFPSlength):
                    self.mod_Pygame__.display.set_caption(
                        "".join((f"Pycraft: v{self.version}: Benchmark | ",
                                 f"Running Animated Window Benchmark @ {SetFPS[self.FPScounter]} FPS")))

                    while not iteration == MaxIteration:
                        if not self.clock.get_fps() == 0:
                            FPSlistX2.append(iteration)
                            FPSlistY2.append(self.clock.get_fps())

                        self.Display.fill(self.BackgroundCol)

                        self.mod_DrawingUtils__.DrawRose.CreateRose(
                            self,
                            1,
                            1,
                            False)

                        self.mod_DrawingUtils__.DrawRose.CreateRose(
                            self,
                            1,
                            1,
                            False)

                        self.mod_DrawingUtils__.DrawRose.CreateRose(
                            self,
                            1,
                            1,
                            False)

                        self.mod_DrawingUtils__.DrawRose.CreateRose(
                            self,
                            1,
                            1,
                            False)

                        self.mod_DrawingUtils__.DrawRose.CreateRose(
                            self,
                            1,
                            1,
                            False)

                        self.mod_DrawingUtils__.DrawRose.CreateRose(
                            self,
                            1,
                            1,
                            False)

                        self.mod_DrawingUtils__.DrawRose.CreateRose(
                            self,
                            1,
                            1,
                            False)

                        self.mod_DrawingUtils__.DrawRose.CreateRose(
                            self,
                            1,
                            1,
                            False)

                        for event in self.mod_Pygame__.event.get():
                            if (event.type == self.mod_Pygame__.QUIT or
                                (event.type == self.mod_Pygame__.KEYDOWN and
                                 (not event.key == self.mod_Pygame__.K_SPACE))):

                                LoadBenchmark.ExitBenchmark(self)

                        self.mod_Pygame__.display.flip()
                        iteration += 1
                        self.clock.tick(SetFPS[self.FPScounter])
                    self.FPScounter += 1
                    MaxIteration += 500

                self.mod_Pygame__.display.set_caption(
                    "".join((f"Pycraft: v{self.version}: Benchmark | ",
                             "Preparing OpenGL Benchmark")))

                iteration = 0
                self.FPScounter = 0
                MaxIteration = 500

                while iteration != 60:
                    self.Display.fill(self.BackgroundCol)
                    for event in self.mod_Pygame__.event.get():
                        if (event.type == self.mod_Pygame__.QUIT or
                            (event.type == self.mod_Pygame__.KEYDOWN and
                             (not event.key == self.mod_Pygame__.K_SPACE))):

                            LoadBenchmark.ExitBenchmark(self)

                    self.mod_Pygame__.display.flip()
                    iteration += 1
                    self.clock.tick(60)

                self.mod_Pygame__.display.quit()
                self.mod_Pygame__.display.init()

                SharedData = self

                class Create3Dbenchmark(self.mod_Base__.BenchmarkWindow):
                    self.mod_Base__.title = "Crate"
                    self.mod_Base__.vsync = False
                    self.mod_Base__.window_size = 1280, 720

                    def __init__(self, **kwargs):
                        self.SharedData = SharedData

                        super().__init__(**kwargs)

                        if SharedData.platform == "Linux":
                            self.prog = self.load_program(
                                SharedData.mod_OS__.path.join(
                                    SharedData.base_folder,
                                    ("programs//benchmark.glsl")))

                            self.scene = self.load_scene(
                                SharedData.mod_OS__.path.join(
                                    SharedData.base_folder,
                                    ("Resources//Benchmark_Resources//Crate.obj")))

                            self.texture = self.load_texture_2d(
                                SharedData.mod_OS__.path.join(
                                    SharedData.base_folder,
                                    ("Resources//Benchmark_Resources//Crate.png")))

                        else:
                            self.prog = self.load_program(
                                SharedData.mod_OS__.path.join(
                                    SharedData.base_folder,
                                    ("programs\\benchmark.glsl")))

                            self.scene = self.load_scene(
                                SharedData.mod_OS__.path.join(
                                    SharedData.base_folder,
                                    ("Resources\\Benchmark_Resources\\Crate.obj")))

                            self.texture = self.load_texture_2d(
                                SharedData.mod_OS__.path.join(
                                    SharedData.base_folder,
                                    ("Resources\\Benchmark_Resources\\Crate.png")))

                        self.mvp = self.prog["Mvp"]
                        self.light = self.prog["Light"]

                        self.vao = self.scene.root_nodes[0].mesh.vao.instance(self.prog)

                        self.SetFPS = SetFPS
                        self.SetFPSlength = SetFPSlength

                        self.FPSlistX3 = FPSlistX3
                        self.FPSlistY3 = FPSlistY3

                        self.iteration = 0
                        self.MaxIteration = 500

                        self.wnd.title = "".join((f"Pycraft: v{self.SharedData.version}: Benchmark | ",
                                                  "Running OpenGL Benchmark ",
                                                  f"@ {self.SetFPS[self.SharedData.FPScounter]} FPS"))

                        self.PreviousFPS = 15

                        self.aFPS = 15

                        self.time = 0

                        while self.iteration < 500*self.SetFPSlength:
                            RunTime = self.SharedData.mod_Time__.perf_counter()
                            try:
                                if self.iteration == self.MaxIteration:
                                    self.SharedData.FPScounter += 1
                                    self.MaxIteration += 500
                                    if self.SharedData.FPScounter <= self.SetFPSlength:
                                        self.wnd.title = "".join((f"Pycraft: v{self.SharedData.version}: ",
                                            "Benchmark | Running OpenGL Benchmark ",
                                            f"@ {self.SetFPS[self.SharedData.FPScounter]} FPS"))

                                angle = self.time
                                self.ctx.clear(
                                    0.0,
                                    0.0,
                                    0.0)

                                self.ctx.enable(self.SharedData.mod_ModernGL__.DEPTH_TEST)

                                camera_pos = (
                                    self.SharedData.mod_Numpy__.cos(angle) * 3.0,
                                    self.SharedData.mod_Numpy__.sin(angle) * 3.0,
                                    2.0)

                                proj = self.SharedData.mod_Pyrr_Matrix44_.perspective_projection(
                                    45.0,
                                    self.aspect_ratio,
                                    0.1,
                                    100.0)

                                lookat = self.SharedData.mod_Pyrr_Matrix44_.look_at(
                                    camera_pos,
                                    (0.0, 0.0, 0.5),
                                    (0.0, 0.0, 1.0),
                                )

                                self.mvp.write((proj * lookat).astype("f4"))
                                self.light.value = camera_pos
                                self.texture.use()
                                self.vao.render()
                                self.SharedData.mod_Time__.sleep(1/(self.SetFPS[self.SharedData.FPScounter]))

                                eFPS = 1/(self.SharedData.mod_Time__.perf_counter()-RunTime)
                                self.aFPS = (eFPS+self.PreviousFPS)/2
                                self.PreviousFPS = eFPS

                                if not eFPS == 0 and len(self.FPSlistX3) < 7500:
                                    self.FPSlistX3.append(self.iteration)
                                    self.FPSlistY3.append(self.aFPS)

                                self.iteration += 1
                                self.time += SharedData.mod_Time__.perf_counter()-RunTime
                                self.wnd.swap_buffers()

                            except Exception as Message:
                                try:
                                    self.wnd.close()
                                    self.wnd.destroy()
                                except:
                                    pass

                                if str(Message) != "'NoneType' object has no attribute 'flip'":
                                    SharedData.ErrorMessage = "".join(("ExBenchmark > ",
                                                                f"Create3Dbenchmark > {str(Message)}"))

                                    SharedData.ErrorMessage_detailed = "".join(
                                        SharedData.mod_Traceback__.format_exception(
                                            None,
                                            Message,
                                            Message.__traceback__))

                                    self.SharedData.mod_ErrorUtils__.GenerateErrorScreen.ErrorScreen(
                                        SharedData)

                                self.SharedData.Command = "Undefined"
                                self.SharedData.mod_Pygame__.display.quit()
                                self.SharedData.mod_Pygame__.init()
                                self.SharedData.mod_DisplayUtils__.DisplayUtils.SetDisplay(self.SharedData)
                                self.SharedData.mod_Main__.Initialize.MenuSelector(self.SharedData)

                        else:
                            self.wnd.close()
                            self.wnd.destroy()

                self.mod_ModernGL_window_.run_window_config(Create3Dbenchmark)
                self.mod_DisplayUtils__.DisplayUtils.SetDisplay(self)
            except Exception as Message:
                if not (str(Message) == "WindowConfig.render not implemented" or
                        str(Message) == "'NoneType' object has no attribute 'flip'"):

                    self.ErrorMessage = "ExBenchmark > LoadBenchmark > run: "+str(Message)
                    self.ErrorMessage_detailed = "".join(
                        self.mod_Traceback__.format_exception(
                            None,
                            Message,
                            Message.__traceback__))

                    self.mod_ErrorUtils__.GenerateErrorScreen.ErrorScreen(self)

                else:
                    return FPSlistX, FPSlistY, FPSlistX2, FPSlistY2, FPSlistX3, FPSlistY3
            else:
                return FPSlistX, FPSlistY, FPSlistX2, FPSlistY2, FPSlistX3, FPSlistY3

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
