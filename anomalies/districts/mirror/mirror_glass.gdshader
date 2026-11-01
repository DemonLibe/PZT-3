shader_type spatial;
render_mode unshaded, cull_disabled;
// Стекло «Зеркала»: показывает картинку фиксированной камеры района.
// cracked = 1 — стекло треснуло изнутри.

uniform sampler2D view_tex : source_color, filter_nearest;
uniform float cracked = 0.0;
uniform vec2 crack_center = vec2(0.47, 0.55);
uniform float brightness = 1.5;

float hash(float n) {
	return fract(sin(n) * 43758.5453);
}

void fragment() {
	vec2 uv = UV;
	vec3 col = texture(view_tex, uv).rgb * brightness;
	if (cracked > 0.5) {
		vec2 d = uv - crack_center;
		float r = length(d);
		float t = (atan(d.y, d.x) + PI) / (2.0 * PI) * 13.0;
		float seg = floor(t);
		float wobble = (hash(seg) - 0.5) * 0.6;
		float radial_dist = abs(fract(t) - 0.5 - wobble * r) * (6.2832 / 13.0) * r;
		float radial = 1.0 - smoothstep(0.0012, 0.0035, radial_dist);
		float ring_dist = min(abs(r - (0.07 + hash(seg) * 0.03)), min(abs(r - (0.17 + hash(seg + 3.0) * 0.05)), abs(r - (0.31 + hash(seg + 5.0) * 0.08))));
		float ring = (1.0 - smoothstep(0.0015, 0.004, ring_dist)) * step(r, 0.42);
		vec2 shard_offset = vec2(hash(seg + 11.0) - 0.5, hash(seg + 17.0) - 0.5) * 0.03 * r;
		col = texture(view_tex, uv + shard_offset).rgb * 0.45;
		col = mix(col, vec3(0.85, 0.85, 0.8), max(radial, ring) * 0.85);
	}
	ALBEDO = col;
}
