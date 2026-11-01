shader_type canvas_item;
// Галлюцинации: волны по экрану и расслоение цветов.

uniform sampler2D screen_texture : hint_screen_texture, filter_linear;

void fragment() {
	vec2 uv = SCREEN_UV;
	uv.x += sin(uv.y * 18.0 + TIME * 1.7) * 0.006;
	uv.y += cos(uv.x * 14.0 + TIME * 1.3) * 0.006;
	float shift = 0.006 + 0.004 * sin(TIME * 0.9);
	vec3 col;
	col.r = texture(screen_texture, uv + vec2(shift, 0.0)).r;
	col.g = texture(screen_texture, uv).g;
	col.b = texture(screen_texture, uv - vec2(shift, 0.0)).b;
	col *= vec3(1.05, 0.92, 0.95);
	COLOR = vec4(col, 1.0);
}
