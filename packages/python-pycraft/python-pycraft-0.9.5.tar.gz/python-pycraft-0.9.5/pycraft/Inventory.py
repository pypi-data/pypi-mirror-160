if __name__ != "__main__":
    print("Started <Pycraft_Inventory>")

    class GenerateInventory:
        def __init__(self):
            pass

        def Inventory(self):
            try:
                self.mod_DisplayUtils__.DisplayUtils.SetDisplay(self)
                self.Display.fill(self.BackgroundCol)
                self.mod_Pygame__.display.update()

                if self.platform == "Linux":
                    self.TitleFont = self.mod_Pygame__.font.Font(
                        self.mod_OS__.path.join(
                            self.base_folder,
                            ("Fonts//Book Antiqua.ttf")), 60)

                else:
                    self.TitleFont = self.mod_Pygame__.font.Font(
                        self.mod_OS__.path.join(
                            self.base_folder,
                            ("Fonts\\Book Antiqua.ttf")), 60)

                PycraftTitle = self.TitleFont.render(
                    "Pycraft",
                    self.aa,
                    self.FontCol).convert_alpha()
                TitleWidth = PycraftTitle.get_width()

                self.realWidth = self.mod_Pygame__.display.get_window_size()[0]
                self.realHeight = self.mod_Pygame__.display.get_window_size()[1]

                AlphaSurface = self.mod_Pygame__.Surface(
                    (self.realWidth, self.realHeight),
                    self.mod_Pygame__.HWSURFACE|
                    self.mod_Pygame__.SRCALPHA).convert_alpha()
                AlphaSurface.set_alpha(204)
                AlphaSurface.fill(self.BackgroundCol)

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
                hover8 = False

                if self.platform == "Linux":
                    ButtonFont1 = self.mod_Pygame__.font.Font(
                        self.mod_OS__.path.join(
                            self.base_folder,
                            ("Fonts//Book Antiqua.ttf")), 30)

                    ButtonFont2 = self.mod_Pygame__.font.Font(
                        self.mod_OS__.path.join(
                            self.base_folder,
                            ("Fonts//Book Antiqua.ttf")), 30)

                    ButtonFont3 = self.mod_Pygame__.font.Font(
                        self.mod_OS__.path.join(
                            self.base_folder,
                            ("Fonts//Book Antiqua.ttf")), 30)

                    ButtonFont4 = self.mod_Pygame__.font.Font(
                        self.mod_OS__.path.join(
                            self.base_folder,
                            ("Fonts//Book Antiqua.ttf")), 30)

                    ButtonFont5 = self.mod_Pygame__.font.Font(
                        self.mod_OS__.path.join(
                            self.base_folder,
                            ("Fonts//Book Antiqua.ttf")), 30)

                    ButtonFont6 = self.mod_Pygame__.font.Font(
                        self.mod_OS__.path.join(
                            self.base_folder,
                            ("Fonts//Book Antiqua.ttf")), 30)

                    ButtonFont7 = self.mod_Pygame__.font.Font(
                        self.mod_OS__.path.join(
                            self.base_folder,
                            ("Fonts//Book Antiqua.ttf")), 30)

                    ButtonFont8 = self.mod_Pygame__.font.Font(
                        self.mod_OS__.path.join(
                            self.base_folder,
                            ("Fonts//Book Antiqua.ttf")), 30)

                else:
                    ButtonFont1 = self.mod_Pygame__.font.Font(
                        self.mod_OS__.path.join(
                            self.base_folder,
                            ("Fonts\\Book Antiqua.ttf")), 30)

                    ButtonFont2 = self.mod_Pygame__.font.Font(
                        self.mod_OS__.path.join(
                            self.base_folder,
                            ("Fonts\\Book Antiqua.ttf")), 30)

                    ButtonFont3 = self.mod_Pygame__.font.Font(
                        self.mod_OS__.path.join(
                            self.base_folder,
                            ("Fonts\\Book Antiqua.ttf")), 30)

                    ButtonFont4 = self.mod_Pygame__.font.Font(
                        self.mod_OS__.path.join(
                            self.base_folder,
                            ("Fonts\\Book Antiqua.ttf")), 30)

                    ButtonFont5 = self.mod_Pygame__.font.Font(
                        self.mod_OS__.path.join(
                            self.base_folder,
                            ("Fonts\\Book Antiqua.ttf")), 30)

                    ButtonFont6 = self.mod_Pygame__.font.Font(
                        self.mod_OS__.path.join(
                            self.base_folder,
                            ("Fonts\\Book Antiqua.ttf")), 30)

                    ButtonFont7 = self.mod_Pygame__.font.Font(
                        self.mod_OS__.path.join(
                            self.base_folder,
                            ("Fonts\\Book Antiqua.ttf")), 30)

                    ButtonFont8 = self.mod_Pygame__.font.Font(
                        self.mod_OS__.path.join(
                            self.base_folder,
                            ("Fonts\\Book Antiqua.ttf")), 30)

                WeaponsText = ButtonFont1.render(
                    "Weapons",
                    self.aa,
                    self.FontCol).convert_alpha()
                WeaponsTextWidth = WeaponsText.get_width()

                RangedWeaponsText = ButtonFont2.render(
                    "Ranged Weapons",
                    self.aa,
                    self.FontCol).convert_alpha()
                RangedWeaponsTextWidth = RangedWeaponsText.get_width()

                ShieldsText = ButtonFont3.render(
                    "Shields",
                    self.aa,
                    self.FontCol).convert_alpha()
                ShieldsTextWidth = ShieldsText.get_width()

                ArmourText = ButtonFont4.render(
                    "Armour",
                    self.aa,
                    self.FontCol).convert_alpha()
                ArmourTextWidth = ArmourText.get_width()

                FoodText = ButtonFont5.render(
                    "Food",
                    self.aa,
                    self.FontCol).convert_alpha()
                FoodTextWidth = FoodText.get_width()

                ItemsText = ButtonFont6.render(
                    "Items",
                    self.aa,
                    self.FontCol).convert_alpha()
                ItemsTextWidth = ItemsText.get_width()

                SpecialItemsText = ButtonFont7.render(
                    "Special Items",
                    self.aa,
                    self.FontCol).convert_alpha()
                SpecialItemsTextWidth = SpecialItemsText.get_width()

                OptionsText = ButtonFont7.render(
                    "Options",
                    self.aa,
                    self.FontCol).convert_alpha()
                OptionsTextWidth = OptionsText.get_width()

                FullscreenX, FullscreenY = self.mod_Pyautogui__.size()

                self.Mx = self.realWidth/2
                self.My = self.realHeight/2

                if self.aa:
                    if self.platform == "Linux":
                        pilImage = self.mod_PIL_Image_.open(
                            self.mod_OS__.path.join(
                                self.base_folder,
                                ("Resources//General_Resources//PauseIMG.png"))).resize(
                                    (self.realWidth,
                                     self.realHeight),
                                    self.mod_PIL_Image_.ANTIALIAS)
                    else:
                        pilImage = self.mod_PIL_Image_.open(
                            self.mod_OS__.path.join(
                                self.base_folder,
                                ("Resources\\General_Resources\\PauseIMG.png"))).resize(
                                    (self.realWidth,
                                     self.realHeight),
                                    self.mod_PIL_Image_.ANTIALIAS)

                else:
                    if self.platform == "Linux":
                        pilImage = self.mod_PIL_Image_.open(
                            self.mod_OS__.path.join(
                                self.base_folder,
                                ("Resources//General_Resources//PauseIMG.png"))).resize(
                                    (self.realWidth,
                                     self.realHeight))

                    else:
                        pilImage = self.mod_PIL_Image_.open(
                            self.mod_OS__.path.join(
                                self.base_folder,
                                ("Resources\\General_Resources\\PauseIMG.png"))).resize(
                                    (self.realWidth,
                                     self.realHeight))

                BLURRED_pilImage = pilImage.filter(self.mod_PIL_ImageFilter_.BoxBlur(4))

                PauseImg = self.mod_ImageUtils__.ConvertImage.pilImageToSurface(
                    self,
                    BLURRED_pilImage)

                self.Display.blit(
                    PauseImg,
                    (0, 0))

                self.Display.blit(
                    AlphaSurface,
                    (0, 0))

                MenuSelector = 0

                while True:
                    self.mod_CaptionUtils__.GenerateCaptions.GetNormalCaption(
                        self,
                        "Inventory")

                    yScaleFact = self.realHeight/720

                    self.Display.fill(self.BackgroundCol)

                    self.Display.blit(
                        PauseImg,
                        (0, 0))

                    self.Display.blit(
                        AlphaSurface,
                        (0, 0))

                    self.Display.blit(
                        PycraftTitle,
                        ((self.realWidth-TitleWidth)/2, 0))

                    self.mod_DisplayUtils__.DisplayFunctionality.CoreDisplayFunctionality(
                        self, checkEvents=False)

                    for event in self.mod_Pygame__.event.get():
                        if (event.type == self.mod_Pygame__.QUIT or
                                (event.type == self.mod_Pygame__.KEYDOWN and
                                    event.key == self.mod_Pygame__.K_ESCAPE) or
                                (event.type == self.mod_Pygame__.KEYDOWN and
                                    event.key == self.mod_Pygame__.K_e)):

                            self.Load3D = False
                            self.JoystickExit = False

                            if self.sound:
                                self.mod_SoundUtils__.PlaySound.PlayClickSound(self)

                            self.mod_Pygame__.display.quit()
                            return

                        if event.type == self.mod_Pygame__.WINDOWSIZECHANGED:
                            self.realWidth = self.mod_Pygame__.display.get_window_size()[0]
                            self.realHeight = self.mod_Pygame__.display.get_window_size()[1]

                            AlphaSurface = self.mod_Pygame__.Surface(
                                (self.realWidth, self.realHeight),
                                self.mod_Pygame__.HWSURFACE|
                                self.mod_Pygame__.SRCALPHA).convert_alpha()
                            AlphaSurface.set_alpha(204)
                            AlphaSurface.fill(self.BackgroundCol)

                            if self.platform == "Linux":
                                if self.aa:
                                    pilImage = self.mod_PIL_Image_.open(
                                        self.mod_OS__.path.join(
                                            self.base_folder,
                                            ("Resources//General_Resources//PauseIMG.png"))).resize(
                                                (self.realWidth,
                                                 self.realHeight),
                                                self.mod_PIL_Image_.ANTIALIAS)

                                else:
                                    pilImage = self.mod_PIL_Image_.open(
                                        self.mod_OS__.path.join(
                                            self.base_folder,
                                            ("Resources//General_Resources//PauseIMG.png"))).resize(
                                                (self.realWidth,
                                                 self.realHeight))

                            else:
                                if self.aa:
                                    pilImage = self.mod_PIL_Image_.open(
                                        self.mod_OS__.path.join(
                                            self.base_folder,
                                            ("Resources\\General_Resources\\PauseIMG.png"))).resize(
                                                (self.realWidth,
                                                 self.realHeight),
                                                self.mod_PIL_Image_.ANTIALIAS)

                                else:
                                    pilImage = self.mod_PIL_Image_.open(
                                        self.mod_OS__.path.join(
                                            self.base_folder,
                                            ("Resources\\General_Resources\\PauseIMG.png"))).resize(
                                                (self.realWidth,
                                                 self.realHeight))

                            BLURRED_pilImage = pilImage.filter(self.mod_PIL_ImageFilter_.BoxBlur(4))

                            PauseImg = self.mod_ImageUtils__.ConvertImage.pilImageToSurface(
                                self,
                                BLURRED_pilImage)

                        if (event.type == self.mod_Pygame__.MOUSEBUTTONDOWN or
                                self.mod_Pygame__.mouse.get_pressed()[0]):
                            self.mousebuttondown = True

                        else:
                            self.mousebuttondown = False

                        if event.type == self.mod_Pygame__.KEYDOWN:
                            if event.key == self.mod_Pygame__.K_F11:
                                self.mod_DisplayUtils__.DisplayUtils.UpdateDisplay(self)

                                AlphaSurface = self.mod_Pygame__.Surface(
                                    (FullscreenX,
                                     FullscreenY),
                                    self.mod_Pygame__.HWSURFACE|
                                    self.mod_Pygame__.SRCALPHA).convert_alpha()
                                AlphaSurface.set_alpha(204)
                                AlphaSurface.fill(self.BackgroundCol)

                    if self.UseMouseInput is False:
                        if self.JoystickHatPressed:
                            self.JoystickHatPressed = False
                            if self.JoystickMouse[1] == "Down" and MenuSelector <= 7:
                                MenuSelector += 1
                                if MenuSelector == 8:
                                    MenuSelector = 0
                            if self.JoystickMouse[1] == "Up" and MenuSelector >= 0:
                                MenuSelector -= 1
                                if MenuSelector == -1:
                                    MenuSelector = 7

                        if self.JoystickExit:
                            self.JoystickExit = False
                            self.Load3D = False

                            if self.sound:
                                self.mod_SoundUtils__.PlaySound.PlayClickSound(self)
                            return

                        if self.JoystickConfirm:
                            self.mousebuttondown = True
                            self.JoystickConfirm = False

                    if ((self.My >= 202*yScaleFact and
                                self.My <= 247*yScaleFact and
                                self.Mx >= 1155) or
                            (MenuSelector == 0 and
                                self.UseMouseInput is False)):

                        hover1 = True
                        if self.mousebuttondown:
                            PauseImg = self.mod_ImageUtils__.ConvertImage.pilImageToSurface(
                                self,
                                BLURRED_pilImage)

                            if self.sound:
                                self.mod_SoundUtils__.PlaySound.PlayClickSound(self)

                            self.mousebuttondown = False
                    else:
                        hover1 = False

                    if ((self.My >= 252*yScaleFact and
                                self.My <= 297*yScaleFact and
                                self.Mx >= 1105) or
                            (MenuSelector == 1 and
                                self.UseMouseInput is False)):

                        hover2 = True
                        if self.mousebuttondown:
                            PauseImg = self.mod_ImageUtils__.ConvertImage.pilImageToSurface(
                                self,
                                BLURRED_pilImage)

                            if self.sound:
                                self.mod_SoundUtils__.PlaySound.PlayClickSound(self)
                            self.mousebuttondown = False
                    else:
                        hover2 = False

                    if ((self.My >= 302*yScaleFact and
                                self.My <= 347*yScaleFact and
                                self.Mx >= 865) or
                            (MenuSelector == 2 and
                                self.UseMouseInput is False)):

                        hover3 = True
                        if self.mousebuttondown:
                            PauseImg = self.mod_ImageUtils__.ConvertImage.pilImageToSurface(
                                self,
                                BLURRED_pilImage)

                            if self.sound:
                                self.mod_SoundUtils__.PlaySound.PlayClickSound(self)
                            self.mousebuttondown = False
                    else:
                        hover3 = False

                    if ((self.My >= 402*yScaleFact and
                                self.My <= 447*yScaleFact and
                                self.Mx >= 1035) or
                            (MenuSelector == 4 and
                                self.UseMouseInput is False)):

                        hover4 = True
                        if self.mousebuttondown:
                            PauseImg = self.mod_ImageUtils__.ConvertImage.pilImageToSurface(
                                self,
                                BLURRED_pilImage)

                            if self.sound:
                                self.mod_SoundUtils__.PlaySound.PlayClickSound(self)
                            self.mousebuttondown = False
                    else:
                        hover4 = False

                    if ((self.My >= 352*yScaleFact and
                                self.My <= 397*yScaleFact and
                                self.Mx >= 880) or
                            (MenuSelector == 3 and
                                self.UseMouseInput is False)):

                        hover5 = True
                        if self.mousebuttondown:
                            PauseImg = self.mod_ImageUtils__.ConvertImage.pilImageToSurface(
                                self,
                                BLURRED_pilImage)

                            if self.sound:
                                self.mod_SoundUtils__.PlaySound.PlayClickSound(self)
                            self.mousebuttondown = False
                    else:
                        hover5 = False

                    if ((self.My >= 502*yScaleFact and
                                self.My <= 547*yScaleFact and
                                self.Mx >= 1095) or
                            (MenuSelector == 6 and
                                self.UseMouseInput is False)):

                        hover6 = True
                        if self.mousebuttondown:
                            PauseImg = self.mod_ImageUtils__.ConvertImage.pilImageToSurface(
                                self,
                                BLURRED_pilImage)

                            if self.sound:
                                self.mod_SoundUtils__.PlaySound.PlayClickSound(self)
                            self.mousebuttondown = False
                    else:
                        hover6 = False

                    if ((self.My >= 452*yScaleFact and
                                self.My <= 497*yScaleFact and
                                self.Mx >= 1095) or
                            (MenuSelector == 5 and
                                self.UseMouseInput is False)):

                        hover7 = True
                        if self.mousebuttondown:
                            PauseImg = self.mod_ImageUtils__.ConvertImage.pilImageToSurface(
                                self,
                                BLURRED_pilImage)

                            if self.sound:
                                self.mod_SoundUtils__.PlaySound.PlayClickSound(self)
                            self.mousebuttondown = False
                    else:
                        hover7 = False

                    if ((self.My >= 552*yScaleFact and
                                self.My <= 597*yScaleFact and self.Mx >= 1095) or
                            (MenuSelector == 7 and
                                self.UseMouseInput is False)):

                        hover8 = True
                        if self.mousebuttondown:
                            PauseImg = self.mod_ImageUtils__.ConvertImage.pilImageToSurface(
                                self,
                                BLURRED_pilImage)

                            if self.sound:
                                self.mod_SoundUtils__.PlaySound.PlayClickSound(self)
                            self.mousebuttondown = False
                    else:
                        hover8 = False

                    ButtonFont1.set_underline(hover1)
                    ButtonFont2.set_underline(hover2)
                    ButtonFont3.set_underline(hover3)
                    ButtonFont4.set_underline(hover4)
                    ButtonFont5.set_underline(hover5)
                    ButtonFont6.set_underline(hover6)
                    ButtonFont7.set_underline(hover7)
                    ButtonFont8.set_underline(hover8)
                    AlphaSurface.fill(self.BackgroundCol)

                    self.Display.blit(
                        WeaponsText,
                        ((self.realWidth-WeaponsTextWidth)-2,
                         200*yScaleFact))
                    if hover1:
                        AlphaSurface.blit(
                            Selector,
                            (self.realWidth-(WeaponsTextWidth+SelectorWidth)-2,
                             200*yScaleFact))

                    self.Display.blit(
                        RangedWeaponsText,
                        ((self.realWidth-RangedWeaponsTextWidth)-2,
                         250*yScaleFact))
                    if hover2:
                        AlphaSurface.blit(
                            Selector,
                            (self.realWidth-(RangedWeaponsTextWidth+SelectorWidth)-2,
                             250*yScaleFact))

                    self.Display.blit(
                        ShieldsText,
                        ((self.realWidth-ShieldsTextWidth)-2,
                         300*yScaleFact))
                    if hover3:
                        AlphaSurface.blit(
                            Selector,
                            (self.realWidth-(ShieldsTextWidth+SelectorWidth)-2,
                             300*yScaleFact))

                    self.Display.blit(
                        ArmourText,
                        ((self.realWidth-ArmourTextWidth)-2,
                         350*yScaleFact))
                    if hover4:
                        AlphaSurface.blit(
                            Selector,
                            (self.realWidth-(FoodTextWidth+SelectorWidth)-2,
                             400*yScaleFact))

                    self.Display.blit(
                        FoodText,
                        ((self.realWidth-FoodTextWidth)-2,
                         400*yScaleFact))
                    if hover5:
                        AlphaSurface.blit(
                            Selector,
                            (self.realWidth-(ArmourTextWidth+SelectorWidth)-2,
                             350*yScaleFact))

                    self.Display.blit(
                        ItemsText,
                        ((self.realWidth-ItemsTextWidth)-2,
                         450*yScaleFact))
                    if hover6:
                        AlphaSurface.blit(
                            Selector,
                            (self.realWidth-(SpecialItemsTextWidth+SelectorWidth)-2,
                             500*yScaleFact))

                    self.Display.blit(
                        SpecialItemsText,
                        ((self.realWidth-SpecialItemsTextWidth)-2,
                         500*yScaleFact))
                    if hover7:
                        AlphaSurface.blit(
                            Selector,
                            (self.realWidth-(ItemsTextWidth+SelectorWidth)-2,
                             450*yScaleFact))

                    self.Display.blit(
                        OptionsText,
                        ((self.realWidth-OptionsTextWidth)-2,
                         550*yScaleFact))
                    if hover8:
                        AlphaSurface.blit(
                            Selector,
                            (self.realWidth-(OptionsTextWidth+SelectorWidth)-2,
                             550*yScaleFact))

                    self.mod_Pygame__.display.flip()
                    self.clock.tick(
                        self.mod_DisplayUtils__.DisplayUtils.GetPlayStatus(self))

                    if self.ErrorMessage is not None:
                        self.ErrorMessage = "".join(("Inventory > GenerateInventory ",
                                                     f"> Inventory: {str(self.ErrorMessage)}"))
                        return
            except Exception as Message:
                self.ErrorMessage = "Inventory > GenerateInventory > Inventory: "+str(Message)

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
