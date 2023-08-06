if __name__ != "__main__":
    print("Started <Pycraft_GameEngineUtils>")

    class Crash:
        def __init__(self):
            pass

        def CreateReport(self, Message):
            print(Message, "".join(
                self.SharedData.mod_Traceback__.format_exception(
                    None,
                    Message,
                    Message.__traceback__)))

            try:
                self.wnd.close()
                self.SharedData.ErrorMessage = "".join(("GameEngine > GameEngine ",
                                                        f"> __init__: {str(Message)}"))

                self.SharedData.ErrorMessage_detailed = "".join(
                    self.SharedData.mod_Traceback__.format_exception(
                        None,
                        Message,
                        Message.__traceback__))

                self.SharedData.mod_ErrorUtils__.GenerateErrorScreen.ErrorScreen(
                    self.SharedData)

            except Exception as Message2:
                try:
                    self.SharedData.ErrorMessage = "".join(("GameEngine > GameEngine ",
                                                            f"> __init__: {str(Message2)}"))

                    self.SharedData.ErrorMessage_detailed = "".join(
                        self.SharedData.mod_Traceback__.format_exception(
                            None,
                            Message2,
                            Message2.__traceback__))

                    self.SharedData.mod_ErrorUtils__.GenerateErrorScreen.ErrorScreen(
                        self.SharedData)
                except:
                    print(Message)
                    print(Message2)

    class LoadPrograms:
        def __init__(self):
            pass

        def LoadProgramText(self):
            self.particles_transform = self.ctx.program(
                vertex_shader='''
                    #version 330

                    in vec2 in_pos;
                    in vec2 in_vel;
                    in vec3 in_color;

                    out vec2 vs_vel;
                    out vec3 vs_color;

                    void main() {
                        gl_Position = vec4(in_pos, 1.0, 1.0);
                        vs_vel = in_vel;
                        vs_color = in_color;
                    }
                    ''',
                geometry_shader='''
                    #version 330

                    layout(points) in;
                    layout(points, max_vertices = 1) out;

                    uniform float gravity;
                    uniform float ft;

                    in vec2 vs_vel[1];
                    in vec3 vs_color[1];

                    out vec2 out_pos;
                    out vec2 out_vel;
                    out vec3 out_color;

                    void main() {
                        vec2 pos = gl_in[0].gl_Position.xy;
                        vec2 velocity = vs_vel[0];

                        if (pos.y > -1.0) {
                            vec2 vel = velocity + vec2(0.0, gravity);
                            out_pos = pos + vel * ft;
                            out_vel = vel;
                            if (out_pos.x == 0.0) {
                                out_pos.y = -1.1;
                            }
                            out_color = vs_color[0];
                            EmitVertex();
                            EndPrimitive();
                        }
                    }
                    ''',
                varyings=['out_pos', 'out_vel', 'out_color'],
            )

            self.gpu_emitter_particles = self.ctx.program(
                vertex_shader='''
                    # version 330
                    #define M_PI 3.1415926535897932384626433832795
                    uniform vec2 mouse_pos;
                    uniform vec2 mouse_vel;
                    uniform float time;

                    out vec2 out_pos;
                    out vec2 out_vel;
                    out vec3 out_color;

                    float rand(float n){
                        return fract(sin(n) * 43758.5453123);
                        }

                    void main() {
                        float a = mod(time * gl_VertexID, M_PI * 2.0);
                        float r = clamp(rand(time + gl_VertexID), 0.1, 0.9);
                        out_pos = mouse_pos;
                        out_vel = vec2(sin(a), cos(a)) * r + mouse_vel;
                        out_color = vec3(0.0, 0.0, rand(time * 2.0 + gl_VertexID));
                    }
                    ''',
                varyings=['out_pos', 'out_vel', 'out_color'],
            )

        def LoadProgramFiles(self):
            if self.SharedData.platform == "Linux":
                self.CloudsProgram = self.load_program(
                    self.SharedData.mod_OS__.path.join(
                        self.SharedData.base_folder,
                        ("programs//clouds.glsl")))

                self.depth_prog = self.load_program(
                    self.SharedData.mod_OS__.path.join(
                        self.SharedData.base_folder,
                        ("programs//raw_depth.glsl")))

                self.shadowmap = self.load_program(
                    self.SharedData.mod_OS__.path.join(
                        self.SharedData.base_folder,
                        ("programs//shadowmap.glsl")))

                self.sun_prog = self.load_program(
                    self.SharedData.mod_OS__.path.join(
                        self.SharedData.base_folder,
                        ("programs//cube_simple.glsl")))

                self.moon_prog = self.load_program(
                    self.SharedData.mod_OS__.path.join(
                        self.SharedData.base_folder,
                        ("programs//cube_simple.glsl")))

                self.prog = self.load_program(
                    self.SharedData.mod_OS__.path.join(
                        self.SharedData.base_folder,
                        ("programs//cubemap.glsl")))

                self.particles_screen = self.load_program(
                    self.SharedData.mod_OS__.path.join(
                        self.SharedData.base_folder,
                        ("programs//particles_screen.glsl")))

            else:
                self.CloudsProgram = self.load_program(
                    self.SharedData.mod_OS__.path.join(
                        self.SharedData.base_folder,
                        ("programs\\clouds.glsl")))

                self.depth_prog = self.load_program(
                    self.SharedData.mod_OS__.path.join(
                        self.SharedData.base_folder,
                        ("programs\\raw_depth.glsl")))

                self.shadowmap = self.load_program(
                    self.SharedData.mod_OS__.path.join(
                        self.SharedData.base_folder,
                        ("programs\\shadowmap.glsl")))

                self.sun_prog = self.load_program(
                    self.SharedData.mod_OS__.path.join(
                        self.SharedData.base_folder,
                        ("programs\\cube_simple.glsl")))

                self.moon_prog = self.load_program(
                    self.SharedData.mod_OS__.path.join(
                        self.SharedData.base_folder,
                        ("programs\\cube_simple.glsl")))

                self.prog = self.load_program(
                    self.SharedData.mod_OS__.path.join(
                        self.SharedData.base_folder,
                        ("programs\\cubemap.glsl")))

                self.particles_screen = self.load_program(
                    self.SharedData.mod_OS__.path.join(
                        self.SharedData.base_folder,
                        ("programs\\particles_screen.glsl")))

    class Particles:
        def __init__(self):
            pass

        def emit_gpu(self, time, frame_time):
            """
            Emit new particles using a shader.
            """
            # Transform all particles recoding how many elements were emitted by geometry shader
            with self.query:
                self.transform_vao1.transform(
                    self.vbo2,
                    self.SharedData.mod_ModernGL__.POINTS,
                    vertices=self.active_particles)

            emit_count = min(self.N - self.query.primitives,
                             self.emit_buffer_elements,
                             self.max_emit_count)

            if emit_count > 0:
                self.gpu_emitter_particles["mouse_pos"].value = (0, 2)

                if self.weather == "rain.light":
                    self.gpu_emitter_particles["mouse_vel"].value = (
                        0,
                        self.SharedData.mod_Random__.randint(50, 100)/100)

                if self.weather == "rain.heavy":
                    self.gpu_emitter_particles["mouse_vel"].value = (
                        0,
                        self.SharedData.mod_Random__.randint(75, 125)/100)

                if self.weather == "rain.heavy.thundery":
                    self.gpu_emitter_particles["mouse_vel"].value = (
                        0,
                        self.SharedData.mod_Random__.randint(75, 150)/100)

                self.gpu_emitter_particles["time"].value = max(time, 0)
                self.gpu_emitter_vao.transform(
                    self.vbo2,
                    vertices=emit_count,
                    buffer_offset=self.query.primitives * self.stride)

            self.active_particles = self.query.primitives + emit_count
            self.render_vao2.render(
                self.SharedData.mod_ModernGL__.POINTS, vertices=self.active_particles)

        def gen_particles(self, n):
            for _ in range(n):
                # Current mouse position (2 floats)
                yield 0
                yield 2
                # Random velocity (2 floats)
                a = self.SharedData.mod_Numpy__.random.uniform(
                    0.0, self.SharedData.mod_Numpy__.pi * 2.0)
                r = self.SharedData.mod_Numpy__.random.uniform(0.1, 0.9)
                yield self.SharedData.mod_Numpy__.cos(a) * r + 0
                yield self.SharedData.mod_Numpy__.sin(a) * r + 0
                # Random color (4 floats)
                yield 0.0
                yield 0.0
                yield self.SharedData.mod_Numpy__.random.uniform(0.0, 1.0)
                #yield self.SharedData.mod_Numpy__.random.uniform(0.0, 1.0)

        def projection(self):
            return self.SharedData.mod_Pyrr_matrix44_.create_orthogonal_projection(
                -self.wnd.aspect_ratio, self.wnd.aspect_ratio,
                -1, 1,
                -1, 100,
                dtype='f4',
            )

    class ComputeWeather:
        def __init__(self):
            pass

        def ComputeCloudModel(self, size):
            try:
                vertices = self.SharedData.mod_Numpy__.dstack(
                    self.SharedData.mod_Numpy__.mgrid[0:size, 0:size][::-1]) / size

                temp = self.SharedData.mod_Numpy__.dstack(
                    [self.SharedData.mod_Numpy__.arange(0, size * size - size),
                    self.SharedData.mod_Numpy__.arange(size, size * size)])

                index = self.SharedData.mod_Numpy__.pad(
                    temp.reshape(size - 1, 2 * size),
                    [[0, 0], [0, 1]],
                    "constant",
                    constant_values=-1)

                return vertices, index
            except Exception as Message:
                self.SharedData.ErrorMessage = "".join(("GameEngineUtils > ComputeWeather ",
                                                        f"> ComputeCloudModel: {str(Message)}"))

                self.SharedData.ErrorMessage_detailed = "".join(
                    self.SharedData.mod_Traceback__.format_exception(
                        None,
                        Message,
                        Message.__traceback__))

                self.SharedData.mod_ErrorUtils__.GenerateErrorScreen.ErrorScreen(
                    self.SharedData)

        def ComputeCloudNoise(self, shape):
            try:
                if self.SharedData.AddedPerlin:
                    scale = 100.0
                    octaves = 6
                    persistence = 0.5
                    lacunarity = 2.0

                    seed = self.SharedData.mod_Random__.randint(1, 100)

                    world = self.SharedData.mod_Numpy__.zeros(shape)
                    CloudData = []
                    for i in range(shape[0]):
                        for j in range(shape[1]):
                            world[i][j] = (self.SharedData.mod_Noise__.pnoise2(i/scale,
                                                        j/scale,
                                                        octaves=octaves,
                                                        persistence=persistence,
                                                        lacunarity=lacunarity,
                                                        repeatx=1024,
                                                        repeaty=1024,
                                                        base=seed))

                            CloudData.append(world[i][j])


                    image = self.SharedData.mod_PIL_Image_.fromarray(
                        self.SharedData.mod_Numpy__.uint8(
                            self.SharedData.mod_Matplotlib_cm_.gist_earth(world)*255))

                    if self.SharedData.platform == "Linux":
                        try:
                            self.SharedData.mod_OS__.remove(
                                self.SharedData.mod_OS__.path.join(
                                    self.SharedData.base_folder,
                                    ("Resources//G3_Resources//clouds//Rnd_noise.png")))
                        except:
                            print("".join(("Unable to clear the previous Perlin-noise image, ",
                                                "attempting to overwrite instead")))

                        image.save(
                            self.SharedData.mod_OS__.path.join(
                                self.SharedData.base_folder,
                                ("Resources//G3_Resources//clouds//Rnd_noise.png")))

                    else:
                        try:
                            self.SharedData.mod_OS__.remove(
                                self.SharedData.mod_OS__.path.join(
                                    self.SharedData.base_folder,
                                    ("Resources\\G3_Resources\\clouds\\Rnd_noise.png")))
                        except:
                            print("".join(("Unable to clear the previous Perlin-noise image, ",
                                                "attempting to overwrite instead")))

                        image.save(
                            self.SharedData.mod_OS__.path.join(
                                self.SharedData.base_folder,
                                ("Resources\\G3_Resources\\clouds\\Rnd_noise.png")))

                    image.close()
                    return CloudData
            except Exception as Message:
                self.SharedData.ErrorMessage = "".join(("GameEngineUtils > ComputeWeather ",
                                                        f"> ComputeCloudNoise: {str(Message)}"))

                self.SharedData.ErrorMessage_detailed = "".join(
                    self.SharedData.mod_Traceback__.format_exception(
                        None,
                        Message,
                        Message.__traceback__))

                self.SharedData.mod_ErrorUtils__.GenerateErrorScreen.ErrorScreen(
                    self.SharedData)

        def BlendWeather(self):
            def mix(start, end, time, duration):
                return (((end-start)/duration)*time)+start

            if self.weather != self.PreviousWeather and self.WeatherTime < 3:
                if self.weather == "sunny":
                    self.shadowmap["w_min"] = mix(
                        self.Previous_Fog_Distance_Min,
                        1200.0,
                        self.WeatherTime,
                        3)

                    self.shadowmap["w_max"] = mix(
                        self.Previous_Fog_Distance_Max,
                        1600.0,
                        self.WeatherTime,
                        3)

                    Temporary_color = mix(
                        self.Previous_color,
                        1.0,
                        self.WeatherTime,
                        3)

                    self.color.value = (
                        Temporary_color,
                        Temporary_color,
                        Temporary_color)

                    self.CloudsProgram["w_min"] = mix(
                        self.Previous_Fog_Distance_Min,
                        1200.0,
                        self.WeatherTime,
                        3)

                    self.CloudsProgram["w_max"] = mix(
                        self.Previous_Fog_Distance_Max,
                        1600.0,
                        self.WeatherTime,
                        3)

                    self.CloudsProgram["WeatherAlpha"] = mix(
                        self.Previous_CloudsProgram_Alpha,
                        0.0,
                        self.WeatherTime,
                        3)

                    self.CloudsProgram["CloudColor"] = mix(
                        self.Previous_CloudsProgram_CloudColor,
                        1.0,
                        self.WeatherTime,
                        3)

                    multiplier = mix(
                        self.Previous_multiplier,
                        self.CloudHeightMultiplier,
                        self.WeatherTime,
                        3)

                    self.CloudsProgram["CloudHeightMultiplier"] = multiplier
                    self.shadowmap["CloudHeightMultiplier"] = multiplier

                    self.prog["transparency"] = mix(
                        self.Previous_prog_transparency,
                        1.0,
                        self.WeatherTime,
                        3)

                elif self.weather == "rain.light":
                    self.shadowmap["w_min"] = mix(
                        self.Previous_Fog_Distance_Min,
                        1000.0,
                        self.WeatherTime,
                        3)

                    self.shadowmap["w_max"] = mix(
                        self.Previous_Fog_Distance_Max,
                        1600.0,
                        self.WeatherTime,
                        3)

                    Temporary_color = mix(
                        self.Previous_color,
                        0.8,
                        self.WeatherTime,
                        3)

                    self.color.value = (
                        Temporary_color,
                        Temporary_color,
                        Temporary_color)

                    self.CloudsProgram["w_min"] = mix(
                        self.Previous_Fog_Distance_Min,
                        1200.0,
                        self.WeatherTime,
                        3)

                    self.CloudsProgram["w_max"] = mix(
                        self.Previous_Fog_Distance_Max,
                        1600.0,
                        self.WeatherTime,
                        3)

                    self.CloudsProgram["WeatherAlpha"] = mix(
                        self.Previous_CloudsProgram_Alpha,
                        0.75,
                        self.WeatherTime,
                        3)

                    self.CloudsProgram["CloudColor"] = mix(
                        self.Previous_CloudsProgram_CloudColor,
                        0.75,
                        self.WeatherTime,
                        3)

                    multiplier = mix(
                        self.Previous_multiplier,
                        self.CloudHeightMultiplier,
                        self.WeatherTime,
                        3)

                    self.CloudsProgram["CloudHeightMultiplier"] = multiplier
                    self.shadowmap["CloudHeightMultiplier"] = multiplier

                    self.prog["transparency"] = mix(
                        self.Previous_prog_transparency,
                        self.prog_Transparency,
                        self.WeatherTime,
                        3)

                elif self.weather == "rain.heavy":
                    self.shadowmap["w_min"] = mix(
                        self.Previous_Fog_Distance_Min,
                        1000.0,
                        self.WeatherTime,
                        3)

                    self.shadowmap["w_max"] = mix(
                        self.Previous_Fog_Distance_Max,
                        1600.0,
                        self.WeatherTime,
                        3)

                    Temporary_color = mix(
                        self.Previous_color,
                        0.7,
                        self.WeatherTime,
                        3)

                    self.color.value = (
                        Temporary_color,
                        Temporary_color,
                        Temporary_color)

                    self.CloudsProgram["w_min"] = mix(
                        self.Previous_Fog_Distance_Min,
                        800.0,
                        self.WeatherTime,
                        3)

                    self.CloudsProgram["w_max"] = mix(
                        self.Previous_Fog_Distance_Max,
                        1200.0,
                        self.WeatherTime,
                        3)

                    self.CloudsProgram["WeatherAlpha"] = mix(
                        self.Previous_CloudsProgram_Alpha,
                        1.0,
                        self.WeatherTime,
                        3)

                    self.CloudsProgram["CloudColor"] = mix(
                        self.Previous_CloudsProgram_CloudColor,
                        0.35,
                        self.WeatherTime,
                        3)

                    multiplier = mix(
                        self.Previous_multiplier,
                        self.CloudHeightMultiplier,
                        self.WeatherTime,
                        3)

                    self.CloudsProgram["CloudHeightMultiplier"] = multiplier
                    self.shadowmap["CloudHeightMultiplier"] = multiplier

                    self.prog["transparency"] = mix(
                        self.Previous_prog_transparency,
                        self.prog_Transparency,
                        self.WeatherTime,
                        3)

                else:
                    self.shadowmap["w_min"] = mix(
                        self.Previous_Fog_Distance_Min,
                        600.0,
                        self.WeatherTime,
                        3)

                    self.shadowmap["w_max"] = mix(
                        self.Previous_Fog_Distance_Max,
                        800.0,
                        self.WeatherTime,
                        3)

                    Temporary_color = mix(
                        self.Previous_color,
                        0.6,
                        self.WeatherTime,
                        3)

                    self.color.value = (
                        Temporary_color,
                        Temporary_color,
                        Temporary_color)

                    self.CloudsProgram["w_min"] = mix(
                        self.Previous_Fog_Distance_Min,
                        800.0,
                        self.WeatherTime,
                        3)

                    self.CloudsProgram["w_max"] = mix(
                        self.Previous_Fog_Distance_Max,
                        1200.0,
                        self.WeatherTime,
                        3)

                    self.CloudsProgram["WeatherAlpha"] = mix(
                        self.Previous_CloudsProgram_Alpha,
                        1.0,
                        self.WeatherTime,
                        3)

                    self.CloudsProgram["CloudColor"] = mix(
                        self.Previous_CloudsProgram_CloudColor,
                        0.25,
                        self.WeatherTime,
                        3)

                    multiplier = mix(
                        self.Previous_multiplier,
                        self.CloudHeightMultiplier,
                        self.WeatherTime,
                        3)

                    self.CloudsProgram["CloudHeightMultiplier"] = multiplier
                    self.shadowmap["CloudHeightMultiplier"] = multiplier

                    self.prog["transparency"] = mix(
                        self.Previous_prog_transparency,
                        self.prog_Transparency,
                        self.WeatherTime,
                        3)

            else:
                if self.weather == "sunny":
                    self.color.value = (1.0, 1.0, 1.0)

                elif self.weather == "rain.light":
                    self.color.value = (0.8, 0.8, 0.8)

                elif self.weather == "rain.heavy":
                    self.color.value = (0.7, 0.7, 0.7)

                else:
                    self.color.value = (0.6, 0.6, 0.6)

        def ComputeWeather(self):
            try:
                if self.SharedData.mod_Random__.randint(0, 100) <= 65:
                    self.weather += "sunny"

                    self.color.value = (1.0, 1.0, 1.0)

                    self.shadowmap["w_min"] = 1200.0
                    self.shadowmap["w_max"] = 1600.0

                    self.CloudsProgram["w_min"] = 1200.0
                    self.CloudsProgram["w_max"] = 1600.0
                    self.CloudsProgram["WeatherAlpha"] = 0.0
                    self.CloudsProgram["CloudColor"] = 1.0

                    self.CloudHeightMultiplier = self.SharedData.mod_Random__.randint(1, 500)
                    self.CloudsProgram["CloudHeightMultiplier"] = self.CloudHeightMultiplier
                    self.shadowmap["CloudHeightMultiplier"] = self.CloudHeightMultiplier

                    self.prog["transparency"] = 1.0

                else:
                    self.weather += "rain"

                    if self.SharedData.mod_Random__.randint(0, 100) <= 80:
                        self.weather += ".light"

                        self.color.value = (0.8, 0.8, 0.8)

                        self.shadowmap["w_min"] = 1000.0
                        self.shadowmap["w_max"] = 1600.0

                        self.CloudsProgram["w_min"] = 1000.0
                        self.CloudsProgram["w_max"] = 1600.0
                        self.CloudsProgram["WeatherAlpha"] = 0.75
                        self.CloudsProgram["CloudColor"] = 0.75

                        self.CloudHeightMultiplier = self.SharedData.mod_Random__.randint(139, 500)
                        self.CloudsProgram["CloudHeightMultiplier"] = self.CloudHeightMultiplier
                        self.shadowmap["CloudHeightMultiplier"] = self.CloudHeightMultiplier

                        self.prog_Transparency = self.SharedData.mod_Random__.randint(35, 50)/100
                        self.prog["transparency"] = self.prog_Transparency

                    else:
                        self.weather += ".heavy"
                        self.CloudsProgram["WeatherAlpha"] = 1

                        if self.SharedData.mod_Random__.randint(0, 100) <= 50:
                            self.weather += ".thundery"

                            self.color.value = (0.6, 0.6, 0.6)

                            self.LengthenStorm = True

                            self.shadowmap["w_min"] = 600.0
                            self.shadowmap["w_max"] = 800.0

                            self.CloudsProgram["w_min"] = 600.0
                            self.CloudsProgram["w_max"] = 800.0
                            self.CloudsProgram["CloudColor"] = 0.25

                            self.CloudHeightMultiplier = self.SharedData.mod_Random__.randint(
                                278,
                                500)

                            self.CloudsProgram["CloudHeightMultiplier"] = self.CloudHeightMultiplier
                            self.shadowmap["CloudHeightMultiplier"] = self.CloudHeightMultiplier

                            self.prog_Transparency = self.SharedData.mod_Random__.randint(0, 45)/100
                            self.prog["transparency"] = self.prog_Transparency

                        else:
                            self.color.value = (0.7, 0.7, 0.7)

                            self.shadowmap["w_min"] = 800.0
                            self.shadowmap["w_max"] = 1200.0

                            self.CloudsProgram["w_min"] = 800.0
                            self.CloudsProgram["w_max"] = 1200.0
                            self.CloudsProgram["CloudColor"] = 0.35

                            self.CloudHeightMultiplier = self.SharedData.mod_Random__.randint(
                                361,
                                500)

                            self.CloudsProgram["CloudHeightMultiplier"] = self.CloudHeightMultiplier
                            self.shadowmap["CloudHeightMultiplier"] = self.CloudHeightMultiplier

                            self.prog_Transparency = self.SharedData.mod_Random__.randint(0, 25)/100
                            self.prog["transparency"] = self.prog_Transparency
            except Exception as Message:
                self.SharedData.ErrorMessage = "".join(("GameEngineUtils > ComputeWeather ",
                                                        f"> ComputeWeather: {str(Message)}"))

                self.SharedData.ErrorMessage_detailed = "".join(
                    self.SharedData.mod_Traceback__.format_exception(
                        None,
                        Message,
                        Message.__traceback__))

                self.SharedData.mod_ErrorUtils__.GenerateErrorScreen.ErrorScreen(
                    self.SharedData)

    class AccessOtherGUIs:
        def __init__(self):
            pass

        def AccessGUI(self):
            try:
                fullscreen = self.wnd.fullscreen
                self.SharedData.Fullscreen = not fullscreen
                WindowSize = self.wnd.width, self.wnd.height
                WindowPos = self.wnd.position
                self.wnd.position = (-WindowSize[0],
                                     -WindowSize[1])

                self.wnd.mouse_exclusivity = False
                self.SharedData.mod_Pygame__.init()

                if self.Inventory:
                    self.SharedData.mod_ModernGL_window_Screenshot.create(
                        source=self.wnd.fbo,
                        name=self.SharedData.mod_OS__.path.join(
                            self.SharedData.base_folder,
                            ("Resources\\General_Resources\\PauseIMG.png")))

                    self.SharedData.Command = "Inventory"
                    self.SharedData.mod_Inventory__.GenerateInventory.Inventory(self.SharedData)
                    self.Inventory = False

                elif self.Map:
                    self.SharedData.Command = "Map"
                    self.SharedData.mod_MapGUI__.GenerateMapGUI.MapGUI(self.SharedData)
                    self.Map = False

                self.wnd.mouse_exclusivity = self.camera_enabled
                self.wnd.position = WindowPos
                self.wnd.fullscreen = fullscreen
                self.SharedData.Command = "Play"
            except Exception as Message:
                self.SharedData.ErrorMessage = "".join(("GameEngineUtils > AccessOtherGUIs ",
                                                        f"> AccessGUI: {str(Message)}"))

                self.SharedData.ErrorMessage_detailed = "".join(
                    self.SharedData.mod_Traceback__.format_exception(
                        None,
                        Message,
                        Message.__traceback__))

                self.SharedData.mod_ErrorUtils__.GenerateErrorScreen.ErrorScreen(self.SharedData)

    class ShadowmappingMathematics:
        def __init__(self):
            pass

        def ComputeCelestialEntities(self):
            scene_pos = self.SharedData.mod_Pyrr_Vector3_(
                        (0, -5, -32),
                        dtype="f4")

            distance = (self.skybox_distance-self.sun_radius)/1.355

            if self.GameTime >= 1056:
                self.GameTime = 0
                self.day += 1

            sun_prepro_time = (self.GameTime/168)-1.5707975

            SunPos_YZ = self.SharedData.mod_Math__.cos(
                sun_prepro_time) * distance

            SunPos_X = self.SharedData.mod_Math__.sin(
                sun_prepro_time) * distance

            self.sun_lightpos = self.SharedData.mod_Pyrr_Vector3_(
                (SunPos_X+self.camera.position.x,
                    SunPos_YZ+self.camera.position.y,
                    0),
                dtype="f4")

            moon_prepro_time = (self.GameTime/168)-4.7123925

            MoonPos_YZ = self.SharedData.mod_Math__.cos(
                moon_prepro_time) * distance
            MoonPos_X = self.SharedData.mod_Math__.sin(
                moon_prepro_time) * distance

            self.moon_lightpos = self.SharedData.mod_Pyrr_Vector3_(
                (MoonPos_X+self.camera.position.x,
                    MoonPos_YZ+self.camera.position.y,
                    0),
                dtype="f4")


            self.sun_prog["m_proj"].write(self.camera.projection.matrix)
            self.sun_prog["m_camera"].write(self.camera.matrix)
            self.sun_prog["m_model"].write(
                self.SharedData.mod_Pyrr_Matrix44_.from_translation(
                    self.sun_lightpos + scene_pos,
                    dtype="f4"))


            self.moon_prog["m_proj"].write(self.camera.projection.matrix)
            self.moon_prog["m_camera"].write(self.camera.matrix)
            self.moon_prog["m_model"].write(
                self.SharedData.mod_Pyrr_Matrix44_.from_translation(
                    self.moon_lightpos + scene_pos,
                    dtype="f4"))

        def ComputeShadows(self):
            try:
                cam_proj = self.camera.projection.matrix
                cam_look_at = self.camera.matrix

                cam_mvp = cam_proj * cam_look_at
                self.mvp.write(cam_mvp.astype("f4").tobytes())

                # build light camera
                self.light.value = tuple(self.sun_lightpos)
                sun_light_look_at = self.SharedData.mod_Pyrr_Matrix44_.look_at(
                    self.sun_lightpos,
                    target=(0, 0, 0),
                    up=(0.0, 0.0, 1.0),
                )

                # light projection matrix (scene dependant)
                light_proj = self.SharedData.mod_Pyrr_Matrix44_.perspective_projection(
                    fovy=90.0 / 2,  # smaller value increase shadow precision 2000
                    aspect=self.wnd.aspect_ratio,
                    near=0.01,
                    far=2000.0
                )
                # light model view projection matrix
                mvp_light = light_proj * sun_light_look_at

                bias_matrix = (
                        self.SharedData.mod_Pyrr_Matrix44_.from_translation(
                            (0.5, 0.5, 0.5),
                            dtype="f4")
                        *
                        self.SharedData.mod_Pyrr_Matrix44_.from_scale(
                            (0.5, 0.5, 0.5),
                            dtype="f4")
                )

                mvp_depth_bias = bias_matrix * mvp_light

                # send uniforms to shaders
                self.mvp_depth.write(mvp_depth_bias.astype("f4").tobytes())
                self.mvp_shadow.write(mvp_light.astype("f4").tobytes())

                # pass 1: render shadow-map (depth framebuffer -> texture) from light view
                #self.fbo_depth.use()
                #self.fbo_depth.clear(
                    #1.0,
                    #1.0,
                    #1.0)

                # https://moderngl.readthedocs.io/en/stable/reference/context.html?highlight=culling#moderngl.Context.front_face
                # clock wise -> render back faces
                #self.ctx.front_face = "cw"
            except Exception as Message:
                print(Message)
                self.SharedData.ErrorMessage = "GameEngine > GameEngine > __init__: "+str(Message)
                self.SharedData.ErrorMessage_detailed = "".join(
                    self.SharedData.mod_Traceback__.format_exception(
                        None,
                        Message,
                        Message.__traceback__))

                self.SharedData.mod_ErrorUtils__.GenerateErrorScreen.ErrorScreen(self.SharedData)

    class OnscreenEventFunction:
        def __init__(self):
            pass

        def game_events(self):
            try:
                if self.SharedData.UseMouseInput is False:
                    self.camera.rot_state(
                        -self.Joystick_Rotation[0]*self.SharedData.cameraANGspeed,
                        -self.Joystick_Rotation[1]*self.SharedData.cameraANGspeed)

                if self.Akeydown:
                    self.SharedData.Total_move_z -= 10
                    if self.SharedData.UseMouseInput is False:
                        self.camera.key_input(
                            self.keys.A,
                            self.keys.ACTION_PRESS,
                            None)

                else:
                    if self.SharedData.UseMouseInput is False:
                        self.camera.key_input(
                            self.keys.A,
                            self.keys.ACTION_RELEASE,
                            None)

                if self.Skeydown:
                    self.SharedData.Total_move_x -= 10
                    if self.SharedData.UseMouseInput is False:
                        self.camera.key_input(
                            self.keys.S,
                            self.keys.ACTION_PRESS,
                            None)

                else:
                    if self.SharedData.UseMouseInput is False:
                        self.camera.key_input(
                            self.keys.S,
                            self.keys.ACTION_RELEASE,
                            None)

                if self.Dkeydown:
                    self.SharedData.Total_move_z += 10
                    if self.SharedData.UseMouseInput is False:
                        self.camera.key_input(
                            self.keys.D,
                            self.keys.ACTION_PRESS,
                            None)

                else:
                    if self.SharedData.UseMouseInput is False:
                        self.camera.key_input(
                            self.keys.D,
                            self.keys.ACTION_RELEASE,
                            None)

                if self.SharedData.sound:
                    if self.Wkeydown:
                        CurrentTime = self.SharedData.mod_Time__.perf_counter()
                        WPressedTime = CurrentTime-self.RunForwardTimer_start_sound
                        if self.Sprinting:
                            if WPressedTime >= (self.SharedData.mod_Random__.randint(25, 75)/100):
                                self.SharedData.mod_SoundUtils__.PlaySound.PlayFootstepsSound(
                                    self.SharedData)

                                self.RunForwardTimer_start_sound = self.SharedData.mod_Time__.perf_counter()

                        else:
                            if WPressedTime >= (self.SharedData.mod_Random__.randint(50, 100)/100):
                                self.SharedData.mod_SoundUtils__.PlaySound.PlayFootstepsSound(
                                    self.SharedData)

                                self.RunForwardTimer_start_sound = self.SharedData.mod_Time__.perf_counter()

                    elif self.Akeydown:
                        CurrentTime = self.SharedData.mod_Time__.perf_counter()
                        APressedTime = CurrentTime-self.AkeydownTimer_start

                        if APressedTime >= (self.SharedData.mod_Random__.randint(50, 100)/100):
                            self.SharedData.mod_SoundUtils__.PlaySound.PlayFootstepsSound(
                                self.SharedData)

                            self.AkeydownTimer_start = self.SharedData.mod_Time__.perf_counter()

                    elif self.Skeydown:
                        CurrentTime = self.SharedData.mod_Time__.perf_counter()
                        SPressedTime = CurrentTime-self.SkeydownTimer_start

                        if SPressedTime >= (self.SharedData.mod_Random__.randint(50, 100)/100):
                            self.SharedData.mod_SoundUtils__.PlaySound.PlayFootstepsSound(
                                self.SharedData)

                            self.SkeydownTimer_start = self.SharedData.mod_Time__.perf_counter()

                    elif self.Dkeydown:
                        CurrentTime = self.SharedData.mod_Time__.perf_counter()
                        DPressedTime = CurrentTime-self.DkeydownTimer_start

                        if DPressedTime >= (self.SharedData.mod_Random__.randint(50, 100)/100):
                            self.SharedData.mod_SoundUtils__.PlaySound.PlayFootstepsSound(
                                self.SharedData)

                            self.DkeydownTimer_start = self.SharedData.mod_Time__.perf_counter()

                if self.RunForwardTimer:
                    if self.SharedData.mod_Time__.perf_counter()-self.RunForwardTimer_start > 3.5:
                        self.Sprinting = True
                else:
                    self.Sprinting = False

                if self.Wkeydown:
                    if self.Sprinting:
                        if self.UpdateProjection:
                            if self.SharedData.Devmode == 10 and self.IKeyPressed:
                                self.camera.velocity = 55
                                self.camera.projection.update(
                                    near=0.1,
                                    far=2000.0,
                                    fov=100)

                                self.SharedData.Total_move_x += 35
                            else:
                                self.camera.projection.update(
                                    near=0.1,
                                    far=2000.0,
                                    fov=80)

                                self.camera.velocity = 15 #2.2352
                                self.SharedData.Total_move_x += 15
                else:
                    if self.SharedData.Devmode == 10 and self.IKeyPressed:
                        self.camera.velocity = 35
                        self.camera.projection.update(
                            near=0.1,
                            far=2000.0,
                            fov=90)

                    if self.UpdateProjection:
                        self.UpdateProjection = False
                        self.camera.velocity = 10 #1.42
                        self.camera.projection.update(
                            near=0.1,
                            far=2000.0,
                            fov=70)

                if self.Wkeydown:
                    if self.Sprinting:
                        self.UpdateProjection = True
                        self.RunForwardTimer_start = self.SharedData.mod_Time__.perf_counter()
                        if self.SharedData.UseMouseInput is False:
                            self.camera.key_input(
                                self.keys.W,
                                self.keys.ACTION_PRESS,
                                None)

                    else:
                        self.SharedData.Total_move_x += 10
                        if self.SharedData.UseMouseInput is False:
                            self.camera.key_input(
                                self.keys.W,
                                self.keys.ACTION_PRESS,
                                None)

                else:
                    if self.SharedData.UseMouseInput is False:
                        self.camera.key_input(
                            self.keys.W,
                            self.keys.ACTION_RELEASE,
                            None)

                if self.Jump:
                    if self.JumpUP:
                        self.camera.position.y += (1/self.Jump_Start_FPS)
                        if self.camera.position.y >= self.StartYposition+0.5:
                            self.JumpUP = False

                    else:
                        self.camera.position.y -= 1/self.Jump_Start_FPS
                        if self.camera.position.y <= self.StartYposition:
                            self.Jump = False
                            if self.Collision is False:
                                self.camera.position.y = self.StartYposition

            except Exception as Message:
                self.SharedData.ErrorMessage = "GameEngine > GameEngine > __init__: "+str(Message)
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
