if __name__ != "__main__":
    print("Started <Pycraft_SoundUtils>")

    class PlaySound:
        def __init__(self):
            pass

        def PlayInvSound(self):
            try:
                if self.platform == "Linux":
                    self.mod_Pygame__.mixer.music.load(
                        self.mod_OS__.path.join(
                            self.base_folder,
                            ("Resources//General_Resources//InventoryGeneral.ogg")))

                else:
                    self.mod_Pygame__.mixer.music.load(
                        self.mod_OS__.path.join(
                            self.base_folder,
                            ("Resources\\General_Resources\\InventoryGeneral.ogg")))

                self.mod_Pygame__.mixer.music.set_volume(self.musicVOL/100)
                self.mod_Pygame__.mixer.music.play(-1)
            except Exception as Message:
                if not self.Stop_Thread_Event.is_set():
                    self.ErrorMessage = "SoundUtils > PlaySound > PlayInvSound: "+str(Message)

                    self.ErrorMessage_detailed = "".join(
                        self.mod_Traceback__.format_exception(
                            None,
                            Message,
                            Message.__traceback__))

                    self.mod_ErrorUtils__.GenerateErrorScreen.ErrorScreen(self)

        def PlayClickSound(self):
            try:
                channel0 = self.mod_Pygame__.mixer.Channel(0)
                if self.platform == "Linux":
                    clickMUSIC = self.mod_Pygame__.mixer.Sound(
                        self.mod_OS__.path.join(
                            self.base_folder,
                            ("Resources//General_Resources//Click.ogg")))

                else:
                    clickMUSIC = self.mod_Pygame__.mixer.Sound(
                        self.mod_OS__.path.join(
                            self.base_folder,
                            ("Resources\\General_Resources\\Click.ogg")))

                channel0.set_volume(self.soundVOL/100)
                channel0.play(clickMUSIC)
                self.mod_Pygame__.time.wait(40)
            except Exception as Message:
                if not self.Stop_Thread_Event.is_set():
                    self.ErrorMessage = "SoundUtils > PlaySound > PlayClickSound: "+str(Message)

                    self.ErrorMessage_detailed = "".join(
                        self.mod_Traceback__.format_exception(
                            None,
                            Message,
                            Message.__traceback__))

                    self.mod_ErrorUtils__.GenerateErrorScreen.ErrorScreen(self)

        def PlayFootstepsSound(self):
            try:
                channel1 = self.mod_Pygame__.mixer.Channel(1)
                RandomNum = self.mod_Random__.randint(0, 5)

                if self.platform == "Linux":
                    Footsteps = self.mod_Pygame__.mixer.Sound(
                        self.mod_OS__.path.join(
                            self.base_folder,
                            (f"Resources//G3_Resources//GameSounds//footstep//footsteps{RandomNum}.wav")))

                else:
                    Footsteps = self.mod_Pygame__.mixer.Sound(
                        self.mod_OS__.path.join(
                            self.base_folder,
                            (f"Resources\\G3_Resources\\GameSounds\\footstep\\footsteps{RandomNum}.wav")))

                channel1.set_volume(self.soundVOL/100)
                channel1.play(Footsteps)
            except Exception as Message:
                if not self.Stop_Thread_Event.is_set():
                    self.ErrorMessage = "SoundUtils > PlaySound > PlayFootstepsSound: "+str(Message)

                    self.ErrorMessage_detailed = "".join(
                        self.mod_Traceback__.format_exception(
                            None,
                            Message,
                            Message.__traceback__))

                    self.mod_ErrorUtils__.GenerateErrorScreen.ErrorScreen(self)

        def PlayAmbientSound(self):
            try:
                channel2 = self.mod_Pygame__.mixer.Channel(2)
                if self.platform == "Linux":
                    LoadAmb = self.mod_Pygame__.mixer.Sound(
                        self.mod_OS__.path.join(
                            self.base_folder,
                            ("Resources//G3_Resources//GameSounds//FieldAmb.ogg")))

                else:
                    LoadAmb = self.mod_Pygame__.mixer.Sound(
                        self.mod_OS__.path.join(
                            self.base_folder,
                            ("Resources\\G3_Resources\\GameSounds\\FieldAmb.ogg")))

                channel2.set_volume(self.soundVOL/100)
                channel2.play(LoadAmb)
            except Exception as Message:
                if not self.Stop_Thread_Event.is_set():
                    self.ErrorMessage = "SoundUtils > PlaySound > PlayAmbientSound: "+str(Message)

                    self.ErrorMessage_detailed = "".join(
                        self.mod_Traceback__.format_exception(
                            None,
                            Message,
                            Message.__traceback__))

                    self.mod_ErrorUtils__.GenerateErrorScreen.ErrorScreen(self)

        def PlayThunderSound(self):
            try:
                channel3 = self.mod_Pygame__.mixer.Channel(3)
                RandomNum = self.mod_Random__.randint(0, 10)

                if self.platform == "Linux":
                    Thunder = self.mod_Pygame__.mixer.Sound(
                        self.mod_OS__.path.join(
                            self.base_folder,
                            (f"Resources//G3_Resources//GameSounds//thunder//thunder{RandomNum}.ogg")))

                else:
                    Thunder = self.mod_Pygame__.mixer.Sound(
                        self.mod_OS__.path.join(
                            self.base_folder,
                            (f"Resources\\G3_Resources\\GameSounds\\thunder\\thunder{RandomNum}.ogg")))

                channel3.set_volume(self.soundVOL/100)
                channel3.play(Thunder)
            except Exception as Message:
                if not self.Stop_Thread_Event.is_set():
                    self.ErrorMessage = "SoundUtils > PlaySound > PlayThunderSound: " + \
                        str(Message)

                    self.ErrorMessage_detailed = "".join(
                        self.mod_Traceback__.format_exception(
                            None,
                            Message,
                            Message.__traceback__))

                    self.mod_ErrorUtils__.GenerateErrorScreen.ErrorScreen(self)

        def PlayRainSound(self):
            try:
                channel4 = self.mod_Pygame__.mixer.Channel(4)

                if self.platform == "Linux":
                    Rain = self.mod_Pygame__.mixer.Sound(
                        self.mod_OS__.path.join(
                            self.base_folder,
                            ("Resources//G3_Resources//GameSounds//rain.ogg")))

                else:
                    Rain = self.mod_Pygame__.mixer.Sound(
                        self.mod_OS__.path.join(
                            self.base_folder,
                            ("Resources\\G3_Resources\\GameSounds\\rain.ogg")))

                channel4.set_volume(self.soundVOL/100)
                channel4.play(Rain)
            except Exception as Message:
                if not self.Stop_Thread_Event.is_set():
                    self.ErrorMessage = "SoundUtils > PlaySound > PlayRainSound: " + \
                        str(Message)

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
