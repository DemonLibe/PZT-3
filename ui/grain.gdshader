shader_type canvas_item;
// Фон меню: тёмный, с зерном плёнки и медленным мерцанием.

float hash(vec2 p) {
	return fract(sin(dot(p, vec2(12.9898, 78.233))) * 43758.5453);
}

void fragment() {
	vec2 cell = floor(FRAGCOORD.xy / 3.0);
	float n = hash(cell + floor(TIME * 12.0));
	float vignette = smoothstep(1.1, 0.3, distance(UV, vec2(0.35, 0.5)));
	vec3 base = COLOR.rgb + vec3(0.02, 0.022, 0.02) * vignette;
	COLOR = vec4(base + (n - 0.5) * 0.025, 1.0);
}
