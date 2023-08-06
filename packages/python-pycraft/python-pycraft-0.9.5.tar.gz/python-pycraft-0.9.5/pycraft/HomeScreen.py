if __name__ != "__main__":
    print("Started <Pycraft_HomeScreen>")

    class GenerateHomeScreen:
        def __init__(self):
            pass

        def CreateBanner(self):
            try:
                global ShowMessage, MessageColor

                if self.platform == "Linux":
                    SideFont = self.mod_Pygame__.font.Font(
                        self.mod_OS__.path.join(
                            self.base_folder, ("Fonts//Book Antiqua.ttf")), 20)

                    VersionFont = self.mod_Pygame__.font.Font(
                        self.mod_OS__.path.join(
                            self.base_folder, ("Fonts//Book Antiqua.ttf")), 20)

                    MessageFont = self.mod_Pygame__.font.Font(
                        self.mod_OS__.path.join(
                            self.base_folder, ("Fonts//Book Antiqua.ttf")), 20)

                else:
                    SideFont = self.mod_Pygame__.font.Font(
                        self.mod_OS__.path.join(
                            self.base_folder, ("Fonts\\Book Antiqua.ttf")), 20)

                    VersionFont = self.mod_Pygame__.font.Font(
                        self.mod_OS__.path.join(
                            self.base_folder, ("Fonts\\Book Antiqua.ttf")), 20)

                    MessageFont = self.mod_Pygame__.font.Font(
                        self.mod_OS__.path.join(
                            self.base_folder, ("Fonts\\Book Antiqua.ttf")), 20)

                Name = SideFont.render(
                    "By PycraftDev",
                    self.aa,
                    self.FontCol).convert_alpha()
                NameHeight = Name.get_height()

                Version = VersionFont.render(
                    f"Version: {self.version}",
                    self.aa,
                    self.FontCol).convert_alpha()
                VersionWidth = Version.get_width()
                VersionHeight = Version.get_height()

                Timer_start = 0
                RenderedText = False

                while self.Command == "Undefined":
                    if ShowMessage is not None and MessageColor is not None and RenderedText is False:
                        Timer_start = self.mod_Time__.perf_counter()

                        MessageText = MessageFont.render(
                            ShowMessage,
                            self.aa,
                            MessageColor).convert_alpha()
                        MessageTextWidth = MessageText.get_width()
                        MessageTextHeight = MessageText.get_height()

                        RenderedText = True

                    if RenderedText:
                        if self.mod_Time__.perf_counter()-Timer_start < 3:
                            self.Display.blit(
                                MessageText,
                                ((self.realWidth-MessageTextWidth)/2,
                                 (self.realHeight-MessageTextHeight)))

                        else:
                            ShowMessage = None
                            MessageColor = None
                            RenderedText = False
                    else:
                        if self.UseMouseInput is False:
                            MessageText = MessageFont.render(
                                "".join(("On the controller; use the D-pad to navigate the menu, ",
                                         "press 'B' to confirm or press 'Y' to exit")),
                                self.aa,
                                self.FontCol).convert_alpha()
                            MessageTextWidth = MessageText.get_width()
                            MessageTextHeight = MessageText.get_height()

                            self.Display.blit(
                                MessageText,
                                ((self.realWidth-MessageTextWidth)/2,
                                 (self.realHeight-MessageTextHeight)))

                    self.Display.blit(
                        Name,
                        (0,
                         (self.realHeight-NameHeight)))

                    self.Display.blit(
                        Version,
                        ((self.realWidth-VersionWidth)-2,
                         (self.realHeight-VersionHeight)))

                    self.mod_Pygame__.display.update(
                        0,
                        self.realHeight-40,
                        self.realWidth,
                        self.realHeight)

                    self.clock.tick(
                        self.mod_DisplayUtils__.DisplayUtils.GetPlayStatus(self))
            except Exception as Message:
                if str(Message) != "display Surface quit":
                    self.ErrorMessage = "".join(("HomeScreen > GenerateHomeScreen > ",
                                                 "CreateBanner (thread): {str(Message)}"))

                    self.ErrorMessage_detailed = "".join(
                        self.mod_Traceback__.format_exception(
                            None,
                            Message,
                            Message.__traceback__))

                    self.mod_ErrorUtils__.GenerateErrorScreen.ErrorScreen(self)

        def Home_Screen(self):
            try:
                global ShowMessage, MessageColor

                ShowMessage = None
                MessageColor = self.FontCol

                BannerThread = self.mod_Threading__.Thread(
                    target=self.mod_HomeScreen__.GenerateHomeScreen.CreateBanner,
                    args=(self,))
                BannerThread.name = "Thread_BannerThread_HS"
                BannerThread.daemon = True
                BannerThread.start()

                self.mod_CaptionUtils__.GenerateCaptions.GetNormalCaption(
                    self,
                    "Home screen")

                if self.platform == "Linux":
                    Selector = self.mod_Pygame__.image.load(
                        self.mod_OS__.path.join(
                            self.base_folder,
                            (f"Resources//General_Resources//selectorICON{self.theme}.jpg")))
                    Selector.convert()

                else:
                    Selector = self.mod_Pygame__.image.load(
                        self.mod_OS__.path.join(
                            self.base_folder,
                            (f"Resources\\General_Resources\\selectorICON{self.theme}.jpg")))
                    Selector.convert()

                SelectorWidth = Selector.get_width()
                hover1 = False
                hover2 = False
                hover3 = False
                hover4 = False
                hover5 = False
                hover6 = False
                hover7 = False

                PycraftTitle = self.TitleFont.render(
                    "Pycraft",
                    self.aa,
                    self.FontCol)
                TitleWidth = PycraftTitle.get_width()

                self.realWidth = self.mod_Pygame__.display.get_window_size()[0]
                self.realHeight = self.mod_Pygame__.display.get_window_size()[1]

                self.Display.blit(
                    PycraftTitle,
                    ((self.realWidth-TitleWidth)/2, 0))

                self.mod_Pygame__.display.flip()

                if self.platform == "Linux":
                    ButtonFont1 = self.mod_Pygame__.font.Font(
                        self.mod_OS__.path.join(
                            self.base_folder, ("Fonts//Book Antiqua.ttf")), 30)

                    ButtonFont2 = self.mod_Pygame__.font.Font(
                        self.mod_OS__.path.join(
                            self.base_folder, ("Fonts//Book Antiqua.ttf")), 30)

                    ButtonFont3 = self.mod_Pygame__.font.Font(
                        self.mod_OS__.path.join(
                            self.base_folder, ("Fonts//Book Antiqua.ttf")), 30)

                    ButtonFont4 = self.mod_Pygame__.font.Font(
                        self.mod_OS__.path.join(
                            self.base_folder, ("Fonts//Book Antiqua.ttf")), 30)

                    ButtonFont5 = self.mod_Pygame__.font.Font(
                        self.mod_OS__.path.join(
                            self.base_folder, ("Fonts//Book Antiqua.ttf")), 30)

                    ButtonFont6 = self.mod_Pygame__.font.Font(
                        self.mod_OS__.path.join(
                            self.base_folder, ("Fonts//Book Antiqua.ttf")), 30)

                    ButtonFont7 = self.mod_Pygame__.font.Font(
                        self.mod_OS__.path.join(
                            self.base_folder, ("Fonts//Book Antiqua.ttf")), 30)

                    DataFont = self.mod_Pygame__.font.Font(
                        self.mod_OS__.path.join(
                            self.base_folder, ("Fonts//Book Antiqua.ttf")), 15)

                else:
                    ButtonFont1 = self.mod_Pygame__.font.Font(
                        self.mod_OS__.path.join(
                            self.base_folder, ("Fonts\\Book Antiqua.ttf")), 30)

                    ButtonFont2 = self.mod_Pygame__.font.Font(
                        self.mod_OS__.path.join(
                            self.base_folder, ("Fonts\\Book Antiqua.ttf")), 30)

                    ButtonFont3 = self.mod_Pygame__.font.Font(
                        self.mod_OS__.path.join(
                            self.base_folder, ("Fonts\\Book Antiqua.ttf")), 30)

                    ButtonFont4 = self.mod_Pygame__.font.Font(
                        self.mod_OS__.path.join(
                            self.base_folder, ("Fonts\\Book Antiqua.ttf")), 30)

                    ButtonFont5 = self.mod_Pygame__.font.Font(
                        self.mod_OS__.path.join(
                            self.base_folder, ("Fonts\\Book Antiqua.ttf")), 30)

                    ButtonFont6 = self.mod_Pygame__.font.Font(
                        self.mod_OS__.path.join(
                            self.base_folder, ("Fonts\\Book Antiqua.ttf")), 30)

                    ButtonFont7 = self.mod_Pygame__.font.Font(
                        self.mod_OS__.path.join(
                            self.base_folder, ("Fonts\\Book Antiqua.ttf")), 30)

                    DataFont = self.mod_Pygame__.font.Font(
                        self.mod_OS__.path.join(
                            self.base_folder, ("Fonts\\Book Antiqua.ttf")), 15)

                oldTHEME = self.theme
                coloursARRAY = []

                anim = False

                special = [30,
                           30,
                           30]

                TargetARRAY = []

                ColourDisplacement = 80

                increment = False

                self.CurrentlyDisplayingMessage = False

                Outdated = self.Outdated

                self.MovementSpeed = 3

                SelectButton = False
                MenuSelector = 0

                self.Mx = self.realWidth/2
                self.My = self.realHeight/2

                while True:
                    StartTime = self.mod_Time__.perf_counter()

                    if self.GetOutdated == [True, False]:
                        self.GetOutdated = [
                            True,
                            True]

                        Outdated = self.Outdated

                    if self.UseMouseInput:
                        SelectButton = False

                    if self.FancyGraphics:
                        coloursARRAY = []
                        if anim:
                            anim = False
                            TargetARRAY = []
                            for a in range(self.mod_Random__.randint(0, 32)):
                                TargetARRAY.append(a)

                        if len(TargetARRAY) == 0:
                            TargetARRAY = [33]

                        for i in range(32):
                            for j in range(len(TargetARRAY)):
                                if i == TargetARRAY[j]:
                                    coloursARRAY.append(special)

                                else:
                                    coloursARRAY.append(self.ShapeCol)

                        if increment is False:
                            RandomInt = self.mod_Random__.randint(0, 10)
                            if self.aFPS == 0 or self.Iteration == 0:
                                ColourDisplacement -= RandomInt/(self.FPS/4)

                            else:
                                ColourDisplacement -= RandomInt/((self.aFPS/self.Iteration)/4)

                            special[0] = ColourDisplacement
                            special[1] = ColourDisplacement
                            special[2] = ColourDisplacement

                        if increment:
                            RandomInt = self.mod_Random__.randint(0, 10)
                            if self.aFPS == 0 or self.Iteration == 0:
                                ColourDisplacement += RandomInt/(self.FPS/4)

                            else:
                                ColourDisplacement += RandomInt/((self.aFPS/self.Iteration)/4)

                            special[0] = ColourDisplacement
                            special[1] = ColourDisplacement
                            special[2] = ColourDisplacement

                        if special[0] <= 30:
                            increment = True
                            special[0] = 30
                            special[1] = 30
                            special[2] = 30

                        if special[0] >= 80:
                            increment = False
                            anim = True
                            special[0] = 80
                            special[1] = 80
                            special[2] = 80
                    else:
                        coloursARRAY = self.FancyGraphics

                    if str(self.Display) == "<Surface(Dead Display)>":
                        if self.Fullscreen is False:
                            self.mod_DisplayUtils__.DisplayUtils.SetDisplay(self)

                        elif self.Fullscreen:
                            self.mod_DisplayUtils__.DisplayUtils.SetDisplay(self)

                    yScaleFact = self.realHeight/720
                    xScaleFact = self.realWidth/1280

                    if not oldTHEME == self.theme:
                        if self.platform == "Linux":
                            Selector = self.mod_Pygame__.image.load(
                                self.mod_OS__.path.join(
                                    self.base_folder,
                                    ("".join(("Resources//General_Resources",
                                              f"//selectorICON{self.theme}.jpg")))))
                            Selector.convert()

                        else:
                            Selector = self.mod_Pygame__.image.load(
                                self.mod_OS__.path.join(
                                    self.base_folder,
                                    ("".join(("Resources\\General_Resources",
                                              f"\\selectorICON{self.theme}.jpg")))))
                            Selector.convert()

                        SelectorWidth = Selector.get_width()
                        oldTHEME = self.theme

                    self.Display.fill(self.BackgroundCol)

                    PycraftTitle = self.TitleFont.render(
                        "Pycraft",
                        self.aa,
                        self.FontCol).convert_alpha()
                    TitleWidth = PycraftTitle.get_width()

                    Play = ButtonFont1.render(
                        "Play",
                        self.aa,
                        self.FontCol).convert_alpha()
                    PlayWidth = Play.get_width()

                    SettingsText = ButtonFont2.render(
                        "Settings",
                        self.aa,
                        self.FontCol).convert_alpha()
                    SettingsWidth = SettingsText.get_width()

                    Character_DesignerText = ButtonFont3.render(
                        "Character Designer",
                        self.aa,
                        self.FontCol).convert_alpha()
                    CharDesignerWidth = Character_DesignerText.get_width()

                    AchievementsText = ButtonFont4.render(
                        "Achievements",
                        self.aa,
                        self.FontCol).convert_alpha()
                    AchievementsWidth = AchievementsText.get_width()

                    Credits_and_Change_Log_Text = ButtonFont5.render(
                        "Credits",
                        self.aa,
                        self.FontCol).convert_alpha()
                    CreditsWidth = Credits_and_Change_Log_Text.get_width()

                    BenchmarkText = ButtonFont6.render(
                        "Benchmark",
                        self.aa,
                        self.FontCol).convert_alpha()
                    BenchmarkWidth = BenchmarkText.get_width()

                    InstallerText = ButtonFont7.render(
                        "Installer",
                        self.aa,
                        self.FontCol).convert_alpha()
                    InstallerWidth = InstallerText.get_width()

                    DisplayEvents = self.mod_DisplayUtils__.DisplayFunctionality.CoreDisplayFunctionality(
                        self,
                        location="saveANDexit")

                    if self.UseMouseInput:
                        for event in DisplayEvents:
                            if (event.type == self.mod_Pygame__.MOUSEBUTTONDOWN or
                                    self.mod_Pygame__.mouse.get_pressed()[0]):

                                self.mousebuttondown = True

                            else:
                                self.mousebuttondown = False

                    self.mod_CaptionUtils__.GenerateCaptions.GetNormalCaption(
                        self,
                        "Home screen")

                    ButtonFont1.set_underline(hover1)
                    ButtonFont2.set_underline(hover2)
                    ButtonFont3.set_underline(hover3)
                    ButtonFont4.set_underline(hover4)
                    ButtonFont5.set_underline(hover5)
                    ButtonFont6.set_underline(hover6)
                    ButtonFont7.set_underline(hover7)

                    if self.GoTo is None:
                        if ((self.My >= 202*yScaleFact and
                                self.My <= 247*yScaleFact and
                                self.Mx >= (self.realWidth-(PlayWidth+SelectorWidth))-2) or
                                (SelectButton and
                                    MenuSelector == 0)):

                            hover1 = True

                            if self.mousebuttondown:
                                if self.sound:
                                    self.mod_SoundUtils__.PlaySound.PlayClickSound(self)

                                if self.ShowMessage:
                                    self.GoTo = "Play"
                                    self.StartAnimation = True
                                    self.RunTimer = 0

                                else:
                                    self.GoTo = "Play"
                                    self.StartAnimation = True
                                    self.RunTimer = 0

                                    self.ShowMessage = True

                                    self.ShowLightning = self.mod_Tkinter_messagebox_.askquestion(
                                        "Caution",
                                        "".join(("In a recent addition to the game engine it now ",
                                                 "includes lightning, this therefore means there ",
                                                 "are quick flashes of light in game, like a strobe ",
                                                 "effect. If you are not comfortable with this ",
                                                 "feature then click 'no' and we will turn this ",
                                                 "feature off for you, if you want to continue ",
                                                 "with the lightning effect then press 'yes', ",
                                                 "after doing so the game will load.\n\nThis is a ",
                                                 "one-time message and in the next update there ",
                                                 "will be a setting to toggle this feature in ",
                                                 "the settings menu.")))

                                    if self.ShowLightning == "yes":
                                        self.ShowLightning = True

                                    else:
                                        self.ShowLightning = False

                        else:
                            hover1 = False

                        if ((self.My >= 252*yScaleFact and
                                self.My <= 297*yScaleFact and
                                self.Mx >= (self.realWidth-(SettingsWidth+SelectorWidth))-2) or
                                (SelectButton and
                                    MenuSelector == 1)):

                            hover2 = True

                            if self.mousebuttondown:
                                if self.sound:
                                    self.mod_SoundUtils__.PlaySound.PlayClickSound(self)

                                self.GoTo = "Settings"
                                self.StartAnimation = True
                                self.RunTimer = 0

                        else:
                            hover2 = False

                        if ((self.My >= 302*yScaleFact and
                                self.My <= 347*yScaleFact and
                                self.Mx >= (self.realWidth-(CharDesignerWidth+SelectorWidth)-2)) or
                                (SelectButton and
                                    MenuSelector == 2)):

                            hover3 = True

                            if self.mousebuttondown:
                                if self.sound:
                                    self.mod_SoundUtils__.PlaySound.PlayClickSound(self)

                                self.GoTo = "CharacterDesigner"
                                self.StartAnimation = True
                                self.RunTimer = 0

                        else:
                            hover3 = False

                        if ((self.My >= 402*yScaleFact and
                                self.My <= 447*yScaleFact and
                                self.Mx >= (self.realWidth-(AchievementsWidth+SelectorWidth)-2)) or
                                (SelectButton and
                                    MenuSelector == 4)):

                            hover4 = True

                            if self.mousebuttondown:
                                if self.sound:
                                    self.mod_SoundUtils__.PlaySound.PlayClickSound(self)

                                self.GoTo = "Achievements"
                                self.StartAnimation = True
                                self.RunTimer = 0

                        else:
                            hover4 = False

                        if ((self.My >= 352*yScaleFact and
                                self.My <= 397*yScaleFact and
                                self.Mx >= (self.realWidth-(CreditsWidth+SelectorWidth)-2)) or
                                (SelectButton and
                                    MenuSelector == 3)):

                            hover5 = True

                            if self.mousebuttondown:
                                if self.sound:
                                    self.mod_SoundUtils__.PlaySound.PlayClickSound(self)

                                self.GoTo = "Credits"
                                self.StartAnimation = True
                                self.RunTimer = 0

                        else:
                            hover5 = False

                        if ((self.My >= 452*yScaleFact and
                                self.My <= 497*yScaleFact and
                                self.Mx >= (self.realWidth-(BenchmarkWidth+SelectorWidth)-2)) or
                                (SelectButton and
                                    MenuSelector == 5)):

                            hover6 = True

                            if self.mousebuttondown:
                                if self.sound:
                                    self.mod_SoundUtils__.PlaySound.PlayClickSound(self)

                                self.GoTo = "Benchmark"
                                self.StartAnimation = True
                                self.RunTimer = 0

                        else:
                            hover6 = False

                        if ((self.My >= 502*yScaleFact and
                                self.My <= 547*yScaleFact and
                                self.Mx >= (self.realWidth-(InstallerWidth+SelectorWidth)-2)) or
                                (SelectButton and
                                    MenuSelector == 6)):

                            hover7 = True

                            if self.mousebuttondown:
                                if self.sound:
                                    self.mod_SoundUtils__.PlaySound.PlayClickSound(self)

                                self.GoTo = "Installer"
                                self.StartAnimation = True
                                self.RunTimer = 0

                        else:
                            hover7 = False

                    self.Display.fill(self.BackgroundCol)

                    if ShowMessage is None:
                        if self.Updated:
                            self.Updated = False
                            ShowMessage = f"Successfully updated Pycraft to v{self.version}"
                            MessageColor = (0, 255, 0)

                        elif Outdated and self.TotalNumUpdate == 1:
                            Outdated = False
                            ShowMessage = f"There are {self.TotalNumUpdate} updates available!"
                            MessageColor = (0, 255, 0)

                        elif Outdated and self.TotalNumUpdate == 1:
                            Outdated = False
                            ShowMessage = "There is an update available!"
                            MessageColor = (0, 255, 0)

                        elif self.DeviceConnected_Update:
                            if self.DeviceConnected:
                                ShowMessage = "".join(("There is a new input device available! ",
                                                   "You can change input modes in settings"))

                                MessageColor = (0, 255, 0)

                            else:
                                if self.UseMouseInput:
                                    ShowMessage = "Terminated connection to an input device"
                                    MessageColor = (255, 0, 0)

                                else:
                                    ShowMessage = "".join(("Terminated connection to current ",
                                                       "input device, returning to ",
                                                       "default setting"))

                                    MessageColor = (255, 0, 0)
                                    self.UseMouseInput = True

                            self.DeviceConnected_Update = False

                    self.Display.blit(
                        PycraftTitle,
                        ((self.realWidth-TitleWidth)/2, 0))

                    self.Display.blit(
                        Play,
                        ((self.realWidth-PlayWidth)-2, 200*yScaleFact))

                    self.Display.blit(
                        SettingsText,
                        ((self.realWidth-SettingsWidth)-2, 250*yScaleFact))

                    self.Display.blit(
                        Character_DesignerText,
                        ((self.realWidth-CharDesignerWidth)-2, 300*yScaleFact))

                    self.Display.blit(
                        Credits_and_Change_Log_Text,
                        ((self.realWidth-CreditsWidth)-2, 350*yScaleFact))

                    self.Display.blit(
                        AchievementsText,
                        ((self.realWidth-AchievementsWidth)-2, 400*yScaleFact))

                    self.Display.blit(
                        BenchmarkText,
                        ((self.realWidth-BenchmarkWidth)-2, 450*yScaleFact))

                    self.Display.blit(
                        InstallerText,
                        ((self.realWidth-InstallerWidth)-2, 500*yScaleFact))

                    if self.JoystickHatPressed:
                        self.JoystickHatPressed = False
                        if self.JoystickMouse[0] == "Right":
                            SelectButton = True

                        if self.JoystickMouse[0] == "Left":
                            SelectButton = False

                        if SelectButton:
                            if self.JoystickMouse[1] == "Down" and MenuSelector <= 6:
                                MenuSelector += 1
                                if MenuSelector == 7:
                                    MenuSelector = 0

                            if self.JoystickMouse[1] == "Up" and MenuSelector >= 0:
                                MenuSelector -= 1
                                if MenuSelector == -1:
                                    MenuSelector = 6

                    if hover1 or (SelectButton and MenuSelector == 0):
                        self.Display.blit(
                            Selector,
                            (self.realWidth-(PlayWidth+SelectorWidth)-2, 200*yScaleFact))
                        #if self.UseMouseInput == False:
                            #BoundingRect = self.mod_Pygame__.Rect(
                                # (self.realWidth-PlayWidth)-4,
                                # (200*yScaleFact)-2,
                                # PlayWidth+4,
                                # Play.get_height()+4)

                            #self.mod_Pygame__.draw.rect(
                                # self.Display,
                                # self.ShapeCol,
                                # BoundingRect,
                                # 2)

                        #else:
                            #self.mod_Pygame__.mouse.set_cursor(
                                # self.mod_Pygame__.SYSTEM_CURSOR_HAND)

                        if self.UseMouseInput:
                            self.mod_Pygame__.mouse.set_cursor(self.mod_Pygame__.SYSTEM_CURSOR_HAND)

                    elif hover2 or (SelectButton and MenuSelector == 1):
                        self.Display.blit(
                            Selector,
                            (self.realWidth-(SettingsWidth+SelectorWidth)-2, 250*yScaleFact))
                        #if self.UseMouseInput == False:
                            #BoundingRect = self.mod_Pygame__.Rect(
                                # (self.realWidth-SettingsWidth)-4,
                                # (250*yScaleFact)-2,
                                # SettingsWidth+4,
                                # SettingsText.get_height()+4)

                            #self.mod_Pygame__.draw.rect(
                                # self.Display,
                                # self.ShapeCol,
                                # BoundingRect,
                                # 2)

                        #else:
                            #self.mod_Pygame__.mouse.set_cursor(
                                # self.mod_Pygame__.SYSTEM_CURSOR_HAND)
                        if self.UseMouseInput:
                            self.mod_Pygame__.mouse.set_cursor(self.mod_Pygame__.SYSTEM_CURSOR_HAND)

                    elif hover3 or (SelectButton and MenuSelector == 2):
                        self.Display.blit(
                            Selector,
                            (self.realWidth-(CharDesignerWidth+SelectorWidth)-2, 300*yScaleFact))
                        #if self.UseMouseInput == False:
                            #BoundingRect = self.mod_Pygame__.Rect(
                                # (self.realWidth-CharDesignerWidth)-4,
                                # (300*yScaleFact)-2,
                                # CharDesignerWidth+4,
                                # Character_DesignerText.get_height()+4)

                            #self.mod_Pygame__.draw.rect(
                                # self.Display,
                                # self.ShapeCol,
                                # BoundingRect,
                                # 2)

                        #else:
                            #self.mod_Pygame__.mouse.set_cursor(
                                # self.mod_Pygame__.SYSTEM_CURSOR_HAND)
                        if self.UseMouseInput:
                            self.mod_Pygame__.mouse.set_cursor(self.mod_Pygame__.SYSTEM_CURSOR_HAND)

                    elif hover5 or (SelectButton and MenuSelector == 3):
                        self.Display.blit(
                            Selector,
                            (self.realWidth-(CreditsWidth+SelectorWidth)-2, 350*yScaleFact))
                        #if self.UseMouseInput == False:
                            #BoundingRect = self.mod_Pygame__.Rect(
                                # (self.realWidth-CreditsWidth)-4,
                                # (350*yScaleFact)-2,
                                # CreditsWidth+4,
                                # Credits_and_Change_Log_Text.get_height()+4)

                            #self.mod_Pygame__.draw.rect(
                                # self.Display,
                                # self.ShapeCol,
                                # BoundingRect,
                                # 2)

                        #else:
                            #elf.mod_Pygame__.mouse.set_cursor(
                                # self.mod_Pygame__.SYSTEM_CURSOR_HAND)
                        if self.UseMouseInput:
                            self.mod_Pygame__.mouse.set_cursor(self.mod_Pygame__.SYSTEM_CURSOR_HAND)

                    elif hover4 or (SelectButton and MenuSelector == 4):
                        self.Display.blit(
                            Selector,
                            (self.realWidth-(AchievementsWidth+SelectorWidth)-2, 400*yScaleFact))
                        #if self.UseMouseInput == False:
                            #BoundingRect = self.mod_Pygame__.Rect(
                                # (self.realWidth-AchievementsWidth)-4,
                                # (400*yScaleFact)-2,
                                # AchievementsWidth+4,
                                # AchievementsText.get_height()+4)

                            #self.mod_Pygame__.draw.rect(
                                # self.Display,
                                # self.ShapeCol,
                                # BoundingRect,
                                # 2)

                        #else:
                            #self.mod_Pygame__.mouse.set_cursor(
                                # self.mod_Pygame__.SYSTEM_CURSOR_HAND)
                        if self.UseMouseInput:
                            self.mod_Pygame__.mouse.set_cursor(self.mod_Pygame__.SYSTEM_CURSOR_HAND)

                    elif hover6 or (SelectButton and MenuSelector == 5):
                        self.Display.blit(
                            Selector,
                            (self.realWidth-(BenchmarkWidth+SelectorWidth)-2, 450*yScaleFact))
                        #if self.UseMouseInput == False:
                            #BoundingRect = self.mod_Pygame__.Rect(
                                # (self.realWidth-BenchmarkWidth)-4,
                                # (450*yScaleFact)-2,
                                # BenchmarkWidth+4,
                                # BenchmarkText.get_height()+4)

                            #self.mod_Pygame__.draw.rect(
                                # self.Display,
                                # self.ShapeCol,
                                # BoundingRect,
                                # 2)

                        #else:
                            #self.mod_Pygame__.mouse.set_cursor(
                                # self.mod_Pygame__.SYSTEM_CURSOR_HAND)
                        if self.UseMouseInput:
                            self.mod_Pygame__.mouse.set_cursor(self.mod_Pygame__.SYSTEM_CURSOR_HAND)

                    elif hover7 or (SelectButton and MenuSelector == 6):
                        self.Display.blit(
                            Selector,
                            (self.realWidth-(InstallerWidth+SelectorWidth)-2, 500*yScaleFact))
                        #if self.UseMouseInput == False:
                            #BoundingRect = self.mod_Pygame__.Rect(
                                # (self.realWidth-InstallerWidth)-4,
                                # (500*yScaleFact)-2,
                                # InstallerWidth+4,
                                # InstallerText.get_height()+4)

                            #self.mod_Pygame__.draw.rect(
                                # self.Display,
                                # self.ShapeCol,
                                # BoundingRect,
                                # 2)

                        #else:
                            #self.mod_Pygame__.mouse.set_cursor(
                                # self.mod_Pygame__.SYSTEM_CURSOR_HAND)
                        if self.UseMouseInput:
                            self.mod_Pygame__.mouse.set_cursor(self.mod_Pygame__.SYSTEM_CURSOR_HAND)

                    else:
                        if self.UseMouseInput:
                            self.mod_Pygame__.mouse.set_cursor(
                                self.mod_Pygame__.SYSTEM_CURSOR_ARROW)

                    self.mod_DrawingUtils__.GenerateGraph.CreateDevmodeGraph(
                        self,
                        DataFont)

                    self.mod_DrawingUtils__.DrawRose.CreateRose(
                        self,
                        xScaleFact,
                        yScaleFact,
                        coloursARRAY)

                    if self.StartAnimation is False and (self.GoTo is not None):
                        return self.GoTo

                    if self.GoTo is None:
                        self.mod_DisplayUtils__.DisplayAnimations.FadeIn(self)
                    else:
                        self.mod_DisplayUtils__.DisplayAnimations.FadeOut(self)

                    self.mod_Pygame__.display.update(
                        0,
                        0,
                        self.realWidth,
                        self.realHeight-40)

                    self.clock.tick(self.mod_DisplayUtils__.DisplayUtils.GetPlayStatus(self))
                    self.RunTimer += self.mod_Time__.perf_counter()-StartTime

                    if self.ErrorMessage is not None:
                        self.ErrorMessage = "HomeScreen: "+str(self.ErrorMessage)
                        return

            except Exception as Message:
                self.ErrorMessage = "HomeScreen > GenerateHomeScreen > Home_Screen: "+ str(Message)
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
