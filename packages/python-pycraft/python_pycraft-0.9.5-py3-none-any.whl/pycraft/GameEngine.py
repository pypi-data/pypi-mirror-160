if __name__ != "__main__":
    print("Started <Pycraft_GameEngine>")

    import os
    if ("site-packages" in os.path.dirname(__file__) or
            "dist-packages" in os.path.dirname(__file__)):
        try:
            from pycraft.ShareDataUtils import (
                Class_Startup_variables as SharedData)
        except:
            from ShareDataUtils import (
                Class_Startup_variables as SharedData)
    else:
        from ShareDataUtils import (
            Class_Startup_variables as SharedData)

    SharedData.mod_ModernGL_window_.setup_basic_logging(0)


    class GameEngine(SharedData.mod_Base__.CameraWindow):
        SharedData.mod_Base__.CameraWindow.title = f"Pycraft: v{SharedData.version}: Playing"
        SharedData.mod_Base__.CameraWindow.resource_dir = SharedData.base_folder
        SharedData.mod_Base__.CameraWindow.vsync = False
        SharedData.mod_Base__.CameraWindow.resizable = True

        def __init__(self, **kwargs):
            try:
                global GameEngine_Initialisation
                global GameLoadProgressPercent

                GameLoadProgressPercent = 0

                self.SharedData = SharedData

                self.Joystick_Rotation = [0, 0]

                WindowSize = self.SharedData.realWidth, self.SharedData.realHeight
                CurrentWindowSize = WindowSize

                self.StartLoading = self.SharedData.mod_Time__.perf_counter()

                GameLoadProgressPercent = 10

                GameEngine_Initialisation = True
                CreateLoadScreen = self.SharedData.mod_Threading__.Thread(
                    target=self.SharedData.mod_MainGameEngine__.CreateEngine.RenderLoadDisplay,
                    args=(self.SharedData, ))

                CreateLoadScreen.start()
                CreateLoadScreen.name = "Thread_CreateLoadScreen"
                super().__init__(**kwargs)

                try:
                    DisplayPosition = self.SharedData.mod_DisplayUtils__.DisplayUtils.GetDisplayLocation(
                        self.SharedData)
                except:
                    CurrentWindowSize = self.window_size
                    DisplayPosition = (int((self.SharedData.FullscreenX-CurrentWindowSize[0])/2),
                                        int((self.SharedData.FullscreenY-CurrentWindowSize[1])/2))

                self.skybox_distance = 1600

                self.camera.projection.update(
                    near=1,
                    far=self.skybox_distance,
                    fov=70)

                self.wnd.mouse_exclusivity = True

                if self.SharedData.Fullscreen:
                    self.wnd.position = DisplayPosition
                    self.SharedData.mod_Base__.CameraWindow.resize(
                        self,
                        self.wnd.size[0],
                        self.wnd.size[1])

                if self.SharedData.platform == "Linux":
                    self.wnd.set_icon(
                        self.SharedData.mod_OS__.path.join(
                            self.SharedData.base_folder,
                            ("Resources//General_Resources//Icon.png")))
                else:
                    self.wnd.set_icon(
                        self.SharedData.mod_OS__.path.join(
                            self.SharedData.base_folder,
                            ("Resources\\General_Resources\\Icon.png")))

                GameLoadProgressPercent = 20

                # Offscreen buffer
                offscreen_size = 1024, 1024
                self.offscreen_depth = self.ctx.depth_texture(offscreen_size)
                self.offscreen_depth.compare_func = ""
                self.offscreen_depth.repeat_x = False
                self.offscreen_depth.repeat_y = False
                # Less ugly by default with linear. May need to be NEAREST for some techniques
                self.offscreen_depth.filter = (self.SharedData.mod_ModernGL__.LINEAR,
                                               self.SharedData.mod_ModernGL__.LINEAR)

                self.offscreen = self.ctx.framebuffer(depth_attachment=self.offscreen_depth,)

                self.sun_radius = 50

                self.sun = self.SharedData.mod_ModernGL_window_Geometry.sphere(
                    radius=self.sun_radius)

                self.moon = self.SharedData.mod_ModernGL_window_Geometry.sphere(
                    radius=80)

                self.rain_particle = self.SharedData.mod_ModernGL_window_Geometry.sphere(
                    radius=1)

                GameLoadProgressPercent = 30

                # Debug geometry
                self.offscreen_quad = self.SharedData.mod_ModernGL_window_Geometry.quad_2d(
                    size=(0.5, 0.5),
                    pos=(0.75, 0.75))

                self.offscreen_quad2 = self.SharedData.mod_ModernGL_window_Geometry.quad_2d(
                    size=(0.5, 0.5),
                    pos=(0.25, 0.75))

                self.SkySphere = self.SharedData.mod_ModernGL_window_Geometry.sphere(
                    radius=self.skybox_distance)

                self.objects: self.SharedData.mod_Typing__.Dict[
                    str,
                    self.SharedData.mod_ModernGL__.VertexArray] = {}

                self.objects_shadow: self.SharedData.mod_Typing__.Dict[
                    str,
                    self.SharedData.mod_ModernGL__.VertexArray] = {}

                if self.SharedData.platform == "Linux":
                    # Use 'u' to do things with UVs that this really needs
                    self.scene: self.SharedData.mod_ModernGL_window_.scene.Scene = self.load_scene(
                        self.SharedData.mod_OS__.path.join(
                            self.SharedData.base_folder,
                            ("Resources//G3_Resources//map//map.obj")),
                        cache=True)
                else:
                    self.scene: self.SharedData.mod_ModernGL_window_.scene.Scene = self.load_scene(
                        self.SharedData.mod_OS__.path.join(
                            self.SharedData.base_folder,
                            ("Resources\\G3_Resources\\map\\map.obj")),
                        cache=True)

                GameLoadProgressPercent = 40

                if self.SharedData.platform == "Linux":
                    self.SkyBox_texture_Sun = self.load_texture_array(
                        SharedData.mod_OS__.path.join(
                            SharedData.base_folder,
                            ("Resources//G3_Resources//skysphere//ClearSkyTransition.gif")))

                else:
                    self.SkyBox_texture_Sun = self.load_texture_array(
                        SharedData.mod_OS__.path.join(
                            SharedData.base_folder,
                            ("Resources\\G3_Resources\\skysphere\\ClearSkyTransition.gif")))

                GameLoadProgressPercent = 50

                # Programs
                self.SharedData.mod_GameEngineUtils__.LoadPrograms.LoadProgramFiles(self)

                self.SharedData.mod_GameEngineUtils__.LoadPrograms.LoadProgramText(self)

                GameLoadProgressPercent = 60

                vao = self.scene.root_nodes[0].mesh.vao
                self.objects["map"] = vao.instance(self.shadowmap)
                self.objects_shadow["map"] = vao.instance(self.depth_prog)

                self.prog["texture0"].value = 0
                self.prog["num_layers"].value = 41.0

                # affects the velocity of the particles over time
                # grav?
                self.particles_transform["gravity"].value = -.005
                self.ctx.point_size = self.wnd.pixel_ratio * 2  # point size

                self.N = 25_000  # particle count
                # Initial / current number of active particles
                self.active_particles = self.N // 100
                # Maximum number of particles to emit per frame
                self.max_emit_count = self.N // 100
                self.stride = 28  # byte stride for each vertex
                self.floats = 7
                # Note that passing dynamic=True probably doesn't mean
                # anything to most drivers today
                try:
                    self.vbo1 = self.ctx.buffer(reserve=self.N * self.stride)
                    self.vbo2 = self.ctx.buffer(reserve=self.N * self.stride)
                except:
                    self.vbo1 = self.ctx.buffer(reserve=self.N * self.stride, dynamic=True)
                    self.vbo2 = self.ctx.buffer(reserve=self.N * self.stride, dynamic=True)
                # Write some initial particles
                self.vbo1.write(
                    self.SharedData.mod_Numpy__.fromiter(
                        self.SharedData.mod_GameEngineUtils__.Particles.gen_particles(
                            self,
                            self.active_particles),
                        count=self.active_particles * self.floats, dtype="f4"))

                # Transform vaos. We transform data back and forth to avoid buffer copy
                self.transform_vao1 = self.ctx.vertex_array(
                    self.particles_transform,
                    [(self.vbo1, "2f 2f 3f", "in_pos", "in_vel", "in_color")],
                )
                self.transform_vao2 = self.ctx.vertex_array(
                    self.particles_transform,
                    [(self.vbo2, "2f 2f 3f", "in_pos", "in_vel", "in_color")],
                )

                # Render vaos. The render to screen version of the tranform vaos above
                self.render_vao1 = self.ctx.vertex_array(
                    self.particles_screen,
                    [(self.vbo1, "2f 2x4 3f", "in_pos", "in_color")],
                )
                self.render_vao2 = self.ctx.vertex_array(
                    self.particles_screen,
                    [(self.vbo2, "2f 2x4 3f", "in_pos", "in_color")],
                )

                # The emit buffer size is only max_emit_count.
                self.emit_buffer_elements = self.max_emit_count

                self.gpu_emitter_vao = self.ctx._vertex_array(self.gpu_emitter_particles, [])

                # Query object to inspect render calls
                self.query = self.ctx.query(primitives=True)

                # Cycle emit methods per frame
                self.particles_screen["projection"].write(
                    self.SharedData.mod_GameEngineUtils__.Particles.projection(
                        self))

                self.shadowmap["u_sampler_shadow"].value = 0
                self.shadowmap["Color1"].value = 1
                self.shadowmap["Color2"].value = 2

                self.shadowmap["light_level"] = 0.5

                self.mvp = self.shadowmap["u_mvp"]
                self.mvp_depth = self.shadowmap["u_depth_bias_mvp"]

                self.light = self.shadowmap["u_light"]
                self.color = self.shadowmap["u_color"]

                self.mvp_shadow = self.depth_prog["u_mvp"]

                self.sun_prog["color"].value = (1.0, 1.0, 0.0, 1.0)
                self.moon_prog["color"].value = (1.0, 1.0, 1.0, 1.0)
                self.lightpos = 0, 0, 0

                self.color.value = (1.0, 1.0, 1.0)

                GameLoadProgressPercent = 70

                if self.SharedData.platform == "Linux":
                    self.tex1 = self.load_texture_2d(
                        SharedData.mod_OS__.path.join(
                            SharedData.base_folder,
                            ("Resources//G3_Resources//map//GrassTexture.png")),
                        mipmap=True,)

                    self.tex2 = self.load_texture_2d(
                        SharedData.mod_OS__.path.join(
                            SharedData.base_folder,
                            ("Resources//G3_Resources//map//RockTexture.png")),
                        mipmap=True,)

                else:
                    self.tex1 = self.load_texture_2d(
                        SharedData.mod_OS__.path.join(
                            SharedData.base_folder,
                            ("Resources\\G3_Resources\\map\\GrassTexture.png")),
                        mipmap=True,)

                    self.tex2 = self.load_texture_2d(
                        SharedData.mod_OS__.path.join(
                            SharedData.base_folder,
                            ("Resources\\G3_Resources\\map\\RockTexture.png")),
                        mipmap=True,)

                self.tex1.use(location=1)
                self.tex2.use(location=2)

                SHADOW_SIZE: self.SharedData.mod_Typing_Final[int] = 2 << 7

                shadow_size = (SHADOW_SIZE,
                               SHADOW_SIZE,)

                GameLoadProgressPercent = 80

                self.tex_depth = self.ctx.depth_texture(shadow_size)

                self.tex_color_depth = self.ctx.texture(
                    shadow_size,
                    components=1,
                    dtype="f4")

                self.fbo_depth = self.ctx.framebuffer(
                    color_attachments=[self.tex_color_depth],
                    depth_attachment=self.tex_depth)

                self.sampler_depth = self.ctx.sampler(
                    filter=(self.SharedData.mod_ModernGL__.LINEAR,
                            self.SharedData.mod_ModernGL__.LINEAR),
                    compare_func=">=",
                    repeat_x=False,
                    repeat_y=False,)

                self.Jump = False
                self.JumpUP = True
                self.StartYposition = 0
                self.Jump_Start_FPS = 0
                self.Collision = False

                self.RunForwardTimer = False
                self.RunForwardTimer_start = 0
                self.RunForwardTimer_start_sound = 0
                self.Sprinting = False
                self.WkeydownTimer_start = 0
                self.Wkeydown = False

                self.IKeyPressed = False

                self.AkeydownTimer_start = 0
                self.Akeydown = False

                self.SkeydownTimer_start = 0
                self.Skeydown = False

                self.DkeydownTimer_start = 0
                self.Dkeydown = False

                z = 1000
                size = (z, z)

                if self.SharedData.AddedPerlin:
                    CloudData = self.SharedData.mod_GameEngineUtils__.ComputeWeather.ComputeCloudNoise(
                        self,
                        size)

                    self.range = max(CloudData) - min(CloudData)
                else:
                    self.range = 0.75

                self.CloudsProgram["CloudHeight"] = 500.0
                self.CloudsProgram["height_max"] = self.range

                self.shadowmap["height_max"] = self.range

                vertices, index = self.SharedData.mod_GameEngineUtils__.ComputeWeather.ComputeCloudModel(
                    self,
                    size[0])

                self.vbo = self.ctx.buffer(vertices.astype("f4"))
                self.ibo = self.ctx.buffer(index.astype("i4"))

                cloud_vao_content = [(
                    self.vbo,
                    "2f",
                    "in_vert"),]

                self.vao = self.ctx.vertex_array(
                    self.CloudsProgram,
                    cloud_vao_content,
                    self.ibo)

                if self.SharedData.platform == "Linux":
                    self.cloud_texture = self.load_texture_2d(
                        SharedData.mod_OS__.path.join(
                            SharedData.base_folder,
                            ("Resources//G3_Resources//clouds//Rnd_noise.png")))

                else:
                    self.cloud_texture = self.load_texture_2d(
                        SharedData.mod_OS__.path.join(
                            SharedData.base_folder,
                            ("Resources\\G3_Resources\\clouds\\Rnd_noise.png")))

                GameLoadProgressPercent = 90

                if self.SharedData.Fullscreen is False:
                    self.wnd.fullscreen = True

                self.OnStart = True

                self.time = 0
                self.frametime = 1

                self.Running = True

                self.Inventory = False
                self.Map = False

                self.SharedData.mod_Globals__.Share.initialize_controller_game(self)

                self.UpdateProjection = False

                self.Time_Percent = 0

                self.day = 1
                self.daycycleTime = 0

                self.scrollTime = 0
                self.GameSunTime = 0

                self.DayCycle = 1

                self.GameTime = 0

                self.weather = ""
                WeatherDelta = 1
                self.DefaultSkyCol = 1.0

                self.SharedData.mod_GameEngineUtils__.ComputeWeather.ComputeWeather(self)

                self.WeatherTime = 0
                self.ThunderTimer = 0
                self.LightningTimer = 0
                self.ShowLightning = False
                self.ThunderTimer_Target = self.SharedData.mod_Random__.randint(15, 30)
                switchWeather = self.SharedData.mod_Random__.randint(60, 120)
                self.FlashTimer = 0
                self.ShowFlash = False
                self.LengthenStorm = False
                self.PreviousWeather = self.weather

                self.Previous_Fog_Distance_Min = self.shadowmap["w_min"].value
                self.Previous_Fog_Distance_Max = self.shadowmap["w_max"].value

                self.Previous_color = self.color.value[0]

                self.Previous_CloudsProgram_Alpha = self.CloudsProgram["WeatherAlpha"].value
                self.Previous_CloudsProgram_CloudColor = self.CloudsProgram["CloudColor"].value

                self.Previous_multiplier = self.shadowmap["CloudHeightMultiplier"].value

                self.Previous_prog_transparency = self.prog["transparency"].value

                GameLoadProgressPercent = 100
                while self.Running:
                    # 250 is base FPS w/ shadowmapping
                    # 205 is avg w/ shadowmapping + dynamic skybox
                    start = SharedData.mod_Time__.perf_counter()
                    self.GameTimeDelta = self.time
                    if self.Inventory or self.Map:
                        self.SharedData.mod_GameEngineUtils__.AccessOtherGUIs.AccessGUI(self)

                    self.SharedData.Game_Engine_variables = self

                    self.keys = self.wnd.keys

                    self.wnd.clear()
                    self.ctx.clear(self.DefaultSkyCol,
                                   self.DefaultSkyCol,
                                   self.DefaultSkyCol)

                    if self.WeatherTime >= switchWeather:
                        switchWeather = self.SharedData.mod_Random__.randint(60, 120)
                        self.WeatherTime = 0
                        self.weather = ""
                        WeatherDelta += 1

                        self.PreviousWeather = self.weather

                        self.Previous_Fog_Distance_Min = self.shadowmap["w_min"].value
                        self.Previous_Fog_Distance_Max = self.shadowmap["w_max"].value

                        self.Previous_color = self.color.value[0]

                        self.Previous_CloudsProgram_Alpha = self.CloudsProgram["WeatherAlpha"].value
                        self.Previous_CloudsProgram_CloudColor = self.CloudsProgram["CloudColor"].value

                        self.Previous_multiplier = self.shadowmap["CloudHeightMultiplier"].value

                        self.Previous_prog_transparency = self.prog["transparency"].value

                        self.SharedData.mod_GameEngineUtils__.ComputeWeather.ComputeWeather(self)

                    self.SharedData.aFPS += self.SharedData.eFPS
                    self.SharedData.Iteration += 1

                    if self.SharedData.Devmode == 10:
                        self.SharedData.mod_CaptionUtils__.GenerateCaptions.GetOpenGLCaption(
                            SharedData,
                            self)

                    self.SharedData.Total_move_x = 0
                    self.SharedData.Total_move_y = 0
                    self.SharedData.Total_move_z = 0

                    try:
                        if (SharedData.mod_Pygame__.mixer.Channel(2).get_busy() is False and
                                SharedData.sound):

                            SharedData.mod_SoundUtils__.PlaySound.PlayAmbientSound(SharedData)
                    except Exception as Message:
                        self.SharedData.ErrorMessage = "".join(("GameEngine > GameEngine ",
                                                                f"> __init__: {str(Message)}"))

                        self.SharedData.ErrorMessage_detailed = "".join(
                            self.mod_Traceback__.format_exception(
                                None,
                                Message,
                                Message.__traceback__))

                        self.SharedData.mod_ErrorUtils__.GenerateErrorScreen.ErrorScreen(
                            self.SharedData)

                    try:
                        if (SharedData.mod_Pygame__.mixer.Channel(4).get_busy() is False and
                                SharedData.sound and
                                self.weather != "sunny"):

                            SharedData.mod_SoundUtils__.PlaySound.PlayRainSound(SharedData)
                    except Exception as Message:
                        self.SharedData.ErrorMessage = "".join(("GameEngine > GameEngine ",
                                                                f"> __init__: {str(Message)}"))

                        self.SharedData.ErrorMessage_detailed = "".join(
                            self.mod_Traceback__.format_exception(
                                None,
                                Message,
                                Message.__traceback__))

                        self.SharedData.mod_ErrorUtils__.GenerateErrorScreen.ErrorScreen(
                            self.SharedData)

                    if self.frametime > 0:
                        self.SharedData.eFPS = 1/self.frametime

                    self.Time_Percent = ((100/1056)*(self.GameTime))

                    self.SharedData.mod_GameEngineUtils__.ShadowmappingMathematics.ComputeCelestialEntities(
                        self)

                    self.ctx.enable(
                        self.SharedData.mod_ModernGL__.DEPTH_TEST |
                        self.SharedData.mod_ModernGL__.CULL_FACE)

                    # --- PASS 1: Render shadow map
                    self.SharedData.mod_GameEngineUtils__.ShadowmappingMathematics.ComputeShadows(
                        self)

                    # --- PASS 2: Render scene to screen
                    self.wnd.use()
                    cam = self.camera.matrix
                    self.SharedData.X = int(self.camera.position.x*100)/100
                    self.SharedData.Y = int(self.camera.position.y*100)/100
                    self.SharedData.Z = int(self.camera.position.z*100)/100

                    cam[3][0] = 0
                    cam[3][1] = 0
                    cam[3][2] = 0

                    translation = self.SharedData.mod_Pyrr_Matrix44_.from_translation(
                        (0.0, 0.0, 0.0),
                        dtype="f4")

                    modelview = translation

                    self.prog["m_proj"].write(self.camera.projection.matrix)
                    self.prog["m_model"].write(modelview)
                    self.prog["m_camera"].write(cam)

                    self.particles_screen["projection"].write(self.SharedData.mod_GameEngineUtils__.Particles.projection(self))

                    self.daycycleTime = self.time

                    if self.Time_Percent < 40: # day
                        self.prog["time"].value = 0
                        self.DefaultSkyCol = 1.0

                    elif self.Time_Percent < 50: # sunset
                        self.DefaultSkyCol = 1-((0.7/10)*(self.Time_Percent-40))
                        self.prog["time"].value = ((19/10)*(self.Time_Percent-40))+1

                    elif self.Time_Percent < 90: # night
                        self.prog["time"].value = 21
                        self.DefaultSkyCol = 0.3

                    else: # sunrise
                        self.DefaultSkyCol = 1-((0.7/10)*(100-self.Time_Percent))
                        self.prog["time"].value = 21-(((21/10)*(self.Time_Percent-90)))

                    self.CloudsProgram["DefaultSkyCol"] = self.DefaultSkyCol

                    self.ctx.front_face = "cw"

                    self.SharedData.mod_GameEngineUtils__.ComputeWeather.BlendWeather(
                        self)

                    if self.ThunderTimer > self.ThunderTimer_Target:
                        self.ThunderTimer_Target = self.SharedData.mod_Random__.randint(5, 30)
                        self.ThunderTimer = 0
                        self.FlashTimer = 0
                        self.LightningTimer = 0
                        if self.SharedData.ShowLightning:
                            self.color.value = (1.0, 1.0, 1.0)
                        self.ShowLightning = True
                        self.ShowFlash = True
                        if self.SharedData.sound:
                            self.SharedData.mod_SoundUtils__.PlaySound.PlayThunderSound(
                                self.SharedData)

                    if self.weather == "rain.heavy.thundery":
                        LightningDelay = self.SharedData.mod_Random__.randint(30, 75)/100
                        if (self.LightningTimer > LightningDelay and
                                self.ShowLightning):

                            self.FlashTimer = 0
                            self.DefaultSkyCol = 1
                            self.LightningTimer = 0
                            self.ShowLightning = False
                            self.ShowFlash = True

                    if self.ShowFlash:
                        if self.FlashTimer <= 1/60:
                            self.DefaultSkyCol = 1
                            if self.SharedData.ShowLightning:
                                self.color.value = (1.0, 1.0, 1.0)
                        else:
                            self.ShowFlash = False

                    if self.weather != "sunny":
                        self.SharedData.mod_Pygame__.mixer.Channel(4).unpause()
                        if self.weather == "rain.light":
                            RandomiseVolumeReduction = self.SharedData.mod_Random__.randint(2, 5)
                            self.SharedData.mod_Pygame__.mixer.Channel(2).set_volume(
                                (self.SharedData.soundVOL/100)/RandomiseVolumeReduction)

                            self.SharedData.mod_Pygame__.mixer.Channel(4).set_volume(
                                (((self.SharedData.soundVOL/100)*10)/100))

                        else:
                            self.SharedData.mod_Pygame__.mixer.Channel(2).pause()
                            if self.weather == "rain.heavy.thundery":
                                self.SharedData.mod_Pygame__.mixer.Channel(4).set_volume(
                                    (((self.SharedData.soundVOL/100)*30)/100)
                                )
                            else:
                                self.SharedData.mod_Pygame__.mixer.Channel(4).set_volume(
                                    (((self.SharedData.soundVOL/100)*20)/200)
                                )

                    else:
                        self.SharedData.mod_Pygame__.mixer.Channel(4).pause()
                        self.SharedData.mod_Pygame__.mixer.Channel(2).set_volume(
                            self.SharedData.soundVOL/100)

                        self.SharedData.mod_Pygame__.mixer.Channel(2).unpause()

                    if self.weather != "sunny":
                        self.ctx.enable(self.SharedData.mod_ModernGL__.BLEND)

                    self.SkyBox_texture_Sun.use(location=0)
                    self.SkySphere.render(self.prog)

                    if self.weather != "sunny":
                        self.ctx.disable(self.SharedData.mod_ModernGL__.BLEND)

                    self.ctx.front_face = "ccw"

                    # pass 5: Render the sun position
                    self.moon.render(self.moon_prog)
                    self.sun.render(self.sun_prog)

                    self.ctx.front_face = "cw"

                    if self.weather != "sunny":
                        self.particles_transform["ft"].value = self.frametime

                        self.SharedData.mod_GameEngineUtils__.Particles.emit_gpu(
                            self,
                            self.time,
                            self.frametime)

                    self.CloudPos = self.SharedData.mod_Pyrr_Vector3_(
                            (self.camera.position.x,
                            0,
                            self.camera.position.z),
                        dtype="f4")

                    self.CloudsProgram["m_proj"].write(self.camera.projection.matrix)
                    self.CloudsProgram["m_camera"].write(self.camera.matrix)
                    self.CloudsProgram["m_model"].write(
                        self.SharedData.mod_Pyrr_Matrix44_.from_translation(
                            self.CloudPos,
                            dtype="f4"))

                     # shadows, variable rendering maybe

                    self.CloudsProgram["X_Offset"] = self.SharedData.mod_Math__.sin(self.time/50)/10
                    self.CloudsProgram["Y_Offset"] = self.SharedData.mod_Math__.cos(self.time/50)/10

                    self.cloud_texture.use(location=0)

                    self.ctx.enable(self.SharedData.mod_ModernGL__.BLEND)

                    self.vao.render(mode=self.SharedData.mod_ModernGL__.TRIANGLE_STRIP)

                    self.ctx.blend_func = self.SharedData.mod_ModernGL__.DEFAULT_BLENDING
                    # pass 2: render the scene and retro project depth shadow-map
                    # counter clock wise -> render front faces

                    self.sampler_depth.use(location=0)
                    self.tex_depth.use(location=0)
                    self.cloud_texture.use(location=0)

                    self.ctx.front_face = "ccw"

                    # pass 4: render textured scene with shadow

                    self.objects["map"].render()
                    self.ctx.disable(self.SharedData.mod_ModernGL__.BLEND)

                    if self.weather == "rain.heavy.thundery" and self.LengthenStorm:
                        switchWeather = switchWeather*(self.SharedData.mod_Random__.randint(
                            15,
                            30)/10)
                        self.LengthenStorm = False

                    self.SharedData.mod_GameEngineUtils__.OnscreenEventFunction.game_events(self)

                    self.SharedData.Iteration += 1
                    if self.OnStart:
                        self.OnStart = False

                        GameEngine_Initialisation = False

                        if SharedData.FromGameGUI is False:
                            CurrentLoadTime = SharedData.mod_Time__.perf_counter()-self.StartLoading
                            SharedData.LoadTime = [
                                SharedData.LoadTime[0] + CurrentLoadTime,
                                self.SharedData.LoadTime[1] + 1]

                        else:
                            SharedData.FromGameGUI = False

                    if SharedData.FPS_Overclock is False:
                        try:
                            ComputedPause = SharedData.mod_Time__.perf_counter()-start
                            SharedData.mod_Time__.sleep((1/SharedData.FPS)-ComputedPause)
                        except:
                            SharedData.mod_Time__.sleep((1/SharedData.FPS))

                    # Swap around objects for next frame
                    self.wnd.swap_buffers()

                    if self.weather != "sunny":
                        self.transform_vao1, self.transform_vao2 = self.transform_vao2, self.transform_vao1
                        self.render_vao1, self.render_vao2 = self.render_vao2, self.render_vao1
                        self.vbo1, self.vbo2 = self.vbo2, self.vbo1

                    self.frametime = self.SharedData.mod_Time__.perf_counter()-start
                    self.time += self.frametime
                    self.GameTime += self.frametime
                    self.WeatherTime += self.frametime

                    if self.weather == "rain.heavy.thundery":
                        if self.SharedData.mod_Pygame__.mixer.Channel(3).get_busy() is False:
                            self.ThunderTimer += self.frametime

                        self.LightningTimer += self.frametime
                        self.FlashTimer += self.frametime

                    self.SharedData.PlayTime = self.time

                    Message = self.ctx.error
                    if (Message != "GL_NO_ERROR" and Message != "GL_INVALID_OPERATION"):
                        try:
                            self.wnd.close()
                            self.SharedData.ErrorMessage = "".join(("GameEngine > GameEngine ",
                                                                    f"> __init__: {str(Message)}"))

                            self.SharedData.ErrorMessage_detailed = self.SharedData.ErrorMessage

                            self.SharedData.mod_ErrorUtils__.GenerateErrorScreen.ErrorScreen(
                                self.SharedData)

                        except Exception as Message2:
                            print(Message)
                            print(Message2)

                self.SharedData.Command = "Undefined"
                self.SharedData.FromPlay = True
                self.SharedData.Fullscreen = not self.wnd.fullscreen
                self.wnd.close()
                self.SharedData.mod_Pygame__.display.quit()
                self.SharedData.mod_Pygame__.init()
                self.SharedData.mod_Main__.Initialize.MenuSelector(self)
            except Exception as Message:
                self.SharedData.mod_GameEngineUtils__.Crash.CreateReport(self, Message)

    class CreateEngine:
        def __init__(self):
            pass


        def RenderLoadDisplay(self):
            try:
                self.mod_CaptionUtils__.GenerateCaptions.GetNormalCaption(
                    self,
                    "Loading Pycraft")

                self.mod_DisplayUtils__.DisplayUtils.SetDisplay(self)

                if self.platform == "Linux":
                    SecondaryFont = self.mod_Pygame__.font.Font(
                        self.mod_OS__.path.join(
                            self.base_folder,
                            ("Fonts//Book Antiqua.ttf")), 35)

                    LoadingFont = self.mod_Pygame__.font.Font(
                        self.mod_OS__.path.join(
                            self.base_folder,
                            ("Fonts//Book Antiqua.ttf")), 15)

                    LoadingTextFont = self.mod_Pygame__.font.Font(
                        self.mod_OS__.path.join(
                            self.base_folder,
                            ("Fonts//Book Antiqua.ttf")), 15)

                else:
                    SecondaryFont = self.mod_Pygame__.font.Font(
                        self.mod_OS__.path.join(
                            self.base_folder,
                            ("Fonts\\Book Antiqua.ttf")), 35)

                    LoadingFont = self.mod_Pygame__.font.Font(
                        self.mod_OS__.path.join(
                            self.base_folder,
                            ("Fonts\\Book Antiqua.ttf")), 15)

                    LoadingTextFont = self.mod_Pygame__.font.Font(
                        self.mod_OS__.path.join(
                            self.base_folder,
                            ("Fonts\\Book Antiqua.ttf")), 15)

                global GameEngine_Initialisation
                global GameLoadProgressPercent

                time = 0

                self.clock = self.mod_Pygame__.time.Clock()

                self.ProgressMessageText = self.mod_TextUtils__.GenerateText.LoadQuickText(self)

                Completion_Percentage = 0

                AverageLoadTime = self.LoadTime[0]/self.LoadTime[1]

                while GameEngine_Initialisation:
                    eFPS = self.clock.get_fps()
                    if self.LoadTime[0] != 0:
                        if eFPS > 0:
                            time += 1/eFPS

                        Loading_Line_X_value = (((self.realWidth-200)/AverageLoadTime)*time)+100

                    if GameLoadProgressPercent <= 10:
                        text = "Initializing"
                    elif GameLoadProgressPercent <= 20:
                        text = "Creating display"
                    elif GameLoadProgressPercent <= 30:
                        text = "Creating celestial entities"
                    elif GameLoadProgressPercent <= 40:
                        text = "Loading in-game objects: Map"
                    elif GameLoadProgressPercent <= 50:
                        text = "Loading in-game textures: Skysphere"
                    elif GameLoadProgressPercent <= 60:
                        text = "Loading in-game programmes"
                    elif GameLoadProgressPercent <= 70:
                        text = "Applying programme configurations"
                    elif GameLoadProgressPercent <= 80:
                        text = "Loading in-game textures: Grass"
                    else:
                        text = "Making final touches"

                    self.Progress_Line = [
                        (100, self.realHeight-100),
                        (100, self.realHeight-100)]

                    if self.LoadTime[0] != 0:
                        if Loading_Line_X_value > self.realWidth-100:
                            Loading_Line_X_value = self.realWidth-100

                        self.Progress_Line.append((Loading_Line_X_value, self.realHeight-100))
                        Completion_Percentage = (100/(self.LoadTime[0]/self.LoadTime[1]))*time
                        if Completion_Percentage > 100:
                            Completion_Percentage = 100
                    else:
                        self.Progress_Line.append((
                            ((self.realWidth/100)*GameLoadProgressPercent)-100,
                            self.realHeight-100))

                        Completion_Percentage = GameLoadProgressPercent

                    CreateEngine.GenerateLoadDisplay(
                        self,
                        LoadingFont,
                        text,
                        SecondaryFont,
                        LoadingTextFont,
                        Completion_Percentage)

                    for event in self.mod_Pygame__.event.get():
                        if (event.type == self.mod_Pygame__.QUIT or
                            (event.type == self.mod_Pygame__.KEYDOWN and
                             event.key == self.mod_Pygame__.K_ESCAPE)):

                            global Global_Save_and_QUIT
                            Global_Save_and_QUIT = True
                            quit()

                    self.mod_Pygame__.display.flip()

                    tempFPS = self.mod_DisplayUtils__.DisplayUtils.GetPlayStatus(self)

                    self.clock.tick(tempFPS)

                if self.LoadTime[1] >= 25:
                    self.LoadTime = [0, 1]

                self.mod_Pygame__.display.quit()
                self.mod_Pygame__.display.init()
            except Exception as Message:
                self.ErrorMessage = "GameEngine > CreateEngine > RenderLoadDisplay: "+str(Message)
                self.ErrorMessage_detailed = "".join(
                    self.mod_Traceback__.format_exception(
                        None,
                        Message,
                        Message.__traceback__))

                self.mod_ErrorUtils__.GenerateErrorScreen.ErrorScreen(self)


        def GenerateLoadDisplay(self, LoadingFont,
                                text, SecondaryFont,
                                LoadingTextFont, Completion_Percentage):
            try:
                self.Display.fill(self.BackgroundCol)

                self.realWidth = self.mod_Pygame__.display.get_window_size()[0]
                self.realHeight = self.mod_Pygame__.display.get_window_size()[1]

                PycraftTitle = self.TitleFont.render(
                    "Pycraft",
                    self.aa,
                    self.FontCol)
                TitleWidth = PycraftTitle.get_width()
                self.Display.blit(
                    PycraftTitle,
                    ((self.realWidth-TitleWidth)/2, 0))

                LoadingTitle = SecondaryFont.render(
                    "Loading",
                    self.aa,
                    self.SecondFontCol)
                self.Display.blit(
                    LoadingTitle,
                    (((self.realWidth-TitleWidth)/2)+55, 50))

                self.mod_Pygame__.draw.lines(
                    self.Display,
                    self.ShapeCol,
                    self.aa,
                    [(100, self.realHeight-100),
                     (self.realWidth-100, self.realHeight-100)],
                    3)

                self.mod_Pygame__.draw.lines(
                    self.Display,
                    self.AccentCol,
                    self.aa,
                    self.Progress_Line)

                DisplayMessage = LoadingFont.render(
                    self.ProgressMessageText,
                    self.aa,
                    self.FontCol)
                DisplayMessageWidth = DisplayMessage.get_width()
                self.Display.blit(
                    DisplayMessage,
                    ((self.realWidth-DisplayMessageWidth)/2, self.realHeight-120))

                TextFontRendered = LoadingTextFont.render(
                    f"{text}",
                    self.aa,
                    self.FontCol)
                TextFontRenderedWidth = TextFontRendered.get_width()
                self.Display.blit(
                    TextFontRendered,
                    ((self.realWidth-TextFontRenderedWidth)/2, self.realHeight-100))

                ProgressText = LoadingTextFont.render(
                    f"{round(Completion_Percentage)}% complete",
                    self.aa,
                    self.FontCol)
                ProgressTextWidth = ProgressText.get_width()
                self.Display.blit(
                    ProgressText,
                    ((self.realWidth-ProgressTextWidth)/2, self.realHeight-80))

            except Exception as Message:
                self.ErrorMessage = "".join(("GameEngine > CreateEngine > ",
                                             f"GenerateLoadDisplay: {str(Message)}"))

                self.ErrorMessage_detailed = "".join(
                    self.mod_Traceback__.format_exception(
                        None,
                        Message,
                        Message.__traceback__))

                self.mod_ErrorUtils__.GenerateErrorScreen.ErrorScreen(self)

        def Play(self):
            try:
                self.mod_Pygame__.mouse.set_cursor(self.mod_Pygame__.SYSTEM_CURSOR_WAIT)
                self.mod_Pygame__.display.quit()
                self.mod_Pygame__.display.init()
                if self.platform == "Linux":
                    self.TitleFont = self.mod_Pygame__.font.Font(
                        self.mod_OS__.path.join(
                            self.base_folder, ("Fonts//Book Antiqua.ttf")), 60)

                    self.WindowIcon = self.mod_Pygame__.image.load(
                        self.mod_OS__.path.join(
                            self.base_folder, ("Resources//General_Resources//Icon.png")))

                else:
                    self.TitleFont = self.mod_Pygame__.font.Font(
                        self.mod_OS__.path.join(
                            self.base_folder, ("Fonts\\Book Antiqua.ttf")), 60)

                    self.WindowIcon = self.mod_Pygame__.image.load(
                        self.mod_OS__.path.join(
                            self.base_folder, ("Resources\\General_Resources\\Icon.png")))

                self.mod_Globals__.Share.initialize(self)

                try:
                    self.mod_ModernGL_window_.run_window_config(GameEngine)
                except Exception as Message:
                    if ((str(Message) != "argument 2: <class 'TypeError'>: wrong type" or
                         str(Message) == "'NoneType' object has no attribute 'flip'")):

                        self.ErrorMessage = "GameEngine > CreateEngine > Play: " + str(Message)
                        SharedData.Command = "Undefined"

                return SharedData.Command
            except Exception as Message:
                self.ErrorMessage = "GameEngine > CreateEngine > Play: " + str(Message)
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
