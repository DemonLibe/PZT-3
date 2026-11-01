shader_type spatial;
render_mode diffuse_lambert, specular_disabled;
// PS1: вершины прилипают к сетке низкого разрешения — геометрия «дрожит».

uniform vec4 albedo : source_color = vec4(1.0);
uniform sampler2D albedo_texture : source_color, filter_nearest, repeat_enable;
uniform bool use_texture = false;
uniform vec4 emission : source_color = vec4(0.0, 0.0, 0.0, 1.0);
uniform float emission_energy = 0.0;
uniform vec2 snap_resolution = vec2(320.0, 240.0);

void vertex() {
	vec4 clip = PROJECTION_MATRIX * MODELVIEW_MATRIX * vec4(VERTEX, 1.0);
	vec2 grid = snap_resolution * 0.5;
	clip.xy = round(clip.xy / clip.w * grid) / grid * clip.w;
	POSITION = clip;
}

void fragment() {
	vec4 color = albedo;
	if (use_texture) {
		color *= texture(albedo_texture, UV);
	}
	ALBEDO = color.rgb;
	ROUGHNESS = 1.0;
	EMISSION = emission.rgb * emission_energy;
}
