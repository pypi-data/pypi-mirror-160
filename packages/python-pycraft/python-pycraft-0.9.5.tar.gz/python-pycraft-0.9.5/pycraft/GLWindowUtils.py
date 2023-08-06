if __name__ != "__main__":
    print("Started <Pycraft_Base>")

    import moderngl_window as mglw

    class BenchmarkWindow(mglw.WindowConfig):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            self.camera = self.SharedData.mod_ModernGL_window_KeyboardCamera(
                self.wnd.keys,
                aspect_ratio=self.wnd.aspect_ratio)

            self.camera_enabled = True

        def key_event(self, key, action, modifiers):
            try:
                keys = self.wnd.keys


                if action == keys.ACTION_PRESS:
                    self.wnd.close()
                    self.wnd.destroy()
            except Exception as Message:
                try:
                    self.wnd.close()
                    self.SharedData.ErrorMessage = "".join(("GLWindowUtils > BenchmarkWindow ",
                                                            f"> key_event: {str(Message)}"))

                    self.SharedData.ErrorMessage_detailed = "".join(
                        self.SharedData.mod_Traceback__.format_exception(
                            None,
                            Message,
                            Message.__traceback__))

                    self.SharedData.mod_ErrorUtils__.GenerateErrorScreen.ErrorScreen(
                        self.SharedData)
                except Exception as Message:
                    self.SharedData.ErrorMessage = "".join(("GLWindowUtils > BenchmarkWindow ",
                                                            f"> key_event: {str(Message)}"))

                    self.SharedData.ErrorMessage_detailed = "".join(
                        self.SharedData.mod_Traceback__.format_exception(
                            None,
                            Message,
                            Message.__traceback__))

                    self.SharedData.mod_ErrorUtils__.GenerateErrorScreen.ErrorScreen(
                        self.SharedData)

        def close(self):
            try:
                self.SharedData.Command = "Undefined"
                self.iteration = 7500
            except Exception as Message:
                self.SharedData.ErrorMessage = "GLWindowUtils > BenchmarkWindow > close: " + \
                    str(Message)

                self.SharedData.ErrorMessage_detailed = "".join(
                    self.SharedData.mod_Traceback__.format_exception(
                        None,
                        Message,
                        Message.__traceback__))

                self.SharedData.mod_ErrorUtils__.GenerateErrorScreen.ErrorScreen(
                    self.SharedData)

    class CameraWindow(mglw.WindowConfig):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            self.camera = self.SharedData.mod_ModernGL_window_KeyboardCamera(
                self.wnd.keys,
                aspect_ratio=self.wnd.aspect_ratio)

            self.camera_enabled = True

        def key_event(self, key, action, modifiers):
            try:
                keys = self.wnd.keys

                if self.camera_enabled:
                    CurrentRunTime = self.SharedData.mod_Time__.perf_counter()

                    if key == keys.D:
                        if action == keys.ACTION_PRESS:
                            self.camera.key_input(
                                keys.D,
                                keys.ACTION_PRESS,
                                modifiers)

                            self.DkeydownTimer_start = CurrentRunTime
                            self.Dkeydown = True

                        elif action == keys.ACTION_RELEASE:
                            self.camera.key_input(
                                keys.D,
                                keys.ACTION_RELEASE,
                                modifiers)

                            self.Dkeydown = False

                    if key == keys.A:
                        if action == keys.ACTION_PRESS:
                            self.camera.key_input(
                                keys.A,
                                keys.ACTION_PRESS,
                                modifiers)

                            self.AkeydownTimer_start = CurrentRunTime
                            self.Akeydown = True

                        elif action == keys.ACTION_RELEASE:
                            self.camera.key_input(
                                keys.A,
                                keys.ACTION_RELEASE,
                                modifiers)

                            self.Akeydown = False

                    if key == keys.W:
                        if action == keys.ACTION_PRESS:
                            self.camera.key_input(
                                keys.W,
                                keys.ACTION_PRESS,
                                modifiers)

                            self.RunForwardTimer = True
                            self.Wkeydown = True

                            self.RunForwardTimer_start = CurrentRunTime
                            self.RunForwardTimer_start_sound = CurrentRunTime

                        elif action == keys.ACTION_RELEASE:
                            self.camera.key_input(
                                keys.W,
                                keys.ACTION_RELEASE,
                                modifiers)

                            self.RunForwardTimer = False
                            self.Wkeydown = False

                    if key == keys.S:
                        if action == keys.ACTION_PRESS:
                            self.camera.key_input(
                                keys.S,
                                keys.ACTION_PRESS,
                                modifiers)

                            self.Skeydown = True
                            self.SkeydownTimer_start = CurrentRunTime

                        elif action == keys.ACTION_RELEASE:
                            self.camera.key_input(
                                keys.S,
                                keys.ACTION_RELEASE,
                                modifiers)

                            self.Skeydown = False

                if action == keys.ACTION_PRESS:
                    if key == keys.L:
                        self.camera_enabled = not self.camera_enabled
                        self.wnd.mouse_exclusivity = self.camera_enabled
                        self.wnd.cursor = not self.camera_enabled

                    elif key == keys.SPACE and self.Jump is False:
                        self.Jump = True
                        self.JumpUP = True
                        self.StartYposition = self.camera.position.y
                        self.Jump_Start_FPS = self.SharedData.eFPS

                    elif key == keys.K and self.SharedData.Devmode == 10:
                        self.time += 30
                        self.GameTime += 30
                        self.WeatherTime += 30

                    elif key == keys.I and self.SharedData.Devmode == 10:
                        self.IKeyPressed = True

                    elif key == keys.Q and self.SharedData.Devmode == 10:
                        self.SharedData.mod_TkinterUtils__.TkinterInfo.CreateTkinterWindow(
                            self.SharedData)

                    elif key == keys.E:
                        self.Inventory = True

                    elif key == keys.R:
                        self.Map = True

                elif action == keys.ACTION_RELEASE:
                    self.IKeyPressed = False
            except Exception as Message:
                try:
                    self.wnd.close()
                    self.SharedData.ErrorMessage = "".join(("GLWindowUtils > CameraWindow ",
                                                            f"> key_event: {str(Message)}"))

                    self.SharedData.ErrorMessage_detailed = "".join(
                        self.SharedData.mod_Traceback__.format_exception(
                            None,
                            Message,
                            Message.__traceback__))

                    self.SharedData.mod_ErrorUtils__.GenerateErrorScreen.ErrorScreen(
                        self.SharedData)
                except Exception as Message:
                    self.SharedData.ErrorMessage = "".join(("GLWindowUtils > CameraWindow ",
                                                            f"> key_event: {str(Message)}"))

                    self.SharedData.ErrorMessage_detailed = "".join(
                        self.SharedData.mod_Traceback__.format_exception(
                            None,
                            Message,
                            Message.__traceback__))

                    self.SharedData.mod_ErrorUtils__.GenerateErrorScreen.ErrorScreen(
                        self.SharedData)


        def mouse_position_event(self, x: int, y: int, dx, dy):
            try:
                if self.camera_enabled:
                    self.camera.rot_state(
                        -dx,
                        -dy)
            except Exception as Message:
                self.SharedData.ErrorMessage = "".join(("GLWindowUtils > CameraWindow > ",
                                                        f"mouse_position_event: {str(Message)}"))

                self.SharedData.ErrorMessage_detailed = "".join(
                    self.SharedData.mod_Traceback__.format_exception(
                        None,
                        Message,
                        Message.__traceback__))

                self.SharedData.mod_ErrorUtils__.GenerateErrorScreen.ErrorScreen(self.SharedData)

        def mouse_scroll_event(self, x_offset: float, y_offset: float):
            self.time += y_offset*2
            self.GameTime += y_offset*2
            #if self.weather != "rain.heavy.thundery":
            self.WeatherTime += y_offset*2
            #if self.weather == "rain.heavy.thundery":
            #self.ThunderTimer += y_offset*2

        def resize(self, width: int, height: int):
            try:
                self.SharedData.Fullscreen = not self.wnd.fullscreen
                self.SharedData.realWidth, self.SharedData.realHeight = self.window_size
                self.camera.projection.update(aspect_ratio=self.wnd.aspect_ratio)
            except Exception as Message:
                self.SharedData.ErrorMessage = "".join(("GLWindowUtils > CameraWindow > ",
                                                        f"resize: {str(Message)}"))

                self.SharedData.ErrorMessage_detailed = "".join(
                    self.SharedData.mod_Traceback__.format_exception(
                        None,
                        Message,
                        Message.__traceback__))

                self.SharedData.mod_ErrorUtils__.GenerateErrorScreen.ErrorScreen(self.SharedData)

        def close(self):
            try:
                self.SharedData.Command = "Undefined"
                self.Running = False
            except Exception as Message:
                self.SharedData.ErrorMessage = "GLWindowUtils > CameraWindow > close: "+str(Message)

                self.SharedData.ErrorMessage_detailed = "".join(
                    self.SharedData.mod_Traceback__.format_exception(
                        None,
                        Message,
                        Message.__traceback__))

                self.SharedData.mod_ErrorUtils__.GenerateErrorScreen.ErrorScreen(self.SharedData)

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
