if __name__ != "__main__":
    print("Started <Pycraft_JoystickUtils>")

    class EstablishJoystickRemoved:
        def __init__(self):
            pass

        def JoystickRemoved(self):
            while True:
                try:
                    if self.mod_Pygame__.init():
                        if (self.mod_Pygame__.joystick.get_count() == 0 and
                                self.Pygame_DeviceRemoved_Update is False and
                                self.JoystickConnected):

                            self.Pygame_DeviceRemoved_Update = True
                            self.DeviceConnected = False
                            self.DeviceConnected_Update = True
                            self.Pygame_DeviceAdded_Update = False

                        elif (self.mod_Pygame__.joystick.get_count() >= 1 and
                                self.Pygame_DeviceAdded_Update is False):

                            self.DeviceConnected = True
                            self.DeviceConnected_Update = True
                            self.DeviceRemoved_Update = True
                            self.Pygame_DeviceAdded_Update = True
                            self.Pygame_DeviceRemoved_Update = False
                            self.JoystickConnected = True
                except:
                    pass
                finally:
                    self.mod_Time__.sleep(1)

            print("'Thread_JoystickRemoved' has stopped")


    class EstablishJoystickConnection:
        def __init__(self):
            pass

        def JoystickEvents(self):
            def print_add(joy):
                pass

            def print_remove(joy):
                pass

            def key_received(key):
                import os
                if ("site-packages" in os.path.dirname(__file__) or
                        "dist-packages" in os.path.dirname(__file__)):
                    try:
                        from pycraft.ShareDataUtils import Game_SharedData
                    except:
                        from ShareDataUtils import Game_SharedData
                else:
                    from ShareDataUtils import Game_SharedData

                try:
                    if self.UseMouseInput is False:
                        if self.Command == "Play":
                            if "Button" in str(key) or "Hat" in str(key):
                                self.JoystickConfirm_toggle = not self.JoystickConfirm_toggle

                                if self.JoystickConfirm_toggle:
                                    if "Button 3" in str(key) and Game_SharedData.Jump is False:
                                        Game_SharedData.Jump = True
                                        Game_SharedData.JumpUP = True

                                        Ypos = Game_SharedData.camera.position.y
                                        Game_SharedData.StartYposition = Ypos

                                        eFPS = Game_SharedData.SharedData.eFPS
                                        Game_SharedData.Jump_Start_FPS = eFPS

                                    if "Hat" in str(key):
                                        Game_SharedData.SharedData.mod_Base__.CameraWindow.close(
                                            Game_SharedData)

                                    else:
                                        if "Button 7" in str(key):
                                            Game_SharedData.SharedData.mod_Base__.CameraWindow.key_event(
                                                Game_SharedData,
                                                Game_SharedData.wnd.keys.E,
                                                Game_SharedData.wnd.keys.ACTION_PRESS,
                                                None)

                                        elif "Button 6" in str(key):
                                            Game_SharedData.SharedData.mod_Base__.CameraWindow.key_event(
                                                Game_SharedData,
                                                Game_SharedData.wnd.keys.R,
                                                Game_SharedData.wnd.keys.ACTION_PRESS,
                                                None)

                                        else:
                                            self.JoystickConfirm = True
                                else:
                                    self.JoystickConfirm = False

                            if "Axis" in str(key):
                                if "Axis 3" in str(key):
                                    Axis3value = self.mod_pyjoystick__.Key.get_value(key)
                                    Game_SharedData.Joystick_Rotation[0] = Axis3value

                                if "Axis 4" in str(key):
                                    Axis4value = self.mod_pyjoystick__.Key.get_value(key)
                                    Game_SharedData.Joystick_Rotation[1] = Axis4value

                                if "Axis 1" in str(key):
                                    try:
                                        if self.mod_pyjoystick__.Key.get_value(key) < -0.25:
                                            Game_SharedData.SharedData.mod_Base__.CameraWindow.key_event(
                                                Game_SharedData,
                                                Game_SharedData.wnd.keys.W,
                                                Game_SharedData.wnd.keys.ACTION_PRESS,
                                                None)

                                        else:
                                            Game_SharedData.SharedData.mod_Base__.CameraWindow.key_event(
                                                Game_SharedData,
                                                Game_SharedData.wnd.keys.W,
                                                Game_SharedData.wnd.keys.ACTION_RELEASE,
                                                None)

                                        if self.mod_pyjoystick__.Key.get_value(key) > 0.25:
                                            Game_SharedData.SharedData.mod_Base__.CameraWindow.key_event(
                                                Game_SharedData,
                                                Game_SharedData.wnd.keys.S,
                                                Game_SharedData.wnd.keys.ACTION_PRESS,
                                                None)

                                        else:
                                            Game_SharedData.SharedData.mod_Base__.CameraWindow.key_event(
                                                Game_SharedData,
                                                Game_SharedData.wnd.keys.S,
                                                Game_SharedData.wnd.keys.ACTION_RELEASE,
                                                None)
                                    except Exception as Message:
                                        print(Message)

                                if "Axis 0" in str(key):
                                    try:
                                        if self.mod_pyjoystick__.Key.get_value(key) < -0.25:
                                            Game_SharedData.SharedData.mod_Base__.CameraWindow.key_event(
                                                Game_SharedData,
                                                Game_SharedData.wnd.keys.A,
                                                Game_SharedData.wnd.keys.ACTION_PRESS,
                                                None)

                                        else:
                                            Game_SharedData.SharedData.mod_Base__.CameraWindow.key_event(
                                                Game_SharedData,
                                                Game_SharedData.wnd.keys.A,
                                                Game_SharedData.wnd.keys.ACTION_RELEASE,
                                                None)

                                        if self.mod_pyjoystick__.Key.get_value(key) > 0.25:
                                            Game_SharedData.SharedData.mod_Base__.CameraWindow.key_event(
                                                Game_SharedData,
                                                Game_SharedData.wnd.keys.D,
                                                Game_SharedData.wnd.keys.ACTION_PRESS,
                                                None)

                                        else:
                                            Game_SharedData.SharedData.mod_Base__.CameraWindow.key_event(
                                                Game_SharedData,
                                                Game_SharedData.wnd.keys.D,
                                                Game_SharedData.wnd.keys.ACTION_RELEASE,
                                                None)
                                    except Exception as Message:
                                        print(Message)

                        else:
                            self.JoystickMouse = [0, 0]
                            if "Button" in str(key):
                                self.JoystickConfirm_toggle = not self.JoystickConfirm_toggle

                                if self.JoystickConfirm_toggle:
                                    if "Button 3" in str(key):
                                        self.JoystickExit = True

                                    else:
                                        if "Button 2" in str(key):
                                            self.JoystickZoom = "+"

                                        elif "Button 1" in str(key):
                                            self.JoystickZoom = "-"

                                        elif "Button 0" in str(key):
                                            self.JoystickReset = True

                                        self.JoystickExit = False
                                        self.JoystickConfirm = True

                                else:
                                    self.JoystickConfirm = False

                            if "Hat" in str(key):
                                self.JoystickHatPressed = True
                                self.JoystickMouse = [0, 0]

                                if "Right" in str(key):
                                    self.JoystickMouse[0] = "Right"

                                if "Left" in str(key):
                                    self.JoystickMouse[0] = "Left"

                                if  "Up" in str(key):
                                    self.JoystickMouse[1] = "Up"

                                if  "Down" in str(key):
                                    self.JoystickMouse[1] = "Down"
                            else:
                                self.JoystickHatPressed = False

                except Exception as Message:
                    self.ErrorMessage = "".join(("JoystickUtils > EstablishJoystickConnection ",
                                                 "> JoystickEvents > ",
                                                 f"key_received: {str(Message)}"))

                    self.ErrorMessage_detailed = "".join(
                        self.mod_Traceback__.format_exception(
                            None,
                            Message,
                            Message.__traceback__))

                    self.mod_ErrorUtils__.GenerateErrorScreen.ErrorScreen(self)
            try:
                while True:
                    self.mod_pyjoystick_run_event_loop_(print_add, print_remove, key_received)
            except Exception as Message:
                self.ErrorMessage = "".join(("JoystickUtils > GenerateHomeScreen > ",
                                             f"JoystickEvents: {str(Message)}"))

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
