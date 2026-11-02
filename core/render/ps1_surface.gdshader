shader_type spatial;
render_mode diffuse_lambert, specular_disabled;
// PS1: вершины прилипают к сетке низкого разрешения — геометрия «дрожит».
// Текстура накладывается по мировым координатам (triplanar) — для CSG-блоков.

uniform vec4 albedo : source_color = vec4(1.0);
uniform sampler2D albedo_texture : source_color, filter_nearest_mipmap, repeat_enable;
uniform bool use_texture = false;
uniform bool use_triplanar = false;
uniform float triplanar_scale = 0.5;
uniform vec4 emission : source_color = vec4(0.0, 0.0, 0.0, 1.0);
uniform float emission_energy = 0.0;
uniform vec2 snap_resolution = vec2(640.0, 480.0);
uniform bool snap_enabled = true;

varying vec3 world_position;
varying vec3 world_normal;

void vertex() {
	world_position = (MODEL_MATRIX * vec4(VERTEX, 1.0)).xyz;
	world_normal = normalize((MODEL_MATRIX * vec4(NORMAL, 0.0)).xyz);
	vec4 clip = PROJECTION_MATRIX * MODELVIEW_MATRIX * vec4(VERTEX, 1.0);
	if (snap_enabled) {
		vec2 grid = snap_resolution * 0.5;
		clip.xy = round(clip.xy / clip.w * grid) / grid * clip.w;
	}
	POSITION = clip;
}

void fragment() {
	vec4 color = albedo;
	if (use_texture) {
		if (use_triplanar) {
			vec3 weights = pow(abs(world_normal), vec3(4.0));
			weights /= dot(weights, vec3(1.0));
			vec3 p = world_position * triplanar_scale;
			color *= texture(albedo_texture, p.zy) * weights.x
				+ texture(albedo_texture, p.xz) * weights.y
				+ texture(albedo_texture, p.xy) * weights.z;
		} else {
			color *= texture(albedo_texture, UV);
		}
	}
	ALBEDO = color.rgb;
	ROUGHNESS = 1.0;
	EMISSION = emission.rgb * emission_energy;
}
