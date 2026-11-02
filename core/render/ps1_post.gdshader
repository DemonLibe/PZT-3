shader_type canvas_item;
// PS1: крупные пиксели и урезанная палитра. Дизеринг выключен по умолчанию — на тёмных
// градиентах он «ползёт» при повороте камеры.

uniform sampler2D screen_texture : hint_screen_texture, filter_nearest;
uniform float pixel_size = 2.0;
uniform float color_levels = 56.0;
uniform float dither_strength = 0.0;

const float BAYER[16] = float[16](0.0, 8.0, 2.0, 10.0, 12.0, 4.0, 14.0, 6.0, 3.0, 11.0, 1.0, 9.0, 15.0, 7.0, 13.0, 5.0);

void fragment() {
	vec2 cell_size = vec2(pixel_size) * SCREEN_PIXEL_SIZE;
	vec2 cell = floor(SCREEN_UV / cell_size);
	vec3 color = texture(screen_texture, (cell + 0.5) * cell_size).rgb;
	int index = int(mod(cell.x, 4.0)) + int(mod(cell.y, 4.0)) * 4;
	float threshold = BAYER[index] / 16.0 - 0.5;
	color = floor(color * color_levels + threshold * dither_strength + 0.5) / color_levels;
	COLOR = vec4(color, 1.0);
}
