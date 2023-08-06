#version 330

#if defined VERTEX_SHADER

in vec3 in_normal;
in vec3 in_position;
in vec2 in_texcoord_0;
in vec3 in_color;

uniform mat4 u_depth_bias_mvp;
uniform mat4 u_mvp;

uniform sampler2D Heightmap;
uniform float CloudHeightMultiplier;
uniform float height_max;

out vec4 mVertex;
out vec3 v_norm;
out vec4 v_shadow_coord;
out vec2 v_text;
out vec3 v_vert;      
out float col;      
out float model_height;

void main() {
    float height = ((texture(Heightmap, vec2(in_texcoord_0.x, in_texcoord_0.y)).r)*CloudHeightMultiplier);
    col = 1.0-((1/(height_max*CloudHeightMultiplier))*height);

    gl_Position = u_mvp * vec4(in_position, 1.0);

    v_shadow_coord = u_depth_bias_mvp * vec4(in_position, 1.0);

    v_vert = in_position;
    v_norm = in_normal;
    v_text = in_texcoord_0;

    model_height = (in_position.y/100);

    mVertex = u_mvp * vec4(in_position, 1.0);
}

#elif defined FRAGMENT_SHADER

in vec4 mVertex;
in vec3 v_norm;
in vec4 v_shadow_coord;
in vec2 v_text;
in vec3 v_vert;    
in float col;     
in float model_height;

uniform vec4 CameraEye;
uniform vec4 FogColor;
uniform float light_level;
uniform vec3 u_color;
uniform vec3 u_light;

uniform sampler2D Color1;
uniform sampler2D Color2;

uniform sampler2DShadow u_sampler_shadow;
uniform bool u_use_color_texture;
uniform float w_max;
uniform float w_min;

out vec4 f_color;

float compute_visibility(in float cos_theta) {
    // shadow coordinates in light space
    vec2 shadow_coord_ls = v_shadow_coord.xy / v_shadow_coord.w;
    
    // bias according to the slope
    float bias = 0.005 * tan(acos(cos_theta));
    bias = clamp(bias, 0.0, 0.01);

    float z_from_cam = v_shadow_coord.z / v_shadow_coord.w - bias;
    vec3 shadow_coord = vec3(shadow_coord_ls, z_from_cam);
    float shadow_value = texture(u_sampler_shadow, shadow_coord);
    return 1.0 - shadow_value;
}

float getFogFactor(float d, float w_max, float w_min) {
    if (d >= w_max) discard;
    if (d <= w_min) return 0.0;

    return 1.0 - (w_max - d) / (w_max - w_min);
}

void main() {
    // Lighting
    // Diffuse lighting + ambient
    vec4 V = mVertex;
    float d = distance(CameraEye, V);
    float alpha = getFogFactor(d, w_max, w_min);

    vec3 light_vector_obj_space = normalize(u_light - v_vert);
    vec3 normal_obj_space = normalize(v_norm);
    float cos_theta = dot(light_vector_obj_space, normal_obj_space);
    float diffuse = clamp(cos_theta, 0.0, 1.0);
    // Shadow component
    float lum = mix(light_level, 1.0, diffuse * compute_visibility(cos_theta)) * col;
    // Color object (color or texture)
    float border = smoothstep(0.5, 0.7, model_height);

    vec3 color1 = texture(Color1, v_text).rgb;
    vec3 color2 = texture(Color2, v_text).rgb;

    vec3 color = color1 * (1.0 - border) + color2 * border;

    // Final pixel color
    f_color = vec4((color.r * u_color.r) * lum, (color.g * u_color.g) * lum, (color.b * u_color.b) * lum, 1.0-alpha);
}
#endif