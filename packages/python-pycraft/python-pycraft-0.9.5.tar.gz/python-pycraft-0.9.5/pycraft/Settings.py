if __name__ != "__main__":
    print("Started <Pycraft_Settings>")

    class GenerateSettings:
        def __init__(self):
            pass

        def settings(self):
            try:
                self.mod_CaptionUtils__.GenerateCaptions.GetNormalCaption(
                    self,
                    "Settings")

                if self.platform == "Linux":
                    VersionFont = self.mod_Pygame__.font.Font(
                        self.mod_OS__.path.join(
                            self.base_folder,
                            ("Fonts//Book Antiqua.ttf")), 15)

                    InfoTitleFont = self.mod_Pygame__.font.Font(
                        self.mod_OS__.path.join(
                            self.base_folder,
                            ("Fonts//Book Antiqua.ttf")), 35)

                    LOWFont = self.mod_Pygame__.font.Font(
                        self.mod_OS__.path.join(
                            self.base_folder,
                            ("Fonts//Book Antiqua.ttf")), 15)

                    MEDIUMFont = self.mod_Pygame__.font.Font(
                        self.mod_OS__.path.join(
                            self.base_folder,
                            ("Fonts//Book Antiqua.ttf")), 15)

                    HIGHFont = self.mod_Pygame__.font.Font(
                        self.mod_OS__.path.join(
                            self.base_folder,
                            ("Fonts//Book Antiqua.ttf")), 15)

                    ADAPTIVEFont = self.mod_Pygame__.font.Font(
                        self.mod_OS__.path.join(
                            self.base_folder,
                            ("Fonts//Book Antiqua.ttf")), 15)

                    LightThemeFont = self.mod_Pygame__.font.Font(
                        self.mod_OS__.path.join(
                            self.base_folder,
                            ("Fonts//Book Antiqua.ttf")), 15)

                    DarkThemeFont = self.mod_Pygame__.font.Font(
                        self.mod_OS__.path.join(
                            self.base_folder,
                            ("Fonts//Book Antiqua.ttf")), 15)

                    DataFont = self.mod_Pygame__.font.Font(
                        self.mod_OS__.path.join(
                            self.base_folder,
                            ("Fonts//Book Antiqua.ttf")), 15)

                    SettingsInformationFont = self.mod_Pygame__.font.Font(
                        self.mod_OS__.path.join(
                            self.base_folder,
                            ("Fonts//Book Antiqua.ttf")), 15)

                else:
                    VersionFont = self.mod_Pygame__.font.Font(
                        self.mod_OS__.path.join(
                            self.base_folder,
                            ("Fonts\\Book Antiqua.ttf")), 15)

                    InfoTitleFont = self.mod_Pygame__.font.Font(
                        self.mod_OS__.path.join(
                            self.base_folder,
                            ("Fonts\\Book Antiqua.ttf")), 35)

                    LOWFont = self.mod_Pygame__.font.Font(
                        self.mod_OS__.path.join(
                            self.base_folder,
                            ("Fonts\\Book Antiqua.ttf")), 15)

                    MEDIUMFont = self.mod_Pygame__.font.Font(
                        self.mod_OS__.path.join(
                            self.base_folder,
                            ("Fonts\\Book Antiqua.ttf")), 15)

                    HIGHFont = self.mod_Pygame__.font.Font(
                        self.mod_OS__.path.join(
                            self.base_folder,
                            ("Fonts\\Book Antiqua.ttf")), 15)

                    ADAPTIVEFont = self.mod_Pygame__.font.Font(
                        self.mod_OS__.path.join(
                            self.base_folder,
                            ("Fonts\\Book Antiqua.ttf")), 15)

                    LightThemeFont = self.mod_Pygame__.font.Font(
                        self.mod_OS__.path.join(
                            self.base_folder,
                            ("Fonts\\Book Antiqua.ttf")), 15)

                    DarkThemeFont = self.mod_Pygame__.font.Font(
                        self.mod_OS__.path.join(
                            self.base_folder,
                            ("Fonts\\Book Antiqua.ttf")), 15)

                    DataFont = self.mod_Pygame__.font.Font(
                        self.mod_OS__.path.join(
                            self.base_folder,
                            ("Fonts\\Book Antiqua.ttf")), 15)

                    SettingsInformationFont = self.mod_Pygame__.font.Font(
                        self.mod_OS__.path.join(
                            self.base_folder,
                            ("Fonts\\Book Antiqua.ttf")), 15)

                TempMx = 0

                scroll = 50

                FocusedOn = [False, None]
                MoveToPosition = [False,
                                  False,
                                  False,
                                  False,
                                  False]

                ChangeLine = []
                self.MovementSpeed = 1

                MenuSelector = 13
                LeftAndRight = 0

                while True:
                    StartTime = self.mod_Time__.perf_counter()
                    TempMx = self.Mx

                    if self.UseMouseInput is False:
                        if (MenuSelector not in range(0, 2) or LeftAndRight == 0):
                            LeftAndRight = 0

                    if self.JoystickHatPressed:
                        self.JoystickHatPressed = False
                        if self.JoystickMouse[1] == "Down" and MenuSelector <= 13:
                            MenuSelector += 1
                            if MenuSelector == 14:
                                MenuSelector = 0
                                
                        if self.JoystickMouse[1] == "Up" and MenuSelector >= 0:
                            MenuSelector -= 1
                            if MenuSelector == -1:
                                MenuSelector = 13
                                
                        if self.JoystickMouse[0] == "Right":
                            LeftAndRight += 1
                            
                        if self.JoystickMouse[0] == "Left":
                            LeftAndRight -= 1

                    xScaleFact = self.realWidth/1280

                    DisplayEvents = self.mod_DisplayUtils__.DisplayFunctionality.CoreDisplayFunctionality(
                        self)

                    for event in DisplayEvents:
                        if ((event.type == self.mod_Pygame__.MOUSEBUTTONDOWN or
                                    self.mod_Pygame__.mouse.get_pressed()[0]) and
                                self.UseMouseInput):

                            self.mousebuttondown = True

                        if ((event.type == self.mod_Pygame__.MOUSEBUTTONUP or
                                    self.mod_Pygame__.mouse.get_pressed()[0] is False) and
                                self.UseMouseInput):

                            self.mousebuttondown = False

                        if event.type == self.mod_Pygame__.MOUSEWHEEL and self.realHeight <= 760:
                            if self.UseMouseInput:
                                self.mod_Pygame__.mouse.set_cursor(
                                    self.mod_Pygame__.SYSTEM_CURSOR_SIZENS)
                                if str(event.y)[0] == "-":
                                    scroll -= 5

                                else:
                                    scroll += 5

                        else:
                            if self.UseMouseInput:
                                self.mod_Pygame__.mouse.set_cursor(
                                    self.mod_Pygame__.SYSTEM_CURSOR_ARROW)

                    self.mod_CaptionUtils__.GenerateCaptions.GetNormalCaption(
                        self,
                        "Settings")

                    if scroll > 35:
                        scroll = 35
                    elif scroll < -40:
                        scroll = -40

                        if self.JoystickHatPressed:
                            self.JoystickHatPressed = False
                            if self.JoystickMouse[1] == "Down" and MenuSelector <= 13:
                                MenuSelector += 1
                                if MenuSelector == 14:
                                    MenuSelector = 0

                            if self.JoystickMouse[1] == "Up" and MenuSelector >= 0:
                                MenuSelector -= 1
                                if MenuSelector == -1:
                                    MenuSelector = 13

                            if self.JoystickMouse[0] == "Right":
                                LeftAndRight += 1

                            if self.JoystickMouse[0] == "Left":
                                LeftAndRight -= 1

                        if self.JoystickConfirm:
                            self.mousebuttondown = True
                            self.JoystickConfirm = False

                        else:
                            if self.JoystickConfirm_toggle is False:
                                self.mousebuttondown = False

                    TitleFont = self.TitleFont.render(
                        "Pycraft",
                        self.aa,
                        self.FontCol)
                    TitleWidth = TitleFont.get_width()

                    InfoFont = InfoTitleFont.render(
                        "Settings",
                        self.aa,
                        self.SecondFontCol)

                    FPSFont = VersionFont.render(
                        "".join((f"FPS: Actual: {int(self.eFPS)} ",
                                 f"Max: {int(self.FPS)} ",
                                 f"Average: {int((self.aFPS/self.Iteration))}")),
                        self.aa,
                        self.FontCol)

                    FOVFont = VersionFont.render(
                        f"FOV: {self.FOV}",
                        self.aa,
                        self.FontCol)

                    CamRotFont = VersionFont.render(
                        f"Camera Rotation Speed: {round(self.cameraANGspeed, 1)}",
                        self.aa,
                        self.FontCol)

                    ModeFont = VersionFont.render(
                        "Mode;         ,                 ,            ,          .",
                        self.aa,
                        self.FontCol)

                    AAFont = VersionFont.render(
                        f"Anti-Aliasing: {self.aa}",
                        self.aa,
                        self.FontCol)

                    RenderFogFont = VersionFont.render(
                        f"Render Fog: {self.RenderFOG}",
                        self.aa,
                        self.FontCol)

                    FancySkyFont = VersionFont.render(
                        f"Fancy Graphics: {self.FancyGraphics}",
                        self.aa,
                        self.FontCol)

                    FancyParticleFont = VersionFont.render(
                        f"Fancy Particles: {self.FanPart}",
                        self.aa,
                        self.FontCol)

                    SoundFont = VersionFont.render(
                        f"Sound: {self.sound}",
                        self.aa,
                        self.FontCol)

                    if self.sound:
                        SoundVoltFont = VersionFont.render(
                            f"Sound Volume: {self.soundVOL}%",
                            self.aa,
                            self.FontCol)

                    else:
                        SoundVoltFont = VersionFont.render(
                            f"Sound Volume: {self.soundVOL}%",
                            self.aa,
                            self.ShapeCol)

                    MusicFont = VersionFont.render(
                        f"Music: {self.music}",
                        self.aa,
                        self.FontCol)

                    if self.music:
                        MusicVoltFont = VersionFont.render(
                            f"Music Volume: {self.musicVOL}%",
                            self.aa,
                            self.FontCol)

                    else:
                        MusicVoltFont = VersionFont.render(
                            f"Music Volume: {self.musicVOL}%",
                            self.aa,
                            self.ShapeCol)

                    ThemeFont = VersionFont.render(
                        f"Theme:          ,          | Current Theme: {self.theme}",
                        self.aa,
                        self.FontCol)

                    ToggleControllerSupportFont = VersionFont.render(
                        f"Enable controller support: {not self.UseMouseInput}",
                        self.aa,
                        self.FontCol)

                    ThemeInformationFont = SettingsInformationFont.render(
                        "Gives you control over which theme you can use",
                        self.aa,
                        self.AccentCol)

                    ModeInformationFont = SettingsInformationFont.render(
                        "".join(("Gives you 4 separate pre-sets for settings, ",
                                 "Adaptive mode will automatically adjust your settings")),
                        self.aa,
                        self.AccentCol)

                    FPSInformationFont = SettingsInformationFont.render(
                        "".join(("Controls the maximum frame rate the game ",
                                 "will limit to, does not guarantee that FPS unfortunately")),
                        self.aa,
                        self.AccentCol)

                    FOVInformationFont = SettingsInformationFont.render(
                        "Controls the FOV of the camera in-game",
                        self.aa,
                        self.AccentCol)

                    CameraRotationSpeedInformationFont = SettingsInformationFont.render(
                        "Controls the rotation speed of the camera in-game (1 is low, 5 is high)",
                        self.aa,
                        self.AccentCol)

                    AAInformationFont = SettingsInformationFont.render(
                        "".join(("Enables/Disables anti-aliasing in game and in ",
                                 "the GUI, will give you a minor performance ",
                                 "improvement, mainly for low powered devices")),
                        self.aa,
                        self.AccentCol)

                    RenderFogInformationFont = SettingsInformationFont.render(
                        "".join(("Enables/Disables fog effects in game, for ",
                                 "a small performance benefit")),
                        self.aa,
                        self.AccentCol)

                    FancyGraphicsInformationFont = SettingsInformationFont.render(
                        "".join(("Enables/Disables some graphical features, this ",
                                 "can result in better performance when turned off")),
                        self.aa,
                        self.AccentCol)

                    FancyParticlesInformationFont = SettingsInformationFont.render(
                        "".join(("Enables/Disables particles in game as particles ",
                                 "can have a significant performance decrease")),
                        self.aa,
                        self.AccentCol)

                    SoundInformationFont = SettingsInformationFont.render(
                        "".join(("Enables/Disables sound effects in game, ",
                                 "like for example the click sound and footsteps in game")),
                        self.aa,
                        self.AccentCol)

                    SoundVolInformationFont = SettingsInformationFont.render(
                        "".join(("Controls the volume of the sound effects, ",
                                 "where 100% is maximum and 0% is minimum volume")),
                        self.aa,
                        self.AccentCol)

                    MusicInformationFont = SettingsInformationFont.render(
                        "Enables/Disables music in game, like for example the GUI music",
                        self.aa,
                        self.AccentCol)

                    MusicVolInformationFont = SettingsInformationFont.render(
                        "".join(("Controls the volume of the music, some effects ",
                                 "may not apply until the game reloads")),
                        self.aa,
                        self.AccentCol)

                    ToggleControllerSupportInformationFont = SettingsInformationFont.render(
                        "".join(("Toggles the use of either keyboard and mouse or a ",
                                 "controller to control the mouse and interact with the GUI")),
                        self.aa,
                        self.AccentCol)

                    self.Display.fill(self.BackgroundCol)

                    FPS_rect = self.mod_Pygame__.Rect(
                        50,
                        180+scroll,
                        450*xScaleFact,
                        10)

                    FOV_rect = self.mod_Pygame__.Rect(
                        50,
                        230+scroll,
                        450*xScaleFact,
                        10)

                    CAM_rect = self.mod_Pygame__.Rect(
                        50,
                        280+scroll,
                        450*xScaleFact,
                        10)

                    sound_rect = self.mod_Pygame__.Rect(
                        50,
                        580+scroll,
                        450*xScaleFact,
                        10)

                    music_rect = self.mod_Pygame__.Rect(
                        50,
                        680+scroll,
                        450*xScaleFact,
                        10)

                    aa_rect = self.mod_Pygame__.Rect(
                        50,
                        330+scroll,
                        50,
                        10)

                    RenderFOG_Rect = self.mod_Pygame__.Rect(
                        50,
                        380+scroll,
                        50,
                        10)

                    Fansky_Rect = self.mod_Pygame__.Rect(
                        50,
                        430+scroll,
                        50,
                        10)

                    FanPart_Rect = self.mod_Pygame__.Rect(
                        50,
                        480+scroll,
                        50,
                        10)

                    sound_Rect = self.mod_Pygame__.Rect(
                        50,
                        530+scroll,
                        50,
                        10)

                    music_Rect = self.mod_Pygame__.Rect(
                        50,
                        630+scroll,
                        50,
                        10)

                    Controller_Rect = self.mod_Pygame__.Rect(
                        50,
                        730+scroll,
                        50,
                        10)

                    self.mod_Pygame__.draw.rect(
                        self.Display,
                        self.ShapeCol,
                        FPS_rect,
                        0)

                    self.mod_Pygame__.draw.rect(
                        self.Display,
                        self.ShapeCol,
                        FOV_rect,
                        0)

                    self.mod_Pygame__.draw.rect(
                        self.Display,
                        self.ShapeCol,
                        CAM_rect,
                        0)

                    self.mod_Pygame__.draw.rect(
                        self.Display,
                        self.ShapeCol,
                        sound_rect,
                        0)

                    self.mod_Pygame__.draw.rect(
                        self.Display,
                        self.ShapeCol,
                        music_rect,
                        0)

                    self.mod_Pygame__.draw.rect(
                        self.Display,
                        self.ShapeCol,
                        aa_rect,
                        0)

                    self.mod_Pygame__.draw.rect(
                        self.Display,
                        self.ShapeCol,
                        RenderFOG_Rect,
                        0)

                    self.mod_Pygame__.draw.rect(
                        self.Display,
                        self.ShapeCol,
                        Fansky_Rect,
                        0)

                    self.mod_Pygame__.draw.rect(
                        self.Display,
                        self.ShapeCol,
                        FanPart_Rect,
                        0)

                    self.mod_Pygame__.draw.rect(
                        self.Display,
                        self.ShapeCol,
                        sound_Rect,
                        0)

                    self.mod_Pygame__.draw.rect(
                        self.Display,
                        self.ShapeCol,
                        music_Rect,
                        0)

                    self.mod_Pygame__.draw.rect(
                        self.Display,
                        self.ShapeCol,
                        Controller_Rect,
                        0)

                    if self.mousebuttondown:
                        if ((self.My > 180+scroll and
                                    self.My < 190+scroll) or
                                (FocusedOn[0] and
                                    FocusedOn[1] == "FPS") or
                                (MenuSelector == 2 and
                                    self.UseMouseInput is False)):

                            FocusedOn = [True, "FPS"]
                            if self.UseMouseInput:
                                self.My = 185+scroll

                        else:
                            self.mod_Pygame__.draw.circle(
                                self.Display,
                                (255, 255, 255),
                                (int(self.FPS+45)*xScaleFact,
                                    185+scroll),
                                9)

                        if ((self.My > 230+scroll and
                                    self.My < 240+scroll) or
                                (FocusedOn[0] and
                                    FocusedOn[1] == "FOV") or
                                (MenuSelector == 3 and
                                    self.UseMouseInput is False)):

                            FocusedOn = [True, "FOV"]
                            if self.UseMouseInput:
                                self.My = 235+scroll

                        else:
                            self.mod_Pygame__.draw.circle(
                                self.Display,
                                (255, 255, 255),
                                (int(self.FOV*5)*xScaleFact,
                                    235+scroll),
                                9)

                        if ((self.My > 280+scroll and
                                    self.My < 290+scroll) or
                                (FocusedOn[0] and
                                    FocusedOn[1] == "CAS") or
                                (MenuSelector == 4 and
                                    self.UseMouseInput is False)):

                            FocusedOn = [True, "CAS"] # CAS = Camera Angle Speed
                            if self.UseMouseInput:
                                self.My = 285+scroll

                        else:
                            self.mod_Pygame__.draw.circle(
                                self.Display,
                                (255, 255, 255),
                                ((int(self.cameraANGspeed*89)+45)*xScaleFact,
                                    285+scroll),
                                9)

                        if ((self.My > 580+scroll and
                                    self.My < 590+scroll and
                                    self.sound) or
                                (FocusedOn[0] and
                                    FocusedOn[1] == "SVL") or
                                (MenuSelector == 10 and
                                    self.UseMouseInput is False)):

                            FocusedOn = [True, "SVL"]
                            if self.UseMouseInput:
                                self.My = 585+scroll

                        else:
                            self.mod_Pygame__.draw.circle(
                                self.Display,
                                (255, 255, 255),
                                ((int(self.soundVOL*4.4)+50)*xScaleFact,
                                    585+scroll),
                                9)

                        if ((self.My > 680+scroll and
                                    self.My < 690+scroll and
                                    self.music) or
                                (FocusedOn[0] and
                                    FocusedOn[1] == "MVL") or
                                (MenuSelector == 12 and
                                    self.UseMouseInput is False)):

                            FocusedOn = [True, "MVL"]
                            if self.UseMouseInput:
                                self.My = 685+scroll

                        else:
                            self.mod_Pygame__.draw.circle(
                                self.Display,
                                (255, 255, 255),
                                ((int(self.musicVOL*4.4)+50)*xScaleFact,
                                    685+scroll),
                                9)

                        if ((self.My > 330+scroll and
                                    self.My < 340+scroll) or
                                (MenuSelector == 5 and
                                    self.UseMouseInput is False)):

                            if self.UseMouseInput:
                                self.mod_Pygame__.mouse.set_cursor(
                                    self.mod_Pygame__.SYSTEM_CURSOR_HAND)

                            if self.aa:
                                self.aa = False
                                if self.sound:
                                    self.mod_SoundUtils__.PlaySound.PlayClickSound(self)

                                self.mousebuttondown = False

                            elif self.aa is False:
                                self.aa = True
                                if self.sound:
                                    self.mod_SoundUtils__.PlaySound.PlayClickSound(self)

                                self.mousebuttondown = False

                        if self.aa:
                            self.mod_Pygame__.draw.circle(
                                self.Display,
                                (255, 255, 255),
                                (90, 335+scroll),
                                9)

                            self.mod_Pygame__.draw.circle(
                                self.Display,
                                self.ShapeCol,
                                (90, 335+scroll),
                                6)

                        elif self.aa is False:
                            self.mod_Pygame__.draw.circle(
                                self.Display,
                                (255, 255, 255),
                                (60, 335+scroll),
                                9)

                            self.mod_Pygame__.draw.circle(
                                self.Display,
                                self.ShapeCol,
                                (60, 335+scroll),
                                6)

                        if ((self.My > 380+scroll and
                                    self.My < 390+scroll) or
                                (MenuSelector == 6 and
                                    self.UseMouseInput is False)):

                            if self.UseMouseInput:
                                self.mod_Pygame__.mouse.set_cursor(
                                    self.mod_Pygame__.SYSTEM_CURSOR_HAND)

                            if self.RenderFOG:
                                self.RenderFOG = False
                                if self.sound:
                                    self.mod_SoundUtils__.PlaySound.PlayClickSound(self)

                                self.mousebuttondown = False

                            elif self.RenderFOG is False:
                                self.RenderFOG = True
                                if self.sound:
                                    self.mod_SoundUtils__.PlaySound.PlayClickSound(self)

                                self.mousebuttondown = False

                        if self.RenderFOG:
                            self.mod_Pygame__.draw.circle(
                                self.Display,
                                (255, 255, 255),
                                (90, 385+scroll),
                                9)

                            self.mod_Pygame__.draw.circle(
                                self.Display,
                                self.ShapeCol,
                                (90, 385+scroll),
                                6)

                        elif self.RenderFOG is False:
                            self.mod_Pygame__.draw.circle(
                                self.Display,
                                (255, 255, 255),
                                (60, 385+scroll),
                                9)

                            self.mod_Pygame__.draw.circle(
                                self.Display,
                                self.ShapeCol,
                                (60, 385+scroll),
                                6)

                        if ((self.My > 430+scroll and
                                    self.My < 440+scroll) or
                                (MenuSelector == 7 and
                                    self.UseMouseInput is False)):

                            if self.UseMouseInput:
                                self.mod_Pygame__.mouse.set_cursor(
                                    self.mod_Pygame__.SYSTEM_CURSOR_HAND)

                            if self.FancyGraphics:
                                self.FancyGraphics = False
                                if self.sound:
                                    self.mod_SoundUtils__.PlaySound.PlayClickSound(self)

                                self.mousebuttondown = False

                            elif self.FancyGraphics is False:
                                self.FancyGraphics = True
                                if self.sound:
                                    self.mod_SoundUtils__.PlaySound.PlayClickSound(self)

                                self.mousebuttondown = False

                        if self.FancyGraphics:
                            self.mod_Pygame__.draw.circle(
                                self.Display,
                                (255, 255, 255),
                                (90, 435+scroll),
                                9)

                            self.mod_Pygame__.draw.circle(
                                self.Display,
                                self.ShapeCol,
                                (90, 435+scroll),
                                6)

                        elif self.FancyGraphics is False:
                            self.mod_Pygame__.draw.circle(
                                self.Display,
                                (255, 255, 255),
                                (60, 435+scroll),
                                9)

                            self.mod_Pygame__.draw.circle(
                                self.Display,
                                self.ShapeCol,
                                (60, 435+scroll),
                                6)

                        if ((self.My > 480+scroll and
                                    self.My < 490+scroll) or
                                (MenuSelector == 8 and
                                    self.UseMouseInput is False)):

                            if self.UseMouseInput:
                                self.mod_Pygame__.mouse.set_cursor(
                                    self.mod_Pygame__.SYSTEM_CURSOR_HAND)

                            if self.FanPart:
                                self.FanPart = False
                                if self.sound:
                                    self.mod_SoundUtils__.PlaySound.PlayClickSound(self)

                                self.mousebuttondown = False

                            elif self.FanPart is False:
                                self.FanPart = True
                                if self.sound:
                                    self.mod_SoundUtils__.PlaySound.PlayClickSound(self)

                                self.mousebuttondown = False

                        if self.FanPart:
                            self.mod_Pygame__.draw.circle(
                                self.Display,
                                (255, 255, 255),
                                (90, 485+scroll),
                                9)

                            self.mod_Pygame__.draw.circle(
                                self.Display,
                                self.ShapeCol,
                                (90, 485+scroll),
                                6)

                        elif self.FanPart is False:
                            self.mod_Pygame__.draw.circle(
                                self.Display,
                                (255, 255, 255),
                                (60, 485+scroll),
                                9)

                            self.mod_Pygame__.draw.circle(
                                self.Display,
                                self.ShapeCol,
                                (60, 485+scroll),
                                6)

                        if ((self.My > 530+scroll and
                                    self.My < 540+scroll) or
                                (MenuSelector == 9 and
                                    self.UseMouseInput is False)):

                            if self.UseMouseInput:
                                self.mod_Pygame__.mouse.set_cursor(
                                    self.mod_Pygame__.SYSTEM_CURSOR_HAND)

                            if self.sound:
                                self.sound = False
                                if self.sound:
                                    self.mod_SoundUtils__.PlaySound.PlayClickSound(self)

                                self.mousebuttondown = False

                            elif self.sound is False:
                                self.sound = True
                                if self.sound:
                                    self.mod_SoundUtils__.PlaySound.PlayClickSound(self)

                                self.mousebuttondown = False

                        if self.sound:
                            self.mod_Pygame__.draw.circle(
                                self.Display,
                                (255, 255, 255),
                                (90, 535+scroll), 9)

                            self.mod_Pygame__.draw.circle(
                                self.Display,
                                self.ShapeCol,
                                (90, 535+scroll), 6)

                        elif self.sound is False:
                            self.mod_Pygame__.draw.circle(
                                self.Display,
                                (255, 255, 255),
                                (60, 535+scroll),
                                9)

                            self.mod_Pygame__.draw.circle(
                                self.Display,
                                self.ShapeCol,
                                (60, 535+scroll),
                                6)

                        if ((self.My > 630+scroll and
                                    self.My < 640+scroll and
                                    self.UseMouseInput) or
                                (MenuSelector == 11 and
                                    self.UseMouseInput is False)):

                            if self.UseMouseInput:
                                self.mod_Pygame__.mouse.set_cursor(
                                    self.mod_Pygame__.SYSTEM_CURSOR_HAND)

                            if self.music:
                                self.music = False
                                self.mod_Pygame__.mixer.music.fadeout(500)
                                if self.sound:
                                    self.mod_SoundUtils__.PlaySound.PlayClickSound(self)

                                self.mousebuttondown = False

                            elif self.music is False:
                                self.music = True
                                if self.sound:
                                    self.mod_SoundUtils__.PlaySound.PlayClickSound(self)

                                self.mousebuttondown = False

                        if self.music:
                            self.mod_Pygame__.draw.circle(
                                self.Display,
                                (255, 255, 255),
                                (90, 635+scroll),
                                9)

                            self.mod_Pygame__.draw.circle(
                                self.Display,
                                self.ShapeCol,
                                (90, 635+scroll),
                                6)

                        elif self.music is False:
                            self.mod_Pygame__.draw.circle(
                                self.Display,
                                (255, 255, 255),
                                (60, 635+scroll),
                                9)

                            self.mod_Pygame__.draw.circle(
                                self.Display,
                                self.ShapeCol,
                                (60, 635+scroll),
                                6)

                        if ((self.My > 730+scroll and
                                    self.My < 740+scroll and
                                    self.UseMouseInput) or
                                (MenuSelector == 13 and
                                    self.UseMouseInput is False)):

                            if self.UseMouseInput:
                                self.mod_Pygame__.mouse.set_cursor(
                                    self.mod_Pygame__.SYSTEM_CURSOR_HAND)

                            if self.UseMouseInput:
                                self.UseMouseInput = False
                                if self.sound:
                                    self.mod_SoundUtils__.PlaySound.PlayClickSound(self)

                                self.mousebuttondown = False

                            elif self.UseMouseInput is False:
                                self.UseMouseInput = True
                                if self.sound:
                                    self.mod_SoundUtils__.PlaySound.PlayClickSound(self)

                                self.mousebuttondown = False

                        if not self.UseMouseInput:
                            self.mod_Pygame__.draw.circle(
                                self.Display,
                                (255, 255, 255),
                                (90, 735+scroll),
                                9)

                            self.mod_Pygame__.draw.circle(
                                self.Display,
                                self.ShapeCol,
                                (90, 735+scroll),
                                6)

                        elif not self.UseMouseInput is False:
                            self.mod_Pygame__.draw.circle(
                                self.Display,
                                (255, 255, 255),
                                (60, 735+scroll),
                                9)

                            self.mod_Pygame__.draw.circle(
                                self.Display,
                                self.ShapeCol,
                                (60, 735+scroll),
                                6)

                    else:
                        FocusedOn = [False, None]
                        if self.UseMouseInput:
                            self.mod_Pygame__.mouse.set_visible(True)

                        self.mod_Pygame__.draw.circle(
                            self.Display,
                            (255, 255, 255),
                            ((int(self.soundVOL*4.4)+50)*xScaleFact,
                                585+scroll),
                            9)

                        self.mod_Pygame__.draw.circle(
                            self.Display,
                            (255, 255, 255),
                            ((int(self.FPS+45)*xScaleFact),
                                185+scroll),
                            9)

                        self.mod_Pygame__.draw.circle(
                            self.Display,
                            (255, 255, 255),
                            ((int(self.cameraANGspeed*89)+45)*xScaleFact,
                                285+scroll),
                            9)

                        self.mod_Pygame__.draw.circle(
                            self.Display,
                            (255, 255, 255),
                            ((int(self.FOV*5))*xScaleFact,
                                235+scroll),
                            9)

                        self.mod_Pygame__.draw.circle(
                            self.Display,
                            (255, 255, 255),
                            ((int(self.musicVOL*4.4)+50)*xScaleFact,
                                685+scroll),
                            9)

                        if self.aa:
                            self.mod_Pygame__.draw.circle(
                                self.Display,
                                (255, 255, 255),
                                (90, 335+scroll),
                                9)

                            self.mod_Pygame__.draw.circle(
                                self.Display,
                                self.ShapeCol,
                                (90, 335+scroll),
                                6)

                        elif self.aa is False:
                            self.mod_Pygame__.draw.circle(
                                self.Display,
                                (255, 255, 255),
                                (60, 335+scroll),
                                9)

                            self.mod_Pygame__.draw.circle(
                                self.Display,
                                self.ShapeCol,
                                (60, 335+scroll),
                                6)

                        if self.RenderFOG:
                            self.mod_Pygame__.draw.circle(
                                self.Display,
                                (255, 255, 255),
                                (90, 385+scroll),
                                9)

                            self.mod_Pygame__.draw.circle(
                                self.Display,
                                self.ShapeCol,
                                (90, 385+scroll),
                                6)

                        elif self.RenderFOG is False:
                            self.mod_Pygame__.draw.circle(
                                self.Display,
                                (255, 255, 255),
                                (60, 385+scroll),
                                9)

                            self.mod_Pygame__.draw.circle(
                                self.Display,
                                self.ShapeCol,
                                (60, 385+scroll),
                                6)

                        if self.FancyGraphics:
                            self.mod_Pygame__.draw.circle(
                                self.Display,
                                (255, 255, 255),
                                (90, 435+scroll),
                                9)

                            self.mod_Pygame__.draw.circle(
                                self.Display,
                                self.ShapeCol,
                                (90, 435+scroll),
                                6)

                        elif self.FancyGraphics is False:
                            self.mod_Pygame__.draw.circle(
                                self.Display,
                                (255, 255, 255),
                                (60, 435+scroll),
                                9)

                            self.mod_Pygame__.draw.circle(
                                self.Display,
                                self.ShapeCol,
                                (60, 435+scroll),
                                6)

                        if self.FanPart:
                            self.mod_Pygame__.draw.circle(
                                self.Display,
                                (255, 255, 255),
                                (90, 485+scroll),
                                9)

                            self.mod_Pygame__.draw.circle(
                                self.Display,
                                self.ShapeCol,
                                (90, 485+scroll),
                                6)

                        elif self.FanPart is False:
                            self.mod_Pygame__.draw.circle(
                                self.Display,
                                (255, 255, 255),
                                (60, 485+scroll),
                                9)

                            self.mod_Pygame__.draw.circle(
                                self.Display,
                                self.ShapeCol,
                                (60, 485+scroll),
                                6)

                        if self.sound:
                            self.mod_Pygame__.draw.circle(
                                self.Display,
                                (255, 255, 255),
                                (90, 535+scroll),
                                9)

                            self.mod_Pygame__.draw.circle(
                                self.Display,
                                self.ShapeCol,
                                (90, 535+scroll),
                                6)

                        elif self.sound is False:
                            self.mod_Pygame__.draw.circle(
                                self.Display,
                                (255, 255, 255),
                                (60, 535+scroll),
                                9)

                            self.mod_Pygame__.draw.circle(
                                self.Display,
                                self.ShapeCol,
                                (60, 535+scroll),
                                6)

                        if self.music:
                            self.mod_Pygame__.draw.circle(
                                self.Display,
                                (255, 255, 255),
                                (90, 635+scroll),
                                9)

                            self.mod_Pygame__.draw.circle(
                                self.Display,
                                self.ShapeCol,
                                (90, 635+scroll),
                                6)

                        elif self.music is False:
                            self.mod_Pygame__.draw.circle(
                                self.Display,
                                (255, 255, 255),
                                (60, 635+scroll),
                                9)

                            self.mod_Pygame__.draw.circle(
                                self.Display,
                                self.ShapeCol,
                                (60, 635+scroll),
                                6)

                        if not self.UseMouseInput:
                            self.mod_Pygame__.draw.circle(
                                self.Display,
                                (255, 255, 255),
                                (90, 735+scroll),
                                9)

                            self.mod_Pygame__.draw.circle(
                                self.Display,
                                self.ShapeCol,
                                (90, 735+scroll),
                                6)

                        elif not self.UseMouseInput is False:
                            self.mod_Pygame__.draw.circle(
                                self.Display,
                                (255, 255, 255),
                                (60, 735+scroll),
                                9)

                            self.mod_Pygame__.draw.circle(
                                self.Display,
                                self.ShapeCol,
                                (60, 735+scroll),
                                6)

                        if ((self.My > 330+scroll and
                                    self.My < 340+scroll and
                                    self.UseMouseInput) or
                                (MenuSelector == 5 and
                                    self.UseMouseInput is False)):

                            if self.UseMouseInput:
                                self.mod_Pygame__.mouse.set_cursor(
                                    self.mod_Pygame__.SYSTEM_CURSOR_HAND)

                            self.Display.blit(
                                AAInformationFont,
                                (120, 325+scroll))

                            if self.aa:
                                self.mod_Pygame__.draw.circle(
                                    self.Display,
                                    self.AccentCol,
                                    (90, 335+scroll),
                                    9)

                                self.mod_Pygame__.draw.circle(
                                    self.Display,
                                    self.ShapeCol,
                                    (90, 335+scroll),
                                    6)

                            elif self.aa is False:
                                self.mod_Pygame__.draw.circle(
                                    self.Display,
                                    self.AccentCol,
                                    (60, 335+scroll),
                                    9)

                                self.mod_Pygame__.draw.circle(
                                    self.Display,
                                    self.ShapeCol,
                                    (60, 335+scroll),
                                    6)

                        if ((self.My > 380+scroll and
                                    self.My < 390+scroll and
                                    self.UseMouseInput) or
                                (MenuSelector == 6 and
                                    self.UseMouseInput is False)):

                            if self.UseMouseInput:
                                self.mod_Pygame__.mouse.set_cursor(
                                    self.mod_Pygame__.SYSTEM_CURSOR_HAND)

                            self.Display.blit(
                                RenderFogInformationFont,
                                (120, 375+scroll))

                            if self.RenderFOG:
                                self.mod_Pygame__.draw.circle(
                                    self.Display,
                                    self.AccentCol,
                                    (90, 385+scroll),
                                    9)

                                self.mod_Pygame__.draw.circle(
                                    self.Display,
                                    self.ShapeCol,
                                    (90, 385+scroll),
                                    6)

                            elif self.RenderFOG is False:
                                self.mod_Pygame__.draw.circle(
                                    self.Display,
                                    self.AccentCol,
                                    (60, 385+scroll),
                                    9)

                                self.mod_Pygame__.draw.circle(
                                    self.Display,
                                    self.ShapeCol,
                                    (60, 385+scroll),
                                    6)

                        if ((self.My > 430+scroll and
                                    self.My < 440+scroll and
                                    self.UseMouseInput) or
                                (MenuSelector == 7 and
                                    self.UseMouseInput is False)):

                            if self.UseMouseInput:
                                self.mod_Pygame__.mouse.set_cursor(
                                    self.mod_Pygame__.SYSTEM_CURSOR_HAND)

                            self.Display.blit(
                                FancyGraphicsInformationFont,
                                (120, 425+scroll))

                            if self.FancyGraphics:
                                self.mod_Pygame__.draw.circle(
                                    self.Display,
                                    self.AccentCol,
                                    (90, 435+scroll),
                                    9)

                                self.mod_Pygame__.draw.circle(
                                    self.Display,
                                    self.ShapeCol,
                                    (90, 435+scroll),
                                    6)

                            elif self.FancyGraphics is False:
                                self.mod_Pygame__.draw.circle(
                                    self.Display,
                                    self.AccentCol,
                                    (60, 435+scroll),
                                    9)

                                self.mod_Pygame__.draw.circle(
                                    self.Display,
                                    self.ShapeCol,
                                    (60, 435+scroll),
                                    6)


                        if ((self.My > 480+scroll and
                                    self.My < 490+scroll and
                                    self.UseMouseInput) or
                                (MenuSelector == 8 and
                                    self.UseMouseInput is False)):

                            self.Display.blit(
                                FancyParticlesInformationFont,
                                (120, 475+scroll))

                            if self.UseMouseInput:
                                self.mod_Pygame__.mouse.set_cursor(
                                    self.mod_Pygame__.SYSTEM_CURSOR_HAND)

                            if self.FanPart:
                                self.mod_Pygame__.draw.circle(
                                    self.Display,
                                    self.AccentCol,
                                    (90, 485+scroll),
                                    9)

                                self.mod_Pygame__.draw.circle(
                                    self.Display,
                                    self.ShapeCol,
                                    (90, 485+scroll),
                                    6)

                            elif self.FanPart is False:
                                self.mod_Pygame__.draw.circle(
                                    self.Display,
                                    self.AccentCol,
                                    (60, 485+scroll),
                                    9)

                                self.mod_Pygame__.draw.circle(
                                    self.Display,
                                    self.ShapeCol,
                                    (60, 485+scroll),
                                    6)

                        if ((self.My > 530+scroll and
                                    self.My < 540+scroll and
                                    self.UseMouseInput) or
                                (MenuSelector == 9 and
                                 self.UseMouseInput is False)):

                            self.Display.blit(
                                SoundInformationFont,
                                (120, 525+scroll))

                            if self.UseMouseInput:
                                self.mod_Pygame__.mouse.set_cursor(
                                    self.mod_Pygame__.SYSTEM_CURSOR_HAND)

                            if self.sound:
                                self.mod_Pygame__.draw.circle(
                                    self.Display,
                                    self.AccentCol,
                                    (90, 535+scroll),
                                    9)

                                self.mod_Pygame__.draw.circle(
                                    self.Display,
                                    self.ShapeCol,
                                    (90, 535+scroll),
                                    6)

                            elif self.sound is False:
                                self.mod_Pygame__.draw.circle(
                                    self.Display,
                                    self.AccentCol,
                                    (60, 535+scroll),
                                    9)

                                self.mod_Pygame__.draw.circle(
                                    self.Display,
                                    self.ShapeCol,
                                    (60, 535+scroll),
                                    6)

                        if ((self.My > 630+scroll and
                                    self.My < 640+scroll and
                                    self.UseMouseInput) or
                                (MenuSelector == 11 and
                                    self.UseMouseInput is False)):

                            if self.UseMouseInput:
                                self.mod_Pygame__.mouse.set_cursor(
                                    self.mod_Pygame__.SYSTEM_CURSOR_HAND)

                            self.Display.blit(
                                MusicInformationFont,
                                (120, 625+scroll))

                            if self.music:
                                self.mod_Pygame__.draw.circle(
                                    self.Display,
                                    self.AccentCol,
                                    (90, 635+scroll),
                                    9)

                                self.mod_Pygame__.draw.circle(
                                    self.Display,
                                    self.ShapeCol,
                                    (90, 635+scroll),
                                    6)

                            elif self.music is False:
                                self.mod_Pygame__.draw.circle(
                                    self.Display,
                                    self.AccentCol,
                                    (60, 635+scroll),
                                    9)

                                self.mod_Pygame__.draw.circle(
                                    self.Display,
                                    self.ShapeCol,
                                    (60, 635+scroll),
                                    6)

                        if ((self.My > 730+scroll and
                                    self.My < 740+scroll and
                                    self.UseMouseInput) or
                                (MenuSelector == 13 and
                                    self.UseMouseInput is False)):

                            if self.UseMouseInput:
                                self.mod_Pygame__.mouse.set_cursor(
                                    self.mod_Pygame__.SYSTEM_CURSOR_HAND)

                            self.Display.blit(
                                ToggleControllerSupportInformationFont,
                                (120, 725+scroll))

                            if not self.UseMouseInput:
                                self.mod_Pygame__.draw.circle(
                                    self.Display,
                                    (255, 255, 255),
                                    (90, 735+scroll),
                                    9)

                                self.mod_Pygame__.draw.circle(
                                    self.Display,
                                    self.ShapeCol,
                                    (90, 735+scroll),
                                    6)

                            elif not self.UseMouseInput is False:
                                self.mod_Pygame__.draw.circle(
                                    self.Display,
                                    (255, 255, 255),
                                    (60, 735+scroll),
                                    9)

                                self.mod_Pygame__.draw.circle(
                                    self.Display,
                                    self.ShapeCol,
                                    (60, 735+scroll),
                                    6)

                    if ((self.My >= 65+scroll and
                                self.My <= 75+scroll) or
                            (MenuSelector == 0 and
                                self.UseMouseInput is False)):

                        if self.UseMouseInput:
                            self.mod_Pygame__.mouse.set_cursor(self.mod_Pygame__.SYSTEM_CURSOR_HAND)

                        self.Display.blit(
                            ThemeInformationFont,
                            (300, 67+scroll))

                    if ((self.My >= 65+scroll and
                                self.My <= 75+scroll and
                                self.Mx >= 55 and
                                self.Mx <= 95) or
                            (MenuSelector == 0 and
                                self.UseMouseInput is False and
                                LeftAndRight == 0)):

                        if self.UseMouseInput:
                            self.mod_Pygame__.mouse.set_cursor(self.mod_Pygame__.SYSTEM_CURSOR_HAND)

                        LightTheme = LightThemeFont.render(
                            "Light",
                            self.aa,
                            self.AccentCol)
                        LightThemeFont.set_underline(True)

                        if self.mousebuttondown:
                            self.theme = "light"
                            self.mod_ThemeUtils__.DetermineThemeColours.GetColours(self)
                            if self.sound:
                                self.mod_SoundUtils__.PlaySound.PlayClickSound(self)

                            self.mousebuttondown = False

                    else:
                        if (self.UseMouseInput is False and
                                LeftAndRight < 0 and
                                MenuSelector == 0):

                            LeftAndRight = 1

                        LightTheme = LightThemeFont.render(
                            "Light",
                            self.aa,
                            self.FontCol)
                        LightThemeFont.set_underline(False)

                    if ((self.My >= 65+scroll and
                                self.My <= 75+scroll and
                                self.Mx >= 95 and
                                self.Mx <= 135) or
                            (MenuSelector == 0 and
                                self.UseMouseInput is False and
                                LeftAndRight == 1)):

                        if self.UseMouseInput:
                            self.mod_Pygame__.mouse.set_cursor(self.mod_Pygame__.SYSTEM_CURSOR_HAND)

                        DarkTheme = DarkThemeFont.render(
                            "Dark",
                            self.aa,
                            self.AccentCol)
                        DarkThemeFont.set_underline(True)

                        if self.mousebuttondown:
                            self.theme = "dark"
                            self.mod_ThemeUtils__.DetermineThemeColours.GetColours(self)
                            if self.sound:
                                self.mod_SoundUtils__.PlaySound.PlayClickSound(self)

                            self.mousebuttondown = False

                    else:
                        if (self.UseMouseInput is False and
                                LeftAndRight > 1 and
                                MenuSelector == 0):

                            LeftAndRight = 0

                        DarkTheme = DarkThemeFont.render(
                            "Dark",
                            self.aa,
                            self.FontCol)
                        DarkThemeFont.set_underline(False)

                    if ((self.My >= 85+scroll and
                                self.My <= 95+scroll) or
                            (MenuSelector == 1 and
                                self.UseMouseInput is False)):

                        if self.UseMouseInput:
                            self.mod_Pygame__.mouse.set_cursor(self.mod_Pygame__.SYSTEM_CURSOR_HAND)

                        self.Display.blit(
                            ModeInformationFont,
                            (300, 85+scroll))

                    if ((self.My > 680+scroll and
                                self.My < 690+scroll and
                                self.UseMouseInput) or
                            (MenuSelector == 12 and
                                self.UseMouseInput is False)):

                        if self.UseMouseInput:
                            self.mod_Pygame__.mouse.set_cursor(self.mod_Pygame__.SYSTEM_CURSOR_HAND)

                        self.Display.blit(
                            MusicVolInformationFont,
                            (520*xScaleFact, 675+scroll))

                    if ((self.My > 580+scroll and
                                self.My < 590+scroll and
                                self.UseMouseInput) or
                            (MenuSelector == 10 and
                                self.UseMouseInput is False)):

                        if self.UseMouseInput:
                            self.mod_Pygame__.mouse.set_cursor(self.mod_Pygame__.SYSTEM_CURSOR_HAND)

                        self.Display.blit(
                            SoundVolInformationFont,
                            (520*xScaleFact, 575+scroll))

                    if ((self.My > 280+scroll and
                                self.My < 290+scroll and
                                self.UseMouseInput) or
                            (MenuSelector == 4 and
                                self.UseMouseInput is False)):

                        if self.UseMouseInput:
                            self.mod_Pygame__.mouse.set_cursor(self.mod_Pygame__.SYSTEM_CURSOR_HAND)

                        self.Display.blit(
                            CameraRotationSpeedInformationFont,
                            (520*xScaleFact, 275+scroll))

                    if ((self.My > 230+scroll and
                                self.My < 240+scroll and
                                self.UseMouseInput) or
                            (MenuSelector == 3 and
                                self.UseMouseInput is False)):

                        if self.UseMouseInput:
                            self.mod_Pygame__.mouse.set_cursor(self.mod_Pygame__.SYSTEM_CURSOR_HAND)

                        self.Display.blit(
                            FOVInformationFont,
                            (520*xScaleFact, 225+scroll))

                    if ((self.My > 180+scroll and
                                self.My < 190+scroll and
                                self.UseMouseInput) or
                            (MenuSelector == 2 and
                                self.UseMouseInput is False)):

                        if self.UseMouseInput:
                            self.mod_Pygame__.mouse.set_cursor(self.mod_Pygame__.SYSTEM_CURSOR_HAND)

                        self.Display.blit(
                            FPSInformationFont,
                            (520*xScaleFact, 175+scroll))

                    if ((self.My >= 85+scroll and
                                self.My <= 95+scroll and
                                self.Mx >= 40 and
                                self.Mx <= 80) or
                            (MenuSelector == 1 and
                                self.UseMouseInput is False and
                                LeftAndRight == 0)):

                        if self.UseMouseInput:
                            self.mod_Pygame__.mouse.set_cursor(self.mod_Pygame__.SYSTEM_CURSOR_HAND)

                        LOWtFont = LOWFont.render(
                            "Low",
                            self.aa,
                            self.AccentCol)
                        LOWFont.set_underline(True)

                        if self.mousebuttondown:
                            self.SettingsPreference = "Low"
                            self.FPS = 15
                            self.aa = False
                            self.RenderFOG = False
                            self.FancyGraphics = False
                            self.FanPart = False
                            self.mousebuttondown = False

                            if self.sound:
                                self.mod_SoundUtils__.PlaySound.PlayClickSound(self)

                            self.aFPS = (self.aFPS/self.Iteration)
                            self.Iteration = 1

                    else:
                        if (self.UseMouseInput is False and
                                LeftAndRight < 0 and
                                MenuSelector == 1):

                            LeftAndRight = 1

                        LOWtFont = LOWFont.render(
                            "Low",
                            self.aa,
                            self.FontCol)
                        LOWFont.set_underline(False)

                    if ((self.My >= 85+scroll and
                                self.My <= 95+scroll and
                                self.Mx >= 90 and
                                self.Mx <= 155) or
                            (MenuSelector == 1 and
                                self.UseMouseInput is False and
                                LeftAndRight == 1)):

                        if self.UseMouseInput:
                            self.mod_Pygame__.mouse.set_cursor(self.mod_Pygame__.SYSTEM_CURSOR_HAND)

                        MEDIUMtFont = MEDIUMFont.render(
                            "Medium",
                            self.aa,
                            self.AccentCol)
                        MEDIUMFont.set_underline(True)

                        if self.mousebuttondown:
                            self.SettingsPreference = "Medium"
                            self.FPS = 30
                            self.aa = True
                            self.RenderFOG = False
                            self.FancyGraphics = True
                            self.FanPart = False

                            if self.sound:
                                self.mod_SoundUtils__.PlaySound.PlayClickSound(self)

                            self.mousebuttondown = False
                            self.aFPS = (self.aFPS/self.Iteration)
                            self.Iteration = 1

                    else:
                        MEDIUMtFont = MEDIUMFont.render(
                            "Medium",
                            self.aa,
                            self.FontCol)
                        MEDIUMFont.set_underline(False)

                    if ((self.My >= 85+scroll and
                                self.My <= 95+scroll and
                                self.Mx >= 165 and
                                self.Mx <= 205) or
                            (MenuSelector == 1 and
                                self.UseMouseInput is False and LeftAndRight == 2)):

                        if self.UseMouseInput:
                            self.mod_Pygame__.mouse.set_cursor(self.mod_Pygame__.SYSTEM_CURSOR_HAND)

                        HIGHFontText = HIGHFont.render(
                            "High",
                            self.aa,
                            self.AccentCol)

                        HIGHFont.set_underline(True)

                        if self.mousebuttondown:
                            self.SettingsPreference = "High"
                            self.FPS = 60
                            self.aa = True
                            self.RenderFOG = True
                            self.FancyGraphics = True
                            self.FanPart = True

                            if self.sound:
                                self.mod_SoundUtils__.PlaySound.PlayClickSound(self)

                            self.mousebuttondown = False
                            self.aFPS = (self.aFPS/self.Iteration)
                            self.Iteration = 1

                    else:
                        HIGHFontText = HIGHFont.render(
                            "High",
                            self.aa,
                            self.FontCol)

                        HIGHFont.set_underline(False)

                    if ((self.My >= 85+scroll and
                                self.My <= 95+scroll and
                                self.Mx >= 215 and
                                self.Mx <= 300) or
                            (MenuSelector == 1 and
                                self.UseMouseInput is False and
                                LeftAndRight == 3)):

                        if self.UseMouseInput:
                            self.mod_Pygame__.mouse.set_cursor(self.mod_Pygame__.SYSTEM_CURSOR_HAND)

                        ADAPTIVEtFont = ADAPTIVEFont.render(
                            "Adaptive",
                            self.aa,
                            self.AccentCol)
                        ADAPTIVEFont.set_underline(True)

                        if self.mousebuttondown:
                            self.SettingsPreference = "Adaptive"
                            self.FPS = (self.mod_Psutil__.cpu_freq(percpu=True)[0][2])/35

                            CPU_Freq = (self.mod_Psutil__.cpu_freq(percpu=True)[0][2])/10
                            MEM_Total = self.mod_Psutil__.virtual_memory().total

                            if (CPU_Freq > 300 and
                                    MEM_Total > 8589934592):

                                self.aa = True
                                self.RenderFog = True
                                self.FancyGraphics = True
                                self.FanPart = True

                            elif (CPU_Freq > 200 and
                                    MEM_Total > 4294967296):

                                self.aa = True
                                self.RenderFog = True
                                self.FancyGraphics = True
                                self.FanPart = False

                            elif (CPU_Freq > 100 and
                                    MEM_Total > 2147483648):

                                self.aa = False
                                self.RenderFog = False
                                self.FancyGraphics = True
                                self.FanPart = False

                            elif (CPU_Freq < 100 and
                                    CPU_Freq > 75 and
                                    MEM_Total > 1073741824):

                                self.aa = False
                                self.RenderFog = False
                                self.FancyGraphics = False
                                self.FanPart = False

                            if self.sound:
                                self.mod_SoundUtils__.PlaySound.PlayClickSound(self)

                            self.mousebuttondown = False

                    else:
                        if (self.UseMouseInput is False and
                                LeftAndRight > 3 and
                                MenuSelector == 1):

                            LeftAndRight = 0

                        ADAPTIVEtFont = ADAPTIVEFont.render(
                            "Adaptive",
                            self.aa,
                            self.FontCol)
                        ADAPTIVEFont.set_underline(False)


                    if (FocusedOn[0] and
                            FocusedOn[1] == "FPS"):

                        if self.UseMouseInput:
                            self.mod_Pygame__.mouse.set_visible(False)

                        if self.Mx > TempMx and self.FPS < 445:
                            self.FPS += 1

                        elif self.Mx < TempMx and self.FPS > 15:
                            self.FPS -= 1

                        if self.FPS < 15:
                            self.FPS = 16

                        elif self.FPS > 445:
                            self.FPS = 444

                        if self.FancyGraphics:
                            ChangeLine.append(
                                (int(self.FPS+45)*xScaleFact,
                                 185+scroll))

                            if len(ChangeLine) >= 2:
                                self.mod_Pygame__.draw.lines(
                                    self.Display,
                                    self.AccentCol,
                                    False,
                                    ChangeLine)

                        self.aFPS = (self.aFPS/self.Iteration)
                        self.Iteration = 1

                        self.mod_Pygame__.draw.circle(
                            self.Display,
                            self.AccentCol,
                            (int(self.FPS+45)*xScaleFact,
                                185+scroll),
                            9)

                        MoveToPosition[0] = True

                    else:
                        if MoveToPosition[0]:
                            ChangeLine = []
                            self.mod_Pygame__.mouse.set_pos(
                                (int(self.FPS+45)*xScaleFact),
                                185+scroll)

                            MoveToPosition[0] = False

                    if (FocusedOn[0] and
                            FocusedOn[1] == "FOV"):

                        if self.UseMouseInput:
                            self.mod_Pygame__.mouse.set_visible(False)

                        if self.Mx > TempMx and self.FOV < 98:
                            self.FOV += 1

                        elif self.Mx < TempMx and self.FOV > 12:
                            self.FOV -= 1

                        if self.FOV < 12:
                            self.FOV = 13

                        elif self.FOV > 98:
                            self.FOV = 97

                        if self.FancyGraphics:
                            ChangeLine.append(
                                (int(self.FOV*5)*xScaleFact,
                                    235+scroll))

                            if len(ChangeLine) >= 2:
                                self.mod_Pygame__.draw.lines(
                                    self.Display,
                                    self.AccentCol,
                                    False,
                                    ChangeLine)

                        self.mod_Pygame__.draw.circle(
                            self.Display,
                            self.AccentCol,
                            (int(self.FOV*5)*xScaleFact,
                             235+scroll),
                            9)

                        MoveToPosition[1] = True

                    else:
                        if MoveToPosition[1]:
                            ChangeLine = []

                            self.mod_Pygame__.mouse.set_pos(
                                (int(self.FOV*5)*xScaleFact),
                                235+scroll)

                            MoveToPosition[1] = False

                    if (FocusedOn[0] and FocusedOn[1] == "CAS"):
                        if self.UseMouseInput:
                            self.mod_Pygame__.mouse.set_visible(False)

                        if self.Mx > TempMx and self.cameraANGspeed < 5.0:
                            self.cameraANGspeed += 0.1

                        elif self.Mx < TempMx and self.cameraANGspeed > 0.0:
                            self.cameraANGspeed -= 0.1

                        if self.cameraANGspeed > 5.0:
                            self.cameraANGspeed = 4.9

                        elif self.cameraANGspeed <= 0:
                            self.cameraANGspeed = 0.1

                        if self.FancyGraphics:
                            ChangeLine.append(
                                ((int(self.cameraANGspeed*89)+45)*xScaleFact,
                                 285+scroll))

                            if len(ChangeLine) >= 2:
                                self.mod_Pygame__.draw.lines(
                                    self.Display,
                                    self.AccentCol,
                                    False,
                                    ChangeLine)

                        self.mod_Pygame__.draw.circle(
                            self.Display,
                            self.AccentCol,
                            ((int(self.cameraANGspeed*89)+45)*xScaleFact,
                             285+scroll),
                            9)

                        MoveToPosition[2] = True

                    else:
                        if MoveToPosition[2]:
                            ChangeLine = []
                            self.mod_Pygame__.mouse.set_pos(
                                ((int(self.cameraANGspeed*89)+45)*xScaleFact),
                                285+scroll)

                            MoveToPosition[2] = False

                    if (FocusedOn[0] and
                            FocusedOn[1] == "SVL"):

                        if self.UseMouseInput:
                            self.mod_Pygame__.mouse.set_visible(False)

                        if self.Mx > TempMx and self.soundVOL < 100:
                            self.soundVOL += 1

                        elif self.Mx < TempMx and self.soundVOL > 0:
                            self.soundVOL -= 1

                        if self.soundVOL > 100:
                            self.soundVOL = 100

                        elif self.soundVOL < 0:
                            self.soundVOL = 0

                        if self.FancyGraphics:
                            ChangeLine.append(
                                ((int(self.soundVOL*4.4)+50)*xScaleFact,
                                 585+scroll))

                            if len(ChangeLine) >= 2:
                                self.mod_Pygame__.draw.lines(
                                    self.Display,
                                    self.AccentCol,
                                    False,
                                    ChangeLine)

                        self.mod_Pygame__.draw.circle(
                            self.Display,
                            self.AccentCol,
                            ((int(self.soundVOL*4.4)+50)*xScaleFact,
                                585+scroll),
                            9)

                        MoveToPosition[3] = True

                    else:
                        if MoveToPosition[3]:
                            ChangeLine = []
                            self.mod_Pygame__.mouse.set_pos(
                                ((int(self.soundVOL*4.4)+50)*xScaleFact),
                                585+scroll)

                            MoveToPosition[3] = False

                    if (FocusedOn[0] and FocusedOn[1] == "MVL"):
                        if self.UseMouseInput:
                            self.mod_Pygame__.mouse.set_visible(False)

                        if self.Mx > TempMx and self.musicVOL < 100:
                            self.musicVOL += 1

                        elif self.Mx < TempMx and self.musicVOL > 0:
                            self.musicVOL -= 1

                        if self.musicVOL > 100:
                            self.musicVOL = 100

                        elif self.musicVOL < 0:
                            self.musicVOL = 0

                        if self.FancyGraphics:
                            ChangeLine.append(
                                ((int(self.musicVOL*4.4)+50)*xScaleFact,
                                 685+scroll))

                            if len(ChangeLine) >= 2:
                                self.mod_Pygame__.draw.lines(
                                    self.Display,
                                    self.AccentCol,
                                    False,
                                    ChangeLine)

                        self.mod_Pygame__.draw.circle(
                            self.Display,
                            self.AccentCol,
                            ((int(self.musicVOL*4.4)+50)*xScaleFact,
                             685+scroll),
                            9)

                        MoveToPosition[4] = True

                    else:
                        if MoveToPosition[4]:
                            ChangeLine = []
                            self.mod_Pygame__.mouse.set_pos(
                                ((int(self.musicVOL*4.4)+50)*xScaleFact),
                                685+scroll)

                            MoveToPosition[4] = False

                    self.Display.blit(
                        FPSFont,
                        (0, 150+scroll))

                    self.Display.blit(
                        FOVFont,
                        (0, 200+scroll))

                    self.Display.blit(
                        CamRotFont,
                        (0, 250+scroll))

                    self.Display.blit(
                        ModeFont,
                        (0, 85+scroll))

                    self.Display.blit(
                        LOWtFont,
                        (48, 85+scroll))

                    self.Display.blit(
                        MEDIUMtFont,
                        (90, 85+scroll))

                    self.Display.blit(
                        HIGHFontText,
                        (165, 85+scroll))

                    self.Display.blit(
                        ADAPTIVEtFont,
                        (215, 85+scroll))

                    self.Display.blit(
                        AAFont,
                        (0, 300+scroll))

                    self.Display.blit(
                        RenderFogFont,
                        (0, 350+scroll))

                    self.Display.blit(
                        FancySkyFont,
                        (0, 400+scroll))

                    self.Display.blit(
                        FancyParticleFont,
                        (0, 450+scroll))

                    self.Display.blit(
                        SoundFont,
                        (0, 500+scroll))

                    self.Display.blit(
                        SoundVoltFont,
                        (0, 550+scroll))

                    self.Display.blit(
                        MusicFont,
                        (0, 600+scroll))

                    self.Display.blit(
                        MusicVoltFont,
                        (0, 650+scroll))

                    self.Display.blit(
                        ToggleControllerSupportFont,
                        (0, 700+scroll))

                    self.Display.blit(
                        ThemeFont,
                        (0, 65+scroll))

                    self.Display.blit(
                        LightTheme,
                        (55, 65+scroll))

                    self.Display.blit(
                        DarkTheme,
                        (95, 65+scroll))

                    self.mod_Pygame__.draw.circle(
                        self.Display,
                        self.ShapeCol,
                        (int(self.FPS+45)*xScaleFact,
                            185+scroll),
                        6)

                    self.mod_Pygame__.draw.circle(
                        self.Display,
                        self.ShapeCol,
                        (int(self.FOV*5)*xScaleFact,
                            235+scroll),
                        6)

                    self.mod_Pygame__.draw.circle(
                        self.Display,
                        self.ShapeCol,
                        ((int(self.cameraANGspeed*89)+45)*xScaleFact,
                            285+scroll),
                        6)

                    self.mod_Pygame__.draw.circle(
                        self.Display,
                        self.ShapeCol,
                        ((int(self.soundVOL*4.4)+50)*xScaleFact,
                         585+scroll),
                        6)

                    self.mod_Pygame__.draw.circle(
                        self.Display,
                        self.ShapeCol,
                        ((int(self.musicVOL*4.4)+50)*xScaleFact,
                         685+scroll),
                        6)

                    cover_Rect = self.mod_Pygame__.Rect(
                        0,
                        0,
                        1280,
                        100)

                    self.mod_Pygame__.draw.rect(
                        self.Display,
                        (self.BackgroundCol),
                        cover_Rect)

                    self.Display.blit(
                        TitleFont,
                        ((self.realWidth-TitleWidth)/2, 0))

                    self.Display.blit(
                        InfoFont,
                        (((self.realWidth-TitleWidth)/2)+55, 50))

                    if self.realHeight <= 760:
                        self.mod_Pygame__.draw.line(
                            self.Display,
                            self.ShapeCol,
                            (self.realWidth-10, scroll+40),
                            (self.realWidth-10, self.realHeight+(scroll-40)+5),
                            1)

                        if self.UseMouseInput is False:
                            if MenuSelector >= 11 and scroll > -40:
                                scroll -= 5/(self.FPS/(self.aFPS/self.Iteration))

                            if MenuSelector <= 5 and scroll < 50:
                                scroll += 5/(self.FPS/(self.aFPS/self.Iteration))

                    else:
                        scroll = 50

                    self.mod_DrawingUtils__.GenerateGraph.CreateDevmodeGraph(
                        self,
                        DataFont)

                    if self.GoTo is None:
                        self.mod_DisplayUtils__.DisplayAnimations.FadeIn(self)

                    else:
                        self.mod_DisplayUtils__.DisplayAnimations.FadeOut(
                            self)

                    if self.StartAnimation is False and (self.GoTo is not None):
                        return None

                    self.mod_Pygame__.display.flip()
                    self.clock.tick(
                        self.mod_DisplayUtils__.DisplayUtils.GetPlayStatus(self))

                    self.RunTimer += self.mod_Time__.perf_counter()-StartTime

                    if self.ErrorMessage is not None:
                        self.ErrorMessage = "".join(("Settings > GenerateSettings ",
                                                     f"> settings: {str(self.ErrorMessage)}"))

                        self.ErrorMessage_detailed = "".join(
                            self.mod_Traceback__.format_exception(
                                None,
                                Message,
                                Message.__traceback__))

                        self.mod_ErrorUtils__.GenerateErrorScreen.ErrorScreen(self)

            except Exception as Message:
                self.ErrorMessage = "Settings > GenerateSettings > settings: "+str(Message)

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
