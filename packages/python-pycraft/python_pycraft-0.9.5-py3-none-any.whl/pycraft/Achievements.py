if __name__ != "__main__":
    print("Started <Pycraft_Achievements>")

    class GenerateAchievements:
        def __init__(self):
            pass

        def Achievements(self):
            try:
                self.mod_CaptionUtils__.GenerateCaptions.GetNormalCaption(
                    self,
                    "Achievements")

                if self.platform == "Linux":
                    InfoTitleFont = self.mod_Pygame__.font.Font(
                        self.mod_OS__.path.join(
                            self.base_folder, ("Fonts//Book Antiqua.ttf")), 35)

                    DataFont = self.mod_Pygame__.font.Font(
                        self.mod_OS__.path.join(
                            self.base_folder, ("Fonts//Book Antiqua.ttf")), 15)
                else:
                    InfoTitleFont = self.mod_Pygame__.font.Font(
                        self.mod_OS__.path.join(
                            self.base_folder, ("Fonts\\Book Antiqua.ttf")), 35)

                    DataFont = self.mod_Pygame__.font.Font(
                        self.mod_OS__.path.join(
                            self.base_folder, ("Fonts\\Book Antiqua.ttf")), 15)

                TitleFont = self.TitleFont.render(
                    "Pycraft",
                    self.aa,
                    self.FontCol)

                TitleWidth = TitleFont.get_width()

                AchievementsFont = InfoTitleFont.render(
                    "Achievements",
                    self.aa,
                    self.SecondFontCol)

                while True:
                    StartTime = self.mod_Time__.perf_counter()

                    DisplayEvents = self.mod_DisplayUtils__.DisplayFunctionality.CoreDisplayFunctionality(
                        self)

                    self.mod_CaptionUtils__.GenerateCaptions.GetNormalCaption(
                        self,
                        "Achievements")

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
                        AchievementsFont,
                        (((self.realWidth-TitleWidth)/2)+55, 50))

                    self.mod_DrawingUtils__.GenerateGraph.CreateDevmodeGraph(
                        self,
                        DataFont)

                    if self.GoTo is None:
                        self.mod_DisplayUtils__.DisplayAnimations.FadeIn(self)
                    else:
                        self.mod_DisplayUtils__.DisplayAnimations.FadeOut(self)

                    if not self.StartAnimation and (self.GoTo is not None):
                        return None

                    self.mod_Pygame__.display.flip()
                    self.clock.tick(
                        self.mod_DisplayUtils__.DisplayUtils.GetPlayStatus(self))

                    if self.ErrorMessage is not None:
                        self.ErrorMessage = "".join(
                            ("Achievements > GenerateAchievements > Achievements: ",
                             str(self.ErrorMessage)))

                        return

                    self.RunTimer += self.mod_Time__.perf_counter()-StartTime
            except Exception as Message:
                self.ErrorMessage = (
                    f"Achievements > GenerateAchievements > Achievements: {str(Message)}")

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
