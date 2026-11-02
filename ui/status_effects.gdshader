shader_type canvas_item;
// Экранные эффекты состояний участника: цветные края, пульсация, обесцвечивание.

uniform sampler2D screen_texture : hint_screen_texture, filter_linear;
uniform vec4 edge_color : source_color = vec4(0.0, 0.0, 0.0, 0.0);
uniform float edge_strength = 0.0;
uniform float pulse_speed = 0.0;
uniform float desaturate = 0.0;
uniform float texture_mix = 0.0;
uniform sampler2D overlay_texture : source_color, filter_nearest, repeat_enable;

void fragment() {
	vec3 col = texture(screen_texture, SCREEN_UV).rgb;
	float gray = dot(col, vec3(0.299, 0.587, 0.114));
	col = mix(col, vec3(gray), desaturate);
	float d = distance(UV, vec2(0.5));
	float pulse = pulse_speed > 0.0 ? 0.6 + 0.4 * sin(TIME * pulse_speed) : 1.0;
	float edge = smoothstep(0.32, 0.75, d) * edge_strength * pulse;
	vec3 over = mix(edge_color.rgb, texture(overlay_texture, UV * 6.0).rgb * edge_color.rgb * 1.6, texture_mix);
	col = mix(col, over, clamp(edge, 0.0, 1.0));
	COLOR = vec4(col, 1.0);
}
