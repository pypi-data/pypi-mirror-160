if __name__ != "__main__":
    print("Started <Pycraft_Credits>")

    class GenerateCredits:
        def __init__(self):
            pass

        def Credits(self):
            try:
                self.mod_CaptionUtils__.GenerateCaptions.GetNormalCaption(
                    self,
                    "Credits")

                if self.platform == "Linux":
                    DataFont = self.mod_Pygame__.font.Font(
                        self.mod_OS__.path.join(
                            self.base_folder, ("Fonts//Book Antiqua.ttf")), 15)

                    LargeCreditsFont = self.mod_Pygame__.font.Font(
                        self.mod_OS__.path.join(
                            self.base_folder, ("Fonts//Book Antiqua.ttf")), 20)

                    InfoTitleFont = self.mod_Pygame__.font.Font(
                        self.mod_OS__.path.join(
                            self.base_folder, ("Fonts//Book Antiqua.ttf")), 35)

                    SmallCreditsFont = self.mod_Pygame__.font.Font(
                        self.mod_OS__.path.join(
                            self.base_folder, ("Fonts//Book Antiqua.ttf")), 15)

                else:
                    DataFont = self.mod_Pygame__.font.Font(
                        self.mod_OS__.path.join(
                            self.base_folder, ("Fonts\\Book Antiqua.ttf")), 15)

                    LargeCreditsFont = self.mod_Pygame__.font.Font(
                        self.mod_OS__.path.join(
                            self.base_folder, ("Fonts\\Book Antiqua.ttf")), 20)

                    InfoTitleFont = self.mod_Pygame__.font.Font(
                        self.mod_OS__.path.join(
                            self.base_folder, ("Fonts\\Book Antiqua.ttf")), 35)

                    SmallCreditsFont = self.mod_Pygame__.font.Font(
                        self.mod_OS__.path.join(
                            self.base_folder, ("Fonts\\Book Antiqua.ttf")), 15)

                TitleFont = self.TitleFont.render(
                    "Pycraft",
                    self.aa,
                    self.FontCol)
                TitleWidth = TitleFont.get_width()
                TitleHeight = TitleFont.get_height()

                CreditsFont = InfoTitleFont.render(
                    "Credits",
                    self.aa,
                    self.SecondFontCol)

                CreditsString = [f"Pycraft: v{self.version}",
                                    " ",
                                    " ",
                                    "Game Director: Tom Jebbo",
                                    " ",
                                    "Art and Music Lead: Tom Jebbo",
                                    " ",
                                    "Additional Music Credits:",
                                    "".join(("Freesound: - Erokia's 'ambient wave compilation' ",
                                             "@ freesound.org/s/473545")),

                                    "".join(("Freesound: - Soundholder's ",
                                                "'ambient meadow near forest' @ ",
                                                "freesound.org/s/425368")),

                                    "".join(("Freesound: - Monte32's 'Footsteps_6_Dirt_shoe' ",
                                                "@ freesound.org/people/monte32/sounds/353799")),

                                    "".join(("Freesound: - Straget's 'Thunder' @ ",
                                                "https://freesound.org/people/straget/sounds/527664/")),

                                    "".join(("Freesound: - FlatHill's 'Rain and Thunder 4' @ ",
                                                "https://freesound.org/people/FlatHill/sounds/237729/")),

                                    "".join(("Freesound: - BlueDelta's 'Heavy Thunder Strike ",
                                                "- no Rain - QUADRO' @ ",
                                                "https://freesound.org/people/BlueDelta/sounds/446753/")),

                                    "".join(("Freesound: - Justkiddink's 'Thunder » Dry thunder1' @ ",
                                                "https://freesound.org/people/juskiddink/sounds/101933/")),

                                    "".join(("Freesound: - Netaj's 'Thunder' @ ",
                                                "https://freesound.org/people/netaj/sounds/193170/")),

                                    "".join(("Freesound: - Nimlos' 'Thunders » Rain Thunder' @ ",
                                                "https://freesound.org/people/Nimlos/sounds/359151/")),

                                    "".join(("Freesound: - Kangaroovindaloo's 'Thunder Clap' @ ",
                                                "https://freesound.org/people/kangaroovindaloo/sounds/585077/")),

                                    "".join(("Freesound: - Laribum's 'Thunder » thunder_01' @ "
                                             "https://freesound.org/people/laribum/sounds/353025/")),

                                    "".join(("Freesound: - Jmbphilmes's 'Rain » Rain light 2 (rural)' @ "
                                             "https://freesound.org/people/jmbphilmes/sounds/200273/")),

                                    " ",
                                    "Pycraft was developed in collaboration with:",
                                    "Dogukan Demir (https://github.com/demirdogukan)",
                                    "Henry Post (https://github.com/HenryFBP)",
                                    "".join(("Count of Freshness Traversal ",
                                             "(https://twitter.com/DmitryChunikhinn)")),
                                    " ",
                                    "With thanks to the developers of:",
                                    "Glcontext",
                                    "GPUtil",
                                    "Moderngl",
                                    "Moderngl-Window",
                                    "MouseInfo",
                                    "MultipleDispatch",
                                    "Numpy",
                                    "Pillow",
                                    "Psutil",
                                    "py-Cpuinfo",
                                    "PyAutoGUI",
                                    "Pygame",
                                    "PyGetWindow",
                                    "Pyglet",
                                    "PyJoystick",
                                    "PyMsgBox",
                                    "Pyperclip",
                                    "PyRect",
                                    "Pyrr",
                                    "PyScreeze",
                                    "PySDL2",
                                    "pytweening",
                                    "PyWavefront",
                                    "Resource-Man",
                                    "Six",
                                    "Microsoft Visual Studio Code",
                                    "",
                                    "".join(("For a more in depth accreditation ",
                                             "please check Pycraft's GitHub Page ",
                                             "here: github.com/PycraftDeveloper/Pycraft")),
                                    " ",
                                    "With thanks to:",
                                    "".join(("All my Twitter followers, and you for installing ",
                                             "this game, that's massively appreciated!")),
                                    "For more information please visit Pycraft's GitHub repository",
                                    " ",
                                    "Final Comments:",
                                    "".join(("Thank you greatly for supporting this project ",
                                             "simply by running it, I am sorry in advance ",
                                             "for any spelling mistakes. The programs will ",
                                             "be updated frequently and I shall do my best ",
                                             "to keep this up to date too. I also want to ",
                                             "add that you are welcome to view and change ",
                                             "the program and share it with your friends ",
                                             "however please may I have some credit, just ",
                                             "a name would do and if you find any bugs or ",
                                             "errors, please feel free to comment in the ",
                                             "comments section any feedback so I can ",
                                             "improve my program, it will all be much ",
                                             "appreciated and give as much detail as ",
                                             "you wish to give out.")),
                                    " ",
                                    " ",
                                    "Thank You!"]

                VisualYdisplacement = self.realHeight
                IntroYDisplacement = (self.realHeight-TitleHeight)/2
                timer = 5

                HoldOnExit = False
                HoldTimer = 0

                LoadText = False
                while True:
                    StartTime = self.mod_Time__.perf_counter()

                    self.mod_CaptionUtils__.GenerateCaptions.GetNormalCaption(
                        self,
                        "Credits")

                    self.mod_DisplayUtils__.DisplayFunctionality.CoreDisplayFunctionality(
                        self)

                    self.Display.fill(self.BackgroundCol)

                    Ypos = 0
                    for i in range(len(CreditsString)):
                        if LoadText:
                            if i > 0:
                                if CreditsString[i-1] == " ":
                                    TextSurface = LargeCreditsFont.render(
                                        CreditsString[i],
                                        self.aa,
                                        self.FontCol)
                                else:
                                    TextSurface = SmallCreditsFont.render(
                                        CreditsString[i],
                                        self.aa,
                                        self.FontCol)
                            else:
                                TextSurface = LargeCreditsFont.render(
                                    CreditsString[i],
                                    self.aa,
                                    self.FontCol)

                            TextSurfaceHeight = TextSurface.get_height()
                            TextSurfaceWidth = TextSurface.get_width()

                            if TextSurfaceWidth > self.realWidth:
                                Ypos += self.mod_TextUtils__.TextWrap.blit_text(
                                    self,
                                    CreditsString[i],
                                    (3, Ypos+VisualYdisplacement),
                                    SmallCreditsFont,
                                    self.AccentCol)
                            else:
                                if i+1 == len(CreditsString) and HoldOnExit:
                                    TextSurface_x_pos = (self.realWidth-TextSurfaceWidth)/2
                                    TextSurface_y_pos = (self.realHeight-TextSurfaceHeight)/2

                                    self.Display.blit(
                                        TextSurface,
                                        (TextSurface_x_pos, TextSurface_y_pos))
                                else:
                                    if (Ypos+VisualYdisplacement >= 0 and
                                        Ypos+VisualYdisplacement <= self.realHeight):

                                        TextSurface_x_pos = (self.realWidth-TextSurfaceWidth)/2
                                        TextSurface_y_pos = Ypos+VisualYdisplacement

                                        self.Display.blit(
                                            TextSurface,
                                            (TextSurface_x_pos, TextSurface_y_pos))

                            Ypos += TextSurfaceHeight

                    if timer >= 1:
                        self.Display.blit(
                            TitleFont,
                            ((self.realWidth-TitleWidth)/2, 0+IntroYDisplacement))

                        timer -= 1/(self.aFPS/self.Iteration)
                        VisualYdisplacement = self.realHeight
                    else:
                        if IntroYDisplacement <= 0:
                            cover_Rect = self.mod_Pygame__.Rect(
                                0,
                                0,
                                self.realWidth,
                                90)

                            self.mod_Pygame__.draw.rect(
                                self.Display,
                                self.BackgroundCol,
                                cover_Rect)

                            self.Display.blit(
                                TitleFont,
                                ((self.realWidth-TitleWidth)/2, 0))

                            self.Display.blit(
                                CreditsFont,
                                (((self.realWidth-TitleWidth)/2)+65, 50))

                            VisualYdisplacement -= 60/(self.aFPS/self.Iteration)
                            LoadText = True
                            if Ypos+VisualYdisplacement <= 360:
                                HoldOnExit = True
                                HoldTimer += 1/(self.aFPS/self.Iteration)
                                if HoldTimer >= 5:
                                    self.GoTo = "Home"
                        else:
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
                                ((self.realWidth-TitleWidth)/2, 0+IntroYDisplacement))

                            self.Display.blit(
                                CreditsFont,
                                (((self.realWidth-TitleWidth)/2)+65, 50+IntroYDisplacement))

                            IntroYDisplacement -= 90/(self.aFPS/self.Iteration)
                            VisualYdisplacement = self.realHeight

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

                    if self.ErrorMessage is not None:
                        self.ErrorMessage = "".join(("Credits > GenerateCredits ",
                                                     f"> Credits: {str(self.ErrorMessage)}"))
                        return

                    self.RunTimer += self.mod_Time__.perf_counter()-StartTime
            except Exception as Message:
                self.ErrorMessage = "Credits > GenerateCredits > Credits: "+str(Message)
                self.ErrorMessage_detailed = "".join(self.mod_Traceback__.format_exception(
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
