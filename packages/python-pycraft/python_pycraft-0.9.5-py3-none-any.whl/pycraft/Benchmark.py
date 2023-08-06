if __name__ != "__main__":
    print("Started <Pycraft_Benchmark>")

    class GenerateBenchmarkMenu:
        def __init__(self):
            pass

        def Benchmark(self):
            try:
                self.mod_Pygame__.mixer.music.fadeout(500)

                self.mod_Pygame__.display.set_caption(f"Pycraft: v{self.version}: Benchmark")

                if self.platform == "Linux":
                    self.VersionFont = self.mod_Pygame__.font.Font(
                        self.mod_OS__.path.join(
                            self.base_folder, ("Fonts//Book Antiqua.ttf")), 15)

                    InfoTitleFont = self.mod_Pygame__.font.Font(
                        self.mod_OS__.path.join(
                            self.base_folder, ("Fonts//Book Antiqua.ttf")), 35)

                    DataFont = self.mod_Pygame__.font.Font(
                        self.mod_OS__.path.join(
                            self.base_folder, ("Fonts//Book Antiqua.ttf")), 15)

                    DetailsFont = self.mod_Pygame__.font.Font(
                        self.mod_OS__.path.join(
                            self.base_folder, ("Fonts//Book Antiqua.ttf")), 20)

                    InfoDetailsFont = self.mod_Pygame__.font.Font(
                        self.mod_OS__.path.join(
                            self.base_folder, ("Fonts//Book Antiqua.ttf")), 15)

                else:
                    self.VersionFont = self.mod_Pygame__.font.Font(
                        self.mod_OS__.path.join(
                            self.base_folder, ("Fonts\\Book Antiqua.ttf")), 15)

                    InfoTitleFont = self.mod_Pygame__.font.Font(
                        self.mod_OS__.path.join(
                            self.base_folder, ("Fonts\\Book Antiqua.ttf")), 35)

                    DataFont = self.mod_Pygame__.font.Font(
                        self.mod_OS__.path.join(
                            self.base_folder, ("Fonts\\Book Antiqua.ttf")), 15)

                    DetailsFont = self.mod_Pygame__.font.Font(
                        self.mod_OS__.path.join(
                            self.base_folder, ("Fonts\\Book Antiqua.ttf")), 20)

                    InfoDetailsFont = self.mod_Pygame__.font.Font(
                        self.mod_OS__.path.join(
                            self.base_folder, ("Fonts\\Book Antiqua.ttf")), 15)

                TitleFont = self.TitleFont.render(
                    "Pycraft",
                    self.aa,
                    self.FontCol)

                TitleWidth = TitleFont.get_width()

                BenchmarkFont = InfoTitleFont.render(
                    "Benchmark",
                    self.aa,
                    self.SecondFontCol)

                FPSinfoTEXT = DetailsFont.render(
                    "FPS benchmark results",
                    self.aa,
                    self.FontCol)
                FPSinfoTEXTWidth = FPSinfoTEXT.get_width()

                FILEinfoTEXT = DetailsFont.render(
                    "Read test results",
                    self.aa,
                    self.FontCol)
                FILEinfoTEXTWidth = FILEinfoTEXT.get_width()

                HARDWAREinfoTEXT = DetailsFont.render(
                    "Hardware results",
                    self.aa,
                    self.FontCol)
                HARDWAREinfoTEXTwidth = HARDWAREinfoTEXT.get_width()

                SixtyFPSData = DataFont.render(
                    "60 Hz",
                    self.aa,
                    self.AccentCol)

                OneFourFourFPSData = DataFont.render(
                    "144 Hz",
                    self.aa,
                    self.AccentCol)

                TwoFortyFPSData = DataFont.render(
                    "240 Hz",
                    self.aa,
                    self.AccentCol)

                BenchmarkIntroString = ["".join(("Welcome to the Benchmark section; ",
                                                 "press SPACE to continue, or any ",
                                                 "other key to leave at any time ")),
                    " ",
                    "Purpose",
                    "The Benchmark section is designed for a few tasks:",
                    "".join(("1. To give an insight into the performance ",
                            "you will likely get when playing the ",
                            "project, which you can then use to ",
                            "change settings.")),

                    "".join(("2. The data collected in the Benchmark ",
                             "section can be used for automating control ",
                             "of settings automatically when ADAPTIVE ",
                             "mode is selected in settings.")),

                    "".join(("3. To give a repeatable demonstration ",
                             "of how the project performs with your ",
                             "current hardware setup or software configuration.")),
                    " ",
                    "Structure",
                    "".join(("The Benchmark will automatically run a ",
                             "variety of tests, this includes a disk ",
                             "read check, as well as a CPU and GPU ",
                             "based load. In the order of occurrence:")),
                    " ",
                    "".join(("1. Once the user has initiated the ",
                             "benchmark (by pressing SPACE), a small ",
                             "amount of information is collected on ",
                             "the hardware your device is running, ",
                             "we try to obtain the CPU's name, as ",
                             "well as its max clock speed, as well as ",
                             "the amount of available memory and how ",
                             "much is used. This is used solely for ",
                             "the results GUI at the end of the menu ",
                             "and is not stored or shared anywhere).")),

                    "".join(("2. Next we enter 1 of 3 graphics oriented ",
                             "tests, starting with a blank screen test ",
                             "to establish a baseline.")),

                    "".join(("3. Then we enter test 2 of the 3 graphics ",
                             "test, this is much more CPU intensive, ",
                             "as lots more data is being processed ",
                             "and drawn to the display.")),

                    "".join(("4. To conclude the graphics test, we enter ",
                             "graphics test 3, this tests 3D performance ",
                             "as well as basic lighting, it is likely ",
                             "your device will get a very good score here ",
                             "as this is very GPU dependant but not ",
                             "difficult to run.")),

                    "".join(("5. Finally we enter a disk read test, in ",
                             "which a 1 MB file is read over a period ",
                             "of time to establish a rough indication ",
                             "of drive performance.")),
                    " ",
                    "Results",
                    "".join(("Once the series of tests has completed, ",
                             "you will be shown a screen that displays ",
                             "your results, listing the scores (minimum ",
                             "and maximum) for the graphics tests, as ",
                             "well as displaying them on a line graph. ",
                             "It is at this point that you are given the ",
                             "results of the disk read test, as well as ",
                             "the information on the hardware in your ",
                             "system, which we collected earlier.")),
                    " ",
                    "Important things to note",
                    "".join(("During this test, the open window may ",
                             "appear unresponsive, or that nothing is ",
                             "happening, you can observe that the ",
                             "caption details some information on the ",
                             "test what section the process is on, if ",
                             "the details change after a period of time ",
                             "then the window is responding. You may ",
                             "also observer your device heating up, ",
                             "this array of tests is designed to ",
                             "challenge and push your hardware, ",
                             "it is unlikely that your device ",
                             "will reach these temperatures whilst ",
                             "playing the game, but the Benchmark is ",
                             "engineered so that the more CPU/GPU ",
                             "intensive tests are quicker, to avoid ",
                             "damage to hardware. The only data ",
                             "collected by this benchmark is scores ",
                             "on how your system has done, which ",
                             "can be used in the ADAPTIVE pre-set ",
                             "in settings, where settings are ",
                             "toggled automatically based on your ",
                             "performance in this test. No data ",
                             "is shared externally."))]

                stage = 0

                resize = False

                while True:
                    StartTime = self.mod_Time__.perf_counter()

                    self.mod_DisplayUtils__.DisplayFunctionality.CoreDisplayFunctionality(
                        self, checkEvents=False)

                    if stage == -1:
                        pass

                    if stage == 0:
                        self.Display.fill(self.BackgroundCol)
                        cover_Rect = self.mod_Pygame__.Rect(
                            0,
                            0,
                            1280,
                            90)

                        self.mod_Pygame__.draw.rect(
                            self.Display,
                            self.BackgroundCol,
                            cover_Rect)

                        self.Display.blit(
                            TitleFont,
                            ((self.realWidth-TitleWidth)/2, 0))

                        self.Display.blit(
                            BenchmarkFont,
                            (((self.realWidth-TitleWidth)/2)+65, 50))

                        Ypos = 100
                        for i in range(len(BenchmarkIntroString)):
                            Ypos += self.mod_TextUtils__.TextWrap.blit_text(
                                self,
                                BenchmarkIntroString[i],
                                (3, Ypos),
                                DataFont,
                                self.FontCol)

                    if stage == 1:
                        self.mod_Pygame__.display.set_caption(
                            f"Pycraft: v{self.version}: Benchmark | Getting System Information")

                        CPUname = self.mod_CPUinfo__.get_cpu_info()["brand_raw"]
                        CPUcores = self.mod_Psutil__.cpu_count(logical=False)
                        CPU_max_Freq = self.mod_Psutil__.cpu_freq().max
                        CPUid = f"{CPUname} w/{CPUcores} cores @ {CPU_max_Freq} MHz"

                        RAMtotal = round((self.mod_Psutil__.virtual_memory().total/1000000000), 2)
                        RAMpercent = self.mod_Psutil__.virtual_memory().percent
                        RAMid = f"{RAMtotal} GB of memory, with {RAMpercent}% used"

                        CPUhwINFO = DataFont.render(
                            CPUid,
                            self.aa,
                            self.FontCol)
                        CPUhwINFOwidth = CPUhwINFO.get_width()

                        RAMhwINFO = DataFont.render(
                            RAMid,
                            self.aa,
                            self.FontCol)
                        RAMhwINFOwidth = RAMhwINFO.get_width()

                        stage += 1

                    if stage == 2:
                        try:
                            FPS_Results = self.mod_ExBenchmark__.LoadBenchmark.run(self)
                            FPSlistX = FPS_Results[0]
                            FPSlistY = FPS_Results[1]
                            FPSlistX2 = FPS_Results[2]
                            FPSlistY2 = FPS_Results[3]
                            FPSlistX3 = FPS_Results[4]
                            FPSlistY3 = FPS_Results[5]
                        except Exception as Message:
                            print("Benchmark > GenerateBenchmarkMenu > Benchmark: "+str(Message))
                            self.mod_DisplayUtils__.DisplayUtils.SetDisplay(self)
                            self.mod_Pygame__.display.set_caption(
                                f"Pycraft: v{self.version}: Benchmark | Cancelled benchmark")

                            self.StartAnimation = True
                            self.RunTimer = 0
                            self.GoTo = "Home"
                            stage = -1
                        else:
                            self.mod_Pygame__.display.set_caption(
                                "".join((f"Pycraft: v{self.version}: Benchmark",
                                         "|",
                                         "Finished FPS based benchmarks")))

                            self.mod_DisplayUtils__.DisplayUtils.SetDisplay(self)

                            stage += 1

                    if stage == 3:
                        self.mod_Pygame__.display.set_caption(
                            f"Pycraft: v{self.version}: Benchmark | Starting disk read test")
                        ReadIteration = 5
                        for i in range(ReadIteration):
                            if self.platform == "Linux":
                                with open(
                                    self.mod_OS__.path.join(
                                        self.base_folder,
                                        ("Data_Files//BenchmarkData.txt")),"r") as Bench:

                                    Benchdata = Bench.read()
                            else:
                                with open(
                                    self.mod_OS__.path.join(
                                        self.base_folder,
                                        ("Data_Files\\BenchmarkData.txt")), "r") as Bench:

                                    Benchdata = Bench.read()
                        aTime = 0
                        ReadIteration = 50
                        for i in range(ReadIteration):
                            start = self.mod_Time__.perf_counter()
                            if self.platform == "Linux":
                                with open(
                                    self.mod_OS__.path.join(
                                        self.base_folder,
                                        ("Data_Files//BenchmarkData.txt")), "r") as Bench:

                                    Benchdata = Bench.read()
                            else:
                                with open(
                                    self.mod_OS__.path.join(
                                        self.base_folder,
                                        ("Data_Files\\BenchmarkData.txt")), "r") as Bench:

                                    Benchdata = Bench.read()

                            aTime += self.mod_Time__.perf_counter()-start
                        aTime = aTime/(ReadIteration+1)
                        ReadSpeed = (1/(aTime))
                        stage += 1

                    if stage == 4:
                        self.mod_Pygame__.display.set_caption(
                            f"Pycraft: v{self.version}: Benchmark | Processing Results")
                        try:
                            Max1 = max(FPSlistY)
                            Min1 = min(FPSlistY)

                            Max2 = max(FPSlistY2)
                            Min2 = min(FPSlistY2)

                            Max3 = max(FPSlistY3)
                            Min3 = min(FPSlistY3)
                        except Exception as Message:
                            Message_To_User = "".join(("(User cancelled) Benchmark ",
                                                       "> GenerateBenchmarkMenu > Benchmark:",
                                                       f"{str(Message)}"))
                            print(Message_To_User)

                            self.mod_DisplayUtils__.DisplayUtils.SetDisplay(self)
                            self.mod_Pygame__.display.set_caption(
                                f"Pycraft: v{self.version}: Benchmark | Cancelled benchmark")

                            self.StartAnimation = True
                            self.RunTimer = 0
                            self.GoTo = "Home"

                        GlobalMaxArray = [Max1, Max2, Max3]

                        GlobalMax = max(GlobalMaxArray)

                        self.RecommendedFPS = GlobalMax/2

                        multiplier = len(FPSlistY)/(self.realWidth-20)
                        temp = []
                        for i in range(len(FPSlistY)):
                            temp.append(130+(300-((300/GlobalMax)*FPSlistY[i])))
                        FPSListY = temp

                        temp = []
                        for i in range(len(FPSlistY2)):
                            temp.append(130+(300-((300/GlobalMax)*FPSlistY2[i])))
                        FPSListY2 = temp

                        temp = []
                        for i in range(len(FPSlistY2)):
                            temp.append(130+(300-((300/GlobalMax)*FPSlistY3[i])))
                        FPSListY3 = temp

                        Results1 = []
                        for i in range(len(FPSlistY)):
                            Results1.append([(FPSlistX[i]/multiplier), FPSListY[i]])

                        Results2 = []
                        for i in range(len(FPSlistY2)):
                            Results2.append([(FPSlistX2[i]/multiplier), FPSListY2[i]])

                        Results3 = []
                        for i in range(len(FPSlistY3)):
                            Results3.append([(FPSlistX3[i]/multiplier), FPSListY3[i]])

                        stage += 1

                    if stage == 5:
                        self.mod_Pygame__.display.set_caption(
                            f"Pycraft: v{self.version}: Benchmark | Results")

                        self.Display.fill(self.BackgroundCol)

                        self.Display.blit(
                            TitleFont,
                            ((self.realWidth-TitleWidth)/2, 0))

                        self.Display.blit(
                            BenchmarkFont,
                            (((self.realWidth-TitleWidth)/2)+65, 50))

                        FPSRect = self.mod_Pygame__.Rect(
                            10,
                            130,
                            self.realWidth-20,
                            300)

                        self.mod_Pygame__.draw.rect(
                            self.Display,
                            self.ShapeCol,
                            FPSRect,
                            0)

                        self.mod_Pygame__.draw.lines(
                            self.Display,
                            (255, 0, 0),
                            False,
                            Results3)

                        self.mod_Pygame__.draw.lines(
                            self.Display,
                            (0, 255, 0),
                            False,
                            Results1)

                        self.mod_Pygame__.draw.lines(
                            self.Display,
                            (0, 0, 255),
                            False,
                            Results2)

                        self.mod_Pygame__.draw.line(
                            self.Display,
                            self.AccentCol,
                            (10, int(130+(300-((300/GlobalMax)*60)))),
                            (self.realWidth-20, int(130+(300-((300/GlobalMax)*60)))))

                        self.Display.blit(
                            SixtyFPSData,
                            (13, int(130+(300-((300/GlobalMax)*60)))))

                        self.mod_Pygame__.draw.line(
                            self.Display,
                            self.AccentCol,
                            (10, int(130+(300-((300/GlobalMax)*144)))),
                            (self.realWidth-20, int(130+(300-((300/GlobalMax)*144)))))

                        self.Display.blit(
                            OneFourFourFPSData,
                            (13, int(130+(300-((300/GlobalMax)*140)))))

                        self.mod_Pygame__.draw.line(
                            self.Display,
                            self.AccentCol,
                            (10, int(130+(300-((300/GlobalMax)*240)))),
                            (self.realWidth-20, int(130+(300-((300/GlobalMax)*240)))))

                        self.Display.blit(TwoFortyFPSData,
                                          (13, int(130+(300-((300/GlobalMax)*240)))))

                        HideRect = self.mod_Pygame__.Rect(
                            0,
                            110,
                            self.realWidth,
                            330)

                        self.mod_Pygame__.draw.rect(
                            self.Display,
                            self.BackgroundCol,
                            HideRect,
                            20)

                        self.Display.blit(
                            FPSinfoTEXT,
                            ((self.realWidth-FPSinfoTEXTWidth)-3, 100))

                        self.Display.blit(
                            FILEinfoTEXT,
                            ((self.realWidth-FILEinfoTEXTWidth)-3, 430))

                        Device_Results = "".join(("Your device achieved a score of: ",
                                                  f"{round(ReadSpeed, 2)}/100 ",
                                                  f"({round((100/100)*ReadSpeed)}%)"))

                        FileResults = DataFont.render(
                            Device_Results,
                            self.aa,
                            self.FontCol)

                        FileResultsWidth = FileResults.get_width()
                        self.Display.blit(
                            FileResults,
                            ((self.realWidth-FileResultsWidth)-3, 460))

                        self.Display.blit(
                            HARDWAREinfoTEXT,
                            ((self.realWidth-HARDWAREinfoTEXTwidth)-3, 480))

                        self.Display.blit(
                            CPUhwINFO,
                            ((self.realWidth-CPUhwINFOwidth)-3, 500))

                        self.Display.blit(
                            RAMhwINFO,
                            ((self.realWidth-RAMhwINFOwidth)-3, 516))

                        GreenResults = "".join(("Blank screen test (green); Minimum: ",
                                                f"{round(Min1, 4)} FPS, Maximum: ",
                                                f"{round(Max1, 4)} FPS"))

                        BlueResults = "".join(("Blank screen test (blue); Minimum: ",
                                                f"{round(Min2, 4)} FPS, Maximum: ",
                                                f"{round(Max2, 4)} FPS"))

                        RedResults = "".join(("Blank screen test (red); Minimum: ",
                                               f"{round(Min3, 4)} FPS, Maximum: ",
                                               f"{round(Max3, 4)} FPS"))

                        GreenInfo = InfoDetailsFont.render(
                            GreenResults,
                            self.aa,
                            self.FontCol)

                        BlueInfo = InfoDetailsFont.render(
                            BlueResults,
                            self.aa,
                            self.FontCol)

                        RedInfo = InfoDetailsFont.render(
                            RedResults,
                            self.aa,
                            self.FontCol)

                        self.Display.blit(
                            GreenInfo,
                            (3, 430))
                        self.Display.blit(
                            BlueInfo,
                            (3, 445))
                        self.Display.blit(
                            RedInfo,
                            (3, 460))

                        if resize:
                            stage = 4
                            resize = False

                    for event in self.mod_Pygame__.event.get():
                        if (event.type == self.mod_Pygame__.QUIT or
                            (event.type == self.mod_Pygame__.KEYDOWN and
                             (event.key != self.mod_Pygame__.K_SPACE) and
                             stage <= 3) or
                            (event.type == self.mod_Pygame__.KEYDOWN and
                             event.key == self.mod_Pygame__.K_ESCAPE)):

                            self.JoystickExit = False
                            if self.sound:
                                self.mod_SoundUtils__.PlaySound.PlayClickSound(self)
                            self.StartAnimation = True
                            self.RunTimer = 0
                            self.GoTo = "Home"
                        if (((event.type == self.mod_Pygame__.KEYDOWN and
                              event.key == self.mod_Pygame__.K_SPACE) or
                             (self.JoystickConfirm and
                              self.UseMouseInput is False)) and
                            stage == 0):

                            stage += 1
                        if event.type == self.mod_Pygame__.VIDEORESIZE:
                            resize = True

                    if self.GoTo is None:
                        self.mod_DisplayUtils__.DisplayAnimations.FadeIn(self)
                    else:
                        self.mod_DisplayUtils__.DisplayAnimations.FadeOut(self)

                    if self.StartAnimation is False and (self.GoTo is not None):
                        return None

                    self.mod_Pygame__.display.flip()
                    self.clock.tick(
                        self.mod_DisplayUtils__.DisplayUtils.GetPlayStatus(self))

                    if not self.ErrorMessage is None:
                        self.ErrorMessage = "".join(("Benchmark > GenerateBenchmarkMenu",
                                                     f"> Benchmark: {str(self.ErrorMessage)}"))
                        return
                    self.RunTimer += self.mod_Time__.perf_counter()-StartTime
            except Exception as Message:
                self.ErrorMessage = "Benchmark > GenerateBenchmarkMenu > Benchmark: "+str(Message)

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
